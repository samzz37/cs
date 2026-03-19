import React, { useState, useEffect } from 'react'
import { FiDownload, FiFilter } from 'react-icons/fi'
import { rankingAPI, exportAPI } from '../utils/api'

const RankingPage = () => {
  const [rankings, setRankings] = useState([])
  const [event, setEvent] = useState('')
  const [year, setYear] = useState(new Date().getFullYear().toString())
  const [exporting, setExporting] = useState(false)

  const loadRankings = async () => {
    if (!event || !year) return

    try {
      const response = await rankingAPI.getByEvent(event, year)
      setRankings(response.data)
    } catch (error) {
      console.error('Failed to load rankings:', error)
    }
  }

  useEffect(() => {
    loadRankings()
  }, [event, year])

  const handleExport = async (format) => {
    setExporting(true)
    try {
      const response = await exportAPI.exportRankings(format)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `rankings.${format}`)
      document.body.appendChild(link)
      link.click()
      link.parentElement.removeChild(link)
    } catch (error) {
      console.error('Failed to export:', error)
      alert('Failed to export rankings')
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold dark:text-white mb-6">Merit Rankings</h1>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium dark:text-gray-300 mb-2">Event</label>
            <input
              type="text"
              value={event}
              onChange={(e) => setEvent(e.target.value)}
              placeholder="Enter event name"
              className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
            />
          </div>

          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium dark:text-gray-300 mb-2">Academic Year</label>
            <select
              value={year}
              onChange={(e) => setYear(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
            >
              {[2024, 2023, 2022, 2021].map((y) => (
                <option key={y} value={y.toString()}>
                  {y}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={loadRankings}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition h-fit"
          >
            <FiFilter /> Filter
          </button>
        </div>

        {/* Export Buttons */}
        <div className="mt-6 flex gap-2 flex-wrap">
          <button
            onClick={() => handleExport('pdf')}
            disabled={exporting}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50"
          >
            <FiDownload /> Export PDF
          </button>
          <button
            onClick={() => handleExport('excel')}
            disabled={exporting}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50"
          >
            <FiDownload /> Export Excel
          </button>
          <button
            onClick={() => handleExport('csv')}
            disabled={exporting}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            <FiDownload /> Export CSV
          </button>
          <button
            onClick={() => handleExport('word')}
            disabled={exporting}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
          >
            <FiDownload /> Export Word
          </button>
        </div>
      </div>

      {/* Rankings Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        {rankings.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold dark:text-white">Rank</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold dark:text-white">Student Name</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold dark:text-white">Email</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold dark:text-white">Marks</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold dark:text-white">Grade</th>
                </tr>
              </thead>
              <tbody className="divide-y dark:divide-gray-700">
                {rankings.map((ranking, index) => (
                  <tr key={ranking.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition">
                    <td className="px-6 py-3 text-sm dark:text-gray-300">
                      <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white font-bold">
                        {index + 1}
                      </span>
                    </td>
                    <td className="px-6 py-3 text-sm font-medium dark:text-white">{ranking.student_name}</td>
                    <td className="px-6 py-3 text-sm dark:text-gray-300">{ranking.student_email}</td>
                    <td className="px-6 py-3 text-sm dark:text-gray-300 font-semibold text-yellow-600">
                      {ranking.marks}
                    </td>
                    <td className="px-6 py-3 text-sm dark:text-gray-300">{ranking.grade || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-12 text-center text-gray-500 dark:text-gray-400">
            <p>No rankings found. Select filters and search to display data.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default RankingPage
