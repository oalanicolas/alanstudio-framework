// Legibilidade do HUD, medida em vez de observada a olho.
//
// Ordem de desenho garante que o texto vença os pixels do orbe, não que ele
// seja legível: texto claro sobre um orbe claro continua ilegível. Cada grupo
// do HUD precisa de uma placa que o contenha inteiro, em qualquer valor que o
// texto possa assumir — inclusive os longos, que são justamente os que vazam.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createRenderer, PALETTES, dashCharge } from "../src/game/render.js";
import { createState, advance, attractEntities, CONFIG, FIELD, PLAYER_Y } from "../src/game/rules.js";
import { ONE_HAND_BINDINGS } from "../src/core/settings.js";

const PLATE_COLORS = new Set(Object.values(PALETTES).map((palette) => palette.plate));
const PLATE_EDGE_COLORS = new Set(Object.values(PALETTES).map((palette) => palette.plateEdge));

// Largura proporcional ao texto, como em qualquer fonte real: o que o teste
// verifica é que a placa mede a mesma string que o `fillText` desenha.
//
// O retângulo do fundo cobre a tela inteira, então "o texto está dentro de
// algum retângulo" seria sempre verdadeiro. Cada retângulo guarda a cor com
// que foi pintado, e só os da cor de placa contam.
function recordingCanvas() {
  const calls = { rects: [], edges: [], texts: [], order: [], arcs: 0, lineTos: 0, radials: 0, paths: [], strokes: [] };
  let font = "8px system-ui";
  let align = "left";
  let pending = null;
  let path = [];
  const size = () => Number.parseFloat(font) || 8;
  const measure = (text) => text.length * size() * 0.62;
  const commit = (rect) => calls.rects.push({ ...rect, style: context.fillStyle });
  const commitEdge = (rect) => calls.edges.push({ ...rect, style: context.strokeStyle });
  const context = {
    setTransform(a, b, c, d, e, f) {
      calls.transform = { e, f };
    },
    save() {},
    restore() {},
    beginPath() {
      pending = null;
      path = [];
    },
    closePath() {},
    moveTo(x, y) {
      path.push({ x, y });
    },
    lineTo(x, y) {
      calls.lineTos += 1;
      path.push({ x, y });
    },
    arc() {
      calls.arcs += 1;
      calls.order.push("entidade");
    },
    ellipse() {},
    quadraticCurveTo() {},
    stroke() {
      if (pending) commitEdge(pending);
      if (path.length >= 2) calls.strokes.push({ points: path.slice(), style: context.strokeStyle });
      pending = null;
      path = [];
    },
    fill() {
      if (pending) commit(pending);
      if (path.length >= 2) calls.paths.push({ points: path.slice(), style: context.fillStyle });
      pending = null;
      path = [];
    },
    fillRect(x, y, width, height) {
      commit({ x, y, width, height });
    },
    roundRect(x, y, width, height) {
      pending = { x, y, width, height };
    },
    strokeRect(x, y, width, height) {
      commitEdge({ x, y, width, height });
    },
    clearRect() {},
    rect() {},
    createLinearGradient: () => ({ addColorStop() {} }),
    createRadialGradient() {
      calls.radials += 1;
      return { addColorStop() {} };
    },
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
    edges: () => calls.edges.filter((rect) => PLATE_EDGE_COLORS.has(rect.style)),
    canvas: {
      width: 360,
      height: 640,
      style: {},
      getContext: () => context,
    },
  };
}

function hudTexts(state, settings = {}, extra = { best: 0 }, frame = { paused: false, alpha: 0, steps: 1 }) {
  const recorder = recordingCanvas();
  const renderer = createRenderer(recorder.canvas, { devicePixelRatio: 1 });
  renderer.resize(360, 640);
  renderer.draw(state, frame, settings, extra);
  return {
    texts: recorder.calls.texts,
    plates: recorder.plates(),
    edges: recorder.edges(),
    order: recorder.calls.order,
    transform: recorder.calls.transform,
  };
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
    // Cobrir não é a mesma coisa que se ver. Cada placa precisa da sua borda,
    // senão ela oclui a cena e ninguém percebe onde a interface começa.
    assert.equal(
      calls.edges.length,
      calls.plates.length,
      `placa sem borda: ${calls.plates.length} placas, ${calls.edges.length} bordas`,
    );
  });
}

// A seta do HUD promete o que guardar a corrente vale. Com corrente 1 ela saía
// como "Corrente 1 → 1": conta certa, informação nenhuma, e um revisor de vídeo
// leu isso como bug de lógica. Ela só aparece quando há ganho a mostrar.
test("a seta da corrente só aparece quando guardar rende mais que a corrente", () => {
  const chainText = (chain) => {
    const state = createState(2);
    state.chain = chain;
    const calls = hudTexts(state);
    return calls.texts.find((item) => item.text.startsWith("Corrente")).text;
  };
  assert.equal(chainText(0), "Corrente 0");
  assert.equal(chainText(1), "Corrente 1");
  assert.equal(chainText(2), "Corrente 2 → 4");
  assert.equal(chainText(7), "Corrente 7 → 49");
});

function chainMarks(state, settings = {}) {
  return paint(state, settings).rects.filter(
    (rect) => rect.style === PALETTES.normal.chain && rect.width < 5 && rect.height < 5,
  );
}

test("a corrente mora no corpo, não só no HUD", () => {
  const empty = createState(1);
  assert.equal(chainMarks(empty).length, 0, "sem corrente o corpo não inventa aposta");
  const one = createState(1);
  one.chain = 1;
  assert.equal(chainMarks(one).length, 1);
  const three = createState(1);
  three.chain = 3;
  assert.equal(chainMarks(three).length, 3);
  const packed = createState(1);
  packed.chain = 12;
  assert.equal(chainMarks(packed).length, CONFIG.feel.chainPips, "o teto dos pips não esconde o HUD");
  const still = createState(1);
  still.chain = 3;
  still.tick = 40;
  const a = chainMarks(still, { reducedMotion: true }).map((rect) => [rect.x, rect.y]);
  still.tick = 80;
  const b = chainMarks(still, { reducedMotion: true }).map((rect) => [rect.x, rect.y]);
  assert.deepEqual(a, b, "com menos movimento a formação trava, não some");
  const spinning = createState(1);
  spinning.chain = 3;
  spinning.tick = 0;
  const first = chainMarks(spinning)[0];
  spinning.tick = 20;
  const later = chainMarks(spinning)[0];
  assert.notEqual(first.x, later.x, "sem redução a órbita precisa andar");
  const ended = createState(1);
  ended.phase = "over";
  ended.chain = 5;
  assert.equal(chainMarks(ended).length, 0, "no fim o corpo não veste a aposta que já caiu");
});

// Dois revisores independentes olharam o vídeo, viram os orbes desaparecerem
// atrás do texto e ainda assim relataram que não havia placa nenhuma. Estavam
// certos sobre o que importa: preenchida com rgba(7,9,13,0.86) sobre o campo
// #171b26, a placa resolve em algo próximo de #0a0c10 — diferença que a
// compressão de vídeo apaga. Em alto contraste era pior: campo preto e placa
// preta são a mesma cor, então a placa não existia visualmente.
test("a placa se distingue do campo em toda paleta, não só o cobre", () => {
  const distance = (a, b) => Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]) + Math.abs(a[2] - b[2]);
  const rgb = (color) => {
    const hex = /^#([0-9a-f]{6})$/i.exec(color);
    if (hex) return [0, 2, 4].map((at) => Number.parseInt(hex[1].slice(at, at + 2), 16));
    const parts = /rgba?\(([^)]+)\)/.exec(color)[1].split(",").map(Number);
    return parts.slice(0, 3);
  };
  // A placa translúcida é composta sobre o campo antes de ser comparada: o que
  // o olho vê é a mistura, não a cor declarada.
  const over = (color, base) => {
    const parts = /rgba\(([^)]+)\)/.exec(color);
    if (!parts) return rgb(color);
    const [r, g, b, alpha = 1] = parts[1].split(",").map(Number);
    return [r, g, b].map((channel, at) => channel * alpha + base[at] * (1 - alpha));
  };

  for (const [name, palette] of Object.entries(PALETTES)) {
    const field = rgb(palette.field);
    const surface = over(palette.plate, field);
    const edge = over(palette.plateEdge, surface);
    assert.ok(
      palette.plateEdge,
      `a paleta ${name} não declara plateEdge, e sem borda a placa depende só do preenchimento`,
    );
    // A borda é o traço que sobrevive à compressão e ao campo da mesma cor.
    assert.ok(
      distance(edge, field) > 60,
      `em ${name} a borda (${edge.map(Math.round)}) não se separa do campo (${field}): distância ${Math.round(distance(edge, field))}`,
    );
  }
});

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

test("em sequência de quadros o HUD continua coberto e as entidades passam por baixo", () => {
  const state = createState(11);
  let framesWithEntities = 0;
  for (let index = 0; index < 240; index += 1) {
    advance(state, { move: index % 18 < 9 ? -1 : 1, dash: index % 40 === 0, bank: false });
    if (state.entities.length === 0) continue;
    const frame = hudTexts(state);
    framesWithEntities += 1;
    assert.ok(frame.order.indexOf("entidade") < frame.order.indexOf("texto"));
    for (const text of frame.texts) {
      assert.ok(covered(text, frame.plates), `texto descoberto em movimento: ${text.text}`);
    }
    assert.ok(frame.edges.length > 0, "borda da placa some no movimento");
  }
  assert.ok(framesWithEntities > 20, "a sequência precisa ter chuva, não só o campo vazio");
});

test("o look dusk pinta o campo diferente do padrão e cede ao alto contraste", () => {
  const state = createState(1);
  const fieldOf = (calls) => calls.rects.find((rect) => rect.width === FIELD.width && rect.height === FIELD.height);
  const normal = fieldOf(paint(state));
  const dusk = fieldOf(paint(state, { look: "dusk" }));
  const contrast = fieldOf(paint(state, { look: "dusk", highContrast: true }));
  assert.ok(normal && dusk && contrast, "o campo precisa ter sido pintado");
  assert.notEqual(dusk.style, normal.style, "dusk precisa ser outro look, não o padrão");
  assert.equal(contrast.style, PALETTES.contrast.field, "alto contraste vence o look");
});

test("a tinta estável troca orbe e estilhaço e cede ao alto contraste", () => {
  const state = createState(1);
  const fieldOf = (calls) => calls.rects.find((rect) => rect.width === FIELD.width && rect.height === FIELD.height);
  const dusk = fieldOf(paint(state, { look: "dusk" }));
  const stable = fieldOf(paint(state, { look: "dusk", colorblind: true }));
  const contrast = fieldOf(paint(state, { look: "dusk", colorblind: true, highContrast: true }));
  assert.equal(stable.style, dusk.style, "o campo do look permanece");
  assert.equal(contrast.style, PALETTES.contrast.field, "alto contraste vence a tinta estável");
});

test("orbe e estilhaço usam primitivas diferentes, não só cores diferentes", () => {
  const orb = createState(1);
  orb.entities = [{ id: 1, kind: "orb", x: 80, y: 70, vy: 0 }];
  const shard = createState(1);
  shard.entities = [{ id: 1, kind: "shard", x: 80, y: 70, vy: 0 }];
  const paintedOrb = paint(orb);
  const paintedShard = paint(shard);
  assert.ok(paintedOrb.arcs > paintedShard.arcs, "o orbe precisa do círculo; o estilhaço não");
  assert.ok(paintedShard.lineTos > paintedOrb.lineTos, "o estilhaço precisa do losango; o orbe não");
});

test("a chuva e o campo ganham volume sem virar faixa no HUD", () => {
  const state = createState(1);
  state.entities = [
    { id: 1, kind: "orb", x: 80, y: 70, vy: 0 },
    { id: 2, kind: "shard", x: 200, y: 70, vy: 0 },
  ];
  const lit = paint(state);
  const still = paint(state, { reducedMotion: true });
  assert.ok(lit.radials > 0, "o campo precisa da vinheta");
  assert.equal(still.radials, 0, "com menos movimento a vinheta some");
  assert.ok(lit.arcs > still.arcs, "o orbe precisa do halo");
  assert.ok(lit.lineTos > still.lineTos, "o estilhaço precisa do halo na mesma forma");
  assert.ok(
    lit.rects.filter((rect) => rect.height === 2 && rect.y < 20 && !PLATE_COLORS.has(rect.style)).length
      === still.rects.filter((rect) => rect.height === 2 && rect.y < 20 && !PLATE_COLORS.has(rect.style)).length,
    "volume no campo não é faixa no HUD",
  );
  const field = lit.rects.find((rect) => rect.width === FIELD.width && rect.height === FIELD.height);
  assert.ok(field, "o campo continua o primeiro recorte");
});

test("a câmera por verbo desloca o campo e some com redução de movimento", () => {
  const state = createState(1);
  state.camera = { x: 5, y: -3 };
  const moved = hudTexts(state);
  const still = hudTexts(state, { reducedMotion: true });
  assert.ok(moved.transform);
  assert.notEqual(moved.transform.e, still.transform.e, "punch horizontal precisa chegar no quadro");
  assert.notEqual(moved.transform.f, still.transform.f, "punch vertical precisa chegar no quadro");
});

test("no fim a câmera senta; o punch do último verbo não atravessa o overlay", () => {
  const leftover = createState(1);
  leftover.phase = "over";
  leftover.camera = { x: 5, y: -3 };
  leftover.shake = 4;
  leftover.flash = 0.8;
  const sat = createState(1);
  sat.phase = "over";
  const ended = hudTexts(leftover);
  const rest = hudTexts(sat);
  assert.equal(ended.transform.e, rest.transform.e, "punch horizontal não atravessa o fim");
  assert.equal(ended.transform.f, rest.transform.f, "punch vertical não atravessa o fim");
  const flash = paint(leftover).rects.some((rect) => String(rect.style).startsWith("rgba(255,245,235"));
  assert.equal(flash, false, "o flash do último verbo não atravessa o fim");
});

test("na pausa a câmera senta; o punch do último verbo não atravessa o overlay", () => {
  const leftover = createState(1);
  leftover.camera = { x: 5, y: -3 };
  leftover.shake = 4;
  leftover.flash = 0.8;
  const sat = createState(1);
  const held = { paused: true, alpha: 0, steps: 1 };
  const paused = hudTexts(leftover, {}, { best: 0 }, held);
  const rest = hudTexts(sat, {}, { best: 0 }, held);
  assert.equal(paused.transform.e, rest.transform.e, "punch horizontal não atravessa a pausa");
  assert.equal(paused.transform.f, rest.transform.f, "punch vertical não atravessa a pausa");
  const flash = paint(leftover, {}, { best: 0 }, held).rects.some((rect) => (
    String(rect.style).startsWith("rgba(255,245,235")
  ));
  assert.equal(flash, false, "o flash do último verbo não atravessa a pausa");
  const live = hudTexts(leftover);
  const idle = hudTexts(sat);
  assert.notEqual(live.transform.e, idle.transform.e, "sem pausa o punch continua");
});

function paint(state, settings = {}, extra = { best: 0 }, frame = { paused: false, alpha: 0, steps: 1 }) {
  const recorder = recordingCanvas();
  const renderer = createRenderer(recorder.canvas, { devicePixelRatio: 1 });
  renderer.resize(360, 640);
  renderer.draw(state, frame, settings, extra);
  return recorder.calls;
}

function playerFill(state) {
  const rects = paint(state).rects.filter(
    (rect) => rect.width < 40 && rect.y < PLAYER_Y && rect.y + rect.height > PLAYER_Y - 8,
  );
  assert.ok(rects.length > 0, "o jogador precisa ter sido pintado");
  return rects[0].style;
}

function playerBox(state) {
  const rects = paint(state).rects.filter(
    (rect) => rect.width < 40 && rect.y < PLAYER_Y && rect.y + rect.height > PLAYER_Y - 8,
  );
  assert.ok(rects.length > 0, "o jogador precisa ter sido pintado");
  return rects[0];
}

function playerNose(state, settings = {}) {
  const box = playerBox(state);
  const color = playerFill(state);
  const drawn = paint(state, settings);
  const noses = drawn.paths.filter((item) => (
    item.style === color
    && item.points.some((point) => point.y >= box.y - 2 && point.y <= box.y + box.height + 2)
  ));
  assert.ok(noses.length >= 1, "o jogador precisa da ponta");
  const points = noses[0].points;
  return {
    minX: Math.min(...points.map((point) => point.x)),
    maxX: Math.max(...points.map((point) => point.x)),
    points,
  };
}

function hudBands(drawn) {
  return drawn.rects.filter((rect) => (
    rect.height === 2 && rect.y < 20 && !PLATE_COLORS.has(rect.style)
  )).length;
}

test("guardar e o erro achatam o corpo diferente da coleta", () => {
  const collected = createState(1);
  collected.player.squash = CONFIG.feel.squashCollect;
  const banked = createState(1);
  banked.player.squash = CONFIG.feel.squashBank;
  const struck = createState(1);
  struck.player.squash = CONFIG.feel.squashHit;
  const a = playerBox(collected);
  const b = playerBox(banked);
  const c = playerBox(struck);
  assert.ok(b.width > a.width, "guardar senta mais que coletar");
  assert.ok(c.width > b.width, "o erro esmaga mais que guardar");
  assert.ok(c.height < b.height && b.height < a.height, "o achatamento precisa chegar no quadro");
});

test("o raspo estreita o corpo; o dash alonga", () => {
  const start = createState(1);
  start.player.squash = CONFIG.feel.squashDash;
  const graze = createState(1);
  graze.player.squash = CONFIG.feel.squashGraze;
  const launched = playerBox(start);
  const rasped = playerBox(graze);
  assert.ok(rasped.width < launched.width, "o contato estreita; o dash alonga");
  assert.ok(rasped.height > launched.height, "o contato alonga na vertical");
});

test("a antecipação do avanço estreita o corpo antes de alongar", () => {
  const idle = createState(1);
  const coil = createState(1);
  coil.player.squash = CONFIG.feel.squashCoil;
  const start = createState(1);
  start.player.squash = CONFIG.feel.squashDash;
  const rest = playerBox(idle);
  const wound = playerBox(coil);
  const launched = playerBox(start);
  assert.ok(wound.width < rest.width, "antecipar estreita");
  assert.ok(wound.height > rest.height, "antecipar alonga na vertical");
  assert.ok(launched.width > rest.width, "o disparo alonga na horizontal");
});

test("perder o orbe senta o corpo menos que coletar", () => {
  const collected = createState(1);
  collected.player.squash = CONFIG.feel.squashCollect;
  const missed = createState(1);
  missed.player.squash = CONFIG.feel.squashMiss;
  const a = playerBox(collected);
  const b = playerBox(missed);
  assert.ok(a.width > b.width, "a queda senta menos que a coleta");
  assert.ok(a.height < b.height, "o achatamento precisa chegar no quadro");
});

test("o término do dash senta mais que a partida e menos que guardar", () => {
  const start = createState(1);
  start.player.squash = CONFIG.feel.squashDash;
  const land = createState(1);
  land.player.squash = CONFIG.feel.squashLand;
  const banked = createState(1);
  banked.player.squash = CONFIG.feel.squashBank;
  const a = playerBox(start);
  const b = playerBox(land);
  const c = playerBox(banked);
  assert.ok(b.width > a.width, "aterrissar senta mais que a partida");
  assert.ok(c.width > b.width, "guardar senta mais que aterrissar");
});

test("a graça do erro some o corpo e o traz de volta sem apagar o tijolo", () => {
  const lit = createState(1);
  lit.player.invuln = 8;
  const dim = createState(1);
  dim.player.invuln = 6;
  const a = playerBox(lit);
  const b = playerBox(dim);
  assert.equal(a.width, b.width, "o fillRect do squash permanece nos dois tempos");
  const rimOn = paint(lit).edges.filter((edge) => (
    edge.style === PALETTES.normal.danger && edge.width < 40 && edge.y < PLAYER_Y
  ));
  const rimOff = paint(dim).edges.filter((edge) => (
    edge.style === PALETTES.normal.danger && edge.width < 40 && edge.y < PLAYER_Y
  ));
  assert.ok(rimOn.length >= 1, "no tempo claro o contorno marca a graça");
  assert.equal(rimOff.length, 0, "no tempo escuro o contorno some com o corpo");
  const still = createState(1);
  still.player.invuln = 6;
  const held = paint(still, { reducedMotion: true }).edges.filter((edge) => (
    edge.style === PALETTES.normal.danger && edge.width < 40 && edge.y < PLAYER_Y
  ));
  assert.ok(held.length >= 1, "com menos movimento o contorno fica, o tijolo não some");
  const heldBox = paint(still, { reducedMotion: true }).rects.filter(
    (rect) => rect.width < 40 && rect.y < PLAYER_Y && rect.y + rect.height > PLAYER_Y - 8,
  );
  assert.ok(heldBox.length > 0, "com menos movimento o fillRect permanece");
});

test("no fim o corpo senta e larga a pose de jogo", () => {
  const idle = createState(1);
  const ended = createState(1);
  ended.phase = "over";
  ended.player.squash = CONFIG.feel.squashOver;
  ended.player.dashTicks = 4;
  ended.player.invuln = 6;
  const rest = playerBox(idle);
  const sat = playerBox(ended);
  assert.ok(sat.width > rest.width, "o relógio senta o corpo");
  assert.ok(sat.height < rest.height, "o achatamento precisa chegar no quadro");
  assert.equal(playerFill(ended), PALETTES.normal.player, "o dash não veste o fim");
  const rim = paint(ended).edges.filter((edge) => (
    edge.style === PALETTES.normal.danger && edge.width < 40 && edge.y < PLAYER_Y
  ));
  assert.equal(rim.length, 0, "a graça não pisca depois do relógio");
  const held = paint(ended, { reducedMotion: true }).rects.filter(
    (rect) => rect.width < 40 && rect.y < PLAYER_Y && rect.y + rect.height > PLAYER_Y - 8,
  );
  assert.ok(held.length > 0, "o fillRect permanece no fim");
  assert.ok(held[0].width > rest.width, "com menos movimento o corpo continua sentado");
});

test("a recuperação do dash não se parece com o dash nem com o descanso", () => {
  const idle = createState(1);
  const dash = createState(1);
  dash.player.dashTicks = 4;
  const recovery = createState(1);
  recovery.player.dashRecovery = 4;
  assert.notEqual(playerFill(dash), playerFill(idle));
  assert.notEqual(playerFill(recovery), playerFill(idle));
  assert.notEqual(playerFill(recovery), playerFill(dash));
});

test("a abertura nomeia sessão volátil e gravação recusada sem inventar faixa", () => {
  const state = createState(1, { entry: "title" });
  const volatile = paint(state, {}, { best: 0, persist: { durable: false, wrote: true, trusted: false } });
  assert.ok(volatile.texts.some((item) => String(item.text).includes("não grava")));
  assert.ok(hudBands(volatile) <= hudBands(paint(state)), "o aviso de save não é faixa no HUD");
  const unsaved = paint(state, {}, { best: 0, persist: { durable: true, wrote: false, trusted: false } });
  assert.ok(unsaved.texts.some((item) => String(item.text).includes("não ficou")));
  const quiet = paint(state, {}, { best: 0, persist: { durable: true, wrote: true, trusted: false } });
  assert.equal(quiet.texts.some((item) => String(item.text).includes("não grava")), false);
  assert.equal(quiet.texts.some((item) => String(item.text).includes("não ficou")), false);
  const ended = createState(1);
  ended.phase = "over";
  const over = paint(ended, {}, { persist: { durable: false, wrote: true, trusted: false } });
  assert.ok(over.texts.some((item) => String(item.text).includes("não grava")));
  assert.doesNotMatch(
    [...volatile.texts, ...unsaved.texts, ...over.texts].map((item) => item.text).join(" "),
    /aprovado|verified|trusted/,
  );
});

test("a abertura nomeia a fantasia, o recorde e a última seed", () => {
  const state = createState(1, { entry: "title" });
  const first = paint(state, {}, { best: 0, canContinue: false });
  assert.ok(first.texts.some((item) => item.text.includes("Jogar")), "a primeira visita pede jogar");
  assert.equal(first.texts.some((item) => String(item.text).includes("Repetir")), false);
  const back = paint(
    state,
    {},
    {
      best: 18,
      canContinue: true,
      fantasy: "guardar a corrente ou continuar",
      lastRun: { score: 7 },
    },
  );
  assert.ok(back.texts.some((item) => item.text.includes("guardar a corrente ou continuar")));
  assert.ok(back.texts.some((item) => item.text.includes("Última") && item.text.includes("7")));
  assert.ok(back.texts.some((item) => item.text.includes("Recorde") && item.text.includes("18")));
  assert.ok(back.texts.some((item) => item.text.includes("Repetir a última")));
  assert.ok(back.texts.some((item) => item.text.includes("Nova partida")));
  assert.ok(hudBands(back) <= hudBands(paint(createState(1))), "a abertura não inventa faixa no HUD");
});

test("a porta também lê a legenda", () => {
  const state = createState(1, { entry: "title" });
  const captions = [{ text: "fim da partida", count: 1 }];
  const drawn = paint(state, {}, { captions, best: 0 });
  const line = drawn.texts.find((item) => String(item.text).includes("fim da partida"));
  assert.ok(line, "a porta precisa da legenda que o mixer ainda guarda");
  const plates = drawn.rects.filter((rect) => PLATE_COLORS.has(rect.style));
  assert.ok(covered(line, plates), "legenda na porta também cabe na placa");
  const muted = paint(state, { captions: false }, { captions, best: 0 });
  assert.equal(
    muted.texts.some((item) => String(item.text).includes("fim da partida")),
    false,
    "captions desligado some a linha",
  );
  assert.ok(hudBands(drawn) <= hudBands(paint(createState(1))), "a legenda da porta não é faixa no HUD");
  assert.ok(line.bottom < PLAYER_Y - 6, `legenda na porta desce até ${line.bottom}`);
});

test("o pulso da mostra vence a cortina sem inventar faixa", () => {
  const door = createState(1, { entry: "title" });
  door.flash = CONFIG.feel.flashGraze;
  const frame = paint(door);
  const curtain = frame.rects.findIndex(
    (rect) => rect.width === FIELD.width && rect.height === FIELD.height && rect.style === PALETTES.normal.plate,
  );
  assert.ok(curtain >= 0, "esperava a cortina da porta");
  const after = frame.rects.slice(curtain + 1).some((rect) => String(rect.style).startsWith("rgba(255"));
  assert.ok(after, "o pulso da mostra precisa nascer depois da cortina");
  assert.ok(hudBands(frame) <= hudBands(paint(createState(1, { entry: "title" }))), "o pulso da porta não é faixa no HUD");
  const still = paint(door, { reducedMotion: true });
  const rim = still.edges.findIndex((edge) => edge.style === PALETTES.normal.danger);
  assert.ok(rim >= 0, "com menos movimento o pulso vira contorno");
});

test("a abertura desenha o aviso sem inventar faixa", () => {
  const door = createState(1, { entry: "title" });
  const drawn = paint(door, {}, { hint: "move", best: 0 });
  const aviso = drawn.texts.filter((item) => item.text.includes("arraste") && item.text.includes("analógico"));
  assert.equal(aviso.length, 1, `esperava o aviso de mover na porta: ${JSON.stringify(drawn.texts.map((item) => item.text))}`);
  const plates = drawn.rects.filter((rect) => PLATE_COLORS.has(rect.style));
  assert.ok(covered(aviso[0], plates), "aviso na porta também cabe na placa");
  assert.ok(hudBands(drawn) <= hudBands(paint(door)), "o aviso da porta não é faixa no HUD");
  const quiet = paint(door, {}, { best: 0 });
  assert.equal(
    quiet.texts.some((item) => String(item.text).includes("arraste")),
    false,
    "sem pedido a porta não inventa o aviso",
  );
});

function railMarks(drawn, x) {
  const rail = PLAYER_Y + 10;
  return (drawn.strokes ?? []).filter((stroke) => (
    stroke.points.some((point) => Math.abs(point.y - rail) < 5)
    && (x === undefined || stroke.points.some((point) => Math.abs(point.x - x) < 4))
  ));
}

test("a porta marca a mostra no trilho sem inventar faixa", () => {
  const door = createState(1, { entry: "title" });
  const rain = attractEntities(door);
  const ahead = rain.filter((entity) => {
    const gap = PLAYER_Y - entity.y;
    return gap > CONFIG.collect.reachY && gap <= CONFIG.feel.telegraphReach;
  });
  assert.ok(ahead.length > 0, "esperava a mostra no alcance do telegraph");
  const drawn = paint(door);
  for (const drop of ahead) {
    assert.ok(
      railMarks(drawn, drop.x).length > 0,
      `a porta precisa marcar a mostra em ${drop.x}`,
    );
  }
  assert.ok(hudBands(drawn) <= hudBands(paint(createState(1))), "o aviso da porta não é faixa no HUD");
  const play = createState(1);
  play.entities = [{ id: 1, kind: "shard", x: 80, y: PLAYER_Y - 24, vy: 1 }];
  const field = paint(play);
  assert.ok(railMarks(field, 80).length > 0, "o campo continua marcando o trilho");
  const quiet = createState(1);
  quiet.entities = [{ id: 2, kind: "shard", x: 80, y: PLAYER_Y, vy: 1 }];
  assert.equal(railMarks(paint(quiet), 80).length, 0, "na faixa o aviso já é o próprio contato");
});

test("a abertura chove sem ser a partida", () => {
  const door = createState(1, { entry: "title" });
  const play = createState(1);
  const drawn = paint(door);
  const live = paint(play);
  assert.ok(drawn.arcs > live.arcs, "a porta precisa do orbe");
  assert.ok(drawn.lineTos > live.lineTos, "a porta precisa do estilhaço");
  assert.equal(door.entities.length, 0);
  assert.equal(door.tick, 0);
  assert.ok(hudBands(drawn) <= hudBands(live), "a chuva da porta não é faixa no HUD");
});

test("a porta chove a mesa sem fingir direção aprovada", () => {
  const spawn = paint(createState(1, { entry: "title" }));
  const dusk = paint(createState(1, { entry: "title", spawnProfile: "dusk" }));
  const calm = paint(createState(1, { entry: "title", spawnProfile: "calm" }));
  assert.ok(dusk.arcs > spawn.arcs, "dusk na porta pinta mais orbe");
  assert.ok(dusk.lineTos > spawn.lineTos, "dusk na porta pinta mais estilhaço");
  assert.ok(calm.lineTos < spawn.lineTos, "calm na porta pinta menos estilhaço");
  assert.ok(
    calm.arcs + calm.lineTos < spawn.arcs + spawn.lineTos,
    "calm na porta pinta menos chuva",
  );
  assert.ok(hudBands(dusk) <= hudBands(spawn), "mais chuva na porta não é faixa no HUD");
});

test("o corpo aponta para o lado do último avanço", () => {
  const left = createState(1);
  left.player.dir = -1;
  const right = createState(1);
  right.player.dir = 1;
  const a = playerBox(left);
  const b = playerBox(right);
  const noseL = playerNose(left);
  const noseR = playerNose(right);
  assert.ok(noseL.minX < a.x - 1, "a ponta esquerda sai do retângulo");
  assert.ok(noseR.maxX > b.x + b.width + 1, "a ponta direita sai do retângulo");
  playerNose(left, { reducedMotion: true });
  assert.equal(hudBands(paint(left)), hudBands(paint(right)), "a ponta não é faixa no HUD");
});

test("a guarda marca o campo sem inventar faixa no HUD", () => {
  const state = createState(2);
  state.chain = 3;
  advance(state, { move: 0, dash: false, bank: true });
  for (let step = 0; step < CONFIG.bank.windupTicks; step += 1) {
    advance(state, { move: 0, dash: false, bank: false });
  }
  const drawn = paint(state);
  const edges = drawn.edges.filter((edge) => edge.style === PALETTES.normal.chain);
  assert.ok(edges.length >= 1, "a guarda precisa contornar o campo");
  assert.ok(edges.some((edge) => edge.width > FIELD.width * 0.8 && edge.height > FIELD.height * 0.8));
  const timerStrips = drawn.rects.filter((rect) => (
    rect.height === 2
    && rect.y < 20
    && !PLATE_COLORS.has(rect.style)
  ));
  assert.equal(timerStrips.length, 0, "a guarda não é faixa no HUD");
  const still = paint(state, { reducedMotion: true });
  assert.ok(
    still.edges.some((edge) => edge.style === PALETTES.normal.chain && edge.x === 6 && edge.y === 6),
    "com menos movimento a guarda vira traço, não some",
  );
  state.tick = state.recoverUntil;
  const gone = paint(state);
  assert.equal(
    gone.edges.filter((edge) => edge.style === PALETTES.normal.chain && edge.width > FIELD.width * 0.8).length,
    0,
    "depois da folga o campo não inventa contorno",
  );
});

test("a antecipação de guardar contorna o corpo sem inventar faixa no HUD", () => {
  const state = createState(2);
  state.chain = 3;
  const idle = paint(state);
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.bankWindup, CONFIG.bank.windupTicks);
  const drawn = paint(state);
  assert.ok(drawn.arcs > idle.arcs, "sentar precisa marcar o corpo");
  assert.equal(hudBands(drawn), 0, "a antecipação não é faixa no HUD");
});

test("a prática marca o campo sem inventar faixa no HUD", () => {
  const start = createState(2);
  const early = paint(start);
  const edges = early.edges.filter((edge) => edge.style === PALETTES.normal.orb);
  assert.ok(edges.length >= 1, "a prática precisa contornar o campo");
  assert.ok(edges.some((edge) => edge.width > FIELD.width * 0.8 && edge.height > FIELD.height * 0.8));
  const timerStrips = early.rects.filter((rect) => (
    rect.height === 2
    && rect.y < 20
    && !PLATE_COLORS.has(rect.style)
  ));
  assert.equal(timerStrips.length, 0, "a prática não é faixa no HUD");
  const still = paint(start, { reducedMotion: true });
  assert.ok(
    still.edges.some((edge) => edge.style === PALETTES.normal.orb && edge.x === 4 && edge.y === 4),
    "com menos movimento a prática vira traço, não some",
  );
  const after = createState(2);
  after.tick = after.spawn.practiceTicks;
  const gone = paint(after);
  assert.equal(
    gone.edges.filter((edge) => edge.style === PALETTES.normal.orb && edge.width > FIELD.width * 0.8).length,
    0,
    "depois da prática o campo não inventa contorno",
  );
});

test("o fecho marca o campo sem inventar faixa no HUD", () => {
  const early = paint(createState(2));
  assert.equal(
    early.edges.filter((edge) => edge.style === PALETTES.normal.danger).length,
    0,
    "antes do fecho o campo não inventa contorno",
  );
  const late = createState(2);
  late.tick = CONFIG.runTicks - 90;
  const drawn = paint(late);
  const edges = drawn.edges.filter((edge) => edge.style === PALETTES.normal.danger);
  assert.ok(edges.length >= 1, "o fecho precisa contornar o campo");
  assert.ok(edges.some((edge) => edge.width > FIELD.width * 0.8 && edge.height > FIELD.height * 0.8));
  const timerStrips = drawn.rects.filter((rect) => (
    rect.height === 2
    && rect.y < 20
    && !PLATE_COLORS.has(rect.style)
  ));
  assert.equal(timerStrips.length, 0, "o fecho não é faixa no HUD");
  const still = paint(late, { reducedMotion: true });
  assert.ok(
    still.edges.some((edge) => edge.style === PALETTES.normal.danger && edge.x === 2 && edge.y === 2),
    "com menos movimento o fecho vira traço, não some",
  );
});

test("o flash do erro some com redução de movimento", () => {
  const state = createState(2);
  state.flash = CONFIG.feel.flashHit;
  const lit = paint(state).rects.some((rect) => String(rect.style).startsWith("rgba(255"));
  const still = paint(state, { reducedMotion: true }).edges.some(
    (edge) => edge.style === PALETTES.normal.danger,
  );
  assert.equal(lit, true, "o erro precisa acender o campo");
  assert.equal(still, true, "com menos movimento o sinal vira contorno, não some");
});

test("a queda da corrente pinta a aposta que não foi guardada", () => {
  const state = createState(1);
  state.phase = "over";
  state.motes = [
    { kind: "lapse", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 1.8, life: 8 },
    { kind: "lapse", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 1.8, life: 8 },
  ];
  const flying = paint(state);
  const pips = flying.rects.filter(
    (rect) => rect.style === PALETTES.normal.chain && Math.abs(rect.width - CONFIG.feel.chainPipSize) < 0.01,
  );
  assert.ok(pips.length >= 2, `esperava a queda na tinta da corrente: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.style]))}`);
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.style === PALETTES.normal.chain && rect.width === 2);
  assert.ok(marks.length >= 2, "com menos movimento a queda vira marca, não some");
});

test("o overlay do fim nomeia a corrente que caiu e a queda vence a cortina", () => {
  const lost = createState(1);
  lost.phase = "over";
  lost.score = 12;
  lost.chain = 5;
  lost.stats.bestChain = 8;
  lost.motes = [
    { kind: "lapse", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 1.8, life: 8 },
    { kind: "lapse", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 1.8, life: 8 },
  ];
  const frame = paint(lost);
  const texts = frame.texts.map((item) => item.text);
  assert.ok(texts.some((text) => text === "Fim — 12"), `título: ${JSON.stringify(texts)}`);
  assert.ok(
    texts.some((text) => text.includes("Corrente 5") && text.includes("Maior corrente: 8") && text.includes("abertura")),
    `esperava a aposta nomeada no overlay: ${JSON.stringify(texts)}`,
  );

  const curtain = frame.rects.findIndex(
    (rect) => rect.width === FIELD.width && rect.height === FIELD.height && rect.style === PALETTES.normal.plate,
  );
  assert.ok(curtain >= 0, "esperava a cortina do fim");
  const after = frame.rects.slice(curtain + 1).filter(
    (rect) => rect.style === PALETTES.normal.chain && Math.abs(rect.width - CONFIG.feel.chainPipSize) < 0.01,
  );
  assert.ok(after.length >= 2, `a queda precisa nascer depois da cortina: ${JSON.stringify(frame.rects.slice(curtain).map((rect) => [rect.width, rect.style]))}`);

  const empty = createState(1);
  empty.phase = "over";
  const idle = paint(empty).texts.map((item) => item.text);
  assert.equal(
    idle.some((text) => text.includes("Corrente") && text.includes("abertura")),
    false,
    `sem aposta o overlay não inventa o rótulo: ${JSON.stringify(idle)}`,
  );
});

test("no fim a pausa não come a aposta que o overlay já nomeava", () => {
  const ended = createState(1);
  ended.phase = "over";
  ended.score = 12;
  ended.chain = 5;
  const held = { paused: true, alpha: 0, steps: 1 };
  const texts = hudTexts(ended, {}, { best: 40 }, held).texts.map((item) => item.text);
  assert.ok(texts.some((text) => text === "Fim — 12"), `título: ${JSON.stringify(texts)}`);
  assert.equal(
    texts.some((text) => text === "Pausado — 12"),
    false,
    `a pausa não come o fim: ${JSON.stringify(texts)}`,
  );
  const hint = texts.find((text) => text.includes("Corrente 5") && text.includes("Recorde 40") && /abertura/i.test(text));
  assert.ok(hint, `esperava a aposta no overlay: ${JSON.stringify(texts)}`);
  const playing = createState(1);
  playing.score = 12;
  const paused = hudTexts(playing, {}, { best: 40 }, held).texts.map((item) => item.text);
  assert.ok(paused.some((text) => text === "Pausado — 12"), "no campo a pausa continua");
});

test("o overlay da pausa nomeia o placar sem inventar faixa nem sessão", () => {
  const state = createState(1);
  state.score = 12;
  const held = { paused: true, alpha: 0, steps: 1 };
  const withBest = hudTexts(state, {}, { best: 40 }, held).texts.map((item) => item.text);
  assert.ok(withBest.some((text) => text === "Pausado — 12"), `título: ${JSON.stringify(withBest)}`);
  const hint = withBest.find((text) => text.includes("Recorde 40") && /continuar/i.test(text));
  assert.ok(hint, `esperava o recorde na pausa: ${JSON.stringify(withBest)}`);
  const empty = hudTexts(state, {}, { best: 0 }, held).texts.map((item) => item.text);
  assert.ok(empty.some((text) => text === "Pausado — 12"), `sem recorde o placar fica: ${JSON.stringify(empty)}`);
  const resume = empty.find((text) => /continuar/i.test(text));
  assert.ok(resume, `esperava o retomar: ${JSON.stringify(empty)}`);
  assert.equal(/recorde/i.test(resume), false, `recorde 0 some do overlay: ${resume}`);
  const live = hudTexts(state, {}, { best: 40 }).texts.map((item) => item.text);
  assert.equal(
    live.some((text) => text === "Pausado — 12"),
    false,
    "sem pausa o overlay não inventa a placa",
  );
});

test("o overlay do fim nomeia o recorde sem inventar faixa nem sessão", () => {
  const ended = createState(1);
  ended.phase = "over";
  ended.score = 12;
  const withBest = paint(ended, {}, { best: 40 }).texts.map((item) => item.text);
  const hint = withBest.find((text) => text.includes("Recorde 40") && text.includes("abertura"));
  assert.ok(hint, `esperava o recorde no overlay: ${JSON.stringify(withBest)}`);
  assert.equal(hint.includes("Corrente"), false, "sem aposta o recorde não inventa corrente");

  const empty = paint(ended, {}, { best: 0 }).texts.map((item) => item.text);
  const door = empty.find((text) => /abertura/i.test(text));
  assert.ok(door, `esperava a porta no overlay: ${JSON.stringify(empty)}`);
  assert.equal(door.includes("Recorde"), false, "recorde zero não entra no overlay");
});

test("a cortina segue o look, a legenda vence e o texto respeita a escala", () => {
  const ended = createState(1);
  ended.phase = "over";
  ended.score = 3;
  const captions = [{ text: "fim da partida", count: 1 }];
  const dusk = paint(ended, { look: "dusk" }, { captions, best: 0 });
  assert.equal(
    dusk.rects.some((rect) => rect.width === FIELD.width && rect.height === FIELD.height && rect.style === PALETTES.dusk.plate),
    true,
    "dusk não herda o preto frio da cortina",
  );
  assert.equal(
    dusk.rects.some((rect) => rect.width === FIELD.width && rect.height === FIELD.height && String(rect.style) === "rgba(0,0,0,0.62)"),
    false,
    `cortina fria no look quente: ${JSON.stringify(dusk.rects.filter((rect) => rect.width === FIELD.width).map((rect) => rect.style))}`,
  );

  const curtain = dusk.rects.findIndex(
    (rect) => rect.width === FIELD.width && rect.height === FIELD.height && rect.style === PALETTES.dusk.plate,
  );
  assert.ok(curtain >= 0, "esperava a cortina do look");
  const caption = dusk.texts.find((item) => item.text === "fim da partida");
  assert.ok(caption, `esperava a legenda no fim: ${JSON.stringify(dusk.texts.map((item) => item.text))}`);
  const platesAfter = dusk.rects.slice(curtain + 1).filter((rect) => rect.style === PALETTES.dusk.plate && rect.width < 200);
  assert.ok(platesAfter.length >= 1, "a faixa da legenda precisa nascer depois da cortina");

  const titleSize = (frame) => {
    const title = frame.texts.find((item) => item.text.startsWith("Fim"));
    assert.ok(title, `esperava o título do fim: ${JSON.stringify(frame.texts.map((item) => item.text))}`);
    return title.bottom - title.top;
  };
  const compact = titleSize(paint(ended));
  const large = titleSize(paint(ended, { uiScale: 1.6 }));
  assert.ok(large > compact, `uiScale precisa crescer o overlay: ${compact} → ${large}`);
});

test("a entrada da corrente pinta o orbe a caminho da órbita", () => {
  const state = createState(1);
  state.motes = [
    { kind: "join", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 0, life: 8 },
    { kind: "join", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 0, life: 8 },
  ];
  const flying = paint(state);
  const pips = flying.rects.filter(
    (rect) => rect.style === PALETTES.normal.orb && Math.abs(rect.width - CONFIG.feel.chainPipSize) < 0.01,
  );
  assert.ok(pips.length >= 2, `esperava os pips nascendo na tinta do orbe: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.style]))}`);
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.style === PALETTES.normal.orb && rect.width === 2);
  assert.ok(marks.length >= 2, "com menos movimento a entrada vira marca, não some");
});

test("o orbe perdido pinta a queda sem inventar faixa no HUD", () => {
  const state = createState(1);
  state.motes = [
    { kind: "missed", x: 40, y: FIELD.height - 3, sx: 40, sy: FIELD.height - 3, vx: 0, vy: 0.25, life: 8 },
    { kind: "missed", x: 90, y: FIELD.height - 3, sx: 90, sy: FIELD.height - 3, vx: 0, vy: 0.25, life: 8 },
  ];
  const flying = paint(state);
  const stains = flying.rects.filter(
    (rect) => rect.style === PALETTES.normal.orb && Math.abs(rect.width - 4.8) < 0.01 && rect.y > PLAYER_Y,
  );
  assert.ok(stains.length >= 2, `esperava a queda na tinta do orbe: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.y, rect.style]))}`);
  const timerStrips = flying.rects.filter((rect) => (
    rect.height === 2
    && rect.y < 20
    && !PLATE_COLORS.has(rect.style)
  ));
  assert.equal(timerStrips.length, 0, "a queda não é faixa no HUD");
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.style === PALETTES.normal.orb && rect.width === 2 && rect.y > PLAYER_Y);
  assert.ok(marks.length >= 2, "com menos movimento a queda vira marca, não some");
});

test("o raspo pinta o estilhaço que passou", () => {
  const state = createState(1);
  state.motes = [
    { kind: "graze", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 0, life: 8 },
    { kind: "graze", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 0, life: 8 },
  ];
  const flying = paint(state);
  const sparks = flying.rects.filter((rect) => rect.style === PALETTES.normal.danger && rect.width < 5);
  assert.ok(sparks.length >= 2, `esperava o raspo na tinta do perigo: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.style]))}`);
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.style === PALETTES.normal.danger && rect.width === 2);
  assert.ok(marks.length >= 2, "com menos movimento o raspo vira marca, não some");
});

test("o depósito da corrente pinta os pips a caminho do placar", () => {
  const state = createState(1);
  state.motes = [
    { kind: "deposit", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 0, life: 8 },
    { kind: "deposit", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 0, life: 8 },
  ];
  const flying = paint(state);
  const pips = flying.rects.filter(
    (rect) => rect.style === PALETTES.normal.chain && Math.abs(rect.width - CONFIG.feel.chainPipSize) < 0.01,
  );
  assert.ok(pips.length >= 2, `esperava os pips depositados na tinta da corrente: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.style]))}`);
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.style === PALETTES.normal.chain && rect.width === 2);
  assert.ok(marks.length >= 2, "com menos movimento o depósito vira marca, não some");
});

test("a quebra da corrente pinta os pips que o corpo perdeu", () => {
  const state = createState(1);
  state.motes = [
    { kind: "break", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 0, life: 8 },
    { kind: "break", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 0, life: 8 },
  ];
  const flying = paint(state);
  const shards = flying.rects.filter((rect) => rect.style === PALETTES.normal.chain && rect.width < 5);
  assert.ok(shards.length >= 2, `esperava os pips quebrados na tinta da corrente: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.style]))}`);
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.style === PALETTES.normal.chain && rect.width === 2);
  assert.ok(marks.length >= 2, "com menos movimento a quebra vira marca, não some");
});

test("o rastro do impacto aparece e com menos movimento vira marca", () => {
  const state = createState(5);
  state.motes = [
    { kind: "collect", x: 40, y: 80, sx: 40, sy: 80, vx: 0, vy: 0, life: 8 },
    { kind: "hit", x: 90, y: 80, sx: 90, sy: 80, vx: 0, vy: 0, life: 8 },
  ];
  const flying = paint(state);
  const sparks = flying.rects.filter((rect) => rect.width < 5 && rect.height < 5);
  assert.ok(sparks.length >= 2, `esperava o rastro no campo: ${JSON.stringify(flying.rects.map((rect) => [rect.width, rect.style]))}`);
  const still = paint(state, { reducedMotion: true });
  const marks = still.rects.filter((rect) => rect.width === 2 && rect.height === 2);
  assert.ok(marks.length >= 2, "com menos movimento o rastro vira marca, não some");
});

test("o aviso do primeiro ciclo cabe na placa e some depois de guardar", () => {
  const inicial = hudTexts(createState(1), {}, { hint: "move" });
  const aviso = inicial.texts.filter((item) => item.text.includes("arraste") && item.text.includes("analógico"));
  assert.equal(aviso.length, 1, `esperava o aviso de mover nas três superfícies: ${JSON.stringify(inicial.texts.map((i) => i.text))}`);
  assert.ok(covered(aviso[0], inicial.plates), "aviso sem placa é texto solto no campo");
  assert.ok(aviso[0].bottom < PLAYER_Y - 6, `aviso desce até a faixa do jogador: ${aviso[0].bottom}`);
  const seeded = hudTexts(createState(1), {}, { hint: "fantasy", fantasy: "guardar a corrente ou continuar" });
  const frase = seeded.texts.filter((item) => item.text.includes("guardar a corrente"));
  assert.equal(frase.length, 1, `esperava a fantasia na tela: ${JSON.stringify(seeded.texts.map((i) => i.text))}`);
  assert.ok(covered(frase[0], seeded.plates), "fantasia sem placa é texto solto no campo");
  const depois = hudTexts(createState(1), {}, { hint: null });
  assert.equal(
    depois.texts.filter((item) => /Mova|orbe|Guarde|Atravesse|arraste já|analógico já/.test(item.text)).length,
    0,
    "depois de guardar o ensino não pode continuar na tela",
  );
});

test("o aviso do dash e da superfície nomeia o mapa sem apagar as outras", () => {
  const state = createState(1);
  const dash = hudTexts(state, {}, { hint: "dash" });
  assert.equal(
    dash.texts.filter((item) => item.text.includes("Espaço") && item.text.includes("cima") && item.text.includes("A")).length,
    1,
    `esperava Espaço, toque e controle no dash: ${JSON.stringify(dash.texts.map((item) => item.text))}`,
  );
  const toque = hudTexts(state, {}, { hint: "touch" });
  assert.equal(
    toque.texts.filter((item) => item.text.includes("arraste já move")).length,
    1,
    `esperava o passo do toque: ${JSON.stringify(toque.texts.map((item) => item.text))}`,
  );
  const pad = hudTexts(state, {}, { hint: "pad" });
  assert.equal(
    pad.texts.filter((item) => item.text.includes("analógico já move")).length,
    1,
    `esperava o passo do controle: ${JSON.stringify(pad.texts.map((item) => item.text))}`,
  );
});

test("o aviso e o overlay nomeiam as teclas do remapeamento", () => {
  const state = createState(1);
  state.chain = 3;
  const padrao = hudTexts(state, {}, { hint: "bank" });
  assert.equal(
    padrao.texts.filter((item) => item.text.includes("Guarde (↓, baixo ou X)")).length,
    1,
    `esperava ↓, toque e controle no padrão: ${JSON.stringify(padrao.texts.map((item) => item.text))}`,
  );
  const uma = hudTexts(state, { bindings: ONE_HAND_BINDINGS }, { hint: "bank" });
  assert.equal(
    uma.texts.filter((item) => item.text.includes("Guarde (K, baixo ou X)")).length,
    1,
    `esperava K, toque e controle no preset: ${JSON.stringify(uma.texts.map((item) => item.text))}`,
  );
  assert.equal(uma.texts.filter((item) => item.text.includes("Guarde (↓")).length, 0);

  const recorder = recordingCanvas();
  const renderer = createRenderer(recorder.canvas, { devicePixelRatio: 1 });
  renderer.resize(360, 640);
  renderer.draw(state, { paused: true }, { bindings: ONE_HAND_BINDINGS }, {});
  const overlay = recorder.calls.texts.map((item) => item.text);
  assert.ok(overlay.some((text) => text.includes("Continuar: P")), `overlay: ${JSON.stringify(overlay)}`);
  assert.equal(overlay.some((text) => text.includes("Esc")), false);
});

test("o aviso ensina as três superfícies e o overlay confirma o controle", () => {
  const state = createState(1);
  state.chain = 3;
  const aviso = hudTexts(state, {}, { hint: "bank", surface: "gamepad" });
  assert.equal(
    aviso.texts.filter((item) => item.text.includes("Guarde (↓, baixo ou X)")).length,
    1,
    `esperava teclado, toque e controle no aviso: ${JSON.stringify(aviso.texts.map((item) => item.text))}`,
  );

  const recorder = recordingCanvas();
  const renderer = createRenderer(recorder.canvas, { devicePixelRatio: 1 });
  renderer.resize(360, 640);
  renderer.draw(state, { paused: true }, {}, { surface: "gamepad" });
  const overlay = recorder.calls.texts.map((item) => item.text);
  assert.ok(overlay.some((text) => text.includes("Continuar: Start")), `overlay: ${JSON.stringify(overlay)}`);
  assert.equal(overlay.some((text) => text.includes("Esc")), false);

  const over = createState(1);
  over.phase = "over";
  renderer.draw(over, {}, {}, { surface: "gamepad" });
  const fim = recorder.calls.texts.map((item) => item.text);
  assert.ok(fim.some((text) => text.includes("Abertura: A")), `fim: ${JSON.stringify(fim)}`);
  assert.equal(fim.some((text) => text.includes("Select")), false, "o overlay do fim nomeia o avanço");
});

test("a recarga do dash enche a faixa sem aprovar o feel", () => {
  const ready = dashCharge(createState(1));
  assert.equal(ready.phase, "ready");
  assert.equal(ready.fill, 1);
  const recovery = createState(1);
  recovery.player.dashRecovery = CONFIG.player.dashRecoveryTicks;
  const start = dashCharge(recovery);
  assert.equal(start.phase, "recovery");
  assert.equal(start.fill, 0);
  recovery.player.dashRecovery = 1;
  assert.ok(dashCharge(recovery).fill > start.fill, "recuperação enche");
  const cool = createState(1);
  cool.player.dashCooldown = CONFIG.player.dashCooldownTicks;
  const waiting = dashCharge(cool);
  assert.equal(waiting.phase, "cooldown");
  assert.ok(waiting.fill > 0 && waiting.fill < 1);
  cool.player.dashCooldown = 1;
  assert.ok(dashCharge(cool).fill > waiting.fill, "cooldown enche");
  const lock = createState(1);
  lock.bankLock = 4;
  assert.equal(dashCharge(lock).phase, "lock");
  assert.equal(dashCharge(lock).fill, 0);
  const dash = createState(1);
  dash.player.dashTicks = 3;
  assert.equal(dashCharge(dash).phase, "dash");
  assert.equal(dashCharge(dash).fill, 1);
  const coil = createState(1);
  coil.player.dashWindup = CONFIG.player.dashWindupTicks;
  const winding = dashCharge(coil);
  assert.equal(winding.phase, "windup");
  assert.ok(winding.fill < 1);
  coil.player.dashWindup = 1;
  assert.ok(dashCharge(coil).fill > winding.fill, "a antecipação enche");
});

test("a faixa do dash veste o look e não a placa", () => {
  const state = longState();
  const charge = dashCharge(state);
  const recorder = recordingCanvas();
  const renderer = createRenderer(recorder.canvas, { devicePixelRatio: 1 });
  renderer.resize(360, 640);
  renderer.draw(state, { paused: false, alpha: 0, steps: 1 }, {}, { best: 0 });
  const dashPlate = recorder.plates().find((plate) => plate.y > 80);
  assert.ok(dashPlate, "placa do dash");
  const strips = recorder.calls.rects.filter((rect) => (
    !PLATE_COLORS.has(rect.style)
    && Math.abs(rect.x - dashPlate.x) < 0.6
    && Math.abs(rect.y + rect.height - (dashPlate.y + dashPlate.height)) < 0.6
  ));
  assert.equal(strips.length, 1, "uma faixa na base da placa");
  assert.ok(Math.abs(strips[0].width - dashPlate.width * charge.fill) < 0.6);
  assert.equal(strips[0].style, PALETTES.normal.muted);
  const dusk = recordingCanvas();
  const duskRenderer = createRenderer(dusk.canvas, { devicePixelRatio: 1 });
  duskRenderer.resize(360, 640);
  duskRenderer.draw(state, { paused: false, alpha: 0, steps: 1 }, { look: "dusk" }, { best: 0 });
  const duskPlate = dusk.plates().find((plate) => plate.y > 80);
  const duskStrip = dusk.calls.rects.find((rect) => (
    !PLATE_COLORS.has(rect.style)
    && duskPlate
    && Math.abs(rect.x - duskPlate.x) < 0.6
    && Math.abs(rect.y + rect.height - (duskPlate.y + duskPlate.height)) < 0.6
  ));
  assert.equal(duskStrip.style, PALETTES.dusk.muted);
  assert.notEqual(duskStrip.style, PALETTES.normal.muted);
  const soft = recordingCanvas();
  const softRenderer = createRenderer(soft.canvas, { devicePixelRatio: 1 });
  softRenderer.resize(360, 640);
  softRenderer.draw(state, { paused: false, alpha: 0, steps: 1 }, { look: "calm" }, { best: 0 });
  const softPlate = soft.plates().find((plate) => plate.y > 80);
  const softStrip = soft.calls.rects.find((rect) => (
    !PLATE_COLORS.has(rect.style)
    && softPlate
    && Math.abs(rect.x - softPlate.x) < 0.6
    && Math.abs(rect.y + rect.height - (softPlate.y + softPlate.height)) < 0.6
  ));
  assert.equal(softStrip.style, PALETTES.calm.muted);
  assert.notEqual(softStrip.style, PALETTES.dusk.muted);
});
