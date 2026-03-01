import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}', './app/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0a0a0f',
          800: '#12121a',
          700: '#1a1a26',
          600: '#252533',
        },
        accent: {
          blue: '#3b82f6',
          purple: '#8b5cf6',
        },
      },
      backgroundImage: {
        'gradient-cyber': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #6366f1 100%)',
        'gradient-subtle': 'linear-gradient(180deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.08) 100%)',
      },
      animation: {
        'scan': 'scan 2s ease-in-out infinite',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
      },
      keyframes: {
        scan: {
          '0%, 100%': { opacity: '0.3', transform: 'translateY(-10px)' },
          '50%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
