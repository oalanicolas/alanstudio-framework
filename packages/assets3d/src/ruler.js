// Régua de "sem perda visível" por papel de textura, em perfis.
//
// Cor e emissive usam SSIMULACRA 2, cuja escala publicada define 90 como "visually lossless"
// (nenhuma diferença num teste de alternância em 1:1) e 80 como nenhuma diferença lado a lado.
// Mapas de dados (normal, material, máscara) não são vistos diretamente e não têm limiar publicado:
// os limites abaixo foram calibrados para cair no mesmo patamar de qualidade do codificador que a cor
// em cada perfil, e devem ser confirmados no render do projeto (ver README).
//
// Um projeto pode endurecer ou trocar qualquer limite com um JSON próprio (--regua). Usar um perfil
// mais frouxo que o padrão é decisão de quem aprova o acabamento. null desliga o critério.

const cor = (ssimulacra2) => ({ ssimulacra2, psnr: null, worstBlock: null, alphaPsnr: 47, alphaWorstBlock: 44 });

export const PROFILES = {
  "sem-perda-visivel": {
    color: cor(90),
    emissive: cor(90),
    normal: { meanDeg: 0.5, p99Deg: 2, worstBlockMeanDeg: 1, z: "stored" },
    material: { psnr: 47, worstBlock: 44 },
    mask: { psnr: 47, worstBlock: 44 },
  },
  "lado-a-lado": {
    color: cor(80),
    emissive: cor(80),
    normal: { meanDeg: 0.8, p99Deg: 3, worstBlockMeanDeg: 1.5, z: "stored" },
    material: { psnr: 42, worstBlock: 38 },
    mask: { psnr: 42, worstBlock: 38 },
  },
};

export const DEFAULT_PROFILE = "sem-perda-visivel";
export const DEFAULT_RULER = PROFILES[DEFAULT_PROFILE];

// Sem o binário ssimulacra2, a cor passa a ser medida por PSNR, com limites calibrados para ficar
// pelo menos tão exigentes quanto o SSIMULACRA 2 do perfil.
export const COLOR_PSNR_FALLBACK = {
  "sem-perda-visivel": { psnr: 50, worstBlock: 48 },
  "lado-a-lado": { psnr: 43, worstBlock: 40 },
};

/** Régua efetiva: perfil + ajustes do projeto + troca da cor por PSNR quando falta o ssimulacra2. */
export function resolveRuler(projectRuler = {}, { hasSsimulacra2 = true, profile = DEFAULT_PROFILE } = {}) {
  if (!PROFILES[profile]) throw new Error(`perfil de régua desconhecido: ${profile} (há ${Object.keys(PROFILES).join(", ")})`);
  const r = structuredClone(PROFILES[profile]);
  if (!hasSsimulacra2) {
    for (const papel of ["color", "emissive"]) r[papel] = { ...r[papel], ssimulacra2: null, ...COLOR_PSNR_FALLBACK[profile], semSsimulacra2: true };
  }
  // o ajuste do projeto vem por último: vence o perfil e a reserva por PSNR
  for (const [papel, limites] of Object.entries(projectRuler)) {
    r[papel] = { ...(r[papel] ?? {}), ...limites };
    if (!hasSsimulacra2 && limites.ssimulacra2 != null && ["color", "emissive"].includes(papel)) r[papel].ssimulacra2 = null;
  }
  return { profile, ...r };
}
