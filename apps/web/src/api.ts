// Cliente da API. VITE_API_URL é embutida no build: nunca coloque segredos em
// variáveis VITE_ (a chave da IA fica só no back-end).
const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const TOKEN_KEY = "estudos.token";

export type Interest = { id: number; label: string; depth: number };
export type Concept = { slug: string; title: string; discipline: string };
export type MappingRow = { universo: string; tecnico: string; trecho_base: string };
export type Payload = {
  conceito: string;
  cena: string;
  mapeamento: MappingRow[];
  onde_falha: string[];
  reformulacao_tecnica: string;
  pergunta_transferencia: { pergunta: string; resposta_esperada: string };
};
export type Explanation = {
  id: number | null;
  concept_slug: string;
  interest_label: string | null;
  provider: string;
  // approved = curada por pessoa; verified = aprovada na autoverificacao da IA
  // (ADR 0003); neutral = texto-base, quando nao ha personalizada valida
  status: string;
  personalized: boolean;
  payload: Payload | null;
  neutral_text: string | null;
  notice: string | null;
};
/** Resposta a uma pergunta livre dentro do conceito (RF11). */
export type Question = {
  status: "respondida" | "fora_do_conceito" | "sem_base";
  resposta: string;
  trechos: string[];
  concept_title: string;
};
export type ReadingPrefs = {
  font_scale: number;
  theme: "claro" | "escuro" | "alto-contraste" | "sistema";
  reduced_motion: boolean;
};

export const CONSENT_VERSION = "2026-1";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function token(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

async function call<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const t = token();
  if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(`${BASE}${path}`, { ...init, headers });
  if (!res.ok) {
    let detail = "Algo deu errado. Tente de novo.";
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      /* resposta sem corpo */
    }
    throw new ApiError(res.status, typeof detail === "string" ? detail : "Dados inválidos.");
  }
  return res.status === 204 ? (undefined as T) : res.json();
}

export async function ensureSession(): Promise<void> {
  if (token()) return;
  const { token: t } = await call<{ token: string }>("/v1/session", { method: "POST" });
  try {
    localStorage.setItem(TOKEN_KEY, t);
  } catch {
    /* navegação privada: a sessão vale só nesta aba */
  }
}

export function forgetSession() {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    /* ignore */
  }
}

export const api = {
  consent: (accepted: boolean) =>
    call<void>("/v1/consent", {
      method: "POST",
      body: JSON.stringify({ version: CONSENT_VERSION, accepted }),
    }),
  interests: () => call<Interest[]>("/v1/me/interests"),
  addInterest: (label: string, depth: number) =>
    call<Interest>("/v1/me/interests", { method: "POST", body: JSON.stringify({ label, depth }) }),
  removeInterest: (id: number) => call<void>(`/v1/me/interests/${id}`, { method: "DELETE" }),
  concepts: () => call<Concept[]>("/v1/concepts"),
  explain: (concept_slug: string, interest_id: number) =>
    call<Explanation>("/v1/explanations", {
      method: "POST",
      body: JSON.stringify({ concept_slug, interest_id }),
    }),
  neutral: (slug: string) => call<{ base_text: string }>(`/v1/concepts/${slug}/neutral`),
  // A pergunta nao e gravada no servidor: so e usada para montar a resposta.
  ask: (slug: string, pergunta: string, interest_id?: number) =>
    call<Question>(`/v1/concepts/${slug}/questions`, {
      method: "POST",
      body: JSON.stringify({ pergunta, interest_id }),
    }),
  feedback: (id: number, kind: "util" | "errada" | "confusa") =>
    call<void>(`/v1/explanations/${id}/feedback`, { method: "POST", body: JSON.stringify({ kind }) }),
  getPrefs: () => call<ReadingPrefs>("/v1/me/reading-prefs"),
  putPrefs: (p: ReadingPrefs) =>
    call<ReadingPrefs>("/v1/me/reading-prefs", { method: "PUT", body: JSON.stringify(p) }),
  exportData: () => call<unknown>("/v1/me/export"),
  deleteMe: () => call<void>("/v1/me", { method: "DELETE" }),
};
