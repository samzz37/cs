import React, { useState } from 'react'
import { FiSave, FiPhone } from 'react-icons/fi'

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    sms_alert_numbers: '',
    theme_mode: 'light',
    enable_sms_alerts: false,
    max_upload_size_mb: 100,
    session_timeout_minutes: 30,
    certificate_expiry_days: 365,
  })

  const handleChange = (field, value) => {
    setSettings((prev) => ({ ...prev, [field]: value }))
  }

  const saveSettings = async () => {
    try {
      // Save to backend
      alert('Settings saved successfully!')
    } catch (error) {
      console.error('Failed to save settings:', error)
      alert('Failed to save settings')
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold dark:text-white mb-6">System Settings</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* General Settings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold dark:text-white mb-6">General Settings</h2>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium dark:text-gray-300 mb-2">
                Theme Mode
              </label>
              <select
                value={settings.theme_mode}
                onChange={(e) => handleChange('theme_mode', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="auto">Auto</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium dark:text-gray-300 mb-2">
                Session Timeout (minutes)
              </label>
              <input
                type="number"
                value={settings.session_timeout_minutes}
                onChange={(e) => handleChange('session_timeout_minutes', parseInt(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium dark:text-gray-300 mb-2">
                Max Upload Size (MB)
              </label>
              <input
                type="number"
                value={settings.max_upload_size_mb}
                onChange={(e) => handleChange('max_upload_size_mb', parseInt(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium dark:text-gray-300 mb-2">
                Certificate Expiry (days)
              </label>
              <input
                type="number"
                value={settings.certificate_expiry_days}
                onChange={(e) => handleChange('certificate_expiry_days', parseInt(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
              />
            </div>
          </div>
        </div>

        {/* SMS Alert Settings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold dark:text-white mb-6">SMS Alerts</h2>

          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="enable_sms"
                checked={settings.enable_sms_alerts}
                onChange={(e) => handleChange('enable_sms_alerts', e.target.checked)}
                className="w-4 h-4 rounded"
              />
              <label htmlFor="enable_sms" className="text-sm font-medium dark:text-gray-300">
                Enable SMS Alerts
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium dark:text-gray-300 mb-2 flex items-center gap-2">
                <FiPhone size={16} /> Alert Phone Numbers
              </label>
              <textarea
                value={settings.sms_alert_numbers}
                onChange={(e) => handleChange('sms_alert_numbers', e.target.value)}
                placeholder="Enter phone numbers separated by commas&#10;Example: +1234567890, +0987654321"
                className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg h-24"
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                Separate multiple numbers with commas. Include country code.
              </p>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 text-sm text-blue-800 dark:text-blue-100">
              <p className="font-semibold mb-2">Alert Types</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Server crash</li>
                <li>Database failure</li>
                <li>Certificate generation failure</li>
                <li>High system resource usage</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="mt-8">
        <button
          onClick={saveSettings}
          className="flex items-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition font-semibold"
        >
          <FiSave /> Save Settings
        </button>
      </div>
    </div>
  )
}

export default SettingsPage
