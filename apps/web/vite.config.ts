import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 5173 },
  // Vitest cobre só os testes de unidade em src/. O e2e/ é do Playwright: o
  // test() dele falha se outro runner coletar o arquivo.
  test: { environment: "node", include: ["src/**/*.{test,spec}.{ts,tsx}"] },
});
