// frontend/src/api/userApi.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const userApi = {
  getProfile: async () => {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${API_URL}/profile/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  updateProfile: async (profileData) => {
    const token = localStorage.getItem('token');
    const response = await axios.put(`${API_URL}/profile/me`, profileData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  updatePlugins: async (pluginId, isActive) => {
    const token = localStorage.getItem('token');
    const response = await axios.put(`${API_URL}/profile/me/plugins`, 
      { 
        plugin_name: pluginId,
        action: isActive ? 'activate' : 'deactivate'
      }, 
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  },
};

export default userApi;
