/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: {
    content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
    options: {
      safelist: [],  
    }
  },
  darkMode: false, 
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [],
}
