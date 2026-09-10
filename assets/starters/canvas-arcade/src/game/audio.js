// Mixagem: barramentos, prioridade, ducking e legenda.
//
// Os papéis do verbo, do orbe perdido, do fecho, da prática, da guarda e a cama têm design original em `public/sfx/<papel>.wav`
// e variante `public/sfx/<papel>-b.wav`: seno e ruído filtrado,
// gerados por tools/design-sfx.py. O mixer alterna as variantes do verbo.
// A cama (`bed`) ocupa o barramento de música em loop; não é informação
// de jogo e não ganha legenda. No fecho o mixer desloca o tom da cama
// (`bedRate`); número no disco não é mix ouvido.
// 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão — esses
// arquivos não usam nenhum dos quatro. Coleta e guarda sobem de tom
// com a corrente; o erro não herda o tom. A legenda desses dois papéis
// nomeia a mesma aposta — sem isto o tom falava e a faixa calava.
// O erro emite `lost`. Sem isto a faixa dizia corrente perdida
// com aposta zero. Número na legenda não é mix ouvido.
// Coleta, queda, raspo, impacto,
// avanço e o término levam o x do campo; o panner marca o lugar. Arquivo no disco
// não é mixagem ouvida: `heard` no harness continua falso.
//
// O jogo carrega o arquivo no mixer. Sem esse consumidor, arquivo no
// disco e jogo mudo eram a mesma coisa. O pedido que chega antes do
// WAV fica na fila e toca quando o buffer entra — sem segunda
// legenda. Os stems sobem juntos; wav no lugar não pede ogg.
// O gesto (tecla ou toque) retoma o contexto suspenso;
// retomar, fila e paralelo não são mix ouvido.
// `missing()` ainda lista o papel se o decode falhar ou o fetch 404.
// O `over` pede fade na cama; pause, title e aba escondida
// continuam cortando a cama seco. Na pausa o mixer também
// corta as vozes do verbo que ainda soavam — overlay
// Pausado com hit no ar era a mesma partida. Número no
// disco não é mix ouvido.
//
// Toda informação sonora tem legenda equivalente: o jogo precisa ser
// completável com o áudio desligado.

import { DEFAULT_BUSES } from "../core/settings.js";
import { chainPlaybackRate, FIELD } from "./rules.js";

// O campo tem lugar. Sem isto, coleta à esquerda e à direita
// ocupam o mesmo ponto. Número no panner não é mix ouvido.
export function stereoPan(x, width = FIELD.width) {
  if (!Number.isFinite(x) || !Number.isFinite(width) || !(width > 0)) return 0;
  return Math.max(-1, Math.min(1, (x / width) * 2 - 1));
}

const CHAIN_ROLES = new Set(["collect", "bank"]);

function resolveRate(id, extra = {}) {
  if (Number.isFinite(extra.rate)) return extra.rate;
  if (CHAIN_ROLES.has(id) && Number.isFinite(extra.chain)) {
    return chainPlaybackRate(extra.chain);
  }
  return 1;
}

// O tom já nomeia a aposta. Sem isto a faixa só dizia o verbo.
// Número na legenda não é mix ouvido nem sessão de alcance.
export function captionFor(id, extra = {}) {
  const definition = SOUNDS[id];
  const base = definition?.caption;
  if (!base) return "";
  if (id === "hit") {
    const lost = Number(extra.lost);
    if (Number.isFinite(lost) && lost > 0) {
      return `${base}: corrente ${Math.trunc(lost)} perdida`;
    }
    return base;
  }
  if (CHAIN_ROLES.has(id) && Number.isFinite(extra.chain) && extra.chain > 0) {
    return `${base}, corrente ${Math.trunc(extra.chain)}`;
  }
  return base;
}

export const BUSES = ["master", "music", "sfx", "ui"];
// Folga no master: overlap de vozes não senta no teto digital.
// Não é loudness aprovado e não substitui sessão no dispositivo.
export const MIX_HEADROOM = 0.82;
// O aviso crítico abaixa a cama, não o próprio verbo. Duck em sfx/ui
// some o hit sob o hit. Número no disco não é mix ouvido.
export const DUCK_BUSES = ["music"];
export const DUCK_LEVEL = 0.35;
// Solta a cama no over. Pause, title e aba escondida
// continuam cortando seco. Número no disco não é mix ouvido.
export const BED_FADE_MS = 280;

export const SOUNDS = {
  dash: { bus: "sfx", caption: "avanço", priority: 1 },
  land: { bus: "sfx", caption: "o avanço senta", priority: 1 },
  graze: { bus: "sfx", caption: "passou raspando", priority: 1 },
  collect: { bus: "sfx", caption: "orbe coletado", priority: 2 },
  missed: { bus: "sfx", caption: "orbe perdido", priority: 1 },
  bank: { bus: "sfx", caption: "corrente guardada", priority: 3, duckMs: 180 },
  hit: { bus: "sfx", caption: "atingido", priority: 4, duckMs: 260 },
  over: { bus: "ui", caption: "fim da partida", priority: 5, duckMs: 400 },
  close: { bus: "ui", caption: "últimos segundos", priority: 2 },
  live: { bus: "ui", caption: "a chuva começa", priority: 2 },
  stir: { bus: "ui", caption: "a chuva volta", priority: 2 },
  bed: { bus: "music", caption: null, priority: 0, loop: true },
};

export function createAudio(options = {}) {
  const maxVoices = options.maxVoices ?? 6;
  const captionLimit = options.captionLimit ?? 8;
  const now = options.now ?? (() => Date.now());
  const createContext = options.createContext ?? defaultContext;

  let settings = options.settings ?? { buses: { ...DEFAULT_BUSES }, captions: true };
  let context = null;
  let gains = null;
  const buffers = new Map();
  const cursors = new Map();
  const missing = new Set();
  const pending = new Map();
  const voices = [];
  const loops = new Map();
  const captions = [];
  let duckUntil = 0;
  let disposed = false;
  let hushed = false;

  function ensureContext() {
    if (disposed) return context;
    if (context) return context;
    context = createContext();
    if (!context) return null;
    gains = {};
    gains.master = context.createGain();
    const limiter =
      typeof context.createDynamicsCompressor === "function" ? context.createDynamicsCompressor() : null;
    if (limiter) {
      limiter.threshold.value = -6;
      limiter.knee.value = 8;
      limiter.ratio.value = 8;
      limiter.attack.value = 0.003;
      limiter.release.value = 0.12;
      gains.master.connect(limiter);
      limiter.connect(context.destination);
    } else {
      gains.master.connect(context.destination);
    }
    for (const bus of BUSES.slice(1)) {
      gains[bus] = context.createGain();
      gains[bus].connect(gains.master);
    }
    applyBusLevels();
    return context;
  }

  // Chrome e Safari nascem suspensos. `decode` no boot cria o
  // contexto fora do gesto; o avanço da porta já é o gesto — se
  // o resume ficar para o quadro, o primeiro verbo continua mudo.
  // Pedir resume não é mix ouvido.
  function unlock() {
    if (disposed) return false;
    const ctx = ensureContext();
    if (!ctx) return false;
    if (ctx.state === "suspended" && typeof ctx.resume === "function") {
      try {
        const pending = ctx.resume();
        if (pending && typeof pending.catch === "function") pending.catch(() => {});
      } catch {
        return false;
      }
    }
    return true;
  }

  function applyBusLevels() {
    if (!gains) return;
    const levels = settings.buses ?? {};
    const ducking = now() < duckUntil;
    for (const bus of BUSES) {
      const level = Number.isFinite(levels[bus]) ? levels[bus] : 1;
      const duck = ducking && DUCK_BUSES.includes(bus) ? DUCK_LEVEL : 1;
      gains[bus].gain.value = bus === "master" ? level * MIX_HEADROOM : level * duck;
    }
  }

  function retire() {
    const time = now();
    for (let index = voices.length - 1; index >= 0; index -= 1) {
      if (voices[index].until <= time) voices.splice(index, 1);
    }
  }

  function cutVoices() {
    for (const voice of voices) voice.stop();
    voices.length = 0;
  }

  function emitVoice(id, extra = {}) {
    const definition = SOUNDS[id];
    if (!definition || disposed) return false;
    if (hushed && !definition.loop) return false;
    const pack = buffers.get(id) ?? [];
    if (!pack.length) return false;
    unlock();
    if (!context) return false;
    applyBusLevels();
    if (definition.loop) return startLoop(id, definition, pack[0]);
    const cursor = cursors.get(id) ?? 0;
    const buffer = pack[cursor % pack.length];
    cursors.set(id, cursor + 1);
    retire();
    if (voices.length >= maxVoices) {
      // Sob pressão, o som menos importante é o que desaparece — não o aviso.
      const weakest = voices.reduce((low, voice) => (voice.priority < low.priority ? voice : low), voices[0]);
      if (weakest.priority >= definition.priority) return false;
      weakest.stop();
      voices.splice(voices.indexOf(weakest), 1);
    }
    const source = context.createBufferSource();
    source.buffer = buffer;
    const rate = resolveRate(id, extra);
    if (source.playbackRate) source.playbackRate.value = rate;
    const bus = gains[definition.bus] ?? gains.master;
    const placed = Number.isFinite(extra.pan) || Number.isFinite(extra.x);
    if (placed && typeof context.createStereoPanner === "function") {
      const panner = context.createStereoPanner();
      panner.pan.value = Number.isFinite(extra.pan) ? Math.max(-1, Math.min(1, extra.pan)) : stereoPan(extra.x);
      source.connect(panner);
      panner.connect(bus);
    } else {
      source.connect(bus);
    }
    source.start();
    const voice = {
      priority: definition.priority,
      until: now() + Math.ceil((buffer.duration ?? 0.2) * 1000),
      stop: () => {
        try {
          source.stop();
        } catch {
          /* já terminou */
        }
      },
    };
    voices.push(voice);
    return true;
  }

  return {
    get available() {
      return Boolean(context);
    },
    unlock,
    register(id, buffer) {
      if (!(id in SOUNDS) || disposed) return false;
      const pack = buffers.get(id) ?? [];
      pack.push(buffer);
      buffers.set(id, pack);
      missing.delete(id);
      const waiting = pending.get(id);
      if (waiting !== undefined) {
        pending.delete(id);
        emitVoice(id, waiting);
      }
      return true;
    },
    async decode(bytes) {
      const ctx = ensureContext();
      if (!ctx || typeof ctx.decodeAudioData !== "function") return null;
      const copy = bytes instanceof ArrayBuffer ? bytes.slice(0) : bytes;
      return ctx.decodeAudioData(copy);
    },
    hush() {
      if (disposed) return false;
      hushed = true;
      cutVoices();
      return true;
    },
    lift() {
      if (disposed) return false;
      hushed = false;
      return true;
    },
    play(id, extra = {}) {
      const definition = SOUNDS[id];
      if (!definition || disposed) return false;
      if (hushed && !definition.loop) return false;
      const text = captionFor(id, extra);
      if (text && settings.captions !== false) {
        captions.push({ id, text, at: now() });
        while (captions.length > captionLimit) captions.shift();
      }
      if (definition.duckMs) duckUntil = now() + definition.duckMs;
      const pack = buffers.get(id) ?? [];
      if (!pack.length) {
        missing.add(id);
        pending.set(id, extra);
        unlock();
        return false;
      }
      return emitVoice(id, extra);
    },
    stop(id, extra = {}) {
      const voice = loops.get(id);
      if (!voice) return false;
      const fadeMs = Number(extra.fadeMs);
      if (Number.isFinite(fadeMs) && fadeMs > 0 && voice.gain) {
        voice.fade = {
          from: voice.gain.gain.value,
          to: 0,
          start: now(),
          ms: fadeMs,
        };
        return true;
      }
      voice.stop();
      loops.delete(id);
      return true;
    },
    // Chamado a cada quadro: o ducking precisa voltar sozinho.
    // `bedRate` desloca a cama no fecho; o fade da cama anda
    // no mesmo tick. Número no disco não é mix ouvido.
    update(extra = {}) {
      applyBusLevels();
      tickFades();
      const rate = Number(extra.bedRate);
      if (Number.isFinite(rate) && rate > 0) applyLoopRate("bed", rate);
    },
    applySettings(next) {
      settings = next;
      applyBusLevels();
    },
    // Rajada de eventos iguais — três orbes em meio segundo — é uma linha com
    // contagem, não três linhas idênticas. Sem juntar, a repetição toma a faixa
    // inteira e empurra para fora a legenda que mudaria a decisão do jogador.
    captions(maxAgeMs = 2600) {
      const time = now();
      const merged = [];
      for (const entry of captions) {
        if (time - entry.at >= maxAgeMs) continue;
        const last = merged[merged.length - 1];
        if (last && last.id === entry.id) {
          last.count += 1;
          last.at = entry.at;
          last.text = entry.text;
          continue;
        }
        merged.push({ ...entry, count: 1 });
      }
      return merged;
    },
    // Lacuna observável: quais papéis sonoros o jogo pede e ainda não tem.
    missing() {
      return { declared: Object.keys(SOUNDS), registered: [...buffers.keys()], requested: [...missing] };
    },
    dispose() {
      disposed = true;
      pending.clear();
      for (const voice of voices) voice.stop();
      voices.length = 0;
      for (const voice of loops.values()) voice.stop();
      loops.clear();
      captions.length = 0;
      if (context && typeof context.close === "function") context.close();
      context = null;
      gains = null;
    },
  };

  function startLoop(id, definition, buffer) {
    const leftover = loops.get(id);
    if (leftover) {
      if (!leftover.fade) return true;
      leftover.stop();
      loops.delete(id);
    }
    const source = context.createBufferSource();
    source.buffer = buffer;
    source.loop = true;
    const gain = context.createGain();
    gain.gain.value = 1;
    source.connect(gain);
    gain.connect(gains[definition.bus] ?? gains.master);
    source.start();
    loops.set(id, {
      source,
      gain,
      stop: () => {
        try {
          source.stop();
        } catch {
          /* já parou */
        }
      },
    });
    return true;
  }

  function tickFades() {
    const time = now();
    for (const [id, voice] of [...loops]) {
      if (!voice.fade || !voice.gain) continue;
      const span = voice.fade.ms;
      const t = span > 0 ? Math.min(1, (time - voice.fade.start) / span) : 1;
      voice.gain.gain.value = voice.fade.from + (voice.fade.to - voice.fade.from) * t;
      if (t >= 1) {
        voice.stop();
        loops.delete(id);
      }
    }
  }

  function applyLoopRate(id, rate) {
    const voice = loops.get(id);
    if (!voice?.source?.playbackRate) return false;
    voice.source.playbackRate.value = rate;
    return true;
  }
}

function defaultContext() {
  const Constructor =
    typeof AudioContext !== "undefined"
      ? AudioContext
      : typeof webkitAudioContext !== "undefined"
        ? webkitAudioContext
        : null;
  if (!Constructor) return null;
  try {
    return new Constructor();
  } catch {
    return null;
  }
}
