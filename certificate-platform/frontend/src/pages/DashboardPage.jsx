import React, { useState } from 'react'
import { FiTrendingUp, FiUsers, FiFileText, FiServer } from 'react-icons/fi'
import StatCard from '../components/StatCard'
import ActivityLog from '../components/ActivityLog'
import { dashboardAPI } from '../utils/api'

const DashboardPage = () => {
  const [stats, setStats] = useState({
    certificates_today: 0,
    active_users: 0,
    total_templates: 0,
    total_certificates: 0,
    cpu_usage: 0,
    memory_usage: 0,
    disk_usage: 0,
  })

  React.useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await dashboardAPI.getStats()
        setStats(response.data)
      } catch (error) {
        console.error('Failed to load stats:', error)
      }
    }

    loadStats()
    const interval = setInterval(loadStats, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Welcome back! Here's your system overview.</p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={FiFileText}
          label="Certificates Today"
          value={stats.certificates_today}
          color="bg-blue-500"
        />
        <StatCard
          icon={FiUsers}
          label="Active Users"
          value={stats.active_users}
          color="bg-green-500"
        />
        <StatCard
          icon={FiFileText}
          label="Total Templates"
          value={stats.total_templates}
          color="bg-purple-500"
        />
        <StatCard
          icon={FiTrendingUp}
          label="Total Certificates"
          value={stats.total_certificates}
          color="bg-orange-500"
        />
      </div>

      {/* System Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <FiServer className="text-red-500" size={24} />
            <h3 className="font-semibold dark:text-white">CPU Usage</h3>
          </div>
          <div className="text-3xl font-bold dark:text-white">{stats.cpu_usage.toFixed(1)}%</div>
          <div className="mt-4 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-red-500 h-2 rounded-full"
              style={{ width: `${stats.cpu_usage}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <FiServer className="text-yellow-500" size={24} />
            <h3 className="font-semibold dark:text-white">Memory Usage</h3>
          </div>
          <div className="text-3xl font-bold dark:text-white">{stats.memory_usage.toFixed(1)}%</div>
          <div className="mt-4 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-yellow-500 h-2 rounded-full"
              style={{ width: `${stats.memory_usage}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <FiServer className="text-blue-500" size={24} />
            <h3 className="font-semibold dark:text-white">Disk Usage</h3>
          </div>
          <div className="text-3xl font-bold dark:text-white">{stats.disk_usage.toFixed(1)}%</div>
          <div className="mt-4 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full"
              style={{ width: `${stats.disk_usage}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Activity Log */}
      <ActivityLog />
    </div>
  )
}

export default DashboardPage
