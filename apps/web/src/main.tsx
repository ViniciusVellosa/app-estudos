import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles/base.css";
// Estilo vidro: só aparência (ver o cabeçalho do arquivo); remover este import
// volta ao visual sólido sem mudar comportamento.
import "./styles/glass.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
