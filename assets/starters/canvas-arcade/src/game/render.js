// Apresentação. Não decide regra e não altera o estado.
//
// Legibilidade antes de estilo: orbe, estilhaço e jogador têm **formas**
// diferentes, não só cores diferentes. O halo segue a mesma primitiva do
// orbe e do estilhaço. O corpo aponta para o último avanço — não é o
// tijolo da placa. O stub distingue as silhuetas com a mesma tinta; o
// dispositivo não foi observado. Tremor, piscada e vinheta respeitam
// redução de movimento — o sinal de causa migra para uma forma estática,
// não desaparece. A ponta do corpo fica: é forma, não brilho. A chuva
// da porta também: com menos movimento ela trava, não some.

import { FIELD, PLAYER_Y, CONFIG, remainingTicks, TICK_HZ, approaching, attractEntities, chainPipCount, chainPipAt, closingWindow, closingPulse, practicePulse, recoveryPulse } from "./rules.js";
import { copy, PALETTES, resolveLookName } from "./tables.js";
import { bindLines } from "../core/keys.js";
import { DEFAULT_BINDINGS } from "../core/settings.js";

// Reexporta a mesa: o token mora em data/palettes.json. Quem não
// desenhou o render troca o look sem republicar o verbo. `consistent`
// continua falso — JSON no disco não é comparação em movimento.
export { PALETTES };

// A recarga do dash era só um rótulo. A faixa enche o tempo inteiro de
// recuperação + cooldown — o verbo some e volta no mesmo sítio. Faixa no
// stub não é peso percebido.
export function dashCharge(state, config = CONFIG) {
  const player = state?.player;
  if (!player) return { phase: "ready", fill: 1 };
  const recoveryTicks = config.player.dashRecoveryTicks;
  const cooldownTicks = config.player.dashCooldownTicks;
  const total = recoveryTicks + cooldownTicks;
  if ((player.dashTicks ?? 0) > 0) return { phase: "dash", fill: 1 };
  if ((player.dashWindup ?? 0) > 0) {
    const total = config.player.dashWindupTicks || 1;
    return {
      phase: "windup",
      fill: Math.max(0, Math.min(1, (total - player.dashWindup) / total)),
    };
  }
  if ((state.bankLock ?? 0) > 0) return { phase: "lock", fill: 0 };
  const remaining = (player.dashRecovery ?? 0) > 0
    ? player.dashRecovery + cooldownTicks
    : (player.dashCooldown ?? 0);
  if (remaining <= 0 || total <= 0) return { phase: "ready", fill: 1 };
  const phase = (player.dashRecovery ?? 0) > 0 ? "recovery" : "cooldown";
  return { phase, fill: Math.max(0, Math.min(1, 1 - remaining / total)) };
}

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
    const lines = bindLines(copy, settings.bindings ?? DEFAULT_BINDINGS, extra.surface);
    const palette =
      settings.palette && typeof settings.palette.field === "string"
        ? settings.palette
        : settings.highContrast
          ? PALETTES.contrast
          : PALETTES[resolveLookName(settings.look)];
    const reduced = Boolean(settings.reducedMotion);
    context.setTransform(1, 0, 0, 1, 0, 0);
    context.fillStyle = palette.background;
    context.fillRect(0, 0, canvas.width, canvas.height);

    const shake = reduced ? 0 : state.shake;
    const punchX = reduced ? 0 : (state.camera?.x ?? 0);
    const punchY = reduced ? 0 : (state.camera?.y ?? 0);
    const jitterX = (shake ? (Math.sin(state.tick * 12.9898) * shake * 3) : 0) + punchX;
    const jitterY = (shake ? (Math.cos(state.tick * 7.233) * shake * 3) : 0) + punchY;
    context.setTransform(scale, 0, 0, scale, offsetX + jitterX * scale, offsetY + jitterY * scale);

    context.fillStyle = palette.field;
    context.fillRect(0, 0, FIELD.width, FIELD.height);
    drawVignette(context, reduced);
    drawPractice(context, palette, state, reduced);
    drawRecovery(context, palette, state, reduced);
    drawClose(context, palette, state, reduced);
    if (state.flash > 0) {
      if (reduced) {
        context.strokeStyle = palette.danger;
        context.lineWidth = 2;
        context.strokeRect(1, 1, FIELD.width - 2, FIELD.height - 2);
      } else {
        context.fillStyle = `rgba(255,245,235,${Math.min(0.32, state.flash * 0.5)})`;
        context.fillRect(0, 0, FIELD.width, FIELD.height);
      }
    }
    context.strokeStyle = palette.muted;
    context.lineWidth = 0.5;
    context.beginPath();
    context.moveTo(0, PLAYER_Y + 10);
    context.lineTo(FIELD.width, PLAYER_Y + 10);
    context.stroke();

    for (const entity of approaching(state)) {
      drawTelegraph(context, palette, entity, reduced);
    }
    for (const entity of state.entities) {
      if (entity.kind === "orb") drawOrb(context, palette, entity, reduced);
      else drawShard(context, palette, entity, reduced);
    }
    drawPlayer(context, palette, state, reduced);
    if (state.phase === "title") {
      for (const entity of attractEntities(state, reduced)) {
        if (entity.kind === "orb") drawOrb(context, palette, entity, reduced);
        else drawShard(context, palette, entity, reduced);
      }
      drawTitle(context, palette, settings, extra, lines);
      return;
    }
    drawChain(context, palette, state, reduced);
    const ending = state.phase === "over";
    // No fim a cortina cobre o campo. A queda da aposta — o verbo que o
    // overlay vai nomear — precisa nascer depois, senão a conta existe
    // e o corpo some. Os outros rastros ficam embaixo: não são o fim.
    drawMotes(context, palette, state, reduced, ending ? (mote) => mote.kind !== "lapse" : null);
    const reserved = drawHud(context, palette, state, settings, extra, lines);
    drawCoach(context, palette, extra.hint, reserved, settings, extra, lines);
    if (frame.paused) drawOverlay(context, palette, lines.paused, lines.resume, settings);
    else if (ending) {
      drawOverlay(context, palette, `${lines.over} — ${state.score}`, overHint(state, lines), settings);
      drawMotes(context, palette, state, reduced, (mote) => mote.kind === "lapse");
    }
    // A cortina cobria a faixa. Com o áudio desligado a informação
    // existia e sumia no fim e na pausa. A legenda nasce depois.
    if (settings.captions !== false) {
      drawCaptions(context, palette, extra.captions ?? [], reserved, settings);
    }
  }

  // A prática era orbe-só e o campo calava. O contorno na tinta do
  // orbe some à medida que a janela acaba; no último tick o campo
  // acende. Não é faixa. Com menos movimento vira traço, não some.
  function drawPractice(target, palette, state, reduced) {
    const pulse = practicePulse(state);
    if (!pulse.active) return;
    target.strokeStyle = palette.orb;
    if (reduced) {
      target.lineWidth = 2;
      target.strokeRect(4, 4, FIELD.width - 8, FIELD.height - 8);
      return;
    }
    const inset = 4 + (1 - pulse.fill) * 6;
    target.globalAlpha = Math.min(0.42, 0.10 + pulse.fill * 0.28);
    target.lineWidth = 0.8 + pulse.fill * 1.6;
    target.strokeRect(inset, inset, FIELD.width - inset * 2, FIELD.height - inset * 2);
    target.globalAlpha = 1;
  }

  // A guarda já alongava a chuva. O campo calava. O contorno na tinta
  // da corrente some à medida que a folga acaba. Não é faixa. Com menos
  // movimento vira traço, não some.
  function drawRecovery(target, palette, state, reduced) {
    const pulse = recoveryPulse(state);
    if (!pulse.active) return;
    target.strokeStyle = palette.chain;
    if (reduced) {
      target.lineWidth = 2;
      target.strokeRect(6, 6, FIELD.width - 12, FIELD.height - 12);
      return;
    }
    const inset = 6 + (1 - pulse.fill) * 5;
    target.globalAlpha = Math.min(0.40, 0.10 + pulse.fill * 0.26);
    target.lineWidth = 0.8 + pulse.fill * 1.4;
    target.strokeRect(inset, inset, FIELD.width - inset * 2, FIELD.height - inset * 2);
    target.globalAlpha = 1;
  }

  // O relógio no HUD já ficava vermelho. O campo agora marca o fecho:
  // contorno que aperta e pulsa a cada segundo. Não é faixa. Com menos
  // movimento vira um traço estático, como o flash do erro.
  function drawClose(target, palette, state, reduced) {
    const pulse = closingPulse(state);
    if (!pulse.active) return;
    target.strokeStyle = palette.danger;
    if (reduced) {
      target.lineWidth = 2;
      target.strokeRect(2, 2, FIELD.width - 4, FIELD.height - 4);
      return;
    }
    const inset = 1 + pulse.fill * 3;
    target.globalAlpha = Math.min(0.55, 0.14 + pulse.fill * 0.22 + pulse.beat * 0.18);
    target.lineWidth = 1.2 + pulse.fill * 1.8 + pulse.beat * 1.2;
    target.strokeRect(inset, inset, FIELD.width - inset * 2, FIELD.height - inset * 2);
    target.globalAlpha = 1;
  }

  // O campo era um retângulo chapado. A vinheta marca o recorte
  // sem ser faixa no HUD. Com menos movimento some: o sinal de
  // causa fica na forma, não no brilho. JSON no disco não é
  // comparação em movimento.
  function drawVignette(target, reduced) {
    if (reduced || typeof target.createRadialGradient !== "function") return;
    const glow = target.createRadialGradient(
      FIELD.width / 2,
      FIELD.height / 2,
      FIELD.height * 0.28,
      FIELD.width / 2,
      FIELD.height / 2,
      FIELD.height * 0.78,
    );
    glow.addColorStop(0, "rgba(0,0,0,0)");
    glow.addColorStop(1, "rgba(0,0,0,0.32)");
    target.fillStyle = glow;
    target.fillRect(0, 0, FIELD.width, FIELD.height);
  }

  function drawOrb(target, palette, entity, reduced) {
    if (!reduced) {
      target.globalAlpha = 0.22;
      target.fillStyle = palette.orb;
      target.beginPath();
      target.arc(entity.x, entity.y, 10, 0, Math.PI * 2);
      target.fill();
      target.globalAlpha = 1;
    }
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

  function drawShard(target, palette, entity, reduced) {
    if (!reduced) {
      target.globalAlpha = 0.2;
      target.fillStyle = palette.shard;
      target.beginPath();
      target.moveTo(entity.x, entity.y - 9);
      target.lineTo(entity.x + 8, entity.y + 7.5);
      target.lineTo(entity.x - 8, entity.y + 7.5);
      target.closePath();
      target.fill();
      target.globalAlpha = 1;
    }
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

  function drawTelegraph(target, palette, entity, reduced) {
    const y = PLAYER_Y + 10;
    target.globalAlpha = reduced ? 1 : 0.62;
    if (entity.kind === "orb") {
      target.strokeStyle = palette.orb;
      target.lineWidth = 1.2;
      target.beginPath();
      target.arc(entity.x, y, 3.5, 0, Math.PI * 2);
      target.stroke();
    } else {
      target.strokeStyle = palette.shard;
      target.lineWidth = 1.2;
      target.beginPath();
      target.moveTo(entity.x, y - 4);
      target.lineTo(entity.x + 3.5, y + 3);
      target.lineTo(entity.x - 3.5, y + 3);
      target.closePath();
      target.stroke();
    }
    target.globalAlpha = 1;
  }

  function moteFill(palette, kind) {
    if (kind === "collect" || kind === "land" || kind === "join" || kind === "missed") return palette.orb;
    if (kind === "bank" || kind === "break" || kind === "deposit" || kind === "lapse") return palette.chain;
    if (kind === "hit" || kind === "over" || kind === "graze") return palette.danger;
    return palette.player;
  }

  function drawMotes(target, palette, state, reduced, allow) {
    const motes = state.motes;
    if (!motes || !motes.length) return;
    for (const mote of motes) {
      if (allow && !allow(mote)) continue;
      const x = reduced ? mote.sx : mote.x;
      const y = reduced ? mote.sy : mote.y;
      target.fillStyle = moteFill(palette, mote.kind);
      if (reduced) {
        target.fillRect(x - 1, y - 1, 2, 2);
      } else if (mote.kind === "hit") {
        target.fillRect(x - 1.6, y - 0.6, 3.2, 1.2);
        target.fillRect(x - 0.6, y - 1.6, 1.2, 3.2);
      } else if (mote.kind === "missed") {
        target.fillRect(x - 2.4, y - 0.5, 4.8, 1.2);
      } else if (mote.kind === "deposit" || mote.kind === "join" || mote.kind === "lapse") {
        const size = CONFIG.feel.chainPipSize;
        target.fillRect(x - size / 2, y - size / 2, size, size);
      } else {
        target.fillRect(x - 1.2, y - 1.2, 2.4, 2.4);
      }
    }
  }

  function drawPlayer(target, palette, state, reduced) {
    const player = state.player;
    const squash = 1 + player.squash;
    const width = CONFIG.player.halfWidth * 2 * squash;
    const height = 12 / squash;
    const left = player.x - width / 2;
    const top = PLAYER_Y - height / 2;
    const dashing = player.dashTicks > 0;
    const recovering = !dashing && player.dashRecovery > 0;
    target.fillStyle = dashing ? palette.chain : recovering ? palette.orb : palette.player;
    target.fillRect(left, top, width, height);
    // O retângulo sozinho era o tijolo da placa. A ponta segue o
    // último avanço: orbe é círculo, estilhaço é losango, o corpo
    // aponta. Forma, não faixa. Com menos movimento a ponta fica.
    // Silhueta no stub não é comparação em movimento.
    const dir = player.dir < 0 ? -1 : 1;
    const nose = Math.max(3, height * 0.42);
    target.beginPath();
    if (dir < 0) {
      target.moveTo(left, top);
      target.lineTo(left - nose, PLAYER_Y);
      target.lineTo(left, top + height);
    } else {
      target.moveTo(left + width, top);
      target.lineTo(left + width + nose, PLAYER_Y);
      target.lineTo(left + width, top + height);
    }
    target.closePath();
    target.fill();
    if (player.invuln > 0) {
      // Com redução de movimento, contorno constante em vez de piscar.
      const visible = reduced || Math.floor(player.invuln / 4) % 2 === 0;
      if (visible) {
        target.strokeStyle = palette.danger;
        target.lineWidth = 1;
        target.strokeRect(left - 2, top - 2, width + 4, height + 4);
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

  // A corrente no HUD é conta. No corpo ela é a aposta: cada elo vira um
  // pip em órbita. A coleta leva o orbe ao slot; guardar leva o pip ao
  // placar; o erro espalha; no fim a aposta não guardada cai e o overlay
  // nomeia o que caiu. Com menos movimento a formação trava, não some.
  // Número no disco não é peso percebido. A conta no estado sobrevive
  // ao fim — a órbita não.
  function drawChain(target, palette, state, reduced) {
    if (state.phase === "over") return;
    const count = chainPipCount(state.chain);
    if (count <= 0) return;
    const size = CONFIG.feel.chainPipSize;
    const tick = Number.isFinite(state.tick) ? state.tick : 0;
    target.fillStyle = palette.chain;
    for (let index = 0; index < count; index += 1) {
      const pip = chainPipAt(index, count, state.player.x, PLAYER_Y, tick, reduced);
      target.fillRect(pip.x - size / 2, pip.y - size / 2, size, size);
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
  function drawHud(target, palette, state, settings, extra, lines) {
    const size = 8 * (settings.uiScale ?? 1);
    target.font = `${size}px system-ui, sans-serif`;
    target.textBaseline = "top";
    const second = 5 + size + 2;
    // A seta existe para mostrar o que guardar vale. Com corrente 1 ela dizia
    // "1 → 1", que não é erro de conta — é ruído, e um revisor leu como bug.
    // Ela aparece quando guardar rende mais do que a corrente já vale.
    const payoff = state.chain * state.chain;
    const chain = `${lines.chain} ${state.chain}${payoff > state.chain ? ` → ${payoff}` : ""}`;
    const score = `${lines.score} ${state.score}`;
    const seconds = Math.ceil(remainingTicks(state) / TICK_HZ);
    const best = extra.best === undefined ? null : `${lines.record} ${extra.best}`;
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
    target.fillStyle = closingWindow(state) ? palette.danger : palette.muted;
    target.fillText(`${seconds}s`, FIELD.width - 6, 5);
    if (best) {
      target.fillStyle = palette.muted;
      target.fillText(best, FIELD.width - 6, second);
    }

    target.textAlign = "left";
    const charge = dashCharge(state);
    const ready = charge.phase === "ready";
    const dash = ready ? lines.dash_ready : lines.dash_recharging;
    const dashBox = plate(target, palette, 6, FIELD.height - size - 5, width(dash), size);
    const strip = 2;
    const ink = charge.phase === "ready" || charge.phase === "dash"
      ? palette.orb
      : charge.phase === "windup"
        ? palette.chain
        : charge.phase === "recovery"
          ? palette.player
          : palette.muted;
    target.fillStyle = ink;
    target.fillRect(dashBox.x, dashBox.y + dashBox.height - strip, dashBox.width * charge.fill, strip);
    target.fillStyle = ready ? palette.orb : palette.muted;
    target.fillText(dash, 6, FIELD.height - size - 5);
    return { score: scoreBox, timer: timerBox, dash: dashBox };
  }

  function drawCoach(target, palette, hint, reserved, settings, extra = {}, lines = copy) {
    const text = hint === "fantasy" ? (extra.fantasy || lines.fantasy) : lines[`hint_${hint}`];
    if (!hint || !text) return;
    const size = 7 * (settings.uiScale ?? 1);
    target.font = `${size}px system-ui, sans-serif`;
    target.textBaseline = "top";
    const width = target.measureText(text).width;
    const x = (FIELD.width - width) / 2;
    const y = reserved.score.y + reserved.score.height + 6;
    plate(target, palette, x, y, width, size);
    target.textAlign = "left";
    target.fillStyle = palette.text;
    target.fillText(text, x, y);
  }

  // A conta no HUD fica sob a cortina. O overlay reusa `chain` e
  // `best_chain` — sem campo novo — para nomear a aposta que caiu.
  // Sem corrente o fim não inventa o rótulo. O avanço abre a porta,
  // não recomeça em silêncio. Texto no disco não é peso percebido.
  function overHint(state, lines) {
    const parts = [];
    if (state.chain > 0) parts.push(`${lines.chain} ${state.chain}`);
    if (state.stats.bestChain) parts.push(`${lines.best_chain}: ${state.stats.bestChain}`);
    parts.push(parts.length ? lines.over_door_inline : lines.over_door);
    return parts.join(" · ");
  }

  // A abertura lê o que o save já guardava. Recorde e última
  // seed — não o tick interrompido. Fantasia do `--idea` mora
  // aqui, não só nos 48 ticks do aviso. Tela no stub não é
  // alguém que voltou.
  function drawTitle(target, palette, settings, extra, lines) {
    const scale = settings.uiScale ?? 1;
    target.fillStyle = palette.plate;
    target.globalAlpha = 0.62;
    target.fillRect(0, 0, FIELD.width, FIELD.height);
    target.globalAlpha = 1;
    target.textAlign = "center";
    const fantasy = String(extra.fantasy || lines.fantasy || "").trim();
    let line = FIELD.height / 2 - 22 * scale;
    if (fantasy) {
      target.fillStyle = palette.text;
      target.font = `${10 * scale}px system-ui, sans-serif`;
      target.fillText(fantasy, FIELD.width / 2, line);
      line += 16 * scale;
    }
    const last = extra.lastRun;
    if (last && Number.isFinite(last.score)) {
      target.fillStyle = palette.muted;
      target.font = `${8 * scale}px system-ui, sans-serif`;
      target.fillText(`${lines.title_last} ${last.score}`, FIELD.width / 2, line);
      line += 12 * scale;
    }
    const best = Number.isFinite(extra.best) ? extra.best : 0;
    if (best > 0) {
      target.fillStyle = palette.muted;
      target.font = `${8 * scale}px system-ui, sans-serif`;
      target.fillText(`${lines.record} ${best}`, FIELD.width / 2, line);
      line += 12 * scale;
    }
    target.fillStyle = palette.text;
    target.font = `${8 * scale}px system-ui, sans-serif`;
    target.fillText(extra.canContinue ? lines.title_again : lines.title_play, FIELD.width / 2, line);
    if (extra.canContinue) {
      target.fillStyle = palette.muted;
      target.fillText(lines.title_new, FIELD.width / 2, line + 12 * scale);
    }
    target.textAlign = "left";
  }

  function drawOverlay(target, palette, title, hint, settings = {}) {
    // A cortina reusa a placa do look — dusk não herda o preto frio.
    // Token no disco não é direção observada. O texto segue uiScale
    // como o HUD; escala no stub não é sessão de alcance.
    const scale = settings.uiScale ?? 1;
    target.fillStyle = palette.plate;
    target.fillRect(0, 0, FIELD.width, FIELD.height);
    target.textAlign = "center";
    target.fillStyle = palette.text;
    target.font = `${16 * scale}px system-ui, sans-serif`;
    target.fillText(title, FIELD.width / 2, FIELD.height / 2 - 14 * scale);
    target.font = `${8 * scale}px system-ui, sans-serif`;
    target.fillStyle = palette.muted;
    target.fillText(hint, FIELD.width / 2, FIELD.height / 2 + 8 * scale);
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
