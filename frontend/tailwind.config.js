/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{js,jsx,ts,tsx}",  // This ensures Tailwind purges unused styles from all your React files
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  