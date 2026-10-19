// Relatório antes × agora em HTML, gerado só dos JSON das execuções (texturas, malhas, verificação)
// e, opcionalmente, de medições do jogo rodando. Nenhum número é escrito à mão.

const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const num = (v) => typeof v === "number" && Number.isFinite(v);
const fmt = (v, d = 1) => (num(v) ? v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d }) : "n/d");
const int = (v) => (num(v) ? Math.round(v).toLocaleString("pt-BR") : "n/d");
const tam = (bytes) => (!num(bytes) ? "n/d" : bytes >= 1e9 ? `${fmt(bytes / 1e9, 2)} GB` : bytes >= 1e6 ? `${fmt(bytes / 1e6, 1)} MB` : `${fmt(bytes / 1e3, 0)} KB`);
const pct = (a, b) => (num(a) && num(b) && a > 0 ? `${b > a ? "+" : "−"}${fmt(Math.abs(((b - a) / a) * 100), 1)}%` : "n/d");
const mediana = (xs) => {
  const v = xs.filter(num).sort((a, b) => a - b);
  return v.length ? (v.length % 2 ? v[(v.length - 1) / 2] : (v[v.length / 2 - 1] + v[v.length / 2]) / 2) : null;
};
const erroPixel = (db) => 255 / 10 ** (db / 20);

const plural = (n, um, varios) => `${int(n)} ${n === 1 ? um : varios}`;

const PAPEL = { color: "Cor", emissive: "Luz própria", normal: "Relevo (normal map)", material: "Material", mask: "Máscara" };

const td = (rotulo, html, cls = "") => `<td class="${cls}" data-label="${esc(rotulo)}">${html}</td>`;

function secaoTexturas(t) {
  const rs = t.resultados;
  const antes = rs.reduce((s, r) => s + (r.pngBytes ?? 0), 0);
  const depois = rs.reduce((s, r) => s + (r.decision === "avif" ? r.avifBytes : r.pngBytes ?? 0), 0);
  const papeis = [...new Set(rs.map((r) => r.role))];
  const linhas = papeis
    .map((p) => {
      const g = rs.filter((r) => r.role === p);
      const av = g.filter((r) => r.decision === "avif");
      const a = g.reduce((s, r) => s + (r.pngBytes ?? 0), 0);
      const d = g.reduce((s, r) => s + (r.decision === "avif" ? r.avifBytes : r.pngBytes ?? 0), 0);
      const metrica =
        p === "normal"
          ? `${fmt(mediana(av.map((r) => r.metrics?.meanDeg)), 2)}° médio`
          : av.some((r) => num(r.metrics?.ssimulacra2))
            ? `SSIMULACRA 2 ${fmt(mediana(av.map((r) => r.metrics?.ssimulacra2)), 1)}`
            : `PSNR ${fmt(mediana(av.map((r) => r.metrics?.psnr)), 1)} dB`;
      return `<tr><th scope="row">${esc(PAPEL[p] ?? p)}</th>${td("Texturas", int(g.length), "n")}${td("Em AVIF", int(av.length), "n")}${td("No original", int(g.length - av.length), "n")}${td("q mediano", fmt(mediana(av.map((r) => r.q)), 0), "n")}${td("Métrica mediana", metrica, "n")}${td("Antes → agora", `${tam(a)} → <b>${tam(d)}</b>`, "n")}${td("Redução", pct(a, d), "n")}</tr>`;
    })
    .join("");
  const motivos = new Map();
  for (const r of rs.filter((x) => x.decision !== "avif")) {
    const k = String(r.reason ?? "sem motivo").replace(/\(q \d+\)/, "(q …)");
    motivos.set(k, (motivos.get(k) ?? 0) + 1);
  }
  const adivinhados = rs.filter((r) => r.guessed).length;
  return `<section aria-labelledby="t-tex"><h2 id="t-tex">Texturas</h2>
  <p class="sub">${plural(rs.length, "textura", "texturas")} · ${int(rs.filter((r) => r.decision === "avif").length)} em AVIF dentro da régua · ${plural(rs.filter((r) => r.decision !== "avif").length, "mantida", "mantidas")} no original · ${tam(antes)} → <b>${tam(depois)}</b> (${pct(antes, depois)}). Perfil da régua: <code>${esc(t.regua?.profile ?? "padrão")}</code>${t.regua?.color?.semSsimulacra2 ? " (cor medida por PSNR: faltou o ssimulacra2)" : ""}.</p>
  <div class="scroll"><table class="stack"><thead><tr><th>Papel</th><th class="n">Texturas</th><th class="n">Em AVIF</th><th class="n">No original</th><th class="n">q mediano</th><th class="n">Métrica mediana</th><th class="n">Antes → agora</th><th class="n">Redução</th></tr></thead><tbody>${linhas}</tbody></table></div>
  ${motivos.size ? `<h3>Por que algumas ficaram no original</h3><ul>${[...motivos].sort((a, b) => b[1] - a[1]).map(([m, n]) => `<li><b>${int(n)}</b> — ${esc(m)}</li>`).join("")}</ul>` : ""}
  ${adivinhados ? `<p class="aviso">${int(adivinhados)} textura(s) sem sufixo reconhecido foram tratadas como cor, a régua mais exigente. Um arquivo de regras (<code>--regras</code>) corrige o papel.</p>` : ""}
  </section>`;
}

function secaoMalhas(m) {
  const rs = m.resultados;
  const conv = rs.filter((r) => r.decision === "glb");
  const a = conv.reduce((s, r) => s + r.bytesAntes, 0);
  const d = conv.reduce((s, r) => s + r.bytesDepois, 0);
  const usos = new Map();
  for (const r of conv) for (const p of r.precisao ?? []) {
    const k = p.uso.replace(/_\d+$/, "_n");
    if (!usos.has(k)) usos.set(k, { bits: [], folga: [] });
    usos.get(k).bits.push(p.bits);
    if (num(p.erro) && num(p.limite) && p.limite > 0) usos.get(k).folga.push(p.erro / p.limite);
  }
  const linhas = [...usos]
    .map(([u, v]) => `<tr><th scope="row">${esc(u)}</th>${td("Accessors", int(v.bits.length), "n")}${td("Bits medianos", fmt(mediana(v.bits), 0), "n")}${td("Maior erro / limite", `${fmt(Math.max(0, ...v.folga) * 100, 0)}%`, "n")}</tr>`)
    .join("");
  const mantidas = rs.filter((r) => r.decision !== "glb");
  return `<section aria-labelledby="t-mal"><h2 id="t-mal">Malhas</h2>
  <p class="sub">${plural(rs.length, "malha", "malhas")} · ${int(conv.length)} em GLB com meshopt · ${plural(mantidas.length, "mantida", "mantidas")} · nas convertidas ${tam(a)} → <b>${tam(d)}</b> (${pct(a, d)}) · ${int(conv.reduce((s, r) => s + (r.triangles ?? 0), 0))} triângulos, todos conferidos depois de decodificar.</p>
  <p class="sub">Limites usados: posição ${fmt((m.opcoes?.positionError ?? 0) * 1e5, 1)}×10⁻⁵ da diagonal · UV ${fmt(m.opcoes?.uvTexels, 2)} texel numa textura de ${int(m.opcoes?.textureSize)} px · normal e tangente ${fmt(m.opcoes?.normalDegrees, 2)}°.</p>
  ${linhas ? `<div class="scroll"><table class="stack"><thead><tr><th>Atributo</th><th class="n">Accessors</th><th class="n">Bits medianos</th><th class="n">Maior erro / limite</th></tr></thead><tbody>${linhas}</tbody></table></div>` : ""}
  ${mantidas.length ? `<h3>Mantidas no original</h3><ul>${mantidas.slice(0, 30).map((r) => `<li><code>${esc(r.arquivo)}</code> — ${esc(r.reason)}</li>`).join("")}</ul>` : ""}
  </section>`;
}

function secaoVerificacao(v) {
  const t = v.texturas ?? [];
  const m = v.malhas ?? [];
  const falhas = [...t, ...m].filter((r) => !r.pass);
  return `<section aria-labelledby="t-ver"><h2 id="t-ver">Verificação N de N</h2>
  <div class="cards"><div class="card ${t.every((r) => r.pass) ? "ok" : "bad"}"><span class="k">Texturas na régua</span><b>${int(t.filter((r) => r.pass).length)} de ${int(t.length)}</b></div>
  <div class="card ${m.every((r) => r.pass) ? "ok" : "bad"}"><span class="k">Malhas iguais na geometria e dentro do erro</span><b>${int(m.filter((r) => r.pass).length)} de ${int(m.length)}</b></div></div>
  ${falhas.length ? `<ul class="falhas">${falhas.slice(0, 40).map((f) => `<li><code>${esc(f.arquivo)}</code> — ${esc((f.failed ?? []).join("; "))}</li>`).join("")}</ul>` : "<p class=\"sub\">Nenhuma falha.</p>"}
  </section>`;
}

function secaoMedicoes(md) {
  const campos = [
    ["downloadMB", "Download da partida", "MB", 1],
    ["vramMB", "Memória de vídeo", "MB", 0],
    ["heapMB", "Memória da aba", "MB", 0],
    ["cargaS", "Tempo até jogar", "s", 1],
    ["fps", "FPS", "", 1],
  ].filter(([k]) => num(md.antes?.[k]) && num(md.agora?.[k]));
  if (!campos.length) return "";
  return `<section aria-labelledby="t-jogo"><h2 id="t-jogo">No jogo</h2>
  ${md.notas ? `<p class="sub">${esc(md.notas)}</p>` : ""}
  <div class="cards">${campos.map(([k, rot, un, d]) => `<div class="card"><span class="k">${esc(rot)}</span><b>${fmt(md.antes[k], d)} → ${fmt(md.agora[k], d)}${un ? ` ${un}` : ""}</b><span class="d">${pct(md.antes[k], md.agora[k])}</span></div>`).join("")}</div></section>`;
}

const COMO_LER = `<section aria-labelledby="t-ler"><h2 id="t-ler">Como ler a régua</h2>
<div class="duas"><div>
<h3>SSIMULACRA 2 (cor)</h3>
<p class="sub">Métrica perceptual da Cloudinary, de −∞ a 100. Escala publicada pelos autores, sempre em 1:1 e distância normal:</p>
<table class="mini"><tbody>
<tr><th>100</th><td>matematicamente sem perda</td></tr>
<tr><th>90</th><td>visualmente sem perda: ninguém nota num teste de alternância</td></tr>
<tr><th>85</th><td>excelente: ninguém nota comparando no mesmo lugar</td></tr>
<tr><th>80</th><td>muito alta: ninguém nota lado a lado</td></tr>
<tr><th>70</th><td>alta: diferença pouco notada lado a lado</td></tr>
<tr><th>50</th><td>média: artefatos levemente incômodos</td></tr>
</tbody></table>
</div><div>
<h3>PSNR (dados e reserva)</h3>
<p class="sub">Erro médio por pixel em decibéis: mais alto é mais parecido; idênticas dão infinito (registrado como 120 dB). A escala é logarítmica: 6 dB a menos dobram o erro.</p>
<table class="mini"><tbody>${[50, 47, 44, 40, 35].map((d) => `<tr><th>${d} dB</th><td>erro médio de ~${fmt(erroPixel(d), 1)} em 255 (${fmt((erroPixel(d) / 255) * 100, 1)}%)</td></tr>`).join("")}</tbody></table>
<p class="sub">O <b>pior bloco</b> é o PSNR do bloco de 64 px com mais erro: a média da textura esconde perda local. Em normal maps a régua usa o <b>erro angular</b> em graus depois de renormalizar, porque o que se vê é a luz batendo no relevo.</p>
</div></div>
<p class="sub">Limites do número: a métrica é calculada na textura em tamanho cheio, antes da compressão em bloco da GPU; no jogo a textura aparece menor e iluminada. A prova final é a captura no render, antes × agora, na mesma pose.</p>
</section>`;

/** HTML completo. fontes: objetos JSON das execuções (com campo tipo); medicoes: { antes, agora, notas }. */
export function renderReport({ titulo = "Antes × agora dos ativos 3D", fontes = [], medicoes = null } = {}) {
  const por = (tipo) => fontes.filter((f) => f.tipo === tipo).at(-1);
  const t = por("texturas");
  const m = por("malhas");
  const v = por("verificacao");
  const datas = fontes.map((f) => f.data).filter(Boolean).sort();
  return `<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(titulo)}</title>
<style>
:root{--bg:#f6f7f9;--panel:#fff;--ink:#14171c;--muted:#5a6270;--rule:#dfe3e8;--ok:#0b7a4b;--bad:#b42335;--accent:#2457c5;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#0f1216;--panel:#171b21;--ink:#e9edf2;--muted:#9aa4b2;--rule:#2a313b;--ok:#3ecf8e;--bad:#ff6b7d;--accent:#7aa2ff;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;padding:24px clamp(16px,4vw,48px) 64px}
main{max-width:1180px;margin:0 auto;display:grid;gap:28px}h1{font-size:clamp(26px,3.6vw,38px);line-height:1.15;margin:0;text-wrap:balance}h2{font-size:22px;margin:0 0 10px}h3{font-size:16px;margin:18px 0 8px}
section{background:var(--panel);border:1px solid var(--rule);border-radius:14px;padding:clamp(16px,2.6vw,28px)}.sub{color:var(--muted);margin:6px 0;max-width:100ch}.aviso{color:var(--bad)}
code{font:13px ui-monospace,Menlo,monospace;background:color-mix(in srgb,var(--rule) 55%,transparent);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}.card{border:1px solid var(--rule);border-radius:12px;padding:14px 16px;display:grid;gap:4px}.card .k{color:var(--muted);font-size:13px}.card b{font-size:22px;font-variant-numeric:tabular-nums}.card .d{color:var(--muted);font:13px ui-monospace,Menlo,monospace}.card.ok b{color:var(--ok)}.card.bad b{color:var(--bad)}
.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{padding:9px 10px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}thead th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}td.n,th.n{text-align:right;white-space:nowrap}
table.mini th{white-space:nowrap;width:1%;font-variant-numeric:tabular-nums}.duas{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}.falhas li{color:var(--bad)}
@media (max-width:700px){table.stack thead{display:none}table.stack,table.stack tbody,table.stack tr{display:block}table.stack tr{padding:10px 0;border-bottom:1px solid var(--rule);display:grid;grid-template-columns:1fr 1fr;gap:6px 12px}table.stack th[scope=row]{grid-column:1/-1;border:0;padding:0}table.stack td{border:0;padding:0;text-align:left;white-space:normal}table.stack td::before{content:attr(data-label);display:block;font-size:11px;text-transform:uppercase;color:var(--muted)}}
</style></head><body><main>
<header><h1>${esc(titulo)}</h1><p class="sub">Gerado pelo pacote assets3d${datas.length ? ` · execuções de ${esc(datas[0].slice(0, 10))}${datas.length > 1 ? ` a ${esc(datas.at(-1).slice(0, 10))}` : ""}` : ""}${t?.ferramentas?.avifenc ? ` · avifenc ${esc(t.ferramentas.avifenc.replace(/^Version:\s*/i, ""))}` : ""}.</p></header>
${medicoes ? secaoMedicoes(medicoes) : ""}
${v ? secaoVerificacao(v) : ""}
${t ? secaoTexturas(t) : ""}
${m ? secaoMalhas(m) : ""}
${COMO_LER}
</main></body></html>
`;
}
