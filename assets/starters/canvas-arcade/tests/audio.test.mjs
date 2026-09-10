// O que precisa estar provado é a mixagem: que a ausência ainda é
// declarada quando o buffer falta, que a legenda cobre a informação
// sonora e que, sob pressão, o som que desaparece é o menos
// importante — não o aviso. Arquivo no disco não entra neste arquivo.

import { test } from "node:test";
import assert from "node:assert/strict";

import { readFileSync } from "node:fs";

import { BED_FADE_MS, DUCK_BUSES, DUCK_LEVEL, MIX_HEADROOM, SOUNDS, audioGapLine, audioGapLive, captionFor, createAudio, stereoPan } from "../src/game/audio.js";
import { FIELD } from "../src/game/rules.js";

const main = readFileSync(new URL("../src/main.js", import.meta.url), "utf8");

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
    state: "running",
    resume() {
      context.state = "running";
      return Promise.resolve();
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

test("fail sem play entra no pedido; papel já registrado recusa", () => {
  const { audio } = build();
  assert.equal(audio.fail("hit"), true);
  assert.deepEqual(audio.missing().requested, ["hit"]);
  assert.equal(audio.fail("trilha-inventada"), false);
  audio.register("dash", { duration: 0.1 });
  assert.equal(audio.fail("dash"), false);
  assert.deepEqual(audio.missing().requested, ["hit"]);
  audio.dispose();
  assert.equal(audio.fail("bank"), false);
});

test("o painel nomeia os vazios mesmo quando outro papel já registrou", () => {
  const declared = Object.keys(SOUNDS);
  assert.equal(audioGapLine({}), "");
  assert.equal(audioGapLine({ declared: [] }), "");
  const empty = audioGapLine({ declared, registered: [] });
  assert.match(empty, /Nenhum arquivo de som embarcado/);
  assert.match(empty, /Papéis declarados e vazios: /);
  assert.match(empty, /dash/);
  assert.doesNotMatch(empty, /Ainda vazios/);
  const mixed = audioGapLine({ declared, registered: ["dash"] });
  assert.match(mixed, /Sons registrados: dash\./);
  assert.match(mixed, /Ainda vazios: /);
  assert.match(mixed, /hit/);
  assert.doesNotMatch(mixed, /Nenhum arquivo de som embarcado/);
  const full = audioGapLine({ declared: ["dash"], registered: ["dash"] });
  assert.equal(full, "Sons registrados: dash.");
  assert.doesNotMatch(full, /Ainda vazios/);
});

test("a região viva só nomeia a lacuna do som, não o catálogo", () => {
  const declared = Object.keys(SOUNDS);
  assert.equal(audioGapLive({}), "");
  assert.equal(audioGapLive({ declared: [], registered: [] }), "");
  assert.equal(audioGapLive({ declared: ["dash"], registered: ["dash"] }), "");
  const empty = audioGapLive({ declared, registered: [] });
  assert.match(empty, /Nenhum arquivo de som embarcado/);
  assert.equal(empty, audioGapLine({ declared, registered: [] }));
  const mixed = audioGapLive({ declared, registered: ["dash"] });
  assert.match(mixed, /Ainda vazios/);
  assert.equal(mixed, audioGapLine({ declared, registered: ["dash"] }));
  assert.doesNotMatch(
    `${empty} ${mixed}`,
    /aprovado|verified|heard|alguém de fora/,
  );
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

test("o pulso do fecho não come a legenda do verbo", () => {
  const { audio, tick, context } = build();
  audio.register("close", { duration: 0.1 });
  for (const id of ["collect", "bank", "hit", "graze", "land", "missed"]) {
    audio.play(id);
    tick(40);
  }
  for (let pulse = 0; pulse < 10; pulse += 1) {
    assert.equal(audio.play("close"), true);
    tick(40);
  }
  const lines = audio.captions();
  const ids = lines.map((entry) => entry.id);
  assert.ok(ids.includes("collect"));
  assert.ok(ids.includes("bank"));
  assert.ok(ids.includes("hit"));
  assert.equal(ids.filter((id) => id === "close").length, 1);
  assert.equal(lines.find((entry) => entry.id === "close").count, 1);
  assert.equal(lines.find((entry) => entry.id === "close").text, "últimos segundos");
  assert.equal(context.sources.length, 10, "o pulso ainda fala; só a faixa para de empilhar");
});

test("o fecho volta à faixa depois do verbo", () => {
  const { audio, tick } = build();
  audio.play("close");
  tick(40);
  audio.play("collect");
  tick(40);
  audio.play("close");
  assert.deepEqual(
    audio.captions().map((entry) => entry.id),
    ["close", "collect", "close"],
  );
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

test("o término legendas sem fingir que o mix foi ouvido", () => {
  const { audio, context } = build();
  audio.register("land", { duration: 0.1 });
  assert.equal(audio.play("land", { x: 0 }), true);
  assert.equal(context.panners[0].pan.value, -1);
  assert.equal(audio.captions()[0].text, "o avanço senta");
  assert.equal(SOUNDS.land.bus, "sfx");
  assert.equal(SOUNDS.land.priority, SOUNDS.dash.priority);
  assert.equal(SOUNDS.land.loop, undefined);
  assert.equal("duckMs" in SOUNDS.land, false);
});

test("o fim leva o x do campo sem fingir que o mix foi ouvido", () => {
  const { audio, context } = build();
  audio.register("over", { duration: 0.1 });
  assert.equal(audio.play("over", { score: 12, unbanked: 0, x: 0 }), true);
  assert.equal(context.panners[0].pan.value, -1);
  assert.equal(audio.play("over", { score: 12, unbanked: 0, x: FIELD.width }), true);
  assert.equal(context.panners[1].pan.value, 1);
  assert.equal(captionFor("over", { score: 12, x: 0 }), "fim da partida");
});

test("a guarda leva o x do campo sem fingir que o mix foi ouvido", () => {
  const { audio, context } = build();
  audio.register("bank", { duration: 0.1 });
  assert.equal(audio.play("bank", { chain: 4, x: 0 }), true);
  assert.equal(context.panners[0].pan.value, -1);
  assert.equal(audio.play("bank", { chain: 4, x: FIELD.width }), true);
  assert.equal(context.panners[1].pan.value, 1);
  assert.equal(captionFor("bank", { chain: 4, x: 0 }), "corrente guardada, corrente 4");
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

test("a legenda da coleta e da guarda nomeia a corrente que o tom já sobe", () => {
  const { audio } = build();
  audio.play("collect", { chain: 3 });
  audio.play("bank", { chain: 4 });
  audio.play("hit", { chain: 4 });
  audio.play("collect");
  const lines = audio.captions().map((entry) => entry.text);
  assert.equal(captionFor("collect", { chain: 3 }), "orbe coletado, corrente 3");
  assert.equal(captionFor("bank", { chain: 4 }), "corrente guardada, corrente 4");
  assert.equal(captionFor("collect"), SOUNDS.collect.caption);
  assert.equal(captionFor("hit", { chain: 4 }), SOUNDS.hit.caption, "o erro não herda o número da aposta");
  assert.ok(lines.includes("orbe coletado, corrente 3"));
  assert.ok(lines.includes("corrente guardada, corrente 4"));
  assert.ok(lines.includes(SOUNDS.collect.caption));
  assert.equal(lines.includes("atingido"), true);
  assert.doesNotMatch(lines.join(" "), /aprovado|verified|heard|felt/);
});

test("a legenda do erro nomeia a corrente que lost derrubou e cala quando era zero", () => {
  assert.equal(captionFor("hit"), "atingido");
  assert.equal(captionFor("hit", { lost: 0 }), "atingido");
  assert.equal(captionFor("hit", { chain: 4 }), "atingido", "o erro não herda o número da aposta");
  assert.equal(captionFor("hit", { lost: 4 }), "atingido: corrente 4 perdida");
  const { audio } = build();
  audio.play("hit", { lost: 0 });
  assert.equal(audio.captions().at(-1).text, "atingido");
  audio.play("hit", { lost: 3 });
  assert.equal(audio.captions().at(-1).text, "atingido: corrente 3 perdida");
  assert.doesNotMatch(audio.captions().map((entry) => entry.text).join(" "), /aprovado|verified|heard|felt/);
});

test("a rajada da coleta fica com a aposta vigente, não com a primeira", () => {
  const { audio } = build();
  audio.play("collect", { chain: 1 });
  audio.play("collect", { chain: 2 });
  audio.play("collect", { chain: 3 });
  const juntas = audio.captions();
  assert.equal(juntas.length, 1);
  assert.equal(juntas[0].count, 3);
  assert.equal(juntas[0].text, "orbe coletado, corrente 3");
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

test("o pedido que chega antes do arquivo toca quando o buffer entra", () => {
  const { audio, context } = build();
  assert.equal(audio.play("dash", { x: 0 }), false);
  assert.equal(audio.captions().length, 1);
  assert.equal(context.sources.length, 0);
  assert.equal(audio.register("dash", { duration: 0.2 }), true);
  assert.equal(context.sources.length, 1);
  assert.equal(context.sources[0].started, true);
  assert.equal(context.panners[0].pan.value, -1);
  assert.equal(audio.captions().length, 1, "a fila não duplica a legenda");
  assert.deepEqual(audio.missing().requested, []);
});

test("a fila guarda o último pedido do papel, não a rajada", () => {
  const { audio, context } = build();
  assert.equal(audio.play("collect", { x: 0 }), false);
  assert.equal(audio.play("collect", { x: FIELD.width }), false);
  audio.register("collect", { duration: 0.2 });
  assert.equal(context.sources.length, 1);
  assert.equal(context.panners[0].pan.value, 1);
  assert.equal(audio.captions()[0].count, 2);
});

test("a cama que pediu antes do arquivo entra em loop quando o buffer chega", () => {
  const { audio, context } = build();
  assert.equal(audio.play("bed"), false);
  assert.equal(audio.captions().some((item) => item.id === "bed"), false);
  audio.register("bed", { duration: 4 });
  assert.equal(context.sources[0].loop, true);
  assert.equal(context.sources[0].started, true);
});

test("o gesto retoma o contexto suspenso sem fingir que o mix foi ouvido", () => {
  const { audio, context } = build();
  context.state = "suspended";
  let resumed = 0;
  context.resume = () => {
    resumed += 1;
    context.state = "running";
    return Promise.resolve();
  };
  assert.equal(audio.unlock(), true);
  assert.equal(resumed, 1);
  audio.register("dash", { duration: 0.2 });
  context.state = "suspended";
  assert.equal(audio.play("dash"), true);
  assert.equal(resumed, 2);
  assert.equal(context.sources[0].started, true);
});

test("resume recusado não derruba o quadro", () => {
  const { audio, context } = build();
  audio.register("dash", { duration: 0.2 });
  context.state = "suspended";
  context.resume = () => {
    throw new Error("NotAllowedError");
  };
  assert.equal(audio.unlock(), false);
  context.resume = () => Promise.reject(new Error("NotAllowedError"));
  assert.equal(audio.play("dash"), false, "disparar no vazio não é ouvir");
  assert.equal(context.sources.length, 0, "contexto suspenso não come o verbo");
});

test("o pedido no contexto suspenso toca quando o gesto retoma", () => {
  const { audio, context } = build();
  audio.register("live", { duration: 0.2 });
  audio.register("dash", { duration: 0.2 });
  context.state = "suspended";
  context.resume = () => Promise.resolve();
  assert.equal(audio.play("live"), false, "a mostra na porta não dispara no vazio");
  assert.equal(audio.play("dash", { x: 0 }), false, "o avanço no gesto ainda suspenso espera");
  assert.equal(context.sources.length, 0);
  assert.equal(audio.captions().length, 2, "a faixa já nomeia o que vai tocar");
  context.state = "running";
  assert.equal(audio.unlock(), true);
  assert.equal(context.sources.length, 2, "live e dash esperavam o gesto");
  assert.equal(context.sources.every((node) => node.started), true);
  assert.equal(audio.captions().length, 2, "retomar não duplica a legenda");
});

test("dispose esquece a fila e recusa o registro", () => {
  const { audio, context } = build();
  audio.play("dash");
  audio.dispose();
  assert.equal(audio.register("dash", { duration: 0.2 }), false);
  assert.equal(context.sources.length, 0);
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

test("o evento crítico abaixa só a cama e o ducking volta sozinho", () => {
  assert.deepEqual(DUCK_BUSES, ["music"]);
  const { audio, context, tick } = build();
  audio.register("hit", { duration: 0.3 });
  audio.play("hit");
  const [master, music, sfx, ui] = context.gains;
  assert.equal(master.gain.value, 0.8 * MIX_HEADROOM, "o volume geral não é alterado pelo ducking");
  assert.equal(sfx.gain.value, 0.9, "o verbo não some sob o próprio aviso");
  assert.equal(ui.gain.value, 0.7, "o ui não some sob o aviso");
  assert.equal(music.gain.value, 0.6 * DUCK_LEVEL);
  tick(SOUNDS.hit.duckMs + 1);
  audio.update();
  assert.equal(master.gain.value, 0.8 * MIX_HEADROOM);
  assert.equal(sfx.gain.value, 0.9);
  assert.equal(ui.gain.value, 0.7);
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

test("parar a cama com fade desce o ganho antes de cortar", () => {
  const { audio, context, tick } = build();
  audio.register("bed", { duration: 4 });
  assert.equal(audio.play("bed"), true);
  const loopGain = context.gains.at(-1);
  assert.equal(loopGain.gain.value, 1);
  assert.equal(audio.stop("bed", { fadeMs: BED_FADE_MS }), true);
  assert.equal(context.sources[0].stopped, false, "ainda não cortou");
  audio.update();
  assert.equal(loopGain.gain.value, 1, "o primeiro quadro ainda não andou");
  tick(BED_FADE_MS / 2);
  audio.update();
  assert.ok(loopGain.gain.value > 0 && loopGain.gain.value < 1, "a cama precisa soltar");
  assert.equal(context.sources[0].stopped, false);
  tick(BED_FADE_MS / 2);
  audio.update();
  assert.equal(loopGain.gain.value, 0);
  assert.equal(context.sources[0].stopped, true);
});

test("play no meio do fade nasce de novo em vez de deixar a cama morrendo", () => {
  const { audio, context, tick } = build();
  audio.register("bed", { duration: 4 });
  assert.equal(audio.play("bed"), true);
  audio.stop("bed", { fadeMs: BED_FADE_MS });
  tick(BED_FADE_MS / 2);
  audio.update();
  assert.equal(context.sources[0].stopped, false);
  assert.ok(context.gains.at(-1).gain.value < 1);
  assert.equal(audio.play("bed"), true);
  assert.equal(context.sources[0].stopped, true, "o leftover some");
  assert.equal(context.sources.length, 2);
  assert.equal(context.sources[1].started, true);
  assert.equal(context.sources[1].stopped, false);
  assert.equal(context.gains.at(-1).gain.value, 1);
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

test("a cama sobe o tom no fecho sem fingir mix ouvido", () => {
  const { audio, context } = build();
  audio.register("bed", { duration: 4 });
  assert.equal(audio.play("bed"), true);
  assert.equal(context.sources[0].playbackRate.value, 1);
  audio.update({ bedRate: 1.08 });
  assert.equal(context.sources[0].playbackRate.value, 1.08);
  audio.update({ bedRate: 1 });
  assert.equal(context.sources[0].playbackRate.value, 1);
  audio.update();
  assert.equal(context.sources[0].playbackRate.value, 1, "sem pedido a cama não inventa tensão");
  assert.doesNotMatch(SOUNDS.bed.caption ?? "", /aprovado|verified|heard|LUFS|-14/);
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

test("a pausa corta o verbo que ainda soava sem fingir mix ouvido", () => {
  const { audio, context } = build();
  audio.register("hit", { duration: 1 });
  audio.register("bed", { duration: 4 });
  assert.equal(audio.play("bed"), true);
  assert.equal(audio.play("hit"), true);
  assert.equal(context.sources[1].stopped, false);
  assert.equal(audio.hush(), true);
  assert.equal(context.sources[1].stopped, true, "o hit não atravessa o overlay");
  assert.equal(context.sources[0].stopped, false, "a cama espera o stop seco");
  assert.equal(audio.play("hit"), false, "hushed, o verbo não nasce");
  assert.equal(audio.play("bed"), true, "a cama não entra no hush");
  audio.lift();
  assert.equal(audio.play("hit"), true);
  assert.equal(context.sources.at(-1).started, true);
  assert.match(main, /if \(state\.phase === "playing"\) audio\.hush\(\)/);
  assert.match(main, /togglePause[\s\S]*syncBed\(\)/);
  assert.doesNotMatch(main, /aprovado|verified|heard|LUFS|-14/);
});

test("no fim a pausa não come o stinger sem fingir mix ouvido", () => {
  assert.match(main, /if \(loop\.paused\) \{/);
  assert.match(main, /if \(state\.phase === "playing"\) audio\.hush\(\)/);
  assert.doesNotMatch(main, /if \(loop\.paused\) \{\s*audio\.hush/);
  assert.doesNotMatch(main, /aprovado|verified|heard|LUFS|-14/);
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
