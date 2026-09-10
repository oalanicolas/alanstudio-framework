// Região viva. A legenda e o perigo à frente já existem no mixer
// e no telegraph. A pausa só entra quando o overlay diz Pausado
// — no fim a cortina do over vence; na porta a placa nem nasce.
// O fim, a porta e a pausa no campo já nomeiam placar e recorde
// no canvas. No fim o overlay também nomeia a corrente que caiu.
// Na porta e no fim o canvas já nomeia sessão volátil; a região
// viva espelha essa linha. Preferências ilegíveis avisam no
// painel; a região viva nomeia a mesma recuperação — a porta
// não. Na porta o canvas já acende o toque
// da mostra; a região viva nomeia esse contato sem fingir coleta.
// O canvas já pinta o aviso do primeiro ciclo; a região viva
// nomeia a mesma linha. Sem isto quem não vê a tela só tinha
// a tabela — e o convite some essa tabela. Jogando sem pausa
// o número não entra. Texto no DOM não é sessão de alcance.

function whole(value) {
  if (!Number.isFinite(value)) return null;
  return String(Math.trunc(value));
}

export function liveText({
  captions = [],
  phase,
  threat,
  paused,
  score,
  best,
  lastScore,
  chain,
  persist,
  settings,
  attractTouch,
  coach,
} = {}) {
  const parts = [];
  const seen = new Set();
  const add = (text) => {
    const value = typeof text === "string" ? text.trim() : "";
    if (!value || seen.has(value)) return;
    seen.add(value);
    parts.push(value);
  };
  const overlayPaused = Boolean(paused) && phase !== "over" && phase !== "title";
  if (overlayPaused) add("pausado");
  if (phase === "over") {
    add("fim da partida");
    const points = whole(score);
    if (points !== null) add(points);
    const stake = whole(chain);
    if (stake !== null && Number(chain) > 0) add(`corrente ${stake}`);
    const record = whole(best);
    if (record !== null && Number(best) > 0) add(`recorde ${record}`);
    add(persist);
    add(settings);
  } else if (phase === "title") {
    add("abertura");
    const last = whole(lastScore);
    if (last !== null) add(`última ${last}`);
    const record = whole(best);
    if (record !== null && Number(best) > 0) add(`recorde ${record}`);
    add(persist);
    add(settings);
  } else if (overlayPaused) {
    // A cortina cobre o HUD. Sem o número aqui só o canvas
    // o mostrava, e a placa o come. Jogando sem pausa o
    // placar continua só no quadro. Texto no DOM não é sessão.
    const points = whole(score);
    if (points !== null) add(points);
    const record = whole(best);
    if (record !== null && Number(best) > 0) add(`recorde ${record}`);
  }
  // O quadro já ensina. Sem isto a região viva calava o
  // primeiro ciclo e o convite some a tabela. No fim o
  // aviso não volta. Texto no DOM não é sessão.
  if (phase !== "over") add(coach);
  if (threat === "ahead") add("perigo à frente");
  // O canvas já acende. Sem isto o live só nomeava o perigo
  // que ainda não tocou. Toque no DOM não é coleta nem sessão.
  if (phase === "title") {
    if (attractTouch === "orb") add("a mostra toca");
    else if (attractTouch === "shard") add("a mostra raspa");
  }
  const latest = captions.length ? captions[captions.length - 1] : null;
  if (latest) add(latest.text);
  return parts.join(". ");
}

export function applyLive({ node, text } = {}) {
  if (!node) return false;
  const next = String(text ?? "");
  if (node.textContent === next) return false;
  node.textContent = next;
  return true;
}
