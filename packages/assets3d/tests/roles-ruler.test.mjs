import test from "node:test";
import assert from "node:assert/strict";
import { roleFor } from "../src/roles.js";
import { DEFAULT_PROFILE, resolveRuler } from "../src/ruler.js";

test("papel pelo sufixo, regras do projeto antes das padrão, e cor quando não reconhece", () => {
  assert.equal(roleFor("pedra/Wall_N.png").role, "normal");
  assert.equal(roleFor("Wall_ORM.png").role, "material");
  assert.equal(roleFor("Lava_EM.png").role, "emissive");
  assert.equal(roleFor("Leaf_Opacity.png").role, "mask");
  assert.equal(roleFor("Wall_BC.png").role, "color");
  const r = roleFor("strange_name.png");
  assert.equal(r.role, "color");
  assert.equal(r.guessed, true);
  assert.equal(roleFor("Hero_D.png", [{ role: "material", pattern: "^hero_d$" }]).role, "material");
});

test("régua: padrão é sem perda visível, cor cai para PSNR sem ssimulacra2, ajuste do projeto vence", () => {
  const r = resolveRuler();
  assert.equal(r.profile, DEFAULT_PROFILE);
  assert.equal(r.color.ssimulacra2, 90);
  const sem = resolveRuler({}, { hasSsimulacra2: false });
  assert.equal(sem.color.ssimulacra2, null);
  assert.ok(sem.color.psnr >= 50);
  assert.equal(resolveRuler({ normal: { meanDeg: 0.2 } }).normal.meanDeg, 0.2);
  assert.equal(resolveRuler({}, { profile: "lado-a-lado" }).color.ssimulacra2, 80);
  assert.throws(() => resolveRuler({}, { profile: "rapido" }), /perfil de régua desconhecido/);
});

test("o ajuste do projeto vence a reserva por PSNR quando falta o ssimulacra2", () => {
  const r = resolveRuler({ color: { psnr: 200 } }, { hasSsimulacra2: false });
  assert.equal(r.color.psnr, 200);
  assert.equal(r.color.ssimulacra2, null);
});
