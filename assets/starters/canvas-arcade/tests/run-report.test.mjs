import { test } from "node:test";
import assert from "node:assert/strict";

import { playReport } from "../src/core/run-report.js";
import { acceptLastRun } from "../tools/serve.mjs";

test("o recibo nasce sem observar e a simulação não se mistura com a partida", () => {
  const played = playReport({
    seed: 9,
    spawn: "dusk",
    run: { seed: 9, ticks: 120, score: 4, banks: 1 },
    curve: { never_banked: false },
    policy: "played",
    observed: true,
    felt: true,
  });
  assert.equal(played.policy, "played");
  assert.equal(played.observed, false);
  assert.equal(played.felt, false);
  assert.equal(played.spawn, "dusk");
  assert.equal(played.curve.never_banked, false);
  assert.match(played.scope, /não é causa/);
  assert.doesNotMatch(played.scope, /aprovado|verified|LUFS|-14|4\.5|enough|consistent/);

  const simulated = playReport({
    seed: 7,
    spawn: "spawn",
    run: { ticks: 3600 },
    policy: "nearest-orb",
  });
  assert.equal(simulated.policy, "nearest-orb");
  assert.equal(simulated.observed, false);
  assert.match(simulated.scope, /nearest-orb/);
});

test("o POST só aceita run com ticks e apaga observed do cliente", () => {
  const accepted = acceptLastRun(JSON.stringify({
    observed: true,
    felt: true,
    policy: "nearest-orb",
    run: { ticks: 80, score: 2, seed: 3 },
    seed: 3,
    spawn: "calm",
    curve: { never_hit: true },
  }));
  assert.equal(accepted.ok, true);
  assert.equal(accepted.report.observed, false);
  assert.equal(accepted.report.felt, false);
  assert.equal(accepted.report.policy, "played");
  assert.equal(accepted.report.spawn, "calm");
  assert.equal(accepted.report.run.ticks, 80);

  assert.equal(acceptLastRun("não-json").ok, false);
  assert.equal(acceptLastRun("{}").ok, false);
  assert.equal(acceptLastRun({ run: { score: 1 } }).ok, false);
});
