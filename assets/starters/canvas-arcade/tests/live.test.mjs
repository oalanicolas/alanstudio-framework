import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyLive, liveText } from "../src/core/live.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");
const main = readFileSync(new URL("../src/main.js", import.meta.url), "utf8");

test("liveText junta fase, perigo e a última legenda sem repetir", () => {
  assert.equal(liveText({}), "");
  assert.equal(liveText({ phase: "title" }), "abertura");
  assert.equal(liveText({ phase: "title", threat: "ahead" }), "abertura. perigo à frente");
  assert.equal(liveText({ phase: "over" }), "fim da partida");
  assert.equal(liveText({ phase: "playing", threat: "ahead" }), "perigo à frente");
  assert.equal(
    liveText({
      phase: "over",
      captions: [{ text: "fim da partida" }],
    }),
    "fim da partida",
  );
  assert.equal(
    liveText({
      phase: "playing",
      threat: "ahead",
      captions: [{ text: "o avanço senta" }],
    }),
    "perigo à frente. o avanço senta",
  );
  assert.equal(/orbe|guarda|estilhaço/i.test(liveText({
    phase: "playing",
    threat: "ahead",
  })), false);
});

test("o placar e o recorde entram na região viva no fim e na porta sem fingir sessão", () => {
  assert.equal(liveText({ phase: "over", score: 12 }), "fim da partida. 12");
  assert.equal(
    liveText({ phase: "over", score: 12, best: 20 }),
    "fim da partida. 12. recorde 20",
  );
  assert.equal(liveText({ phase: "over", score: 0, best: 0 }), "fim da partida. 0");
  assert.equal(liveText({ phase: "title", lastScore: 8 }), "abertura. última 8");
  assert.equal(
    liveText({ phase: "title", lastScore: 8, best: 20 }),
    "abertura. última 8. recorde 20",
  );
  assert.equal(
    liveText({ phase: "playing", score: 12, best: 20, threat: "ahead" }),
    "perigo à frente",
  );
  assert.match(main, /score:\s*state\.score/);
  assert.match(main, /best:\s*progress\.best/);
  assert.match(main, /lastScore:/);
  assert.doesNotMatch(
    liveText({ phase: "over", score: 12, best: 20 }),
    /aprovado|verified|alguém de fora/,
  );
});

test("no fim a região viva nomeia a corrente que caiu sem fingir sessão", () => {
  assert.equal(
    liveText({ phase: "over", score: 12, chain: 5, best: 20 }),
    "fim da partida. 12. corrente 5. recorde 20",
  );
  assert.equal(
    liveText({ phase: "over", score: 12, chain: 0, best: 20 }),
    "fim da partida. 12. recorde 20",
  );
  assert.equal(
    liveText({ phase: "over", score: 12, chain: 5, paused: true }),
    "fim da partida. 12. corrente 5",
  );
  assert.doesNotMatch(
    liveText({ phase: "over", score: 12, chain: 5, paused: true }),
    /pausado/,
  );
  assert.equal(
    liveText({ phase: "playing", chain: 5, score: 12 }),
    "",
  );
  assert.match(main, /chain:\s*state\.chain/);
  assert.doesNotMatch(
    liveText({ phase: "over", score: 12, chain: 5 }),
    /aprovado|verified|alguém de fora|felt|heard/,
  );
});

test("a pausa entra na região viva sem fingir sessão", () => {
  assert.equal(liveText({ paused: true }), "pausado");
  assert.equal(
    liveText({ phase: "playing", threat: "ahead", paused: true }),
    "pausado. perigo à frente",
  );
  assert.equal(
    liveText({ phase: "over", paused: true }),
    "fim da partida",
  );
  assert.equal(
    liveText({ phase: "title", paused: true }),
    "abertura",
  );
  assert.equal(liveText({ phase: "playing", paused: false }), "");
  assert.match(main, /paused:\s*loop\.paused/);
  assert.doesNotMatch(liveText({ paused: true }), /aprovado|verified|alguém de fora/);
});

test("a região viva só diz pausado quando o overlay diz Pausado", () => {
  assert.equal(
    liveText({ phase: "over", paused: true, score: 12, best: 20 }),
    "fim da partida. 12. recorde 20",
  );
  assert.equal(
    liveText({ phase: "title", paused: true, lastScore: 8, best: 20 }),
    "abertura. última 8. recorde 20",
  );
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12, best: 20 }),
    "pausado. 12. recorde 20",
  );
  assert.doesNotMatch(
    liveText({ phase: "over", paused: true, score: 12 }),
    /pausado/,
  );
  assert.doesNotMatch(
    liveText({ phase: "over", paused: true, score: 12 }),
    /aprovado|verified|alguém de fora/,
  );
});

test("a pausa nomeia o placar na região viva sem fingir sessão", () => {
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12, best: 20 }),
    "pausado. 12. recorde 20",
  );
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 0, best: 0 }),
    "pausado. 0",
  );
  assert.equal(
    liveText({ phase: "playing", score: 12, best: 20 }),
    "",
  );
  assert.doesNotMatch(
    liveText({ phase: "playing", paused: true, score: 12, best: 20 }),
    /aprovado|verified|alguém de fora/,
  );
});

test("na porta e no fim a região viva nomeia o aviso da sessão sem fingir confiança", () => {
  assert.equal(
    liveText({ phase: "title", persist: "Esta sessão não grava" }),
    "abertura. Esta sessão não grava",
  );
  assert.equal(
    liveText({ phase: "over", score: 12, persist: "Esta sessão não grava" }),
    "fim da partida. 12. Esta sessão não grava",
  );
  assert.equal(
    liveText({ phase: "over", score: 12, persist: "A última gravação não ficou" }),
    "fim da partida. 12. A última gravação não ficou",
  );
  assert.equal(
    liveText({ phase: "title", persist: "" }),
    "abertura",
  );
  assert.equal(
    liveText({ phase: "playing", persist: "Esta sessão não grava" }),
    "",
  );
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12, persist: "Esta sessão não grava" }),
    "pausado. 12",
  );
  assert.match(main, /persistLine\(persist\(\),\s*copy\)/);
  assert.doesNotMatch(
    liveText({ phase: "title", persist: "Esta sessão não grava" }),
    /aprovado|verified|trusted|alguém de fora/,
  );
});

test("na porta e no fim a região viva nomeia a recuperação que o painel já mostra", () => {
  const recovered = "As preferências voltaram ao padrão; o arquivo ilegível ficou em settings.broken";
  assert.equal(
    liveText({ phase: "title", settings: recovered }),
    `abertura. ${recovered}`,
  );
  assert.equal(
    liveText({ phase: "over", score: 12, settings: recovered }),
    `fim da partida. 12. ${recovered}`,
  );
  assert.equal(
    liveText({
      phase: "title",
      persist: "Esta sessão não grava",
      settings: recovered,
    }),
    `abertura. Esta sessão não grava. ${recovered}`,
  );
  assert.equal(liveText({ phase: "title", settings: "" }), "abertura");
  assert.equal(liveText({ phase: "playing", settings: recovered }), "");
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12, settings: recovered }),
    "pausado. 12",
  );
  assert.match(main, /settingsLine\(settingsLoad,\s*copy\)/);
  assert.doesNotMatch(main, /persistLine\([^)]*settings/);
  assert.doesNotMatch(
    liveText({ phase: "title", settings: recovered }),
    /aprovado|verified|trusted|alguém de fora/,
  );
});

test("na porta a região viva nomeia o toque da mostra sem fingir coleta", () => {
  assert.equal(liveText({ phase: "title", attractTouch: "orb" }), "abertura. a mostra toca");
  assert.equal(liveText({ phase: "title", attractTouch: "shard" }), "abertura. a mostra raspa");
  assert.equal(
    liveText({ phase: "title", attractTouch: "shard", threat: "ahead" }),
    "abertura. perigo à frente. a mostra raspa",
  );
  assert.equal(liveText({ phase: "title" }), "abertura");
  assert.equal(liveText({ phase: "playing", attractTouch: "orb" }), "");
  assert.equal(liveText({ phase: "over", attractTouch: "shard" }), "fim da partida");
  assert.doesNotMatch(
    liveText({ phase: "title", attractTouch: "orb" }),
    /coletado|perdido|atingido|orbe coletado/,
  );
  assert.match(main, /attractTouch:\s*state\.attractTouch/);
  assert.doesNotMatch(
    liveText({ phase: "title", attractTouch: "shard" }),
    /aprovado|verified|alguém de fora|felt|heard/,
  );
});

test("a região viva nomeia o aviso do primeiro ciclo sem fingir sessão", () => {
  assert.equal(
    liveText({ phase: "title", coach: "←/→, arraste ou analógico" }),
    "abertura. ←/→, arraste ou analógico",
  );
  assert.equal(
    liveText({
      phase: "title",
      coach: "guardar a corrente",
      attractTouch: "orb",
      threat: "ahead",
    }),
    "abertura. guardar a corrente. perigo à frente. a mostra toca",
  );
  assert.equal(
    liveText({ phase: "playing", coach: "Passe no orbe — a corrente cresce" }),
    "Passe no orbe — a corrente cresce",
  );
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12, coach: "Guarde antes de perder a corrente" }),
    "pausado. 12. Guarde antes de perder a corrente",
  );
  assert.equal(
    liveText({ phase: "over", score: 12, coach: "Passe no orbe — a corrente cresce" }),
    "fim da partida. 12",
  );
  assert.equal(liveText({ phase: "title" }), "abertura");
  assert.match(main, /coachText/);
  assert.match(main, /bindLines/);
  assert.match(main, /coach:/);
  assert.doesNotMatch(
    liveText({ phase: "title", coach: "←/→, arraste ou analógico" }),
    /aprovado|verified|alguém de fora|felt|heard/,
  );
});

test("applyLive só escreve quando o texto muda", () => {
  const node = { textContent: "" };
  assert.equal(applyLive({}), false);
  assert.equal(applyLive({ node, text: "perigo à frente" }), true);
  assert.equal(node.textContent, "perigo à frente");
  assert.equal(applyLive({ node, text: "perigo à frente" }), false);
  assert.equal(applyLive({ node, text: "fim da partida" }), true);
  assert.equal(node.textContent, "fim da partida");
});

test("a página declara a região viva sem fingir sessão", () => {
  assert.match(html, /id="live"/);
  assert.match(html, /aria-live="polite"/);
  assert.match(html, /sr-only/);
  assert.match(main, /getElementById\("live"\)/);
  assert.match(main, /threatCue/);
  assert.match(main, /applyLive/);
  assert.doesNotMatch(html, /outsider|aprovado|verified|alguém de fora/);
});
