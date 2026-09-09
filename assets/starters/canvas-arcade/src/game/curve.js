// Traça a partida pelos eventos. Número é fato da simulação — never_banked
// não é abandono observado, sequência de hit não é causa. A forma do save
// não passa por aqui.

export function emptyCurve() {
  return {
    first_collect_tick: null,
    first_bank_tick: null,
    first_hit_tick: null,
    never_banked: true,
    never_hit: true,
    longest_hit_streak: 0,
    longest_miss_streak: 0,
    unbanked_at_end: 0,
  };
}

export function createTrace() {
  return { curve: emptyCurve(), hitStreak: 0, missStreak: 0 };
}

export function reportCurve(trace) {
  return { ...trace.curve };
}

export function finishCurve(trace, chain) {
  if (Number.isFinite(chain)) trace.curve.unbanked_at_end = chain;
  return reportCurve(trace);
}

export function traceEvents(trace, events, tick) {
  if (!events) return trace.curve;
  for (let index = 0; index < events.length; index += 1) {
    applyEvent(trace, events[index], tick);
  }
  return trace.curve;
}

export function traceTick(trace, state) {
  return traceEvents(trace, state.events, state.tick);
}

function applyEvent(trace, event, tick) {
  const type = event?.type;
  const curve = trace.curve;
  if (type === "collect") {
    if (curve.first_collect_tick === null) curve.first_collect_tick = tick;
    trace.hitStreak = 0;
    trace.missStreak = 0;
    return;
  }
  if (type === "bank") {
    if (curve.first_bank_tick === null) curve.first_bank_tick = tick;
    curve.never_banked = false;
    trace.hitStreak = 0;
    trace.missStreak = 0;
    return;
  }
  if (type === "hit") {
    if (curve.first_hit_tick === null) curve.first_hit_tick = tick;
    curve.never_hit = false;
    trace.hitStreak += 1;
    if (trace.hitStreak > curve.longest_hit_streak) {
      curve.longest_hit_streak = trace.hitStreak;
    }
    trace.missStreak = 0;
    return;
  }
  if (type === "missed") {
    trace.missStreak += 1;
    if (trace.missStreak > curve.longest_miss_streak) {
      curve.longest_miss_streak = trace.missStreak;
    }
    return;
  }
  if (type === "graze") {
    trace.hitStreak = 0;
    return;
  }
  if (type === "over" && Number.isFinite(event.unbanked)) {
    curve.unbanked_at_end = event.unbanked;
  }
}
