// Legibilidade do HUD, medida em vez de observada a olho.
//
// Ordem de desenho garante que o texto vença os pixels do orbe, não que ele
// seja legível: texto claro sobre um orbe claro continua ilegível. Cada grupo
// do HUD precisa de uma placa que o contenha inteiro, em qualquer valor que o
// texto possa assumir — inclusive os longos, que são justamente os que vazam.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createRenderer, PALETTES } from "../src/game/render.js";
import { createState, advance, CONFIG, FIELD, PLAYER_Y } from "../src/game/rules.js";

const PLATE_COLORS = new Set(Object.values(PALETTES).map((palette) => palette.plate));

// Largura proporcional ao texto, como em qualquer fonte real: o que o teste
// verifica é que a placa mede a mesma string que o `fillText` desenha.
//
// O retângulo do fundo cobre a tela inteira, então "o texto está dentro de
// algum retângulo" seria sempre verdadeiro. Cada retângulo guarda a cor com
// que foi pintado, e só os da cor de placa contam.
function recordingCanvas() {
  const calls = { rects: [], texts: [], order: [] };
  let font = "8px system-ui";
  let align = "left";
  let pending = null;
  const size = () => Number.parseFloat(font) || 8;
  const measure = (text) => text.length * size() * 0.62;
  const commit = (rect) => calls.rects.push({ ...rect, style: context.fillStyle });
  const context = {
    setTransform() {},
    save() {},
    restore() {},
    beginPath() {
      pending = null;
    },
    closePath() {},
    moveTo() {},
    lineTo() {},
    arc() {
      calls.order.push("entidade");
    },
    ellipse() {},
    quadraticCurveTo() {},
    stroke() {},
    fill() {
      if (pending) commit(pending);
      pending = null;
    },
    fillRect(x, y, width, height) {
      commit({ x, y, width, height });
    },
    roundRect(x, y, width, height) {
      pending = { x, y, width, height };
    },
    strokeRect() {},
    clearRect() {},
    rect() {},
    createLinearGradient: () => ({ addColorStop() {} }),
    createRadialGradient: () => ({ addColorStop() {} }),
    measureText(text) {
      return { width: measure(text) };
    },
    fillText(text, x, y) {
      const width = measure(text);
      const left = align === "right" ? x - width : x;
      calls.order.push("texto");
      calls.texts.push({ text, left, right: left + width, top: y, bottom: y + size() });
    },
    set font(value) {
      font = value;
    },
    get font() {
      return font;
    },
    set textAlign(value) {
      align = value;
    },
    get textAlign() {
      return align;
    },
    textBaseline: "top",
    fillStyle: "",
    strokeStyle: "",
    lineWidth: 1,
    globalAlpha: 1,
  };
  return {
    calls,
    plates: () => calls.rects.filter((rect) => PLATE_COLORS.has(rect.style)),
    canvas: {
      width: 360,
      height: 640,
      style: {},
      getContext: () => context,
    },
  };
}

function hudTexts(state, settings = {}, extra = { best: 0 }) {
  const recorder = recordingCanvas();
  const renderer = createRenderer(recorder.canvas, { devicePixelRatio: 1 });
  renderer.resize(360, 640);
  renderer.draw(state, { paused: false, alpha: 0, steps: 1 }, settings, extra);
  return { texts: recorder.calls.texts, plates: recorder.plates(), order: recorder.calls.order };
}

function overlap(a, b) {
  return (
    a.x < b.x + b.width - 0.01 &&
    b.x < a.x + a.width - 0.01 &&
    a.y < b.y + b.height - 0.01 &&
    b.y < a.y + a.height - 0.01
  );
}

function boxOf(text) {
  return { x: text.left, y: text.top, width: text.right - text.left, height: text.bottom - text.top };
}

function covered(text, plates) {
  return plates.some(
    (plate) =>
      text.left >= plate.x - 0.01 &&
      text.right <= plate.x + plate.width + 0.01 &&
      text.top >= plate.y - 0.01 &&
      text.bottom <= plate.y + plate.height + 0.01,
  );
}

// Estados em que o HUD é mais longo: corrente com multiplicador, recorde de
// vários dígitos, dash recarregando, e interface ampliada.
function longState() {
  const state = createState(7);
  state.score = 1234;
  state.chain = 12;
  state.player.dashCooldown = CONFIG.player.dashCooldownTicks;
  return state;
}

for (const [nome, state, settings, extra] of [
  ["estado inicial", createState(3), {}, { best: 0 }],
  ["corrente com multiplicador e recorde longo", longState(), {}, { best: 98765 }],
  ["interface ampliada", longState(), { uiScale: 1.6 }, { best: 4321 }],
  ["alto contraste", longState(), { highContrast: true }, { best: 42 }],
  ["sem recorde", longState(), {}, {}],
]) {
  test(`toda linha do HUD cabe em uma placa — ${nome}`, () => {
    const calls = hudTexts(state, settings, extra);
    const hud = calls.texts.filter((item) => /Pontos|Corrente|Recorde|Dash|^\d+s$/.test(item.text));
    assert.ok(hud.length >= 4, `o HUD desenhou pouca coisa: ${JSON.stringify(hud.map((i) => i.text))}`);
    assert.ok(calls.plates.length >= 3, "cada canto do HUD precisa da sua placa");
    // Nenhuma placa pode ser um retângulo de tela cheia disfarçado.
    for (const plate of calls.plates) assert.ok(plate.width < 200, "placa larga demais para ser placa");
    for (const text of hud) {
      assert.ok(
        covered(text, calls.plates),
        `"${text.text}" vaza da placa: ${JSON.stringify(text)} contra ${JSON.stringify(calls.plates)}`,
      );
    }
  });
}

test("o teste sabe reprovar: sem placa, o texto do HUD fica descoberto", () => {
  const calls = hudTexts(createState(1));
  const semPlacas = calls.texts.filter((item) => item.text.includes("Pontos"));
  assert.ok(semPlacas.length === 1);
  assert.equal(covered(semPlacas[0], []), false);
});

test("a placa acompanha o texto quando ele cresce durante a partida", () => {
  const state = createState(5);
  const antes = hudTexts(state);
  state.chain = 9;
  state.score = 999;
  const depois = hudTexts(state);
  // Só a placa da esquerda, que é a que carrega Pontos e Corrente.
  const esquerda = (calls) => calls.plates.filter((plate) => plate.x < 10).map((plate) => plate.width);
  assert.ok(
    Math.max(...esquerda(depois)) > Math.max(...esquerda(antes)),
    "texto maior precisa de placa maior",
  );
  for (const text of depois.texts.filter((item) => item.text.includes("Corrente"))) {
    assert.ok(covered(text, depois.plates), `"${text.text}" ficou fora da placa`);
  }
});

// A legenda é a única cópia da informação sonora quando o áudio está desligado,
// então uma legenda ilegível é o mesmo que não ter legenda. Ela caía no centro
// inferior, exatamente sobre o jogador e sobre o rótulo do dash.
const RAJADA = [
  { id: "collect", text: "orbe coletado", count: 3 },
  { id: "hit", text: "atingido: corrente perdida", count: 1 },
  { id: "dash", text: "avanço", count: 2 },
];

function withCaptions(captions, settings = {}, extra = { best: 98765 }) {
  const calls = hudTexts(longState(), settings, { ...extra, captions });
  const legenda = calls.texts.filter((item) => captions.some((entry) => item.text.startsWith(entry.text)));
  const hud = calls.texts.filter((item) => /Pontos|Corrente |Recorde|Dash|^\d+s$/.test(item.text));
  return { ...calls, legenda, hud };
}

test("a legenda não ocupa os pixels de nenhum grupo do HUD", () => {
  const { legenda, hud, plates } = withCaptions(RAJADA);
  assert.equal(legenda.length, 3, `esperava três linhas de legenda: ${JSON.stringify(legenda.map((i) => i.text))}`);
  const hudPlates = plates.filter((plate) => hud.some((text) => covered(text, [plate])));
  assert.ok(hudPlates.length >= 3, "o HUD precisa das suas três placas para o teste valer");
  for (const text of legenda) {
    for (const box of hudPlates) {
      assert.ok(!overlap(boxOf(text), box), `"${text.text}" invade uma placa do HUD: ${JSON.stringify(box)}`);
    }
    for (const outro of hud) {
      assert.ok(!overlap(boxOf(text), boxOf(outro)), `"${text.text}" colide com "${outro.text}"`);
    }
  }
});

test("a legenda não cobre a faixa do jogador nem a base do campo", () => {
  for (const settings of [{}, { uiScale: 1.6 }, { highContrast: true }]) {
    const { legenda } = withCaptions(RAJADA, settings);
    for (const text of legenda) {
      assert.ok(
        text.bottom < PLAYER_Y - 6,
        `"${text.text}" desce até ${text.bottom}, dentro da faixa do jogador (${PLAYER_Y - 6})`,
      );
      assert.ok(text.right <= FIELD.width - 6 + 0.01 && text.left >= 0, `"${text.text}" sai do campo`);
    }
  }
});

test("cada linha de legenda cabe na sua própria placa", () => {
  const { legenda, plates } = withCaptions(RAJADA);
  for (const text of legenda) {
    assert.ok(covered(text, plates), `"${text.text}" vaza da placa: ${JSON.stringify(text)}`);
  }
});

test("repetição em rajada aparece com contagem em vez de linha repetida", () => {
  const { legenda } = withCaptions(RAJADA);
  const textos = legenda.map((item) => item.text);
  assert.deepEqual(new Set(textos).size, textos.length, `linha repetida na faixa: ${JSON.stringify(textos)}`);
  assert.ok(textos.includes("orbe coletado ×3"), `faltou a contagem: ${JSON.stringify(textos)}`);
  assert.ok(textos.includes("atingido: corrente perdida"), "contagem 1 não leva sufixo");
});

test("o teste sabe reprovar: no centro inferior a legenda cairia sobre o jogador", () => {
  const antiga = { x: FIELD.width / 2 - 30, y: FIELD.height - 17, width: 60, height: 9 };
  const jogador = { x: 0, y: PLAYER_Y - 6, width: FIELD.width, height: 24 };
  assert.ok(overlap(antiga, jogador), "o detector de colisão precisa acusar a posição antiga");
});

test("o HUD é desenhado depois das entidades, nunca antes", () => {
  const state = createState(9);
  for (let index = 0; index < 400; index += 1) advance(state, { move: 0, dash: false, bank: false });
  assert.ok(state.entities.length > 0, "a cena precisa ter entidades para o teste valer");
  const { order } = hudTexts(state);
  assert.ok(order.includes("entidade"), "a cena precisa ter desenhado entidades");
  assert.ok(order.indexOf("entidade") < order.indexOf("texto"), "o texto do HUD precisa vir por cima");
});
