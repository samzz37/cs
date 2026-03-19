import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore, useDashboardStore } from './context/store'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import TemplateDesignerPage from './pages/TemplateDesignerPage'
import CertificateGeneratorPage from './pages/CertificateGeneratorPage'
import RankingPage from './pages/RankingPage'
import SettingsPage from './pages/SettingsPage'
import MonitoringPage from './pages/MonitoringPage'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  useEffect(() => {
    // Load dark mode preference
    const isDark = localStorage.getItem('darkMode') === 'true'
    setDarkMode(isDark)
    if (isDark) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode
    setDarkMode(newDarkMode)
    localStorage.setItem('darkMode', newDarkMode)
    if (newDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return (
    <Router>
      <div className={`flex h-screen ${darkMode ? 'dark' : ''}`}>
        {isAuthenticated && sidebarOpen && <Sidebar />}
        
        <div className="flex-1 flex flex-col overflow-hidden">
          {isAuthenticated && (
            <Navbar 
              darkMode={darkMode} 
              toggleDarkMode={toggleDarkMode}
              toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
            />
          )}
          
          <main className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-900">
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                }
              />
              
              <Route 
                path="/templates" 
                element={
                  <ProtectedRoute>
                    <TemplateDesignerPage />
                  </ProtectedRoute>
                }
              />
              
              <Route 
                path="/certificates" 
                element={
                  <ProtectedRoute>
                    <CertificateGeneratorPage />
                  </ProtectedRoute>
                }
              />
              
              <Route 
                path="/rankings" 
                element={
                  <ProtectedRoute>
                    <RankingPage />
                  </ProtectedRoute>
                }
              />
              
              <Route 
                path="/monitoring" 
                element={
                  <ProtectedRoute>
                    <MonitoringPage />
                  </ProtectedRoute>
                }
              />
              
              <Route 
                path="/settings" 
                element={
                  <ProtectedRoute>
                    <SettingsPage />
                  </ProtectedRoute>
                }
              />
              
              <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
