import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyArtifactSurface, applyFinding, applyInvite, applyNote, applyRunFacts, applyShare, ARTIFACT_FINDING_HINT, bringPanel, composeFinding, FINDING_FILE, inviteHref, inviteMode, INVITE_LABEL, offerFinding, findingFile, readArtifactMark, runFacts, seedHref } from "../src/core/invite.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");

test("só invite=1 liga o modo; outro valor não esconde a tabela", () => {
  assert.equal(inviteMode("?invite=1"), true);
  assert.equal(inviteMode("invite=1"), true);
  assert.equal(inviteMode("?invite=1&look=dusk"), true);
  assert.equal(inviteMode("?invite=1&seed=8"), true);
  assert.equal(inviteMode("?invite=1&seed=8&spawn=dusk"), true);
  assert.equal(inviteMode("?invite=1&seed=8&spawn=dusk&look=dusk"), true);
  assert.equal(inviteMode("?look=dusk"), false);
  assert.equal(inviteMode("?invite=true"), false);
  assert.equal(inviteMode(""), false);
});

test("o modo some a tabela e não ensina o verbo no rótulo", () => {
  const root = { classList: { invite: false, toggle(name, on) { this[name] = on; } } };
  const stage = { label: "Área de jogo. Colete orbes.", setAttribute(_, value) { this.label = value; } };
  assert.equal(applyInvite({ root, stage, search: "?invite=1" }), true);
  assert.equal(root.classList.invite, true);
  assert.equal(stage.label, INVITE_LABEL);
  assert.equal(INVITE_LABEL.includes("orbe"), false);
  assert.equal(INVITE_LABEL.includes("guarda"), false);

  const idle = { classList: { invite: true, toggle(name, on) { this[name] = on; } } };
  assert.equal(applyInvite({ root: idle, search: "" }), false);
  assert.equal(idle.classList.invite, false);
});

test("a página declara o gancho que some a tabela sem preencher o achado", () => {
  assert.match(html, /id="commands"/);
  assert.match(html, /html\.invite\s+#commands/);
  assert.match(html, /get\("invite"\) === "1"/);
  assert.match(html, /invite-strip/);
  const strip = html.match(/class="invite-strip"[^>]*>([^<]+)/);
  assert.ok(strip, "esperava a faixa do convite");
  assert.match(strip[1], /não ensina o verbo/);
  assert.equal(/mover|dash|guardar|estilhaço|orbe/i.test(strip[1]), false, strip[1]);
  assert.equal(/problema|evidência|hipótese|medição/i.test(strip[1]), false, strip[1]);
  assert.match(html, /id="options-title"/, "o convite não pode some o alcance");
  assert.match(html, /id="settings-gap"/, "o convite não some o aviso das preferências");
  assert.match(html, /settingsLine\(game\.settingsLoad/, "o aviso lê o recibo, não a porta");
  assert.doesNotMatch(html, /persistLine\([^)]*settings/, "a porta não nomeia a recuperação");
  assert.match(html, /id="remap"/, "o convite não some o remapeamento");
  assert.match(html, /id="gameSpeed"/, "o convite não some a velocidade da partida");
  assert.match(html, /id="colorblind"/, "o convite não some a tinta estável");
  assert.doesNotMatch(html, /html\.invite\s+#remap/, "só a tabela some");
  assert.match(html, /id="finding"/);
  assert.match(html, /html\.invite\.finding\s+#finding/);
  assert.match(html, /id="finding-copy"/);
  assert.match(html, /id="finding-save"/);
  assert.match(html, /id="finding-hint"/);
  assert.match(html, /readArtifactMark/);
  assert.match(html, /applyArtifactSurface/);
  assert.match(html, /html\.artifact\s+#finding-save/);
  assert.match(html, /id="finding-run"/);
  assert.match(html, /id="note-run"/);
  assert.match(html, /Copie ou grave/);
  assert.match(html, /anexa o candidato/);
  assert.match(html, /composeFinding/);
  assert.match(html, /offerFinding/);
  assert.match(html, /bringPanel/);
  assert.match(html, /wasShown/);
  assert.match(html, /finding-problema/);
  assert.match(html, /note-text/);
  assert.match(html, /playFinding/);
  assert.match(html, /applyRunFacts/);
  assert.match(html, /FINDING_ROUTE/);
  assert.doesNotMatch(html, /html\.invite\s+#finding\s*\{/);
  assert.match(html, /id="note"/);
  assert.match(html, /html\.note\s+#note/);
  assert.match(html, /id="note-save"/);
  assert.match(html, /id="note-invite"/);
  assert.match(html, /id="note-invite-href"/);
  assert.match(html, /id="note-invite-copy"/);
  assert.match(html, /applyShare/);
  assert.match(html, /inviteHref/);
  assert.match(html, /NOTE_ROUTE/);
  assert.doesNotMatch(html, /html\.invite\s+#note/);
  assert.match(html, /game\.lastRun/, "a porta relê a partida para manter o recibo");
});

test("VERSION.json no root some o Gravar e deixa o Copiar", async () => {
  assert.equal(await readArtifactMark({}), false);
  assert.equal(await readArtifactMark({ fetch: async () => ({ ok: false }) }), false);
  assert.equal(await readArtifactMark({
    fetch: async () => { throw new Error("offline"); },
  }), false);
  assert.equal(await readArtifactMark({ fetch: async () => ({ ok: true }) }), true);
  const save = { hidden: false, disabled: false };
  const copy = { hidden: false, disabled: false };
  const note = { hidden: false, disabled: false };
  const hint = { textContent: "Copie ou grave" };
  const root = { classList: { artifact: false, toggle(name, on) { this[name] = on; } } };
  assert.equal(applyArtifactSurface({
    root,
    findingSave: save,
    noteSave: note,
    findingHint: hint,
    artifact: false,
  }), false);
  assert.equal(save.hidden, false);
  assert.equal(applyArtifactSurface({
    root,
    findingSave: save,
    noteSave: note,
    findingHint: hint,
    artifact: true,
  }), true);
  assert.equal(save.hidden, true);
  assert.equal(save.disabled, true);
  assert.equal(note.hidden, true);
  assert.equal(copy.hidden, false);
  assert.equal(hint.textContent, ARTIFACT_FINDING_HINT);
  assert.match(hint.textContent, /recusa gravar/);
  assert.doesNotMatch(hint.textContent, /outsider|aprovado|verified|alguém de fora/);
  assert.match(hint.textContent, /baixa o markdown/);
  assert.doesNotMatch(FINDING_FILE, /outsider|aprovado|verified/);
  assert.equal(root.classList.artifact, true);
});

test("a seed da partida junta chuva e look sem fingir que observou", () => {
  assert.equal(seedHref(null), null);
  assert.equal(seedHref({ score: 3 }), null);
  assert.equal(seedHref({ seed: 8 }), "/?seed=8");
  assert.equal(seedHref({ run: { seed: 8 } }), "/?seed=8");
  assert.equal(seedHref({ seed: 8, spawn: "spawn" }), "/?seed=8");
  assert.equal(seedHref({ seed: 8, spawn: "dusk" }), "/?seed=8&spawn=dusk");
  assert.equal(seedHref({ seed: 8, run: { spawn: "calm" } }), "/?seed=8&spawn=calm");
  assert.equal(seedHref({ seed: 8, spawn: "../x" }), "/?seed=8");
  assert.equal(seedHref({ seed: 8 }, "http://192.168.1.40:8080"), "http://192.168.1.40:8080/?seed=8");
  assert.equal(
    seedHref({ seed: 8, spawn: "dusk" }, "http://192.168.1.40:8080"),
    "http://192.168.1.40:8080/?seed=8&spawn=dusk",
  );
  assert.equal(seedHref({ seed: 8, look: "normal" }), "/?seed=8");
  assert.equal(seedHref({ seed: 8, look: "contrast" }), "/?seed=8");
  assert.equal(seedHref({ seed: 8, look: "dusk" }), "/?seed=8&look=dusk");
  assert.equal(seedHref({ seed: 8, spawn: "dusk", look: "dusk" }), "/?seed=8&spawn=dusk&look=dusk");
  assert.equal(seedHref({ seed: 8, spawn: "dusk", look: "calm" }), "/?seed=8&spawn=dusk&look=calm");
  assert.equal(seedHref({ seed: 8, look: "../x" }), "/?seed=8");
  assert.equal(
    seedHref({ seed: 8, spawn: "dusk", look: "dusk" }, "http://192.168.1.40:8080"),
    "http://192.168.1.40:8080/?seed=8&spawn=dusk&look=dusk",
  );
});

test("o convite da partida junta a seed sem fingir quem jogou", () => {
  assert.equal(inviteHref(null), "/?invite=1");
  assert.equal(inviteHref({ score: 3 }), "/?invite=1");
  assert.equal(inviteHref({ seed: 8 }), "/?invite=1&seed=8");
  assert.equal(inviteHref({ run: { seed: 8 } }), "/?invite=1&seed=8");
  assert.equal(inviteHref({ seed: 8, spawn: "spawn" }), "/?invite=1&seed=8");
  assert.equal(inviteHref({ seed: 8, spawn: "dusk" }), "/?invite=1&seed=8&spawn=dusk");
  assert.equal(inviteHref({ seed: 8, run: { spawn: "calm" } }), "/?invite=1&seed=8&spawn=calm");
  assert.equal(inviteHref({ seed: 8, spawn: "../x" }), "/?invite=1&seed=8");
  assert.equal(inviteHref({ seed: 8 }, "http://192.168.1.40:8080"), "http://192.168.1.40:8080/?invite=1&seed=8");
  assert.equal(
    inviteHref({ seed: 8, spawn: "dusk" }, "http://192.168.1.40:8080"),
    "http://192.168.1.40:8080/?invite=1&seed=8&spawn=dusk",
  );
  assert.equal(inviteHref({ seed: 8, look: "normal" }), "/?invite=1&seed=8");
  assert.equal(inviteHref({ seed: 8, look: "contrast" }), "/?invite=1&seed=8");
  assert.equal(inviteHref({ seed: 8, look: "dusk" }), "/?invite=1&seed=8&look=dusk");
  assert.equal(inviteHref({ seed: 8, spawn: "dusk", look: "dusk" }), "/?invite=1&seed=8&spawn=dusk&look=dusk");
  assert.equal(inviteHref({ seed: 8, spawn: "dusk", look: "calm" }), "/?invite=1&seed=8&spawn=dusk&look=calm");
  assert.equal(inviteHref({ seed: 8, look: "../x" }), "/?invite=1&seed=8");
  assert.equal(
    inviteHref({ seed: 8, spawn: "dusk", look: "dusk" }, "http://192.168.1.40:8080"),
    "http://192.168.1.40:8080/?invite=1&seed=8&spawn=dusk&look=dusk",
  );
  const hrefNode = { textContent: "" };
  const wrap = { hidden: true };
  assert.equal(applyShare({ hrefNode, wrap, run: { seed: 8 } }), "/?invite=1&seed=8");
  assert.equal(hrefNode.textContent, "/?invite=1&seed=8");
  assert.equal(wrap.hidden, false);
  assert.equal(applyShare({ hrefNode, wrap, run: { seed: 8, spawn: "dusk" } }), "/?invite=1&seed=8&spawn=dusk");
  assert.equal(hrefNode.textContent, "/?invite=1&seed=8&spawn=dusk");
  assert.equal(wrap.hidden, false);
  assert.equal(
    applyShare({ hrefNode, wrap, run: { seed: 8, spawn: "dusk", look: "dusk" } }),
    "/?invite=1&seed=8&spawn=dusk&look=dusk",
  );
  assert.equal(wrap.hidden, false);
  assert.equal(applyShare({ hrefNode, wrap, run: { score: 3 } }), "/?invite=1");
  assert.equal(wrap.hidden, true);
  assert.match(html, /Convite desta partida/);
  assert.match(html, /Copiar endereço/);
  assert.doesNotMatch(html, /outsider|aprovado|verified|alguém de fora/);
});

test("a nota só aparece depois do fim e some no convite", () => {
  const root = { classList: { note: false, toggle(name, on) { this[name] = on; } } };
  assert.equal(applyNote({ root, phase: "title", invite: false }), false);
  assert.equal(applyNote({ root, phase: "playing", invite: false }), false);
  assert.equal(applyNote({ root, phase: "over", invite: true }), false);
  assert.equal(applyNote({ root, phase: "over", invite: false }), true);
  assert.equal(root.classList.note, true);
  assert.equal(applyNote({ root, phase: "title", invite: false, run: { score: 3 } }), true);
  assert.equal(applyNote({ root, phase: "playing", invite: false, run: { score: 3 } }), false);
});

test("o achado só aparece no convite depois do fim", () => {
  const root = { classList: { finding: false, toggle(name, on) { this[name] = on; } } };
  assert.equal(applyFinding({ root, phase: "title", invite: true }), false);
  assert.equal(root.classList.finding, false);
  assert.equal(applyFinding({ root, phase: "playing", invite: true }), false);
  assert.equal(applyFinding({ root, phase: "over", invite: false }), false);
  assert.equal(applyFinding({ root, phase: "over", invite: true }), true);
  assert.equal(root.classList.finding, true);
  assert.equal(applyFinding({ root, phase: "title", invite: true, run: { score: 3 } }), true);
  assert.equal(applyFinding({ root, phase: "title", invite: false, run: { score: 3 } }), false);
});

test("bringPanel só entra no primeiro over", () => {
  const scrolled = [];
  const focused = [];
  const node = { scrollIntoView: (opts) => scrolled.push(opts) };
  const field = { focus: (opts) => focused.push(opts) };
  assert.equal(bringPanel({ node, field, shown: false, wasShown: false, phase: "over" }), false);
  assert.equal(bringPanel({ node, field, shown: true, wasShown: false, phase: "title" }), false);
  assert.equal(bringPanel({ node, field, shown: true, wasShown: false, phase: "playing" }), false);
  assert.equal(bringPanel({ node, field, shown: true, wasShown: true, phase: "over" }), false);
  assert.equal(bringPanel({ shown: true, wasShown: false, phase: "over" }), false);
  assert.equal(bringPanel({ node, field, shown: true, wasShown: false, phase: "over" }), true);
  assert.equal(scrolled.length, 1);
  assert.equal(scrolled[0].block, "start");
  assert.equal(scrolled[0].behavior, "smooth");
  assert.deepEqual(focused, [{ preventScroll: true }]);
  assert.equal(bringPanel({ node, field, shown: true, wasShown: true, phase: "over" }), false);
  assert.equal(scrolled.length, 1);
});

test("bringPanel não anima quando o movimento some", () => {
  const scrolled = [];
  const node = { scrollIntoView: (opts) => scrolled.push(opts) };
  assert.equal(bringPanel({
    node,
    shown: true,
    wasShown: false,
    phase: "over",
    reduceMotion: true,
  }), true);
  assert.equal(scrolled[0].behavior, "auto");
});

test("a partida nomeia seed, pontos e eixos sem preencher o achado", () => {
  assert.equal(runFacts(null), "");
  assert.equal(runFacts({}), "");
  assert.equal(runFacts({ score: 3 }), "3");
  assert.equal(runFacts({ seed: 8 }), "seed 8");
  assert.equal(runFacts({ seed: 8, score: 12 }), "seed 8 · 12");
  assert.equal(runFacts({ seed: 8, score: 12, spawn: "spawn" }), "seed 8 · 12");
  assert.equal(runFacts({ seed: 8, score: 12, spawn: "dusk" }), "seed 8 · 12 · dusk");
  assert.equal(runFacts({ seed: 8, score: 12, spawn: "dusk", look: "dusk" }), "seed 8 · 12 · dusk");
  assert.equal(runFacts({ seed: 8, score: 12, spawn: "dusk", look: "calm" }), "seed 8 · 12 · dusk · calm");
  assert.equal(runFacts({ seed: 8, run: { score: 3, seed: 8 } }), "seed 8 · 3");
  assert.equal(runFacts({ seed: 8, spawn: "../x", look: "normal" }), "seed 8");
  const node = { textContent: "velho", hidden: false };
  assert.equal(applyRunFacts({ node, run: { seed: 8, score: 12, spawn: "dusk" } }), "seed 8 · 12 · dusk");
  assert.equal(node.textContent, "seed 8 · 12 · dusk");
  assert.equal(node.hidden, false);
  assert.equal(applyRunFacts({ node, run: { look: "contrast" } }), "");
  assert.equal(node.textContent, "");
  assert.equal(node.hidden, true);
  assert.equal(runFacts({ seed: 8 }).includes("Problema:"), false);
  assert.equal(runFacts({ seed: 8, score: 12, spawn: "dusk" }).includes("Evidência:"), false);
});

test("findingFile nomeia o markdown que a página pode baixar", () => {
  const file = findingFile("Problema: some no toque");
  assert.equal(file.name, FINDING_FILE);
  assert.equal(file.type, "text/markdown");
  assert.equal(file.text, "Problema: some no toque");
});

test("offerFinding copia quando a área de transferência escreve", async () => {
  const written = [];
  const saved = [];
  assert.equal(
    await offerFinding("Problema: some no toque", {
      clipboard: { writeText: async (text) => written.push(text) },
      save: (file) => saved.push(file),
    }),
    "copied",
  );
  assert.deepEqual(written, ["Problema: some no toque"]);
  assert.deepEqual(saved, []);
});

test("offerFinding baixa quando a área de transferência recusa", async () => {
  const saved = [];
  assert.equal(
    await offerFinding("Problema: some no toque", {
      clipboard: {
        writeText: async () => {
          throw new Error("denied");
        },
      },
      save: (file) => saved.push(file.name),
    }),
    "saved",
  );
  assert.deepEqual(saved, [FINDING_FILE]);
});

test("offerFinding baixa quando não há área de transferência", async () => {
  const saved = [];
  assert.equal(
    await offerFinding("Problema: some no toque", {
      save: (file) => saved.push(file.name),
    }),
    "saved",
  );
  assert.deepEqual(saved, [FINDING_FILE]);
});

test("offerFinding perde o achado quando ninguém recebe", async () => {
  assert.equal(await offerFinding("Problema: some no toque"), "missed");
});

test("copiar o achado preenchido tem forma; o vazio não finge", () => {
  const blank = composeFinding();
  assert.match(blank, /Problema:/);
  assert.match(blank, /Evidência:/);
  assert.match(blank, /Hipótese:/);
  assert.match(blank, /Medição:/);
  assert.equal(blank.includes("o dash"), false);
  const filled = composeFinding({
    problema: "o dash não comunica o contato",
    evidencia: "três sessões, pergunta se atravessou",
    hipotese: "o hitstop some no movimento",
    medicao: "repetir o graze com hitstop 5 e 2",
  });
  assert.match(filled, /o dash não comunica o contato/);
  assert.match(filled, /três sessões/);
});

test("a página nomeia o par sem fingir que alguém de fora escolheu", () => {
  assert.match(html, /id="mood"/);
  assert.match(html, /listMoods/);
  assert.match(html, /pairPatch/);
  assert.match(html, /matchingMood/);
  assert.match(html, /LOOK_LABELS/);
  assert.match(html, /SPAWN_LABELS/);
  assert.doesNotMatch(html, /outsider|aprovado|verified|alguém de fora/);
});
