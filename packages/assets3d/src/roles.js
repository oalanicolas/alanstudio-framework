// Papel de cada textura: decide como codificar e com que régua medir.
// O padrão vem do sufixo do nome; um projeto passa as próprias regras quando o nome não basta.

export const ROLES = {
  color: { label: "cor", space: "srgb", yuv: "444" },
  emissive: { label: "luz própria", space: "srgb", yuv: "444" },
  normal: { label: "relevo (normal map)", space: "linear", yuv: "444" },
  material: { label: "material (metal, rugosidade, oclusão)", space: "linear", yuv: "444" },
  mask: { label: "máscara de 1 canal", space: "linear", yuv: "400" },
};

// Ordem importa: o primeiro padrão que casar decide.
export const DEFAULT_RULES = [
  { role: "normal", pattern: "(_n|_nm|_nrm|_normal|_norm|_normalmap|_n_directx|_ddn)$" },
  { role: "material", pattern: "(_mra|_orm|_arm|_mrh|_mrs|_rma|_mr|_rm|_mrao|_mro|_metallicroughness|_occlusionroughnessmetallic)$" },
  { role: "emissive", pattern: "(_e|_em|_emissive|_emis|_glow)$" },
  { role: "mask", pattern: "(_m|_mask|_msk|_mk|_o|_opacity|_alpha|_r|_rough|_roughness|_ao|_occlusion|_h|_height|_gloss)$" },
  { role: "color", pattern: "(_bc|_d|_diff|_diffuse|_basecolor|_albedo|_color|_col|_c|_df|_a)$" },
];

const compilar = (rules) => rules.map((r) => ({ ...r, re: new RegExp(r.pattern, "i") }));
const PADRAO = compilar(DEFAULT_RULES);

/**
 * Papel pelo nome do arquivo (sem extensão). Regras próprias do projeto vêm antes das padrão.
 * Sem casamento, a textura é tratada como cor: a régua de cor é a mais exigente para o que se vê.
 */
export function roleFor(name, projectRules = []) {
  const base = name.replace(/^.*[\\/]/, "").replace(/\.[^.]+$/, "");
  for (const r of [...compilar(projectRules), ...PADRAO]) if (r.re.test(base)) return { role: r.role, matched: r.pattern, guessed: false };
  return { role: "color", matched: null, guessed: true };
}

/** Canal que um mapa de 1 canal guarda (G por padrão: é o que o alphaMap/roughnessMap do three.js leem). */
export const MASK_CHANNEL = 1;
