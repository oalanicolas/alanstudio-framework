// Mixagem: barramentos, prioridade, ducking e legenda.
//
// Este starter **não embarca arquivos de som**. O piso do estúdio é gravação
// licenciada ou design contemporâneo — 8-bit, chiptune, jsfxr e Kenney arcade
// não são o padrão — então sintetizar bipes aqui seria escolher a estética
// errada por conveniência. Em vez disso os slots ficam declarados e vazios, e
// `missing()` transforma a ausência em uma lacuna observável.
//
// Para preencher, a partir da raiz do framework:
//   python3 scripts/game.py sfx search <termo> --root <laboratorio>
//   python3 scripts/game.py sfx copy <id> --to <projeto>/public/sfx --root <laboratorio>
//
// Toda informação sonora tem legenda equivalente: o jogo precisa ser
// completável com o áudio desligado.

export const BUSES = ["master", "music", "sfx", "ui"];

export const SOUNDS = {
  dash: { bus: "sfx", caption: "avanço", priority: 1 },
  graze: { bus: "sfx", caption: "passou raspando", priority: 1 },
  collect: { bus: "sfx", caption: "orbe coletado", priority: 2 },
  bank: { bus: "sfx", caption: "corrente guardada", priority: 3, duckMs: 180 },
  hit: { bus: "sfx", caption: "atingido: corrente perdida", priority: 4, duckMs: 260 },
  over: { bus: "ui", caption: "fim da partida", priority: 5, duckMs: 400 },
};

export function createAudio(options = {}) {
  const maxVoices = options.maxVoices ?? 6;
  const captionLimit = options.captionLimit ?? 8;
  const now = options.now ?? (() => Date.now());
  const createContext = options.createContext ?? defaultContext;

  let settings = options.settings ?? { buses: { master: 0.8, music: 0.6, sfx: 0.9, ui: 0.7 }, captions: true };
  let context = null;
  let gains = null;
  const buffers = new Map();
  const missing = new Set();
  const voices = [];
  const captions = [];
  let duckUntil = 0;
  let disposed = false;

  function ensureContext() {
    if (disposed || context) return context;
    context = createContext();
    if (!context) return null;
    gains = {};
    gains.master = context.createGain();
    gains.master.connect(context.destination);
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
      gains[bus].gain.value = bus === "master" ? level : level * ducked;
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
      buffers.set(id, buffer);
      missing.delete(id);
      return true;
    },
    play(id) {
      const definition = SOUNDS[id];
      if (!definition || disposed) return false;
      if (settings.captions !== false) {
        captions.push({ id, text: definition.caption, at: now() });
        while (captions.length > captionLimit) captions.shift();
      }
      if (definition.duckMs) duckUntil = now() + definition.duckMs;
      const buffer = buffers.get(id);
      if (!buffer) {
        missing.add(id);
        return false;
      }
      ensureContext();
      if (!context) return false;
      retire();
      if (voices.length >= maxVoices) {
        // Sob pressão, o som menos importante é o que desaparece — não o aviso.
        const weakest = voices.reduce((low, voice) => (voice.priority < low.priority ? voice : low), voices[0]);
        if (weakest.priority >= definition.priority) return false;
        weakest.stop();
        voices.splice(voices.indexOf(weakest), 1);
      }
      applyBusLevels();
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
      captions.length = 0;
      if (context && typeof context.close === "function") context.close();
      context = null;
      gains = null;
    },
  };
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
