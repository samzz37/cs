import React from 'react'

const StatCard = ({ icon: Icon, label, value, color }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">{label}</p>
          <p className="text-3xl font-bold dark:text-white mt-2">{value}</p>
        </div>
        <div className={`${color} p-4 rounded-lg`}>
          <Icon size={28} className="text-white" />
        </div>
      </div>
    </div>
  )
}

export default StatCard
