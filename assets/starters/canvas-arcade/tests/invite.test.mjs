import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyInvite, inviteMode, INVITE_LABEL } from "../src/core/invite.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");

test("só invite=1 liga o modo; outro valor não esconde a tabela", () => {
  assert.equal(inviteMode("?invite=1"), true);
  assert.equal(inviteMode("invite=1"), true);
  assert.equal(inviteMode("?invite=1&look=dusk"), true);
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
