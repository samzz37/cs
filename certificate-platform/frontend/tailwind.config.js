/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,jsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: '#1F4788',
                secondary: '#D4AF37',
                success: '#10B981',
                warning: '#F59E0B',
                error: '#EF4444',
                info: '#0EA5E9',
            },
            fontFamily: {
                sans: ['Segoe UI', 'Roboto', 'sans-serif'],
            },
            animation: {
                fadeIn: 'fadeIn 0.3s ease-in',
                slideUp: 'slideUp 0.3s ease-out',
                pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(10px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
            },
        },
    },
    plugins: [],
}