import React from 'react'
import { FiMenu, FiSun, FiMoon, FiBell } from 'react-icons/fi'

const Navbar = ({ darkMode, toggleDarkMode, toggleSidebar }) => {
  return (
    <nav className="bg-white dark:bg-gray-800 shadow-md border-b dark:border-gray-700">
      <div className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
          >
            <FiMenu size={24} className="text-gray-700 dark:text-gray-300" />
          </button>
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">
            Certificate Platform
          </h2>
        </div>

        <div className="flex items-center gap-4">
          <button
            className="relative p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
          >
            <FiBell size={24} className="text-gray-700 dark:text-gray-300" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-600 rounded-full"></span>
          </button>

          <button
            onClick={toggleDarkMode}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
          >
            {darkMode ? (
              <FiSun size={24} className="text-yellow-500" />
            ) : (
              <FiMoon size={24} className="text-gray-700" />
            )}
          </button>

          <div className="flex items-center gap-3 pl-4 border-l dark:border-gray-700">
            <img
              src="https://via.placeholder.com/40"
              alt="User"
              className="w-10 h-10 rounded-full"
            />
            <div>
              <p className="text-sm font-semibold dark:text-white">Admin User</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">Administrator</p>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
