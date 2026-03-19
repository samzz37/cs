import React, { useState, useEffect } from 'react'
import { dashboardAPI } from '../utils/api'

const ActivityLog = () => {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    const loadLogs = async () => {
      try {
        const response = await dashboardAPI.getActivityLogs(20)
        setLogs(response.data)
      } catch (error) {
        console.error('Failed to load logs:', error)
      }
    }

    loadLogs()
    const interval = setInterval(loadLogs, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold dark:text-white mb-4">Recent Activity</h3>
      <div className="space-y-3">
        {logs.map((log) => (
          <div key={log.id} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-gray-700 rounded transition">
            <div>
              <p className="font-medium dark:text-white">{log.action}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">{log.description}</p>
            </div>
            <span className="text-xs text-gray-500">
              {new Date(log.created_at).toLocaleString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ActivityLog
