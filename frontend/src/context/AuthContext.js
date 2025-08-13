// src/context/AuthContext.js
import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { registerUser, loginUser, getMyProfile } from '../api/authApi'; // Importar funciones de la API
import { useNavigate } from 'react-router-dom'; // Para la navegación

// Crear el contexto de autenticación
const AuthContext = createContext(null);

// Hook personalizado para usar el contexto de autenticación
export const useAuth = () => {
  return useContext(AuthContext);
};

// Proveedor de autenticación que envuelve la aplicación
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Almacena los datos del usuario autenticado
  const [token, setToken] = useState(localStorage.getItem('token')); // Almacena el token JWT
  const [loading, setLoading] = useState(true); // Estado de carga inicial
  const [error, setError] = useState(null); // Estado para mensajes de error
  const navigate = useNavigate(); // Hook para navegar programáticamente

  // Función para establecer el token y el usuario
  const setAuthData = useCallback((newToken, userData) => {
    setToken(newToken);
    setUser(userData);
    console.log("AuthContext: setAuthData - User:", userData, "Token:", newToken ? "present" : "absent");
    if (newToken) {
      localStorage.setItem('token', newToken); // Guardar el token en localStorage
    } else {
      localStorage.removeItem('token'); // Remover el token si es nulo
    }
  }, []);

  // Función para cargar los datos del usuario a partir del token
  const loadUser = useCallback(async (authToken) => {
    console.log("AuthContext: loadUser called. AuthToken present:", !!authToken);
    if (!authToken) {
      setLoading(false);
      console.log("AuthContext: loadUser - No authToken, setLoading(false)");
      return;
    }
    setLoading(true);
    console.log("AuthContext: loadUser - AuthToken present, setLoading(true)");
    setError(null);
    try {
      const userData = await getMyProfile(authToken);
      setUser(userData);
      console.log("AuthContext: loadUser - getMyProfile success, User data:", userData);
    } catch (err) {
      console.error('AuthContext: Error al cargar el perfil del usuario:', err);
      setError('Sesión expirada o inválida. Por favor, inicia sesión de nuevo.');
      setAuthData(null, null); // Limpiar el token y el usuario si falla la carga del perfil
      navigate('/login'); // Redirigir al login si la sesión es inválida
    } finally {
      setLoading(false);
      console.log("AuthContext: loadUser - finally block, setLoading(false)");
    }
  }, [setAuthData, navigate]);

  // Función para registrar un usuario
  const register = useCallback(async (userData) => {
    setLoading(true);
    setError(null);
    try {
      const newUser = await registerUser(userData);
      // Tras el registro, intentamos iniciar sesión automáticamente para obtener un token
      const loginResponse = await loginUser(userData.email, userData.password);
      setAuthData(loginResponse.access_token, newUser);
      navigate('/dashboard'); // Redirigir al dashboard tras el registro y login
      return newUser;
    } catch (err) {
      setError(err.message || 'Error en el registro.');
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      throw err; // Re-lanza el error para que el componente pueda manejarlo
    } finally {
      setLoading(false);
    }
  }, [setAuthData, navigate]);

  // Función para iniciar sesión
  const login = useCallback(async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const data = await loginUser(email, password);
      setAuthData(data.access_token, null); // Establece el token, el usuario se cargará con loadUser
      await loadUser(data.access_token); // Carga los datos completos del usuario
      navigate('/dashboard'); // Redirigir al dashboard tras el login
      return data;
    } catch (err) {
      setError(err.message || 'Error al iniciar sesión.');
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [setAuthData, loadUser, navigate]);

  // Función para cerrar sesión
  const logout = useCallback(() => {
    setAuthData(null, null);
    navigate('/login'); // Redirigir a la pantalla de login tras cerrar sesión
  }, [setAuthData, navigate]);

  // Efecto para cargar el usuario al inicio de la aplicación (si ya hay un token)
  useEffect(() => {
    console.log("AuthContext: useEffect - Token:", token ? "present" : "absent");
    if (token) {
      loadUser(token);
    } else {
      setLoading(false); // If no token, no user to load, finish loading
      console.log("AuthContext: useEffect - No token, setLoading(false)");
    }
  }, [token, loadUser]);

  // Valor del contexto que se proporcionará a los componentes hijos
  const contextValue = React.useMemo(() => ({
    user,
    token,
    isAuthenticated: !!token && !!user, // Verdadero si hay token y datos de usuario
    loading,
    error,
    register,
    login,
    logout,
    setUser, // Permitir actualizar el usuario directamente desde componentes tras una actualización de perfil
    setError, // Permitir borrar errores desde componentes
  }), [user, token, loading, error, register, login, logout, setUser, setError]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};