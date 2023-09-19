/** @type {import('tailwindcss').Config} */
import plugin from 'tailwindcss/plugin'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundColor: {
        'grey-2': '#EAECF0',
        "pink-1": '#F2F4F7',
        "pink-2": "#FEE4E2",
        "green-2": "#D1FADF",
      },
      textColor: {
        "black-1": "#344054",
        "black-2": "#101828",
        "blue-1": "#2E90FA",
        "grey-1": "#98A2B3",
        "grey-2": "#667085",
        "green-1": "#054F31",
        "pink-2": "#FEE4E2",
        "red-1": "#D92D20",
        "red-2": "#7A271A"
      },
      borderColor: {
        'grey-2': '#EAECF0',
        'grey-1': '#D0D5DD',
      },
      gridTemplateColumns: {
        '14': 'repeat(14, minmax(0, 1fr))',
      }
    },
    textShadow: {
      sm: '0px 0px 4px var(--tw-shadow-color)',
      DEFAULT: '2px 2px 4px var(--tw-shadow-color)',
      lg: '4px 4px 8px var(--tw-shadow-color)',
      xl: '4px 4px 16px var(--tw-shadow-color)',
    }
  },
  plugins: [
    plugin(function ({ matchUtilities, theme }) {
      matchUtilities(
        {
          'text-shadow': (value) => ({
            textShadow: value,
          }),
        },
        { values: theme('textShadow') }
      )
    })
  ],
}

