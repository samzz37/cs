import axios from 'axios'

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
})

// Add token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export const authAPI = {
    register: (data) => api.post('/auth/register', data),
    login: (data) => api.post('/auth/login', data),
    getCurrentUser: () => api.get('/auth/me'),
}

export const dashboardAPI = {
    getStats: () => api.get('/dashboard/stats'),
    getActivityLogs: (limit = 50) => api.get(`/dashboard/activity-logs?limit=${limit}`),
}

export const templateAPI = {
    getAll: (skip = 0, limit = 100) => api.get(`/templates?skip=${skip}&limit=${limit}`),
    getById: (id) => api.get(`/templates/${id}`),
    create: (data) => api.post('/templates', data),
    update: (id, data) => api.put(`/templates/${id}`, data),
    uploadBackground: (id, file) => {
        const formData = new FormData()
        formData.append('file', file)
        return api.post(`/templates/${id}/upload-background`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
    },
}

export const certificateAPI = {
    getAll: (skip = 0, limit = 100) => api.get(`/certificates?skip=${skip}&limit=${limit}`),
    getById: (id) => api.get(`/certificates/${id}`),
    create: (data) => api.post('/certificates', data),
    generate: (id) => api.post(`/certificates/${id}/generate`),
    bulkUpload: (templateId, file) => {
        const formData = new FormData()
        formData.append('template_id', templateId)
        formData.append('file', file)
        return api.post('/certificates/bulk-upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
    },
}

export const rankingAPI = {
    getByEvent: (event, year) => api.get(`/rankings/event/${event}?year=${year}`),
    getByDepartment: (department) => api.get(`/rankings/department/${department}`),
    importRankings: (data) => api.post('/rankings/import', data),
}

export const exportAPI = {
    exportRankings: (format) => api.get(`/export/rankings/${format}`),
    exportCertificates: (format) => api.get(`/export/certificates/${format}`),
}

export const monitoringAPI = {
    getSystemStats: () => api.get('/monitoring/system'),
    getActiveUsers: () => api.get('/monitoring/active-users'),
}

export default api