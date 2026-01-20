import type { Config } from 'tailwindcss';

const config: Config = {
  // 1. Content: Point this to every file in your project that contains Tailwind class names.
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./index.html",
    "./node_modules/@tremor/**/*.{js,ts,jsx,tsx}" 
    // Add "./app/**/*.{js,ts,jsx,tsx}" if using Next.js App Router
  ],
  
  // 2. Theme: Customizations go here.
  theme: {
    extend: {
      colors: {
        // Example: defining a custom brand color palette
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        // Example: adding a custom font stack
        sans: ['Inter', 'sans-serif'],
      },
      // Breakpoints
      screens: {
        'xs': '475px', // Adding a smaller breakpoint
      },
    },
  },

  // 3. Plugins: Official plugins are highly recommended for complex UIs.
  plugins: [
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
  ],
};

export default config;