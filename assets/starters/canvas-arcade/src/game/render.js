// Apresentação. Não decide regra e não altera o estado.
//
// Legibilidade antes de estilo: orbe e estilhaço têm **formas** diferentes, não
// só cores diferentes, então o jogo continua jogável em escala de cinza e para
// quem não distingue as duas cores. Tremor e piscada respeitam redução de
// movimento — o sinal de causa migra para uma forma estática, não desaparece.

import { FIELD, PLAYER_Y, CONFIG, remainingTicks, TICK_HZ } from "./rules.js";

const PALETTES = {
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
    drawHud(context, palette, state, settings, extra);
    if (frame.paused) drawOverlay(context, palette, "Pausado", "Continuar: Esc ou P");
    else if (state.phase === "over") {
      drawOverlay(
        context,
        palette,
        `Fim — ${state.score}`,
        state.stats.bestChain ? `Maior corrente: ${state.stats.bestChain} · reiniciar: R` : "Reiniciar: R",
      );
    }
    if (settings.captions !== false) drawCaptions(context, palette, extra.captions ?? []);
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

  function drawHud(target, palette, state, settings, extra) {
    const size = 8 * (settings.uiScale ?? 1);
    target.font = `${size}px system-ui, sans-serif`;
    target.textBaseline = "top";
    target.fillStyle = palette.text;
    target.fillText(`Pontos ${state.score}`, 6, 5);
    target.fillStyle = state.chain > 0 ? palette.chain : palette.muted;
    target.fillText(`Corrente ${state.chain}${state.chain > 0 ? ` → ${state.chain * state.chain}` : ""}`, 6, 5 + size + 2);
    const seconds = Math.ceil(remainingTicks(state) / TICK_HZ);
    target.fillStyle = seconds <= 10 ? palette.danger : palette.muted;
    target.textAlign = "right";
    target.fillText(`${seconds}s`, FIELD.width - 6, 5);
    if (extra.best !== undefined) {
      target.fillStyle = palette.muted;
      target.fillText(`Recorde ${extra.best}`, FIELD.width - 6, 5 + size + 2);
    }
    target.textAlign = "left";
    const ready = state.player.dashCooldown === 0 && state.player.dashRecovery === 0 && state.bankLock === 0;
    target.fillStyle = ready ? palette.orb : palette.muted;
    target.fillText(ready ? "Dash pronto" : "Dash recarregando", 6, FIELD.height - size - 5);
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

  function drawCaptions(target, palette, captions) {
    if (!captions.length) return;
    target.font = "7px system-ui, sans-serif";
    target.textAlign = "center";
    let line = FIELD.height - 16;
    for (const caption of captions.slice(-3)) {
      const width = target.measureText(caption.text).width + 8;
      target.fillStyle = "rgba(0,0,0,0.72)";
      target.fillRect(FIELD.width / 2 - width / 2, line - 1, width, 9);
      target.fillStyle = palette.text;
      target.fillText(caption.text, FIELD.width / 2, line);
      line -= 10;
    }
    target.textAlign = "left";
  }

  return { draw, resize, get scale() { return scale; } };
}
