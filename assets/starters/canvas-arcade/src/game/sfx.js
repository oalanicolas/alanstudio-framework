// Carrega os arquivos que o harness vê em public/sfx e os registra no mixer.
//
// Sem este passo, copiar um .wav preenchia o `roles` e o jogo continuava mudo:
// a legenda tocava, o buffer não. Arquivo no disco não é voz no contexto —
// mas sem consumidor o disco também não chega a ser ouvido.
//
// Os stems sobem juntos. Em série, collect esperava dash+land+graze
// terminarem — a abertura da sessão pedia um papel que ainda nem
// tinha fetch. Extensão seguinte só entra se a atual falhou — fetch
// 404 ou decode nulo. Wav que decodifica não pede ogg. Decode nulo
// no wav não esconde o ogg nem some o pedido. Paralelo não é mix ouvido.

import { SOUNDS } from "./audio.js";

export const SFX_FOLDER = "public/sfx";
export const SFX_EXTENSIONS = [".wav", ".ogg", ".mp3", ".flac"];

export async function loadRoleFiles(audio, options = {}) {
  const fetchFn = options.fetch;
  if (typeof fetchFn !== "function") return [];
  const base = options.base ?? SFX_FOLDER;
  const jobs = Object.keys(SOUNDS).flatMap((id) => (
    [id, `${id}-b`].map((stem) => ({ id, stem, variant: stem !== id }))
  ));
  const results = await Promise.all(
    jobs.map((job) => loadStem(job, audio, { ...options, base, fetch: fetchFn })),
  );
  return results.filter(Boolean);
}

async function loadStem(job, audio, options) {
  const fetchFn = options.fetch;
  const base = options.base;
  for (const ext of SFX_EXTENSIONS) {
    const url = `${base}/${job.stem}${ext}`;
    try {
      const response = await fetchFn(url);
      if (!response || !response.ok) continue;
      const bytes = await response.arrayBuffer();
      const buffer = options.decode ? await options.decode(bytes, job.id) : bytes;
      if (buffer && audio.register(job.id, buffer)) {
        return { id: job.id, url, variant: job.variant };
      }
      // Fetch ok com decode nulo não esgota o stem: a próxima
      // extensão ainda pode falar. Sem isto o wav ilegível
      // escondia o ogg e o pedido.
      continue;
    } catch {
      continue;
    }
  }
  // Variante ausente não é lacuna do papel. O primário que esgota
  // as extensões marca o pedido — sem isto o 404 só aparecia no play.
  if (!job.variant) audio.fail?.(job.id);
  return null;
}
