// frontend/src/screens/RecipeScreen.js
import React from 'react';
import Layout from '../components/Layout';
import Breadcrumbs from '../components/Breadcrumbs';

const RecipeScreen = () => {
  return (
    <Layout>
      <Breadcrumbs items={[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Recetas' }]} />
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Gestión de Recetas</h1>
      <div className="bg-white rounded-2xl shadow-lg p-8">
        <p>Aquí podrás gestionar las recetas de tus productos.</p>
        {/* Add recipe management UI here */}
      </div>
    </Layout>
  );
};

export default RecipeScreen;
