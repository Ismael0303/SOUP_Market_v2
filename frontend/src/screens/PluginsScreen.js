// frontend/src/screens/PluginsScreen.js
import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Breadcrumbs from '../components/Breadcrumbs';
import { useNotification } from '../context/NotificationContext';
import userApi from '../api/userApi'; // Assuming you have a userApi

const PluginsScreen = () => {
  const [plugins, setPlugins] = useState([]);
  const [loading, setLoading] = useState(true);
  const { showNotification } = useNotification();

  useEffect(() => {
    const fetchUserPlugins = async () => {
      try {
        setLoading(true);
        // In the future, this will come from a general list of available plugins
        const availablePlugins = [
          { id: 'bakery', name: 'Herramientas de Panadería', description: 'Gestión de recetas, producción y más.' },
          // { id: 'delivery', name: 'Gestión de Reparto', description: 'Optimización de rutas y seguimiento de entregas.' },
        ];

        // Fetch the user's active plugins
        const userProfile = await userApi.getProfile();
        const activePlugins = userProfile.plugins_activos || [];

        const pluginStatus = availablePlugins.map(p => ({
          ...p,
          isActive: activePlugins.includes(p.id),
        }));

        setPlugins(pluginStatus);
      } catch (error) {
        console.error("Error al cargar los plugins:", error);
        showNotification("No se pudieron cargar los plugins del usuario.", "error");
      } finally {
        setLoading(false);
      }
    };

    fetchUserPlugins();
  }, [showNotification]);

  const handleTogglePlugin = async (pluginId) => {
    try {
      const plugin = plugins.find(p => p.id === pluginId);
      const newStatus = !plugin.isActive;

      await userApi.updatePlugins(pluginId, newStatus);

      setPlugins(plugins.map(p =>
        p.id === pluginId ? { ...p, isActive: newStatus } : p
      ));

      showNotification(`Plugin '${plugin.name}' ${newStatus ? 'activado' : 'desactivado'}.`, 'success');
    } catch (error) {
      console.error("Error al actualizar el plugin:", error);
      showNotification("Error al actualizar el estado del plugin.", "error");
    }
  };

  return (
    <Layout>
      <Breadcrumbs items={[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Plugins' }]} />
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Marketplace de Plugins</h1>

      {loading ? (
        <p>Cargando plugins...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {plugins.map((plugin) => (
            <div key={plugin.id} className="bg-white rounded-2xl shadow-lg p-6 flex flex-col">
              <h2 className="text-xl font-bold text-gray-900 mb-2">{plugin.name}</h2>
              <p className="text-gray-600 mb-4 flex-grow">{plugin.description}</p>
              <div className="flex items-center justify-between">
                <span className={`font-semibold text-sm ${plugin.isActive ? 'text-green-600' : 'text-gray-500'}`}>
                  {plugin.isActive ? 'Activado' : 'Desactivado'}
                </span>
                <button
                  onClick={() => handleTogglePlugin(plugin.id)}
                  className={`px-4 py-2 rounded-lg font-semibold text-white ${
                    plugin.isActive ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'
                  }`}
                >
                  {plugin.isActive ? 'Desactivar' : 'Activar'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
};

export default PluginsScreen;
