// Pulso no aparelho. O stub percorre o actuator; sessão com controle
// continua não observada. felt permanece falso.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createHaptics } from "../src/game/haptics.js";
import { CONFIG } from "../src/game/rules.js";

function stubActuator() {
  const plays = [];
  return {
    plays,
    actuator: {
      playEffect(kind, effect) {
        plays.push({ kind, ...effect });
        return Promise.resolve();
      },
      reset() {
        plays.push("reset");
      },
    },
  };
}

test("cada verbo pulsa com duração e magnitude distintas", () => {
  const { plays, actuator } = stubActuator();
  const haptics = createHaptics({ gamepads: () => [{ vibrationActuator: actuator }] });
  for (const role of ["dash", "land", "collect", "bank", "hit", "over"]) {
    assert.equal(haptics.play(role), true, `${role} precisa pulsar`);
  }
  const pulses = plays.filter((entry) => entry !== "reset");
  assert.equal(pulses.length, 6);
  const durations = pulses.map((entry) => entry.duration);
  const weaks = pulses.map((entry) => entry.weakMagnitude);
  const strongs = pulses.map((entry) => entry.strongMagnitude);
  assert.equal(new Set(durations).size, 6, "duração igual apaga o peso do verbo");
  assert.equal(new Set(weaks).size, 6, "magnitude igual apaga o peso do verbo");
  assert.equal(new Set(strongs).size, 6);
  assert.ok(CONFIG.feel.rumbleHitMs > CONFIG.feel.rumbleBankMs);
  assert.ok(CONFIG.feel.rumbleBankMs > CONFIG.feel.rumbleCollectMs);
  assert.ok(CONFIG.feel.rumbleDashMs > CONFIG.feel.rumbleLandMs);
  assert.ok(CONFIG.feel.rumbleCollectMs > CONFIG.feel.rumbleDashMs);
  assert.ok(CONFIG.feel.rumbleHit > CONFIG.feel.rumbleBank);
  assert.ok(CONFIG.feel.rumbleBank > CONFIG.feel.rumbleCollect);
  const hit = pulses.find((entry) => entry.duration === CONFIG.feel.rumbleHitMs);
  const collect = pulses.find((entry) => entry.duration === CONFIG.feel.rumbleCollectMs);
  assert.ok(hit.weakMagnitude > collect.weakMagnitude);
  assert.ok(hit.strongMagnitude > collect.strongMagnitude);
  haptics.dispose();
});

test("graze e cama não inventam pulso", () => {
  const { plays, actuator } = stubActuator();
  const haptics = createHaptics({ gamepads: () => [{ vibrationActuator: actuator }] });
  assert.equal(haptics.play("graze"), false);
  assert.equal(haptics.play("bed"), false);
  assert.equal(haptics.play("missed"), false);
  assert.deepEqual(plays, []);
  haptics.dispose();
});

test("reducedMotion cancela o pulso e o que ainda vibrava", () => {
  const { plays, actuator } = stubActuator();
  const haptics = createHaptics({
    gamepads: () => [{ vibrationActuator: actuator }],
    settings: { reducedMotion: true },
  });
  assert.equal(haptics.play("hit"), false);
  assert.deepEqual(plays, []);
  const live = createHaptics({ gamepads: () => [{ vibrationActuator: actuator }] });
  live.play("bank");
  live.applySettings({ reducedMotion: true });
  assert.ok(plays.includes("reset"), "reduzir movimento precisa calar o pulso vivo");
  assert.equal(live.play("hit"), false);
  live.dispose();
});

test("pausa e dispose cancelam o pulso vivo", () => {
  const { plays, actuator } = stubActuator();
  const haptics = createHaptics({ gamepads: () => [{ vibrationActuator: actuator }] });
  haptics.play("hit");
  haptics.mute();
  assert.ok(plays.includes("reset"));
  assert.equal(haptics.play("bank"), false, "pausado não pulsa");
  haptics.unmute();
  assert.equal(haptics.play("dash"), true, "retomar devolve o pulso");
  haptics.dispose();
  assert.equal(haptics.play("over"), false, "descartado não pulsa");
});

test("sem actuator cai no vibrate do aparelho", () => {
  const calls = [];
  const haptics = createHaptics({
    gamepads: () => [],
    vibrate: (pattern) => calls.push(pattern),
  });
  assert.equal(haptics.play("collect"), true);
  assert.deepEqual(calls, [CONFIG.feel.rumbleCollectMs]);
  haptics.mute();
  assert.deepEqual(calls.at(-1), 0);
  haptics.dispose();
});
