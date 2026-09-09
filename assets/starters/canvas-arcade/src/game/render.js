// Apresentação. Não decide regra e não altera o estado.
//
// Legibilidade antes de estilo: orbe e estilhaço têm **formas** diferentes, não
// só cores diferentes, então o jogo continua jogável em escala de cinza e para
// quem não distingue as duas cores. Tremor e piscada respeitam redução de
// movimento — o sinal de causa migra para uma forma estática, não desaparece.

import { FIELD, PLAYER_Y, CONFIG, remainingTicks, TICK_HZ } from "./rules.js";
import { copy } from "./tables.js";

// Exportadas para terem consumidor além do desenho: é assim que um teste
// distingue a placa do HUD do preenchimento do campo, e é o gancho para o
// design system do jogo quando ele passar de moodboard a token.
export const PALETTES = {
  normal: {
    background: "#10131a",
    field: "#171b26",
    player: "#f2f4f8",
    orb: "#4ea8ff",
    shard: "#ff8a3d",
    chain: "#ffd166",
    text: "#e7ebf3",
    muted: "#8a93a6",
    danger: "#ff5d5d",
    plate: "rgba(7,9,13,0.86)",
    plateEdge: "rgba(231,235,243,0.22)",
  },
  contrast: {
    background: "#000000",
    field: "#000000",
    player: "#ffffff",
    orb: "#00d2ff",
    shard: "#ff6a00",
    chain: "#ffe600",
    text: "#ffffff",
    muted: "#c9c9c9",
    danger: "#ff2b2b",
    // Campo preto e placa preta: aqui o preenchimento não tem como separar nada,
    // e quem separa é a borda. Ela é branca e opaca porque em alto contraste
    // separar é o objetivo, não a discrição.
    plate: "rgba(0,0,0,0.9)",
    plateEdge: "#ffffff",
  },
};

export function createRenderer(canvas, options = {}) {
  const context = canvas.getContext("2d", { alpha: false });
  let scale = 1;
  let offsetX = 0;
  let offsetY = 0;
  const devicePixels = options.devicePixelRatio ?? (typeof devicePixelRatio === "number" ? devicePixelRatio : 1);

  function resize(width, height) {
    const ratio = Math.min(Math.max(1, devicePixels), 3);
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    scale = Math.max(1, Math.min(canvas.width / FIELD.width, canvas.height / FIELD.height));
    offsetX = (canvas.width - FIELD.width * scale) / 2;
    offsetY = (canvas.height - FIELD.height * scale) / 2;
  }

  function draw(state, frame = {}, settings = {}, extra = {}) {
    const palette = settings.highContrast ? PALETTES.contrast : PALETTES.normal;
    const reduced = Boolean(settings.reducedMotion);
    context.setTransform(1, 0, 0, 1, 0, 0);
    context.fillStyle = palette.background;
    context.fillRect(0, 0, canvas.width, canvas.height);

    const shake = reduced ? 0 : state.shake;
    const jitterX = shake ? (Math.sin(state.tick * 12.9898) * shake * 3) : 0;
    const jitterY = shake ? (Math.cos(state.tick * 7.233) * shake * 3) : 0;
    context.setTransform(scale, 0, 0, scale, offsetX + jitterX * scale, offsetY + jitterY * scale);

    context.fillStyle = palette.field;
    context.fillRect(0, 0, FIELD.width, FIELD.height);
    context.strokeStyle = palette.muted;
    context.lineWidth = 0.5;
    context.beginPath();
    context.moveTo(0, PLAYER_Y + 10);
    context.lineTo(FIELD.width, PLAYER_Y + 10);
    context.stroke();

    for (const entity of state.entities) {
      if (entity.kind === "orb") drawOrb(context, palette, entity);
      else drawShard(context, palette, entity);
    }
    drawPlayer(context, palette, state, reduced);
    const reserved = drawHud(context, palette, state, settings, extra);
    if (settings.captions !== false) {
      drawCaptions(context, palette, extra.captions ?? [], reserved, settings);
    }
    if (frame.paused) drawOverlay(context, palette, copy.paused, copy.resume);
    else if (state.phase === "over") {
      drawOverlay(
        context,
        palette,
        `${copy.over} — ${state.score}`,
        state.stats.bestChain
          ? `${copy.best_chain}: ${state.stats.bestChain} · ${copy.restart_inline}`
          : copy.restart,
      );
    }
  }

  function drawOrb(target, palette, entity) {
    target.fillStyle = palette.orb;
    target.beginPath();
    target.arc(entity.x, entity.y, 4, 0, Math.PI * 2);
    target.fill();
    target.strokeStyle = palette.text;
    target.lineWidth = 0.7;
    target.beginPath();
    target.arc(entity.x, entity.y, 6, 0, Math.PI * 2);
    target.stroke();
  }

  function drawShard(target, palette, entity) {
    target.fillStyle = palette.shard;
    target.beginPath();
    target.moveTo(entity.x, entity.y - 6);
    target.lineTo(entity.x + 5.5, entity.y + 5);
    target.lineTo(entity.x - 5.5, entity.y + 5);
    target.closePath();
    target.fill();
    target.strokeStyle = palette.background;
    target.lineWidth = 0.8;
    target.stroke();
  }

  function drawPlayer(target, palette, state, reduced) {
    const player = state.player;
    const squash = 1 + player.squash;
    const width = CONFIG.player.halfWidth * 2 * squash;
    const height = 12 / squash;
    const dashing = player.dashTicks > 0;
    target.fillStyle = dashing ? palette.chain : palette.player;
    target.fillRect(player.x - width / 2, PLAYER_Y - height / 2, width, height);
    if (player.invuln > 0) {
      // Com redução de movimento, contorno constante em vez de piscar.
      const visible = reduced || Math.floor(player.invuln / 4) % 2 === 0;
      if (visible) {
        target.strokeStyle = palette.danger;
        target.lineWidth = 1;
        target.strokeRect(player.x - width / 2 - 2, PLAYER_Y - height / 2 - 2, width + 4, height + 4);
      }
    }
    if (state.bankLock > 0) {
      target.strokeStyle = palette.chain;
      target.lineWidth = 1;
      target.beginPath();
      target.arc(player.x, PLAYER_Y, 11, 0, (Math.PI * 2 * state.bankLock) / CONFIG.bank.lockTicks);
      target.stroke();
    }
  }

  // Texto do HUD sobre o campo fica ilegível quando um orbe passa atrás dele:
  // ordem de desenho garante que o texto vença os pixels, não que ele seja
  // lido. A placa devolve o contraste sem escurecer a cena inteira.
  //
  // O preenchimento sozinho não bastava. Sobre o campo ele resolve em #0a0c10
  // contra #171b26 — diferença real, imperceptível em vídeo comprimido — e em
  // alto contraste, onde o campo é preto, a placa preta é invisível por
  // definição. Dois revisores independentes descreveram o efeito (o orbe
  // desaparece atrás do texto) negando a placa. Placa que não se vê não
  // tranquiliza ninguém sobre onde termina a interface, então ela ganhou borda:
  // a borda é o que separa a superfície do campo em qualquer compressão, e é o
  // único traço que funciona quando preenchimento e fundo são a mesma cor.
  function plate(target, palette, x, y, width, height) {
    const box = { x: x - 3, y: y - 2.5, width: width + 6, height: height + 5 };
    target.fillStyle = palette.plate;
    target.strokeStyle = palette.plateEdge;
    target.lineWidth = 1;
    // Meio pixel alinha o traço à grade e evita que ele saia com 2px esmaecidos.
    const edge = { x: box.x + 0.5, y: box.y + 0.5, width: box.width - 1, height: box.height - 1 };
    if (typeof target.roundRect !== "function") {
      target.fillRect(box.x, box.y, box.width, box.height);
      target.strokeRect(edge.x, edge.y, edge.width, edge.height);
      return box;
    }
    target.beginPath();
    target.roundRect(box.x, box.y, box.width, box.height, 3);
    target.fill();
    target.beginPath();
    target.roundRect(edge.x, edge.y, edge.width, edge.height, 2.5);
    target.stroke();
    return box;
  }

  // Devolve os retângulos que reservou. É deles que a faixa de legenda tira a
  // sua posição, em vez de repetir os números do HUD e sair de sincronia na
  // primeira vez que alguém mexer na escala da interface.
  function drawHud(target, palette, state, settings, extra) {
    const size = 8 * (settings.uiScale ?? 1);
    target.font = `${size}px system-ui, sans-serif`;
    target.textBaseline = "top";
    const second = 5 + size + 2;
    // A seta existe para mostrar o que guardar vale. Com corrente 1 ela dizia
    // "1 → 1", que não é erro de conta — é ruído, e um revisor leu como bug.
    // Ela aparece quando guardar rende mais do que a corrente já vale.
    const payoff = state.chain * state.chain;
    const chain = `${copy.chain} ${state.chain}${payoff > state.chain ? ` → ${payoff}` : ""}`;
    const score = `${copy.score} ${state.score}`;
    const seconds = Math.ceil(remainingTicks(state) / TICK_HZ);
    const best = extra.best === undefined ? null : `${copy.record} ${extra.best}`;
    const width = (text) => target.measureText(text).width;

    target.textAlign = "left";
    const scoreBox = plate(target, palette, 6, 5, Math.max(width(score), width(chain)), second + size - 5);
    target.fillStyle = palette.text;
    target.fillText(score, 6, 5);
    target.fillStyle = state.chain > 0 ? palette.chain : palette.muted;
    target.fillText(chain, 6, second);

    const rightWidth = Math.max(width(`${seconds}s`), best ? width(best) : 0);
    const timerBox = plate(target, palette, FIELD.width - 6 - rightWidth, 5, rightWidth, best ? second + size - 5 : size);
    target.textAlign = "right";
    target.fillStyle = seconds <= 10 ? palette.danger : palette.muted;
    target.fillText(`${seconds}s`, FIELD.width - 6, 5);
    if (best) {
      target.fillStyle = palette.muted;
      target.fillText(best, FIELD.width - 6, second);
    }

    target.textAlign = "left";
    const ready = state.player.dashCooldown === 0 && state.player.dashRecovery === 0 && state.bankLock === 0;
    const dash = ready ? copy.dash_ready : copy.dash_recharging;
    const dashBox = plate(target, palette, 6, FIELD.height - size - 5, width(dash), size);
    target.fillStyle = ready ? palette.orb : palette.muted;
    target.fillText(dash, 6, FIELD.height - size - 5);
    return { score: scoreBox, timer: timerBox, dash: dashBox };
  }

  function drawOverlay(target, palette, title, hint) {
    target.fillStyle = "rgba(0,0,0,0.62)";
    target.fillRect(0, 0, FIELD.width, FIELD.height);
    target.textAlign = "center";
    target.fillStyle = palette.text;
    target.font = "16px system-ui, sans-serif";
    target.fillText(title, FIELD.width / 2, FIELD.height / 2 - 14);
    target.font = "8px system-ui, sans-serif";
    target.fillStyle = palette.muted;
    target.fillText(hint, FIELD.width / 2, FIELD.height / 2 + 8);
    target.textAlign = "left";
  }

  // A legenda tem faixa própria, encostada à direita e logo abaixo do relógio.
  // No centro inferior ela caía exatamente sobre o jogador e sobre o rótulo do
  // dash: com o áudio desligado a informação existia e não era lida.
  function drawCaptions(target, palette, captions, reserved, settings) {
    if (!captions.length) return;
    const size = 7 * (settings.uiScale ?? 1);
    target.font = `${size}px system-ui, sans-serif`;
    target.textBaseline = "top";
    target.textAlign = "right";
    const right = FIELD.width - 6;
    let line = reserved.timer.y + reserved.timer.height + 4;
    // Mais recente no topo: a linha que acabou de nascer é a que se procura.
    for (const caption of captions.slice(-3).reverse()) {
      const text = caption.count > 1 ? `${caption.text} ×${caption.count}` : caption.text;
      const width = target.measureText(text).width;
      plate(target, palette, right - width, line, width, size);
      target.fillStyle = palette.text;
      target.fillText(text, right, line);
      line += size + 4;
    }
    target.textAlign = "left";
  }

  return { draw, resize, get scale() { return scale; } };
}
