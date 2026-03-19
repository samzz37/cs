import { create } from 'zustand'

export const useAuthStore = create((set) => ({
    user: null,
    token: null,
    isAuthenticated: false,
    login: (user, token) => set({ user, token, isAuthenticated: true }),
    logout: () => set({ user: null, token: null, isAuthenticated: false }),
    setUser: (user) => set({ user }),
}))

export const useDashboardStore = create((set) => ({
    stats: {
        certificates_today: 0,
        active_users: 0,
        total_templates: 0,
        total_certificates: 0,
        cpu_usage: 0,
        memory_usage: 0,
        disk_usage: 0,
    },
    setStats: (stats) => set({ stats }),
    updateStat: (key, value) => set((state) => ({
        stats: {...state.stats, [key]: value }
    })),
}))

export const useTemplateStore = create((set) => ({
    templates: [],
    selectedTemplate: null,
    isLoading: false,
    setTemplates: (templates) => set({ templates }),
    selectTemplate: (template) => set({ selectedTemplate: template }),
    addTemplate: (template) => set((state) => ({
        templates: [...state.templates, template]
    })),
    setLoading: (isLoading) => set({ isLoading }),
}))

export const useCertificateStore = create((set) => ({
    certificates: [],
    filters: { status: 'all', search: '' },
    isLoading: false,
    setCertificates: (certificates) => set({ certificates }),
    setFilter: (filter) => set((state) => ({
        filters: {...state.filters, ...filter }
    })),
    setLoading: (isLoading) => set({ isLoading }),
}))

export const useMonitoringStore = create((set) => ({
    systemStats: null,
    activeUsers: [],
    alerts: [],
    setSystemStats: (stats) => set({ systemStats: stats }),
    setActiveUsers: (users) => set({ activeUsers: users }),
    addAlert: (alert) => set((state) => ({
        alerts: [alert, ...state.alerts].slice(0, 50)
    })),
}))