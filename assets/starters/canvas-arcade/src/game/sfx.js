// Carrega os arquivos que o harness vê em public/sfx e os registra no mixer.
//
// Sem este passo, copiar um .wav preenchia o `roles` e o jogo continuava mudo:
// a legenda tocava, o buffer não. Arquivo no disco não é voz no contexto —
// mas sem consumidor o disco também não chega a ser ouvido.

import { SOUNDS } from "./audio.js";

export const SFX_FOLDER = "public/sfx";
export const SFX_EXTENSIONS = [".wav", ".ogg", ".mp3", ".flac"];

export async function loadRoleFiles(audio, options = {}) {
  const fetchFn = options.fetch;
  if (typeof fetchFn !== "function") return [];
  const base = options.base ?? SFX_FOLDER;
  const loaded = [];
  for (const id of Object.keys(SOUNDS)) {
    for (const ext of SFX_EXTENSIONS) {
      const url = `${base}/${id}${ext}`;
      try {
        const response = await fetchFn(url);
        if (!response || !response.ok) continue;
        const bytes = await response.arrayBuffer();
        const buffer = options.decode ? await options.decode(bytes, id) : bytes;
        if (buffer && audio.register(id, buffer)) {
          loaded.push({ id, url });
        }
        break;
      } catch {
        continue;
      }
    }
  }
  return loaded;
}
