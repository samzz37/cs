import { useEffect, useState } from 'react'
import { useAuthStore } from '../context/store'

export const useWebSocket = (url) => {
    const [data, setData] = useState(null)
    const [isConnected, setIsConnected] = useState(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (!token) return

        const wsUrl = `${url}?token=${token}`
        const ws = new WebSocket(wsUrl)

        ws.onopen = () => setIsConnected(true)
        ws.onmessage = (event) => setData(JSON.parse(event.data))
        ws.onerror = (error) => setError(error)
        ws.onclose = () => setIsConnected(false)

        return () => ws.close()
    }, [url])

    return { data, isConnected, error }
}

export const useLogin = () => {
    const login = useAuthStore((state) => state.login)
    const setUser = useAuthStore((state) => state.setUser)

    const handleLogin = (user, token) => {
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
        login(user, token)
    }

    return { handleLogin }
}

export const useLogout = () => {
    const logout = useAuthStore((state) => state.logout)

    const handleLogout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        logout()
    }

    return { handleLogout }
}

export const useDebounce = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value)

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value)
        }, delay)

        return () => clearTimeout(handler)
    }, [value, delay])

    return debouncedValue
}

export const useFetch = (url) => {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchData = async() => {
            try {
                const response = await fetch(url)
                const json = await response.json()
                setData(json)
            } catch (err) {
                setError(err)
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [url])

    return { data, loading, error }
}