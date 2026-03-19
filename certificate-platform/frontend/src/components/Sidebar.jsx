import React from 'react'
import { Link } from 'react-router-dom'
import { FiHome, FiLayout, FiFileText, FiTrendingUp, FiSettings, FiMonitor, FiLogOut } from 'react-icons/fi'
import { useLogout } from '../hooks/index'

const Sidebar = () => {
  const { handleLogout } = useLogout()

  const menuItems = [
    { label: 'Dashboard', icon: FiHome, path: '/dashboard' },
    { label: 'Templates', icon: FiLayout, path: '/templates' },
    { label: 'Certificates', icon: FiFileText, path: '/certificates' },
    { label: 'Rankings', icon: FiTrendingUp, path: '/rankings' },
    { label: 'Monitoring', icon: FiMonitor, path: '/monitoring' },
    { label: 'Settings', icon: FiSettings, path: '/settings' },
  ]

  return (
    <aside className="w-64 bg-gradient-to-b from-blue-900 to-blue-800 text-white shadow-lg">
      <div className="p-6 border-b border-blue-700">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <span className="text-yellow-400">📜</span> CertHub
        </h1>
        <p className="text-sm text-blue-100 mt-1">Certificate Management</p>
      </div>

      <nav className="p-4 space-y-2">
        {menuItems.map((item) => (
          <Link
            key={item.label}
            to={item.path}
            className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="absolute bottom-0 w-64 p-4 border-t border-blue-700">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition justify-center"
        >
          <FiLogOut size={18} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
