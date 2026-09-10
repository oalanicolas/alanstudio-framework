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
// nomeia a mesma linha. Na pausa o canvas já nomeia continuar
// e reiniciar; a região viva espelha essas linhas. Sem isto
// quem não vê a tela só ouvia pausado. Na porta o canvas já
// nomeia jogar, repetir e seed nova; a região viva espelha
// essas linhas. Sem isto quem não vê a tela só ouvia abertura.
// A porta já chove a mesa e veste o look; o fim já
// gravou os mesmos eixos no last-run. A região viva
// nomeia esses eixos quando não são o padrão. Spawn e
// normal somem. Contrast não é look de arte. Texto no
// DOM não é direção observada.
// Jogando sem pausa o número não entra. O painel já nomeia
// o som que o fetch perdeu; a região viva espelha essa
// lacuna na porta e no fim. Catálogo completo não entra.
// Texto no DOM não é sessão de alcance nem mix ouvido.

function whole(value) {
  if (!Number.isFinite(value)) return null;
  return String(Math.trunc(value));
}

function namedAxis(kind, value, silent) {
  const name = typeof value === "string" ? value.trim() : "";
  if (!name || silent.includes(name)) return "";
  return `${kind} ${name}`;
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
  audio,
  attractTouch,
  spawn,
  look,
  coach,
  resume,
  restart,
  titlePlay,
  titleAgain,
  titleNew,
  overDoor,
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
    // O last-run já gravou a mesa e o look. Sem isto
    // o leitor só ouvia o placar e a chuva dusk
    // vestia o mesmo nome que calm. Texto no DOM
    // não é direção observada.
    add(namedAxis("chuva", spawn, ["spawn"]));
    add(namedAxis("look", look, ["normal", "contrast"]));
    add(persist);
    add(settings);
    add(audio);
    add(overDoor);
  } else if (phase === "title") {
    add("abertura");
    const last = whole(lastScore);
    if (last !== null) add(`última ${last}`);
    const record = whole(best);
    if (record !== null && Number(best) > 0) add(`recorde ${record}`);
    // A porta já chove a mesa e veste o look. Sem isto
    // o leitor só ouvia abertura e a chuva dusk
    // vestia o mesmo nome que calm. Texto no DOM
    // não é direção observada.
    add(namedAxis("chuva", spawn, ["spawn"]));
    add(namedAxis("look", look, ["normal", "contrast"]));
    add(persist);
    add(settings);
    add(audio);
    // O canvas já nomeia jogar, repetir e seed nova.
    // Sem isto o leitor só ouvia abertura. Texto no
    // DOM não é sessão.
    add(titlePlay);
    add(titleAgain);
    add(titleNew);
  } else if (overlayPaused) {
    // A cortina cobre o HUD. Sem o número aqui só o canvas
    // o mostrava, e a placa o come. Jogando sem pausa o
    // placar continua só no quadro. O canvas já nomeia
    // continuar e reiniciar; sem isto o leitor só ouvia
    // pausado. Texto no DOM não é sessão.
    add(resume);
    add(restart);
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
