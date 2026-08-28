import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // public/data/build/*.json is fetched at runtime, so it stays in public/
  // rather than being bundled - contexts can be added without a rebuild.
  server: { open: true },
});
