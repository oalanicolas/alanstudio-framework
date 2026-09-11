// Superfície de remapeamento na página. O código já persistia `bindings`;
// sem botão, só o console trocava a tecla. Toque e controle não entram
// aqui. Trocar no stub não é sessão observada.
// A escuta precisa comer a tecla. Sem a captura, Espaço
// avançava enquanto a pessoa escolhia o verbo.
// Tecla no disco não é felt.

import { actionLabels, keyLabel } from "./keys.js";

export const REMAP_ACTIONS = ["left", "right", "dash", "bank", "pause", "reset"];

export const REMAP_LABELS = {
  left: "Esquerda",
  right: "Direita",
  dash: "Avançar",
  bank: "Guardar",
  pause: "Pausar",
  reset: "Reiniciar",
};

export function applyRebind(bindings, action, code) {
  if (!bindings || !(action in bindings)) return bindings;
  if (typeof code !== "string" || !code.trim()) return bindings;
  return { ...bindings, [action]: [code] };
}

export function remapRows(bindings) {
  return REMAP_ACTIONS.map((action) => ({
    action,
    label: REMAP_LABELS[action],
    keys: actionLabels(bindings, action),
  }));
}

export function rowCaption(row, listening = false) {
  if (listening) return `${row.label}: pressione…`;
  const keys = row.keys.length ? row.keys.join(" / ") : "—";
  return `${row.label}: ${keys}`;
}

export function captureKey(target, onCode) {
  if (!target || typeof target.addEventListener !== "function") return () => {};
  function onKey(event) {
    const code = event && typeof event.code === "string" ? event.code : "";
    if (!code) return;
    if (typeof event.preventDefault === "function") event.preventDefault();
    if (typeof event.stopImmediatePropagation === "function") event.stopImmediatePropagation();
    target.removeEventListener("keydown", onKey, true);
    onCode(code);
  }
  target.addEventListener("keydown", onKey, true);
  return () => target.removeEventListener("keydown", onKey, true);
}

export function mountRemap(host, options = {}) {
  if (!host || typeof host.replaceChildren !== "function") return () => {};
  const target = options.target;
  let cancel = () => {};
  let listening = "";

  function paint() {
    const bindings = options.getBindings ? options.getBindings() : {};
    host.replaceChildren();
    for (const row of remapRows(bindings)) {
      const button = options.document?.createElement
        ? options.document.createElement("button")
        : { type: "button", dataset: {}, textContent: "", addEventListener() {} };
      button.type = "button";
      button.dataset.action = row.action;
      button.textContent = rowCaption(row, listening === row.action);
      button.addEventListener("click", () => {
        cancel();
        listening = row.action;
        paint();
        cancel = captureKey(target, (code) => {
          listening = "";
          if (typeof options.setBindings === "function") {
            options.setBindings(applyRebind(bindings, row.action, code));
          }
          paint();
        });
      });
      host.appendChild(button);
    }
  }

  paint();
  return {
    refresh: paint,
    dispose() {
      cancel();
      listening = "";
    },
  };
}

export { keyLabel };
