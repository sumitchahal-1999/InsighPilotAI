import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#0B0F19",
        "background-dark": "#050811",
        surface: "#10141D",
        "surface-container": "#161B26",
        "surface-container-high": "#1E2433",
        "surface-dim": "#0E121A",
        "surface-bright": "#22293A",
        "on-surface": "#D4E4FA",
        "on-surface-variant": "#94A3B8",
        outline: "#334155",
        "outline-variant": "rgba(255, 255, 255, 0.08)",
        primary: {
          DEFAULT: "#4FDEC8",
          dark: "#14B8A6",
          container: "#005048",
          "on-container": "#70F8E2",
          glow: "rgba(79, 222, 200, 0.25)",
        },
        secondary: {
          DEFAULT: "#38BDF8",
          container: "#0369A1",
          "on-container": "#BAE6FD",
        },
        tertiary: {
          DEFAULT: "#A855F7",
          container: "#6B21A8",
        },
        error: {
          DEFAULT: "#FFB4AB",
          container: "#93000A",
          solid: "#EF4444",
        },
        warning: {
          DEFAULT: "#F59E0B",
          container: "#78350F",
        },
        success: {
          DEFAULT: "#10B981",
          container: "#064E3B",
        },
      },
      fontFamily: {
        display: ["Manrope", "Inter", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 0 20px rgba(79, 222, 200, 0.15)",
        "glow-lg": "0 0 35px rgba(79, 222, 200, 0.25)",
        "glow-error": "0 0 20px rgba(239, 68, 68, 0.2)",
        panel: "0 8px 32px 0 rgba(0, 0, 0, 0.4)",
      },
    },
  },
  plugins: [],
};

export default config;
