// frontend/src/screens/ProductionScreen.js
import React from 'react';
import Layout from '../components/Layout';
import Breadcrumbs from '../components/Breadcrumbs';

const ProductionScreen = () => {
  return (
    <Layout>
      <Breadcrumbs items={[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Producción' }]} />
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Gestión de Producción</h1>
      <div className="bg-white rounded-2xl shadow-lg p-8">
        <p>Aquí podrás gestionar las tandas de producción.</p>
        {/* Add production management UI here */}
      </div>
    </Layout>
  );
};

export default ProductionScreen;
