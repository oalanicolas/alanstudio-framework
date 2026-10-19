// Métricas entre a imagem original e a convertida, sempre na mesma resolução.
// PSNR global e do pior bloco (a média esconde perda local) e, para normal maps,
// erro angular em graus depois de renormalizar. Entradas no formato de png.js.

const MAX_DB = 120; // imagens idênticas: o PSNR é infinito; registramos 120 dB, como o ImageMagick

function amostra(img) {
  const max = img.bitDepth === 16 ? 65535 : 255;
  return (i) => img.data[i] / max;
}

function conferir(a, b) {
  if (a.width !== b.width || a.height !== b.height) {
    throw new Error(`resoluções diferentes: ${a.width}×${a.height} e ${b.width}×${b.height}`);
  }
}

const db = (mse) => (mse <= 0 ? MAX_DB : Math.min(MAX_DB, 10 * Math.log10(1 / mse)));

/**
 * PSNR (dB) sobre os canais pedidos, global e por bloco.
 * channels: índices nos dois lados ([0,1,2] = RGB). canalB permite comparar o canal G de um PNG
 * (canal 1) com uma imagem de 1 canal (canal 0): passe pares [[1, 0]].
 * Retorna { psnr, worstBlock, p01Block, blocks, block }.
 */
export function psnr(a, b, { channels = [0, 1, 2], block = 64 } = {}) {
  conferir(a, b);
  const pares = channels.map((c) => (Array.isArray(c) ? c : [c, c]));
  for (const [ca, cb] of pares) {
    if (ca >= a.channels || cb >= b.channels) throw new Error(`canal inexistente (${ca}/${cb})`);
  }
  const va = amostra(a);
  const vb = amostra(b);
  const { width, height } = a;
  const bx = Math.ceil(width / block);
  const by = Math.ceil(height / block);
  const somaBloco = new Float64Array(bx * by);
  const nBloco = new Float64Array(bx * by);
  let soma = 0;
  for (let y = 0; y < height; y++) {
    const linhaBloco = Math.floor(y / block) * bx;
    for (let x = 0; x < width; x++) {
      const p = y * width + x;
      let e = 0;
      for (const [ca, cb] of pares) {
        const d = va(p * a.channels + ca) - vb(p * b.channels + cb);
        e += d * d;
      }
      soma += e;
      const k = linhaBloco + Math.floor(x / block);
      somaBloco[k] += e;
      nBloco[k] += pares.length;
    }
  }
  const valores = [];
  for (let k = 0; k < somaBloco.length; k++) if (nBloco[k]) valores.push(db(somaBloco[k] / nBloco[k]));
  valores.sort((x, y) => x - y);
  return {
    psnr: db(soma / (width * height * pares.length)),
    worstBlock: valores[0],
    p01Block: valores[Math.floor(valores.length * 0.01)],
    blocks: valores.length,
    block,
  };
}

/**
 * Erro angular (graus) entre dois normal maps codificados em [0,1] → [-1,1].
 * z: "stored" usa o canal B gravado; "reconstruct" refaz z = sqrt(1 - x² - y²), como faz o shader
 * de um formato de dois canais (BC5/EAC_RG). Texels com vetor quase nulo são ignorados.
 * Retorna { mean, p99, max, worstBlockMean, ignored, block }.
 */
export function normalAngle(a, b, { z = "stored", block = 64 } = {}) {
  conferir(a, b);
  const va = amostra(a);
  const vb = amostra(b);
  const { width, height } = a;
  const vetor = (v, img, p) => {
    const x = v(p * img.channels) * 2 - 1;
    const y = v(p * img.channels + 1) * 2 - 1;
    const zz = z === "reconstruct" || img.channels < 3 ? Math.sqrt(Math.max(0, 1 - x * x - y * y)) : v(p * img.channels + 2) * 2 - 1;
    const n = Math.hypot(x, y, zz);
    return n < 1e-3 ? null : [x / n, y / n, zz / n];
  };
  const bx = Math.ceil(width / block);
  const by = Math.ceil(height / block);
  const somaBloco = new Float64Array(bx * by);
  const nBloco = new Float64Array(bx * by);
  const histo = new Float64Array(1801); // décimos de grau, 0..180
  let soma = 0;
  let n = 0;
  let ignorados = 0;
  let max = 0;
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const p = y * width + x;
      const na = vetor(va, a, p);
      const nb = vetor(vb, b, p);
      if (!na || !nb) {
        ignorados++;
        continue;
      }
      const dot = Math.min(1, Math.max(-1, na[0] * nb[0] + na[1] * nb[1] + na[2] * nb[2]));
      const ang = (Math.acos(dot) * 180) / Math.PI;
      soma += ang;
      n++;
      if (ang > max) max = ang;
      histo[Math.min(1800, Math.round(ang * 10))]++;
      const k = Math.floor(y / block) * bx + Math.floor(x / block);
      somaBloco[k] += ang;
      nBloco[k]++;
    }
  }
  let acumulado = 0;
  let p99 = 0;
  for (let i = 0; i < histo.length; i++) {
    acumulado += histo[i];
    if (acumulado >= n * 0.99) {
      p99 = i / 10;
      break;
    }
  }
  let pior = 0;
  for (let k = 0; k < somaBloco.length; k++) if (nBloco[k]) pior = Math.max(pior, somaBloco[k] / nBloco[k]);
  return { mean: n ? soma / n : 0, p99, max, worstBlockMean: pior, ignored: ignorados, block };
}
