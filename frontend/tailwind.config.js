/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["GrosVentre", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        gros: ["GrosVentre", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        bildungswirkung: ["Bildungswirkung", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      boxShadow: {
        panel: "0 18px 50px rgba(15, 23, 42, 0.08)",
      },
    },
  },
  plugins: [],
};
