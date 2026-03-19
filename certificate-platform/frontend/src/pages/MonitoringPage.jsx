import React, { useState, useEffect } from 'react'
import { FiRefreshCw, FiDownload } from 'react-icons/fi'
import { monitoringAPI } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const MonitoringPage = () => {
  const [systemStats, setSystemStats] = useState(null)
  const [activeUsers, setActiveUsers] = useState([])
  const [chartData, setChartData] = useState([])

  const loadData = async () => {
    try {
      const [statsRes, usersRes] = await Promise.all([
        monitoringAPI.getSystemStats(),
        monitoringAPI.getActiveUsers(),
      ])

      setSystemStats(statsRes.data)
      setActiveUsers(usersRes.data)

      // Add to chart data
      setChartData((prev) => [
        ...prev,
        {
          time: new Date().toLocaleTimeString(),
          cpu: statsRes.data.cpu_usage,
          memory: statsRes.data.memory_usage,
          disk: statsRes.data.disk_usage,
        },
      ].slice(-20))
    } catch (error) {
      console.error('Failed to load monitoring data:', error)
    }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 2000)
    return () => clearInterval(interval)
  }, [])

  if (!systemStats) {
    return <div className="p-8 text-center">Loading monitoring data...</div>
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold dark:text-white">System Monitoring</h1>
        <button
          onClick={loadData}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <FiRefreshCw /> Refresh
        </button>
      </div>

      {/* Real-time Stats */}
      <div className="grid grid-cols- 1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gradient-to-br from-red-500 to-red-600 text-white rounded-lg shadow-lg p-6">
          <h3 className="text-sm font-semibold opacity-90">CPU Usage</h3>
          <p className="text-4xl font-bold mt-2">
            {systemStats.cpu_usage ? systemStats.cpu_usage.toFixed(1) : '0'}%
          </p>
          <div className="mt-4 bg-red-400 rounded-full h-2">
            <div
              className="bg-white h-2 rounded-full transition"
              style={{ width: `${Math.min(systemStats.cpu_usage || 0, 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-white rounded-lg shadow-lg p-6">
          <h3 className="text-sm font-semibold opacity-90">Memory Usage</h3>
          <p className="text-4xl font-bold mt-2">
            {systemStats.memory_usage ? systemStats.memory_usage.toFixed(1) : '0'}%
          </p>
          <div className="mt-4 bg-yellow-400 rounded-full h-2">
            <div
              className="bg-white h-2 rounded-full transition"
              style={{ width: `${Math.min(systemStats.memory_usage || 0, 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg shadow-lg p-6">
          <h3 className="text-sm font-semibold opacity-90">Disk Usage</h3>
          <p className="text-4xl font-bold mt-2">
            {systemStats.disk_usage ? systemStats.disk_usage.toFixed(1) : '0'}%
          </p>
          <div className="mt-4 bg-blue-400 rounded-full h-2">
            <div
              className="bg-white h-2 rounded-full transition"
              style={{ width: `${Math.min(systemStats.disk_usage || 0, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Chart */}
      {chartData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
          <h3 className="text-xl font-semibold dark:text-white mb-4">System Usage Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="cpu" fill="#ef4444" name="CPU %" />
              <Bar dataKey="memory" fill="#f59e0b" name="Memory %" />
              <Bar dataKey="disk" fill="#3b82f6" name="Disk %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Active Users */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold dark:text-white mb-4">Active Users ({activeUsers.length})</h3>
        {activeUsers.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-100 dark:bg-gray-700">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold">User ID</th>
                  <th className="px-4 py-2 text-left font-semibold">Current Page</th>
                  <th className="px-4 py-2 text-left font-semibold">Login Time</th>
                  <th className="px-4 py-2 text-left font-semibold">Last Activity</th>
                </tr>
              </thead>
              <tbody className="divide-y dark:divide-gray-700">
                {activeUsers.map((user) => (
                  <tr key={user.session_id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-4 py-2 dark:text-gray-300">User #{user.user_id}</td>
                    <td className="px-4 py-2 dark:text-gray-300">{user.current_page || 'Dashboard'}</td>
                    <td className="px-4 py-2 text-xs dark:text-gray-400">
                      {new Date(user.login_time).toLocaleTimeString()}
                    </td>
                    <td className="px-4 py-2 text-xs dark:text-gray-400">
                      {user.last_activity ? new Date(user.last_activity).toLocaleTimeString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500 dark:text-gray-400">No active users</p>
        )}
      </div>
    </div>
  )
}

export default MonitoringPage
