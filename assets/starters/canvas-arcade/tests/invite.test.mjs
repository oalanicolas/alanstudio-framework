import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyFinding, applyInvite, applyNote, applyShare, composeFinding, inviteHref, inviteMode, INVITE_LABEL, seedHref } from "../src/core/invite.js";

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
  assert.match(html, /id="remap"/, "o convite não some o remapeamento");
  assert.match(html, /id="gameSpeed"/, "o convite não some a velocidade da partida");
  assert.match(html, /id="colorblind"/, "o convite não some a tinta estável");
  assert.doesNotMatch(html, /html\.invite\s+#remap/, "só a tabela some");
  assert.match(html, /id="finding"/);
  assert.match(html, /html\.invite\.finding\s+#finding/);
  assert.match(html, /id="finding-copy"/);
  assert.match(html, /id="finding-save"/);
  assert.match(html, /Copie ou grave/);
  assert.match(html, /anexa o candidato/);
  assert.match(html, /composeFinding/);
  assert.match(html, /playFinding/);
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
