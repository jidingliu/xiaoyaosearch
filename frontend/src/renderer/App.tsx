import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'

import MainLayout from '@/renderer/components/Layout/MainLayout'
import SearchPage from '@/renderer/pages/SearchPage'
import IndexPage from '@/renderer/pages/IndexPage'
import SettingsPage from '@/renderer/pages/SettingsPage'
import FavoritesPage from '@/renderer/pages/FavoritesPage'

const App: React.FC = () => {
  return (
    <div className="app">
      <Layout style={{ height: '100vh' }}>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<SearchPage />} />
            <Route path="search" element={<SearchPage />} />
            <Route path="index" element={<IndexPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="favorites" element={<FavoritesPage />} />
          </Route>
        </Routes>
      </Layout>
    </div>
  )
}

export default App