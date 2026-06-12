/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'hw-red': {
          50: '#FFF0F2',
          100: '#FFD6DB',
          200: '#FFADB8',
          300: '#FF8595',
          400: '#FF5C72',
          500: '#E6002D',   // primary Huawei Red
          600: '#CE0E2D',   // dark Huawei Red
          700: '#A3001E',
          800: '#7A0014',
          900: '#52000A',
        },
        'hw-gray': {
          50: '#F7F8FA',
          100: '#EEF0F4',
          200: '#DDE1E8',
          300: '#C5CAD5',
          400: '#A1A8B5',
          500: '#7E8594',
          600: '#5E6573',
          700: '#3D4352',
          800: '#1E2432',
          900: '#0F131E',
        },
        'hw-gold': {
          400: '#F5C842',
          500: '#D4A830',
          600: '#B0891E',
        },
      },
      fontFamily: {
        display: ['"HarmonyOS Sans"', '"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
    },
  },
  plugins: [],
}
