// Impressão do estado, para comparar duas execuções.
//
// Serve à prova de determinismo: mesma seed e mesma sequência de intenções
// precisam produzir a mesma impressão. Não é fingerprint criptográfica e não
// substitui comparar os campos que importam quando um teste falha.

export function canonical(value) {
  if (value === null || typeof value !== "object") {
    return typeof value === "number" && !Number.isInteger(value)
      ? value.toFixed(6)
      : JSON.stringify(value ?? null);
  }
  if (Array.isArray(value)) {
    return `[${value.map(canonical).join(",")}]`;
  }
  const keys = Object.keys(value).sort();
  return `{${keys.map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
}

export function fingerprint(value) {
  const text = canonical(value);
  let high = 0xdeadbeef;
  let low = 0x41c6ce57;
  for (let index = 0; index < text.length; index += 1) {
    const code = text.charCodeAt(index);
    high = Math.imul(high ^ code, 2654435761) >>> 0;
    low = Math.imul(low ^ code, 1597334677) >>> 0;
  }
  high = (Math.imul(high ^ (high >>> 16), 2246822507) ^ Math.imul(low ^ (low >>> 13), 3266489909)) >>> 0;
  low = (Math.imul(low ^ (low >>> 16), 2246822507) ^ Math.imul(high ^ (high >>> 13), 3266489909)) >>> 0;
  return (high * 4294967296 + low).toString(16);
}
