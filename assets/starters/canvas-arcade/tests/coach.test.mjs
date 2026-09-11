import { test } from "node:test";
import assert from "node:assert/strict";

import { coachHint, coachText, FANTASY_TICKS, MOVE_TICKS } from "../src/game/coach.js";
import { beginRun, CONFIG, createState, restoreState, PLAYER_Y } from "../src/game/rules.js";
import { captureHold } from "../src/core/save.js";

const shardOnRail = () => ({ id: 1, kind: "shard", x: 160, y: PLAYER_Y - 22, vy: 0 });
const orbOnRail = () => ({ id: 2, kind: "orb", x: 160, y: PLAYER_Y - 22, vy: 0 });

test("os primeiros ticks pedem movimento, não a tabela da página", () => {
  const state = createState(1);
  assert.equal(coachHint(state), "move");
});

test("com fantasia na mesa o primeiro aviso é a frase, não o movimento", () => {
  const state = createState(1);
  assert.equal(coachHint(state, { fantasy: "guardar a corrente" }), "fantasy");
  state.tick = 48;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente" }), "move");
});

test("fantasia vazia não toma o lugar do movimento", () => {
  assert.equal(coachHint(createState(1), { fantasy: "   " }), "move");
});

test("sem corrente o aviso nomeia a prática enquanto o campo a marca", () => {
  const state = createState(1);
  state.tick = 90;
  assert.equal(coachHint(state), "practice");
  state.tick = CONFIG.spawn.practiceTicks;
  assert.equal(coachHint(state), "collect", "depois da prática o aviso pede o orbe");
});

test("corrente que já vale mais pede guardar", () => {
  const state = createState(1);
  state.tick = 200;
  state.chain = 3;
  assert.equal(coachHint(state), "bank");
});

test("depois da primeira guarda o ensino some", () => {
  const state = createState(1);
  state.tick = 400;
  state.chain = 4;
  state.stats.banks = 1;
  assert.equal(coachHint(state), null);
});

test("partida encerrada não ensina", () => {
  const state = createState(1);
  state.phase = "over";
  assert.equal(coachHint(state), null);
});

test("a fantasia na porta não come o aviso de mover", () => {
  const state = createState(1, { entry: "title" });
  const lines = { fantasy: "guardar a corrente ou continuar" };
  assert.equal(coachHint(state, lines), "fantasy");
  state.attractTick = FANTASY_TICKS - 1;
  assert.equal(coachHint(state, lines), "fantasy");
  state.attractTick = FANTASY_TICKS;
  assert.equal(coachHint(state, lines), "move", "depois da frase a porta ainda ensina a abrir");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS - 1;
  assert.equal(coachHint(state, lines), "move");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS;
  assert.equal(coachHint(state, lines), null);
  const plain = createState(2, { entry: "title" });
  plain.attractTick = MOVE_TICKS - 1;
  assert.equal(coachHint(plain), "move", "sem frase o aviso de mover continua o mesmo");
  plain.attractTick = MOVE_TICKS;
  assert.equal(coachHint(plain), null);
});

test("depois da porta o campo não repete a frase nem o mover", () => {
  const lines = { fantasy: "guardar a corrente" };
  const door = createState(1, { entry: "title" });
  door.attractTick = FANTASY_TICKS + MOVE_TICKS;
  beginRun(door);
  assert.equal(door.phase, "playing");
  assert.equal(door.tick, 0);
  assert.equal(coachHint(door, lines), "practice", "depois da porta o campo nomeia a prática");
  door.entities = [shardOnRail()];
  assert.equal(coachHint(door, lines), "dash", "depois da porta o estilhaço pede o dash");

  const mid = createState(2, { entry: "title" });
  mid.attractTick = FANTASY_TICKS;
  beginRun(mid);
  assert.equal(coachHint(mid, lines), "move", "se a porta só deu a frase o campo ainda pede mover");
  mid.entities = [shardOnRail()];
  assert.equal(coachHint(mid, lines), "move", "mover ainda vem antes do dash se a porta não terminou");

  const mash = createState(3, { entry: "title" });
  mash.attractTick = 10;
  beginRun(mash);
  assert.equal(coachHint(mash, lines), "fantasy", "quem fura a porta ainda vê a frase no campo");

  const headless = createState(4);
  assert.equal(coachHint(headless, lines), "fantasy", "sem porta a frase continua o primeiro aviso");

  const plain = createState(5, { entry: "title" });
  plain.attractTick = MOVE_TICKS;
  beginRun(plain);
  assert.equal(coachHint(plain), "practice", "sem frase a porta que já ensinou mover não pede de novo");
});

test("o hold não some o relógio da porta", () => {
  const lines = { fantasy: "guardar a corrente" };
  const door = createState(1, { entry: "title" });
  door.attractTick = FANTASY_TICKS + MOVE_TICKS;
  beginRun(door);
  door.tick = 10;
  assert.equal(coachHint(door, lines), "practice", "depois da porta o campo nomeia a prática");
  const hold = captureHold(door);
  assert.ok(hold, "o tick no campo cabe no hold");
  assert.equal(hold.attractTick, FANTASY_TICKS + MOVE_TICKS, "o recorte leva o relógio");
  const resumed = restoreState(hold);
  assert.equal(resumed.attractTick, FANTASY_TICKS + MOVE_TICKS);
  assert.equal(coachHint(resumed, lines), "practice", "retomar não devolve a frase");
  resumed.entities = [shardOnRail()];
  assert.equal(coachHint(resumed, lines), "dash", "retomar não devolve o mover");

  const mid = createState(2, { entry: "title" });
  mid.attractTick = FANTASY_TICKS;
  beginRun(mid);
  mid.tick = 10;
  assert.equal(
    coachHint(restoreState(captureHold(mid)), lines),
    "move",
    "se a porta só deu a frase o hold ainda pede mover",
  );

  const headless = createState(3);
  headless.tick = 10;
  const raw = captureHold(headless);
  assert.equal(raw.attractTick, 0);
  assert.equal(
    coachHint(restoreState(raw), lines),
    "fantasy",
    "sem porta o hold não finge que a frase já passou",
  );

  const forgotten = captureHold(door);
  delete forgotten.attractTick;
  assert.equal(restoreState(forgotten).attractTick, 0, "hold antigo não inventa ensino feito");
  assert.equal(
    coachHint(restoreState(forgotten), lines),
    "fantasy",
    "sem relógio o campo volta ao primeiro aviso",
  );
});

test("a abertura ensina mover sem abrir o ciclo", () => {
  const state = createState(1, { entry: "title" });
  assert.equal(coachHint(state), "move");
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), "fantasy");
  state.attractTick = FANTASY_TICKS;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), "move");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS - 1;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), "move");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), null);
  state.chain = 3;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), null, "a porta não pede guardar");
  assert.equal(coachHint(state, {}, { surface: "pointer" }), null, "a porta não ensina toque");
  assert.equal(coachHint(state, {}, { surface: "gamepad" }), null, "a mostra no trilho não ensina dash na porta");
});

test("estilhaço no trilho pede o dash antes do orbe", () => {
  const state = createState(1);
  state.tick = 90;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), "dash");
  state.stats.dashes = 1;
  assert.equal(coachHint(state), "practice", "depois do avanço o aviso não insiste no dash");
});

test("orbe no trilho não finge ameaça", () => {
  const state = createState(1);
  state.tick = 90;
  state.entities = [orbOnRail()];
  assert.equal(coachHint(state), "practice");
});

test("toque e controle ganham passo depois do movimento", () => {
  const state = createState(1);
  state.tick = 70;
  assert.equal(coachHint(state, {}, { surface: "pointer" }), "touch");
  assert.equal(coachHint(state, {}, { surface: "gamepad" }), "pad");
  assert.equal(coachHint(state, {}, { surface: "keyboard" }), "practice");
  state.tick = 50;
  assert.equal(coachHint(state, {}, { surface: "pointer" }), "move", "o movimento ainda vem primeiro");
  state.tick = 120;
  assert.equal(coachHint(state, {}, { surface: "gamepad" }), "practice", "o passo da superfície some");
});

test("estilhaço no trilho vence o passo da superfície", () => {
  const state = createState(1);
  state.tick = 70;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state, {}, { surface: "pointer" }), "dash");
});

test("o estilhaço nomeia o custo enquanto a corrente voltou a zero", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.hits = 1;
  assert.equal(coachHint(state), "hit");
  state.stats.missed = 1;
  assert.equal(coachHint(state), "hit", "o estilhaço vence a queda");
  state.chain = 1;
  assert.equal(coachHint(state), "practice");
  state.chain = 3;
  assert.equal(coachHint(state), "bank");
  state.stats.banks = 1;
  assert.equal(coachHint(state), null);
});

test("estilhaço no trilho vence o custo do hit", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.hits = 1;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), "dash");
});

test("a porta não ensina a prática", () => {
  const state = createState(1, { entry: "title" });
  state.attractTick = 90;
  assert.equal(coachHint(state), null);
  assert.equal(coachHint(state, {}, { surface: "pointer" }), null, "a porta não ensina toque na prática");
});

test("a porta não ensina o custo do estilhaço", () => {
  const state = createState(1, { entry: "title" });
  state.attractTick = 90;
  state.stats.hits = 1;
  assert.equal(coachHint(state), null);
  assert.equal(coachHint(state, {}, { surface: "pointer" }), null, "a porta não ensina toque no hit");
});

test("orbe perdido nomeia o custo enquanto a corrente é zero", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.missed = 1;
  assert.equal(coachHint(state), "miss");
  state.chain = 1;
  assert.equal(coachHint(state), "practice");
  state.chain = 3;
  assert.equal(coachHint(state), "bank");
  state.stats.banks = 1;
  assert.equal(coachHint(state), null);
});

test("estilhaço no trilho vence a queda", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.missed = 1;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), "dash");
});

test("o fecho pede guardar a corrente viva sem fingir sessão observada", () => {
  const mid = createState(1);
  mid.tick = 1800;
  mid.chain = 4;
  mid.stats.banks = 1;
  assert.equal(coachHint(mid), null, "no meio a primeira guarda encerra o ensino");

  const close = createState(1);
  close.tick = CONFIG.runTicks - 300;
  close.chain = 4;
  close.stats.banks = 1;
  assert.equal(coachHint(close), "bank");
  assert.equal(coachHint(close, {}, { surface: "pointer" }), "bank", "o fecho não reabre o toque");
  assert.equal(coachHint(close, {}, { surface: "gamepad" }), "bank", "o fecho não reabre o controle");

  const empty = createState(1);
  empty.tick = CONFIG.runTicks - 300;
  empty.chain = 0;
  empty.stats.banks = 1;
  assert.equal(coachHint(empty), null);
  assert.equal(coachHint(empty, {}, { surface: "pointer" }), null, "sem corrente o fecho não ensina toque");

  const ended = createState(1);
  ended.phase = "over";
  ended.tick = CONFIG.runTicks;
  ended.chain = 4;
  ended.stats.banks = 1;
  assert.equal(coachHint(ended), null);
});

test("o aviso do primeiro ciclo vira texto, não só a chave", () => {
  const lines = {
    fantasy: "guardar a corrente",
    hint_move: "←/→, arraste ou analógico",
    hint_collect: "Passe no orbe — a corrente cresce",
    hint_practice: "Só orbes — a borda some quando a ameaça começa",
  };
  const door = createState(1, { entry: "title" });
  assert.equal(coachText(door, lines), "guardar a corrente");
  door.attractTick = FANTASY_TICKS;
  assert.equal(coachText(door, lines), "←/→, arraste ou analógico");
  const field = createState(2);
  field.tick = 90;
  assert.equal(coachText(field, lines), "Só orbes — a borda some quando a ameaça começa");
  field.tick = CONFIG.spawn.practiceTicks;
  assert.equal(coachText(field, lines), "Passe no orbe — a corrente cresce");
  field.phase = "over";
  assert.equal(coachText(field, lines), "");
});
