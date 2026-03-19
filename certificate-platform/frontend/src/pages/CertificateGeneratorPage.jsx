import React, { useState } from 'react'
import { FiDownload, FiEye, FiUpload } from 'react-icons/fi'
import { certificateAPI, templateAPI } from '../utils/api'

const CertificateGeneratorPage = () => {
  const [templates, setTemplates] = useState([])
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [formData, setFormData] = useState({
    student_name: '',
    student_email: '',
    student_id: '',
    course: '',
    marks: '',
  })
  const [bulkFile, setBulkFile] = useState(null)

  React.useEffect(() => {
    const loadTemplates = async () => {
      try {
        const response = await templateAPI.getAll()
        setTemplates(response.data)
      } catch (error) {
        console.error('Failed to load templates:', error)
      }
    }

    loadTemplates()
  }, [])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const generateCertificate = async () => {
    if (!selectedTemplate || !formData.student_name || !formData.student_email) {
      alert('Please fill all required fields')
      return
    }

    try {
      const cert = await certificateAPI.create({
        template_id: selectedTemplate.id,
        ...formData,
      })

      alert('Certificate created! Now generating PDF...')

      // Generate the certificate
      await certificateAPI.generate(cert.data.id)
      alert('Certificate generated successfully!')
    } catch (error) {
      console.error('Failed to generate certificate:', error)
      alert('Failed to generate certificate')
    }
  }

  const handleBulkUpload = async (e) => {
    const file = e.target.files[0]
    if (!file || !selectedTemplate) {
      alert('Please select a template')
      return
    }

    try {
      const response = await certificateAPI.bulkUpload(selectedTemplate.id, file)
      alert(`Bulk upload started! Job ID: ${response.data.job_id}`)
    } catch (error) {
      console.error('Failed to upload bulk file:', error)
      alert('Failed to upload bulk file')
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold dark:text-white mb-6">Certificate Generator</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Single Certificate Generation */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold dark:text-white mb-4">Generate Single Certificate</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium dark:text-gray-300 mb-2">
                  Select Template *
                </label>
                <select
                  value={selectedTemplate?.id || ''}
                  onChange={(e) => {
                    const template = templates.find((t) => t.id === parseInt(e.target.value))
                    setSelectedTemplate(template)
                  }}
                  className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
                >
                  <option value="">Choose a template...</option>
                  {templates.map((template) => (
                    <option key={template.id} value={template.id}>
                      {template.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  name="student_name"
                  placeholder="Student Name *"
                  value={formData.student_name}
                  onChange={handleInputChange}
                  className="px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
                />
                <input
                  type="email"
                  name="student_email"
                  placeholder="Email *"
                  value={formData.student_email}
                  onChange={handleInputChange}
                  className="px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  name="student_id"
                  placeholder="Student ID"
                  value={formData.student_id}
                  onChange={handleInputChange}
                  className="px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
                />
                <input
                  type="text"
                  name="course"
                  placeholder="Course"
                  value={formData.course}
                  onChange={handleInputChange}
                  className="px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
                />
              </div>

              <input
                type="number"
                name="marks"
                placeholder="Marks"
                value={formData.marks}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
              />

              <button
                onClick={generateCertificate}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold"
              >
                <FiDownload /> Generate Certificate
              </button>
            </div>
          </div>
        </div>

        {/* Bulk Upload */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold dark:text-white mb-4">Bulk Upload</h2>

            <div className="space-y-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Upload an Excel file with columns: student_name, student_email, student_id, course, marks
              </p>

              <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition"
                onClick={() => document.getElementById('bulk-upload').click()}>
                <FiUpload size={32} className="mx-auto text-gray-400 mb-2" />
                <p className="text-sm font-medium dark:text-gray-300">Click to upload Excel file</p>
              </div>

              <input
                id="bulk-upload"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleBulkUpload}
                className="hidden"
              />

              <button
                disabled={!selectedTemplate}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50"
              >
                Start Upload
              </button>
            </div>
          </div>

          <div className="bg-green-50 dark:bg-green-900 rounded-lg p-4 text-sm text-green-800 dark:text-green-100">
            <p className="font-semibold mb-2">Info:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Supports Excel files (.xlsx, .xls)</li>
              <li>CSV format also accepted</li>
              <li>Max file size: 100 MB</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CertificateGeneratorPage
