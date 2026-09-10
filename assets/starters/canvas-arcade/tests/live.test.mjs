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
  assert.match(main, /persist:\s*persist\(\),\s*settingsLoad/);
  assert.doesNotMatch(main, /persistLine\([^)]*settings/);
  assert.doesNotMatch(
    liveText({ phase: "title", settings: recovered }),
    /aprovado|verified|trusted|alguém de fora/,
  );
});

test("na porta e no fim a região viva nomeia a lacuna do som que o painel já mostra", () => {
  const gap = "Nenhum arquivo de som embarcado. Papéis declarados e vazios: dash.";
  assert.equal(liveText({ phase: "title", audio: gap }), `abertura. ${gap}`);
  assert.equal(
    liveText({ phase: "over", score: 12, audio: gap }),
    `fim da partida. 12. ${gap}`,
  );
  assert.equal(
    liveText({
      phase: "title",
      persist: "Esta sessão não grava",
      settings: "As preferências voltaram ao padrão",
      audio: gap,
    }),
    `abertura. Esta sessão não grava. As preferências voltaram ao padrão. ${gap}`,
  );
  assert.equal(liveText({ phase: "title", audio: "" }), "abertura");
  assert.equal(liveText({ phase: "playing", audio: gap }), "");
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12, audio: gap }),
    "pausado. 12",
  );
  assert.match(main, /audioGapLive\(audio\.missing\(\)\)/);
  assert.equal(liveText({ phase: "title", audio: gap }).includes(gap), true, "o painel falava e o live calava");
  assert.doesNotMatch(
    liveText({ phase: "title", audio: gap }),
    /aprovado|verified|heard|alguém de fora/,
  );
});

test("na porta a região viva nomeia a mesa e o look que a chuva já veste", () => {
  assert.equal(liveText({ phase: "title", spawn: "dusk" }), "abertura. chuva dusk");
  assert.equal(liveText({ phase: "title", look: "dusk" }), "abertura. look dusk");
  assert.equal(
    liveText({ phase: "title", spawn: "dusk", look: "calm" }),
    "abertura. chuva dusk. look calm",
  );
  assert.equal(
    liveText({ phase: "title", spawn: "calm", look: "dusk", lastScore: 8 }),
    "abertura. última 8. chuva calm. look dusk",
  );
  assert.equal(liveText({ phase: "title", spawn: "spawn", look: "normal" }), "abertura");
  assert.equal(liveText({ phase: "title", look: "contrast" }), "abertura");
  assert.equal(liveText({ phase: "title", spawn: "  dusk  " }), "abertura. chuva dusk");
  assert.equal(liveText({ phase: "playing", spawn: "dusk", look: "dusk" }), "");
  assert.equal(
    liveText({ phase: "over", score: 12, spawn: "dusk", look: "dusk" }),
    "fim da partida. 12",
  );
  assert.equal(
    liveText({
      phase: "title",
      spawn: "dusk",
      look: "dusk",
      persist: "Esta sessão não grava",
      titlePlay: "Jogar: toque",
    }),
    "abertura. chuva dusk. look dusk. Esta sessão não grava. Jogar: toque",
  );
  assert.match(main, /spawn:\s*state\.spawnProfile/);
  assert.match(main, /look:\s*settings\.look/);
  assert.doesNotMatch(
    liveText({ phase: "title", spawn: "dusk", look: "dusk" }),
    /aprovado|verified|consistent|alguém de fora|felt/,
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

test("a região viva nomeia como abrir a porta sem fingir sessão", () => {
  assert.equal(
    liveText({ phase: "title", titlePlay: "Jogar: toque" }),
    "abertura. Jogar: toque",
  );
  assert.equal(
    liveText({
      phase: "title",
      lastScore: 8,
      titleAgain: "Repetir a última: toque",
      titleNew: "Nova partida: baixo",
    }),
    "abertura. última 8. Repetir a última: toque. Nova partida: baixo",
  );
  assert.equal(
    liveText({ phase: "title", titlePlay: "Jogar: Espaço" }),
    "abertura. Jogar: Espaço",
  );
  assert.equal(
    liveText({ phase: "over", score: 12, overDoor: "Abertura: toque" }),
    "fim da partida. 12. Abertura: toque",
  );
  assert.equal(
    liveText({ phase: "playing", titlePlay: "Jogar: toque", overDoor: "Abertura: toque" }),
    "",
  );
  assert.equal(liveText({ phase: "title" }), "abertura");
  assert.match(main, /titlePlay:/);
  assert.match(main, /titleNew:/);
  assert.match(main, /overDoor:/);
  assert.match(main, /titleSurface/);
  assert.doesNotMatch(
    liveText({ phase: "title", titlePlay: "Jogar: toque", titleNew: "Nova partida: baixo" }),
    /aprovado|verified|alguém de fora|felt/,
  );
});

test("a região viva nomeia como sair da pausa sem fingir sessão", () => {
  assert.equal(
    liveText({
      phase: "playing",
      paused: true,
      score: 12,
      resume: "Continuar: Esc ou P",
      restart: "Reiniciar: R",
    }),
    "pausado. Continuar: Esc ou P. Reiniciar: R. 12",
  );
  assert.equal(
    liveText({ phase: "playing", paused: true, score: 12 }),
    "pausado. 12",
  );
  assert.equal(
    liveText({
      phase: "over",
      paused: true,
      score: 12,
      resume: "Continuar: Esc ou P",
      restart: "Reiniciar: R",
    }),
    "fim da partida. 12",
  );
  assert.equal(
    liveText({
      phase: "title",
      paused: true,
      resume: "Continuar: Esc ou P",
    }),
    "abertura",
  );
  assert.match(main, /resume:\s*bound\.resume/);
  assert.match(main, /restart:\s*bound\.restart/);
  assert.doesNotMatch(
    liveText({
      phase: "playing",
      paused: true,
      resume: "Continuar: Esc ou P",
      restart: "Reiniciar: R",
    }),
    /aprovado|verified|alguém de fora|felt/,
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
