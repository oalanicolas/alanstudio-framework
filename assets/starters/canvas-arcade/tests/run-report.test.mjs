import { test } from "node:test";
import assert from "node:assert/strict";

import { findingAttachment, playFinding, playNote, playReport } from "../src/core/run-report.js";
import { acceptFinding, acceptLastRun, acceptNote, writeFinding } from "../tools/serve.mjs";
import { mkdtemp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

test("o recibo nasce sem observar e a simulação não se mistura com a partida", () => {
  const played = playReport({
    seed: 9,
    spawn: "dusk",
    look: "dusk",
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
  assert.equal(played.look, "dusk");
  assert.equal(played.speed, 1);
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
  assert.equal(simulated.look, "normal");
  assert.equal(simulated.speed, 1);
  assert.equal(playReport({ seed: 9, speed: 0.75, run: { ticks: 10 } }).speed, 0.75);
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
    look: "dusk",
    curve: { never_hit: true },
  }));
  assert.equal(accepted.ok, true);
  assert.equal(accepted.report.observed, false);
  assert.equal(accepted.report.felt, false);
  assert.equal(accepted.report.policy, "played");
  assert.equal(accepted.report.spawn, "calm");
  assert.equal(accepted.report.look, "dusk");
  assert.equal(accepted.report.run.ticks, 80);

  assert.equal(acceptLastRun("não-json").ok, false);
  assert.equal(acceptLastRun("{}").ok, false);
  assert.equal(acceptLastRun({ run: { score: 1 } }).ok, false);
});

test("a nota vazia não grava e a preenchida não observa", () => {
  assert.equal(playNote({ note: "   " }), null);
  assert.equal(acceptNote({ note: "" }).ok, false);
  const accepted = acceptNote({ note: "  o dash atravessou  ", author: "" });
  assert.equal(accepted.ok, true);
  assert.equal(accepted.author, "página");
  assert.equal(accepted.note, "o dash atravessou");
  const report = playNote({
    author: "página",
    note: "o dash atravessou",
    project: "/tmp/jogo",
    run: { ticks: 40, score: 2 },
    observed: true,
    felt: true,
  });
  assert.equal(report.kind, "observation");
  assert.equal(report.status, "declared");
  assert.equal(report.author, "página");
  assert.equal(report.felt, false);
  assert.equal(report.observed, false);
  assert.equal(report.fields.role, "human");
  assert.match(report.fields.run, /"ticks":40/);
  assert.doesNotMatch(report.scope, /aprovado|verified|LUFS|-14|4\.5|enough|consistent/);
});

test("o achado só nasce com os quatro nomes preenchidos", () => {
  assert.equal(playFinding({}), null);
  assert.equal(playFinding({
    problema: "o dash",
    evidencia: "três sessões",
    hipotese: "hitstop",
    medicao: "",
  }), null);
  assert.equal(acceptFinding({ problema: "o dash" }).ok, false);
  const text = playFinding({
    problema: "o dash não comunica o contato",
    evidencia: "três sessões, pergunta se atravessou",
    hipotese: "o hitstop some no movimento",
    medicao: "repetir o graze com hitstop 5 e 2",
  });
  assert.match(text, /Problema: o dash não comunica o contato/);
  assert.match(text, /Medição: repetir o graze/);
  const accepted = acceptFinding({
    problema: "o dash não comunica o contato",
    evidencia: "três sessões, pergunta se atravessou",
    hipotese: "o hitstop some no movimento",
    medicao: "repetir o graze com hitstop 5 e 2",
  });
  assert.equal(accepted.ok, true);
  assert.equal(accepted.text, text);
});

test("o achado gravado nomeia o last-run simulado que a faixa já mostra", () => {
  const text = playFinding({
    problema: "o dash some no toque",
    evidencia: "três sessões",
    hipotese: "o hitstop some",
    medicao: "repetir o graze",
    run: { seed: 8, score: 12, policy: "nearest-orb" },
  });
  assert.match(text, /simulada/, "o markdown calava a origem que a faixa já nomeia");
  assert.match(text, /seed 8/);
  assert.equal(text.includes("coletas"), false, "sem tally no achado");
  const played = playFinding({
    problema: "o dash some no toque",
    evidencia: "três sessões",
    hipotese: "o hitstop some",
    medicao: "repetir o graze",
    run: { seed: 8, policy: "played" },
  });
  assert.equal(played.includes("simulada"), false, "played some");
  const accepted = acceptFinding({
    problema: "o dash some no toque",
    evidencia: "três sessões",
    hipotese: "o hitstop some",
    medicao: "repetir o graze",
    run: { seed: 8, score: 12, policy: "nearest-orb" },
  });
  assert.equal(accepted.ok, true);
  assert.match(accepted.text, /simulada/);
});

test("o anexo do achado nasce do candidato e não observa", () => {
  const attached = findingAttachment({
    seed: 8,
    spawn: "dusk",
    look: "dusk",
    run: { ticks: 40, score: 3, seed: 8 },
    curve: { never_banked: false },
    finding: "20260910T000000Z-achado.md",
    observed: true,
    outsider: true,
  });
  assert.equal(attached.kind, "finding-attachment");
  assert.equal(attached.policy, "played");
  assert.equal(attached.observed, false);
  assert.equal(attached.felt, false);
  assert.equal(attached.outsider, false);
  assert.equal(attached.finding, "20260910T000000Z-achado.md");
  assert.equal(attached.run.ticks, 40);
  assert.equal(attached.spawn, "dusk");
  assert.equal(attached.look, "dusk");
  assert.match(attached.scope, /não é causa/);
  assert.doesNotMatch(attached.scope, /aprovado|verified|LUFS|-14|4\.5|enough|consistent/);
});

test("gravar o achado anexa last-run e sem partida não inventa anexo", async () => {
  const root = await mkdtemp(join(tmpdir(), "starter-finding-"));
  try {
    const text = playFinding({
      problema: "o dash não comunica o contato",
      evidencia: "três sessões, pergunta se atravessou",
      hipotese: "o hitstop some no movimento",
      medicao: "repetir o graze com hitstop 5 e 2",
    });
    const hollow = await writeFinding(root, text);
    assert.match(hollow, /-achado\.md$/);
    const empty = await readdir(join(root, "docs/playtest"));
    assert.equal(empty.filter((name) => name.endsWith("-achado.run.json")).length, 0);

    await mkdir(join(root, "docs/playtest"), { recursive: true });
    await writeFile(join(root, "docs/playtest/last-run.json"), `${JSON.stringify({
      schema: 2,
      seed: 8,
      spawn: "dusk",
      look: "dusk",
      policy: "played",
      run: { ticks: 40, score: 3, seed: 8 },
      curve: { never_banked: false },
      observed: true,
      felt: true,
    }, null, 2)}\n`);
    const dest = await writeFinding(root, text);
    const companion = dest.replace(/-achado\.md$/, "-achado.run.json");
    const attached = JSON.parse(await readFile(companion, "utf8"));
    assert.equal(attached.kind, "finding-attachment");
    assert.equal(attached.observed, false);
    assert.equal(attached.felt, false);
    assert.equal(attached.outsider, false);
    assert.equal(attached.policy, "played");
    assert.equal(attached.run.ticks, 40);
    assert.equal(attached.spawn, "dusk");
    assert.equal(attached.look, "dusk");
    assert.equal(attached.finding, dest.split(/[/\\]/).pop());
    assert.doesNotMatch(JSON.stringify(attached), /aprovado|verified|LUFS|-14|4\.5|enough|consistent/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
