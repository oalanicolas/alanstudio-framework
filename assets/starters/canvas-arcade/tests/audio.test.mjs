// O que precisa estar provado é a mixagem: que a ausência ainda é
// declarada quando o buffer falta, que a legenda cobre a informação
// sonora e que, sob pressão, o som que desaparece é o menos
// importante — não o aviso. Arquivo no disco não entra neste arquivo.

import { test } from "node:test";
import assert from "node:assert/strict";

import { MIX_HEADROOM, SOUNDS, createAudio, stereoPan } from "../src/game/audio.js";
import { FIELD } from "../src/game/rules.js";

function fakeContext() {
  const gains = [];
  const sources = [];
  const context = {
    closed: false,
    gains,
    sources,
    panners: [],
    destination: {},
    createGain() {
      const node = { gain: { value: 1 }, connect() {} };
      gains.push(node);
      return node;
    },
    createDynamicsCompressor() {
      return {
        threshold: { value: 0 },
        knee: { value: 0 },
        ratio: { value: 0 },
        attack: { value: 0 },
        release: { value: 0 },
        connect() {},
      };
    },
    createStereoPanner() {
      const node = { pan: { value: 0 }, connect() {} };
      context.panners.push(node);
      return node;
    },
    createBufferSource() {
      const node = {
        buffer: null,
        started: false,
        stopped: false,
        playbackRate: { value: 1 },
        connect() {},
        loop: false,
        start() {
          node.started = true;
        },
        stop() {
          node.stopped = true;
        },
      };
      sources.push(node);
      return node;
    },
    close() {
      context.closed = true;
    },
  };
  return context;
}

function build(overrides = {}) {
  let clock = 0;
  const context = fakeContext();
  const audio = createAudio({
    now: () => clock,
    createContext: () => context,
    settings: { buses: { master: 0.8, music: 0.6, sfx: 0.9, ui: 0.7 }, captions: true },
    ...overrides,
  });
  return { audio, context, tick: (ms) => (clock += ms), at: () => clock };
}

test("a ausência de som é uma lacuna declarada, não silêncio", () => {
  const { audio } = build();
  assert.deepEqual(audio.missing().declared, Object.keys(SOUNDS));
  assert.deepEqual(audio.missing().registered, []);
  assert.equal(audio.play("collect"), false);
  assert.deepEqual(audio.missing().requested, ["collect"]);
});

test("a legenda sai mesmo sem arquivo de som", () => {
  const { audio } = build();
  audio.play("hit");
  const captions = audio.captions();
  assert.equal(captions.length, 1);
  assert.equal(captions[0].text, SOUNDS.hit.caption);
});

test("o fecho legendas sem fingir que o mix foi ouvido", () => {
  const { audio } = build();
  audio.play("close");
  assert.equal(audio.captions()[0].text, "últimos segundos");
  assert.equal(SOUNDS.close.bus, "ui");
  assert.equal(SOUNDS.close.priority < SOUNDS.over.priority, true);
});

test("a prática legendas sem fingir que o mix foi ouvido", () => {
  const { audio } = build();
  audio.play("live");
  assert.equal(audio.captions()[0].text, "a chuva começa");
  assert.equal(SOUNDS.live.bus, "ui");
  assert.equal(SOUNDS.live.loop, undefined);
  assert.equal("duckMs" in SOUNDS.live, false);
});

test("a guarda legendas sem fingir que o mix foi ouvido", () => {
  const { audio } = build();
  audio.play("stir");
  assert.equal(audio.captions()[0].text, "a chuva volta");
  assert.equal(SOUNDS.stir.bus, "ui");
  assert.equal(SOUNDS.stir.loop, undefined);
  assert.equal("duckMs" in SOUNDS.stir, false);
});

test("legenda desligada não produz legenda", () => {
  const { audio } = build({ settings: { buses: { master: 1 }, captions: false } });
  audio.play("hit");
  assert.deepEqual(audio.captions(), []);
});

// Uma rajada de eventos iguais gerava uma linha por evento; três "orbe
// coletado" tomavam a faixa inteira e empurravam para fora a legenda do dano,
// que é justamente a que muda a decisão do jogador.
test("evento repetido em sequência vira uma linha com contagem", () => {
  const { audio, tick } = build();
  audio.play("collect");
  tick(60);
  audio.play("collect");
  tick(60);
  audio.play("collect");
  const juntas = audio.captions();
  assert.equal(juntas.length, 1);
  assert.equal(juntas[0].count, 3);
  assert.equal(juntas[0].text, SOUNDS.collect.caption);
});

test("evento diferente no meio da rajada não é absorvido pela contagem", () => {
  const { audio, tick } = build();
  audio.play("collect");
  tick(30);
  audio.play("hit");
  tick(30);
  audio.play("collect");
  assert.deepEqual(
    audio.captions().map((entry) => [entry.id, entry.count]),
    [["collect", 1], ["hit", 1], ["collect", 1]],
  );
});

test("a contagem só soma o que ainda está na janela de leitura", () => {
  const { audio, tick } = build();
  audio.play("collect");
  tick(2700);
  audio.play("collect");
  const juntas = audio.captions();
  assert.equal(juntas.length, 1, "a primeira linha já tinha expirado");
  assert.equal(juntas[0].count, 1);
});

test("a legenda expira em vez de acumular na tela", () => {
  const { audio, tick } = build();
  audio.play("collect");
  assert.equal(audio.captions().length, 1);
  tick(5000);
  assert.deepEqual(audio.captions(), []);
});

test("o orbe perdido legendas sem fingir que o mix foi ouvido", () => {
  const { audio } = build();
  audio.play("missed");
  assert.equal(audio.captions()[0].text, "orbe perdido");
  assert.equal(SOUNDS.missed.bus, "sfx");
  assert.equal(SOUNDS.missed.loop, undefined);
  assert.equal("duckMs" in SOUNDS.missed, false);
});

test("som desconhecido é ignorado sem quebrar o quadro", () => {
  const { audio } = build();
  assert.equal(audio.play("unknown"), false);
  assert.deepEqual(audio.captions(), []);
});

test("duas variantes do mesmo papel alternam em vez de repetir", () => {
  const { audio, context } = build();
  audio.register("collect", { duration: 0.1, mark: "a" });
  audio.register("collect", { duration: 0.1, mark: "b" });
  assert.equal(audio.play("collect"), true);
  assert.equal(audio.play("collect"), true);
  assert.equal(context.sources[0].buffer.mark, "a");
  assert.equal(context.sources[1].buffer.mark, "b");
  assert.deepEqual(audio.missing().registered, ["collect"]);
});

test("coleta e guarda sobem de tom com a corrente; o erro não", () => {
  const { audio, context } = build();
  audio.register("collect", { duration: 0.1 });
  audio.register("bank", { duration: 0.1 });
  audio.register("hit", { duration: 0.1 });
  audio.register("dash", { duration: 0.1 });
  audio.play("collect", { chain: 1 });
  audio.play("collect", { chain: 5 });
  audio.play("bank", { chain: 5 });
  audio.play("hit", { chain: 5 });
  audio.play("dash", { chain: 5 });
  const [first, second, bank, hit, dash] = context.sources;
  assert.ok(first.playbackRate.value > 1);
  assert.ok(second.playbackRate.value > first.playbackRate.value, "elo maior precisa subir o tom");
  assert.equal(bank.playbackRate.value, second.playbackRate.value);
  assert.equal(hit.playbackRate.value, 1, "o erro não herda o tom da aposta");
  assert.equal(dash.playbackRate.value, 1);
  audio.play("collect");
  assert.equal(context.sources.at(-1).playbackRate.value, 1, "sem corrente o tom não inventa aposta");
});

test("registrar um som o remove da lacuna e o toca", () => {
  const { audio, context } = build();
  assert.equal(audio.register("collect", { duration: 0.2 }), true);
  assert.equal(audio.play("collect"), true);
  assert.deepEqual(audio.missing().registered, ["collect"]);
  assert.equal(context.sources.length, 1);
  assert.equal(context.sources[0].started, true);
  assert.equal(audio.available, true);
});

test("registrar um papel inexistente é recusado", () => {
  const { audio } = build();
  assert.equal(audio.register("trilha-inventada", {}), false);
});

test("sob pressão, o aviso importante corta o som menor", () => {
  const { audio, context } = build({ maxVoices: 2 });
  for (const id of ["dash", "graze", "hit"]) audio.register(id, { duration: 1 });
  assert.equal(audio.play("dash"), true);
  assert.equal(audio.play("graze"), true);
  assert.equal(audio.play("hit"), true, "o aviso entra");
  assert.equal(context.sources[0].stopped, true, "o som de menor prioridade sai");
  assert.equal(audio.play("graze"), false, "um som menor não derruba o aviso");
  assert.equal(context.sources.length, 3);
});

test("o evento crítico abaixa os outros barramentos e o ducking volta sozinho", () => {
  const { audio, context, tick } = build();
  audio.register("hit", { duration: 0.3 });
  audio.play("hit");
  const [master, music, sfx] = context.gains;
  assert.equal(master.gain.value, 0.8 * MIX_HEADROOM, "o volume geral não é alterado pelo ducking");
  assert.ok(sfx.gain.value < 0.9);
  assert.ok(music.gain.value < 0.6);
  tick(SOUNDS.hit.duckMs + 1);
  audio.update();
  assert.equal(master.gain.value, 0.8 * MIX_HEADROOM);
  assert.equal(sfx.gain.value, 0.9);
  assert.equal(music.gain.value, 0.6);
});

test("alterar preferências reflete nos barramentos", () => {
  const { audio, context } = build();
  audio.register("dash", { duration: 0.2 });
  audio.play("dash");
  audio.applySettings({ buses: { master: 0.2, music: 0, sfx: 0.5, ui: 0.1 }, captions: true });
  assert.equal(context.gains[0].gain.value, 0.2 * MIX_HEADROOM);
  assert.equal(context.gains[2].gain.value, 0.5);
});

test("a cama entra em loop no barramento de música sem legenda e sem roubar voz", () => {
  const { audio, context } = build({ maxVoices: 1 });
  audio.register("bed", { duration: 4 });
  audio.register("hit", { duration: 1 });
  assert.equal(audio.play("bed"), true);
  assert.equal(context.sources[0].loop, true);
  assert.equal(audio.play("bed"), true, "segunda chamada não abre outra voz");
  assert.equal(context.sources.length, 1);
  assert.equal(audio.play("hit"), true);
  assert.equal(context.sources[0].stopped, false, "a cama não entra no poço de vozes");
  assert.equal(audio.captions().some((item) => item.id === "bed"), false);
  assert.equal(audio.stop("bed"), true);
  assert.equal(context.sources[0].stopped, true);
});

test("o campo tem lugar: esquerda e direita não ocupam o mesmo ponto", () => {
  assert.equal(stereoPan(0), -1);
  assert.equal(stereoPan(FIELD.width), 1);
  assert.equal(stereoPan(FIELD.width / 2), 0);
  assert.equal(stereoPan(Number.NaN), 0);
  const { audio, context } = build();
  audio.register("collect", { duration: 0.2 });
  audio.register("missed", { duration: 0.2 });
  audio.register("close", { duration: 0.2 });
  assert.equal(audio.play("collect", { x: 0 }), true);
  assert.equal(context.panners.length, 1);
  assert.equal(context.panners[0].pan.value, -1);
  assert.equal(audio.play("missed", { x: FIELD.width }), true);
  assert.equal(context.panners[1].pan.value, 1);
  assert.equal(audio.play("close"), true);
  assert.equal(context.panners.length, 2, "fecho, prática e cama ficam no centro");
  const lines = audio.captions().map((item) => item.text).join(" ");
  assert.doesNotMatch(lines, /pan|LUFS|-14|aprovado|verified|heard/);
});

test("dispose encerra as vozes e o contexto", () => {
  const { audio, context } = build();
  audio.register("dash", { duration: 1 });
  audio.play("dash");
  audio.dispose();
  assert.equal(context.sources[0].stopped, true);
  assert.equal(context.closed, true);
  assert.equal(audio.play("dash"), false, "descartado, não toca mais");
});
