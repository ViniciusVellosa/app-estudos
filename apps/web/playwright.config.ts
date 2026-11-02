import { defineConfig, devices } from "@playwright/test";

// Testes de ponta a ponta: sobem a API e o front-end antes de rodar.
// Em CI, use `docker compose up --wait` e defina BASE_URL.
export default defineConfig({
  testDir: "e2e",
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:4173",
    launchOptions: process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {},
  },
  projects: [
    { name: "celular", use: { ...devices["Pixel 7"] } },
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
  ],
  webServer: process.env.BASE_URL
    ? undefined
    : [
        {
          command: "cd ../api && DATABASE_URL=sqlite:///./e2e.db CORS_ORIGINS='[\"http://localhost:4173\"]' uv run uvicorn app.main:app --port 8000",
          url: "http://localhost:8000/v1/health",
          reuseExistingServer: true,
        },
        {
          command: "npm run build && npx vite preview --port 4173 --strictPort",
          url: "http://localhost:4173",
          reuseExistingServer: true,
        },
      ],
});
