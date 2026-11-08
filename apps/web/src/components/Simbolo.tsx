/**
 * Símbolo do app: duas peças de quebra-cabeça que se encaixam. À esquerda, o
 * livro (o conteúdo técnico); à direita, o planeta (o universo do aluno). É a
 * ideia do app em uma imagem: a analogia conecta os dois.
 *
 * Desenhado em SVG, e não como imagem, por dois motivos de acessibilidade:
 * - fica nítido em qualquer ampliação (WCAG 1.4.4, persona Ana);
 * - as cores vêm dos tokens, então o símbolo acompanha os temas claro,
 *   escuro e alto contraste (amarelo sobre preto).
 *
 * É decorativo: o nome do app está escrito ao lado, então o SVG fica fora da
 * árvore de acessibilidade (`aria-hidden`) para o leitor de tela não repetir.
 */
export function Simbolo({ className = "simbolo" }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 120 76" aria-hidden="true" focusable="false">
      {/* Cada peça é um caminho só, para que o contorno (usado nos temas
          escuro e de alto contraste) não risque o interior da peça. */}
      {/* peça da esquerda: o conhecimento, com o pino em cima e o encaixe à direita */}
      <path
        className="simbolo-peca simbolo-peca-a"
        d="M12 18H20.96A10 10 0 1 1 40.04 18H49A9 9 0 0 1 58 27V35.55A10.5 10.5 0 0 0 58 56.45V64A9 9 0 0 1 49 73H12A9 9 0 0 1 3 64V27A9 9 0 0 1 12 18Z"
      />
      {/* peça da direita: o universo do aluno, com o pino entrando no encaixe */}
      <path
        className="simbolo-peca simbolo-peca-b"
        d="M71 18H108A9 9 0 0 1 117 27V64A9 9 0 0 1 108 73H71A9 9 0 0 1 62 64V53.42A8 8 0 1 1 62 38.58V27A9 9 0 0 1 71 18Z"
      />

      {/* livro aberto */}
      <path
        className="simbolo-traco"
        d="M15 37c5-2 10-2 15 2v21c-5-4-10-4-15-2zM46 37c-5-2-10-2-16 2v21c6-4 11-4 16-2z"
      />

      {/* planeta com anel */}
      <g transform="rotate(-22 90 46)">
        <ellipse className="simbolo-anel-fundo" cx="90" cy="46" rx="19.5" ry="6.5" />
      </g>
      <circle className="simbolo-preenchido" cx="90" cy="46" r="12" />
      <g transform="rotate(-22 90 46)">
        {/* a frente do anel passa por cima do planeta: um traço largo da cor
            da peça embaixo dela separa os dois brancos */}
        <path className="simbolo-anel-separador" d="M70.5 46a19.5 6.5 0 0 1 39 0" />
        <path className="simbolo-anel-frente" d="M70.5 46a19.5 6.5 0 0 1 39 0" />
      </g>
      {/* estrela de quatro pontas */}
      <path className="simbolo-preenchido" d="M107 24l1.6 4.4 4.4 1.6-4.4 1.6-1.6 4.4-1.6-4.4-4.4-1.6 4.4-1.6z" />
    </svg>
  );
}
