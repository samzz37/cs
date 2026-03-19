import React, { useState, useRef } from 'react'
import { fabric } from 'fabric'
import { FiPlus, FiDownload, FiUpload } from 'react-icons/fi'
import { templateAPI } from '../utils/api'

const TemplateDesignerPage = () => {
  const canvasRef = useRef(null)
  const [canvas, setCanvas] = useState(null)
  const [templateName, setTemplateName] = useState('')
  const [templates, setTemplates] = useState([])

  React.useEffect(() => {
    // Initialize Fabric canvas
    const fabricCanvas = new fabric.Canvas(canvasRef.current, {
      width: 1000,
      height: 700,
      backgroundColor: '#f5f5f5',
    })
    setCanvas(fabricCanvas)

    return () => fabricCanvas.dispose()
  }, [])

  const addTextElement = () => {
    if (!canvas) return
    const text = new fabric.Text('Click to edit', {
      left: 100,
      top: 100,
      fontSize: 20,
      fill: '#000',
    })
    canvas.add(text)
    canvas.renderAll()
  }

  const addImageElement = async (e) => {
    const file = e.target.files[0]
    if (!file || !canvas) return

    const reader = new FileReader()
    reader.onload = (event) => {
      fabric.Image.fromURL(event.target.result, (img) => {
        img.set({ left: 100, top: 100, scaleX: 0.5, scaleY: 0.5 })
        canvas.add(img)
        canvas.renderAll()
      })
    }
    reader.readAsDataURL(file)
  }

  const addQRCodeElement = () => {
    if (!canvas) return
    const qr = new fabric.Rect({
      left: 500,
      top: 100,
      width: 150,
      height: 150,
      fill: '#fff',
      stroke: '#000',
    })
    canvas.add(qr)
    canvas.renderAll()
  }

  const saveTemplate = async () => {
    if (!templateName || !canvas) {
      alert('Please enter template name')
      return
    }

    const templateJson = JSON.stringify(canvas.toJSON())

    try {
      await templateAPI.create({
        name: templateName,
        description: 'Custom template',
        template_json: templateJson,
        orientation: 'landscape',
        width: 11,
        height: 8.5,
      })
      alert('Template saved successfully!')
      setTemplateName('')
    } catch (error) {
      console.error('Failed to save template:', error)
      alert('Failed to save template')
    }
  }

  const downloadTemplate = () => {
    if (!canvas) return
    const dataUrl = canvas.toDataURL('image/png')
    const link = document.createElement('a')
    link.href = dataUrl
    link.download = `template-${Date.now()}.png`
    link.click()
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold dark:text-white mb-6">Certificate Template Designer</h1>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <canvas ref={canvasRef} className="border-2 border-gray-300 dark:border-gray-600 mx-auto" />
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 className="font-semibold dark:text-white mb-4">Template Tools</h3>

            <div className="space-y-3">
              <input
                type="text"
                placeholder="Template Name"
                value={templateName}
                onChange={(e) => setTemplateName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:bg-gray-700 dark:text-white dark:border-gray-600 rounded-lg"
              />

              <button
                onClick={addTextElement}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                <FiPlus /> Add Text
              </button>

              <button
                onClick={() => document.getElementById('image-upload').click()}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
              >
                <FiUpload /> Upload Image
              </button>
              <input
                id="image-upload"
                type="file"
                accept="image/*"
                onChange={addImageElement}
                className="hidden"
              />

              <button
                onClick={addQRCodeElement}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
              >
                <FiPlus /> Add QR Code
              </button>

              <button
                onClick={saveTemplate}
                className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition font-semibold"
              >
                Save Template
              </button>

              <button
                onClick={downloadTemplate}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
              >
                <FiDownload /> Download
              </button>
            </div>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 text-sm text-blue-800 dark:text-blue-100">
            <p className="font-semibold mb-2">Tips:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Drag elements to move</li>
              <li>Use corners to resize</li>
              <li>Double-click text to edit</li>
              <li>Delete with Backspace key</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TemplateDesignerPage
