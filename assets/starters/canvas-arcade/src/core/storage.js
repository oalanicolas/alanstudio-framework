// Armazenamento com gravação verificada.
//
// `localStorage` falha de formas reais: cota cheia, modo privativo, permissão
// negada, valor truncado por outra aba. Nada disso pode derrubar o jogo nem
// apagar o que já estava salvo. A gravação escreve em uma chave temporária,
// relê, compara e só então promove — e um valor ilegível é preservado em
// `<chave>.broken` em vez de descartado. Se a cópia falhar, a chave original
// fica intacta e novas gravações são recusadas até que ela possa ser preservada.
// A outra aba dispara `storage`. Sem isto esta página
// ficava com o look e o mix velhos. Ouvir não é aba
// fechada; `trusted` continua falso.

export function foreignKey(event, prefix, key) {
  if (!event || typeof event.key !== "string") return false;
  if (typeof prefix !== "string" || !prefix) return false;
  if (typeof key !== "string" || !key) return false;
  return event.key === `${prefix}:${key}`;
}

export function memoryStorage(initial = {}) {
  const data = new Map(Object.entries(initial));
  return {
    persistent: false,
    prefix: "",
    get(key) {
      return data.has(key) ? data.get(key) : null;
    },
    set(key, value) {
      data.set(key, String(value));
    },
    remove(key) {
      data.delete(key);
    },
    keys() {
      return [...data.keys()];
    },
  };
}

export function browserStorage(prefix) {
  const namespace = `${prefix}:`;
  let backend = null;
  try {
    if (typeof localStorage !== "undefined") {
      const probe = `${namespace}__probe`;
      localStorage.setItem(probe, "1");
      localStorage.removeItem(probe);
      backend = localStorage;
    }
  } catch {
    backend = null;
  }
  if (!backend) return { ...memoryStorage(), prefix };
  return {
    persistent: true,
    prefix,
    get(key) {
      try {
        return backend.getItem(namespace + key);
      } catch {
        return null;
      }
    },
    set(key, value) {
      backend.setItem(namespace + key, String(value));
    },
    remove(key) {
      try {
        backend.removeItem(namespace + key);
      } catch {
        /* remover é melhor esforço */
      }
    },
    keys() {
      try {
        return Object.keys(backend)
          .filter((key) => key.startsWith(namespace))
          .map((key) => key.slice(namespace.length));
      } catch {
        return [];
      }
    },
  };
}

export function writeJson(storage, key, value) {
  let text;
  try {
    text = JSON.stringify(value);
  } catch (error) {
    return { ok: false, reason: "unserializable", detail: String(error) };
  }
  const staging = `${key}.tmp`;
  try {
    const current = readJson(storage, key);
    if (current.status === "unreadable" && !current.backupSaved) {
      return { ok: false, reason: "backup_failed", detail: current.backupError };
    }
    storage.set(staging, text);
    if (storage.get(staging) !== text) {
      storage.remove(staging);
      return { ok: false, reason: "verification_failed" };
    }
    storage.set(key, text);
    storage.remove(staging);
  } catch (error) {
    storage.remove(staging);
    return { ok: false, reason: "write_failed", detail: String(error) };
  }
  return { ok: true };
}

export function readJson(storage, key) {
  const raw = storage.get(key);
  if (raw === null || raw === undefined) return { value: null, status: "absent" };
  try {
    const value = JSON.parse(raw);
    if (value === null || typeof value !== "object") {
      throw new TypeError("conteúdo não é objeto");
    }
    return { value, status: "loaded" };
  } catch (error) {
    // Preserva o original: um save ilegível para este código pode ser legível
    // para uma investigação ou para uma versão futura.
    try {
      storage.set(`${key}.broken`, raw);
      if (storage.get(`${key}.broken`) !== raw) throw new Error("backup não persistiu");
      return { value: null, status: "unreadable", detail: String(error), backupSaved: true };
    } catch (backupError) {
      return {
        value: null, status: "unreadable", detail: String(error),
        backupSaved: false, backupError: String(backupError),
      };
    }
  }
}
