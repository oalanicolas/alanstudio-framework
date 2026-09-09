// Mixagem: barramentos, prioridade, ducking e legenda.
//
// Os papéis do verbo e a cama têm design original em `public/sfx/<papel>.wav`
// e variante `public/sfx/<papel>-b.wav`: seno e ruído filtrado,
// gerados por tools/design-sfx.py. O mixer alterna as variantes do verbo.
// A cama (`bed`) ocupa o barramento de música em loop; não é informação
// de jogo e não ganha legenda.
// 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão — esses
// arquivos não usam nenhum dos quatro. Arquivo no disco não é mixagem
// ouvida: `heard` no harness continua falso.
//
// O jogo carrega o arquivo no mixer. Sem esse consumidor, arquivo no
// disco e jogo mudo eram a mesma coisa. `missing()` ainda lista o
// papel se o decode falhar ou o fetch 404.
//
// Toda informação sonora tem legenda equivalente: o jogo precisa ser
// completável com o áudio desligado.

import { DEFAULT_BUSES } from "../core/settings.js";

export const BUSES = ["master", "music", "sfx", "ui"];
// Folga no master: overlap de vozes não senta no teto digital.
// Não é loudness aprovado e não substitui sessão no dispositivo.
export const MIX_HEADROOM = 0.82;

export const SOUNDS = {
  dash: { bus: "sfx", caption: "avanço", priority: 1 },
  graze: { bus: "sfx", caption: "passou raspando", priority: 1 },
  collect: { bus: "sfx", caption: "orbe coletado", priority: 2 },
  bank: { bus: "sfx", caption: "corrente guardada", priority: 3, duckMs: 180 },
  hit: { bus: "sfx", caption: "atingido: corrente perdida", priority: 4, duckMs: 260 },
  over: { bus: "ui", caption: "fim da partida", priority: 5, duckMs: 400 },
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
  const voices = [];
  const loops = new Map();
  const captions = [];
  let duckUntil = 0;
  let disposed = false;

  function ensureContext() {
    if (disposed || context) return context;
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

  function applyBusLevels() {
    if (!gains) return;
    const levels = settings.buses ?? {};
    const ducked = now() < duckUntil ? 0.35 : 1;
    for (const bus of BUSES) {
      const level = Number.isFinite(levels[bus]) ? levels[bus] : 1;
      gains[bus].gain.value = bus === "master" ? level * MIX_HEADROOM : level * ducked;
    }
  }

  function retire() {
    const time = now();
    for (let index = voices.length - 1; index >= 0; index -= 1) {
      if (voices[index].until <= time) voices.splice(index, 1);
    }
  }

  return {
    get available() {
      return Boolean(context);
    },
    register(id, buffer) {
      if (!(id in SOUNDS)) return false;
      const pack = buffers.get(id) ?? [];
      pack.push(buffer);
      buffers.set(id, pack);
      missing.delete(id);
      return true;
    },
    async decode(bytes) {
      const ctx = ensureContext();
      if (!ctx || typeof ctx.decodeAudioData !== "function") return null;
      const copy = bytes instanceof ArrayBuffer ? bytes.slice(0) : bytes;
      return ctx.decodeAudioData(copy);
    },
    play(id) {
      const definition = SOUNDS[id];
      if (!definition || disposed) return false;
      if (definition.caption && settings.captions !== false) {
        captions.push({ id, text: definition.caption, at: now() });
        while (captions.length > captionLimit) captions.shift();
      }
      if (definition.duckMs) duckUntil = now() + definition.duckMs;
      const pack = buffers.get(id) ?? [];
      if (!pack.length) {
        missing.add(id);
        return false;
      }
      ensureContext();
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
      source.connect(gains[definition.bus] ?? gains.master);
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
    },
    stop(id) {
      const voice = loops.get(id);
      if (!voice) return false;
      voice.stop();
      loops.delete(id);
      return true;
    },
    // Chamado a cada quadro: o ducking precisa voltar sozinho.
    update() {
      applyBusLevels();
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
    if (loops.has(id)) return true;
    const source = context.createBufferSource();
    source.buffer = buffer;
    source.loop = true;
    source.connect(gains[definition.bus] ?? gains.master);
    source.start();
    loops.set(id, {
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
