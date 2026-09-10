// Empacota a árvore jogável em dist/.
//
// Copia o que outra pessoa precisa para servir o jogo sem a pasta de
// desenvolvimento. Não minifica, não prova execução em outra máquina e não
// autoriza publicar. O harness lê a existência deste passo; `shipped` continua
// falso.

import { execFileSync } from "node:child_process";
import { cp, mkdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const DIST = join(ROOT, "dist");
const ENTRIES = ["index.html", "src", "data", "public", "CREDITS.md", "tools/serve.mjs"];

await rm(DIST, { recursive: true, force: true });
await mkdir(join(DIST, "tools"), { recursive: true });

for (const relative of ENTRIES) {
  const source = join(ROOT, relative);
  try {
    await stat(source);
  } catch {
    continue;
  }
  await cp(source, join(DIST, relative), { recursive: true });
}

const pack = JSON.parse(await readFile(join(ROOT, "package.json"), "utf8"));
await writeFile(
  join(DIST, "package.json"),
  `${JSON.stringify(
    {
      name: pack.name,
      private: true,
      type: "module",
      description: "Artefato exportado. Serve; não desenvolve.",
      engines: pack.engines ?? { node: ">=20" },
      scripts: { serve: "node tools/serve.mjs" },
    },
    null,
    2,
  )}\n`,
);

await writeFile(
  join(DIST, "README.md"),
  `# ${pack.description?.split("—")[0]?.trim() || pack.name}

Árvore exportada por \`npm run build\`. Não é o repositório de desenvolvimento:
não traz testes, orçamento nem este export.

Node 20 ou mais novo. Não rode \`npm install\`: este artefato não tem
dependências. Não abra \`index.html\` por \`file://\`.

\`\`\`sh
node tools/serve.mjs
\`\`\`

Módulos ES não carregam por \`file://\`. Servir esta pasta é o que a torna
jogável. O serve nomeia esta pasta como árvore exportada. Anunciar a URL
da rede se a máquina tiver outro endereço IPv4 não é outra máquina.
Servir o dist/ na máquina de quem exportou também não. Este README não
afirma que outra máquina já executou o artefato.
`,
);

function gitHead() {
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], { cwd: ROOT, encoding: "utf8" }).trim();
  } catch {
    return null;
  }
}

await writeFile(
  join(DIST, "VERSION.json"),
  `${JSON.stringify(
    {
      name: pack.name,
      version: pack.version,
      git_head: gitHead(),
      scope: "Identidade do artefato. Não prova outra máquina nem reprodução bit a bit.",
    },
    null,
    2,
  )}\n`,
);

console.log(`Artefato em ${DIST}`);
