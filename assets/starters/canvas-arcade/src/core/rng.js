// Gerador determinístico e serializável.
//
// O estado do jogo guarda `rngState`, não o objeto: retomar um save ou repetir
// uma sequência de entradas precisa reproduzir exatamente os mesmos números.
// Aceitar um parâmetro `seed` não prova determinismo; o teste que compara duas
// execuções com a mesma seed prova.

export function createRng(seed, state = null) {
  let current = (state === null ? hashSeed(seed) : state) >>> 0;
  return {
    get seed() {
      return seed;
    },
    get state() {
      return current;
    },
    next() {
      current = (current + 0x6d2b79f5) >>> 0;
      let value = current;
      value = Math.imul(value ^ (value >>> 15), value | 1);
      value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
      return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
    },
    int(bound) {
      return Math.floor(this.next() * bound);
    },
    range(min, max) {
      return min + this.next() * (max - min);
    },
    pick(items) {
      return items[this.int(items.length)];
    },
  };
}

// Aceita seed textual para que uma partida seja compartilhável por nome.
export function hashSeed(seed) {
  if (typeof seed === "number" && Number.isFinite(seed)) {
    return (seed >>> 0) || 1;
  }
  const text = String(seed ?? "");
  let value = 0x811c9dc5;
  for (let index = 0; index < text.length; index += 1) {
    value ^= text.charCodeAt(index);
    value = Math.imul(value, 0x01000193) >>> 0;
  }
  return value || 1;
}
