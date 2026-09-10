#!/usr/bin/env python3
"""Gera os papéis do verbo e a cama em public/sfx/. Design contemporâneo, não 8-bit.

Cada voz é seno ou ruído filtrado com envelope. Quadrada, dente e jsfxr
ficam de fora: o piso do estúdio recusa essa estética como padrão.
`--from` reescreve um papel que o mixer já toca; `--as` desloca a voz
sem pedir a receita de cabeça. O arquivo é original deste starter
(CC0-1.0). O harness não ouve o resultado.
"""
from __future__ import annotations

import json
import math
import struct
import sys
import wave
from pathlib import Path

RATE = 44100
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "sfx"
ROLES = ("dash", "graze", "collect", "missed", "bank", "hit", "over", "close", "live", "stir", "bed")
INTENTS = {
    "brighter": "sobe o tom e abre o brilho",
    "darker": "desce o tom e fecha o grave",
    "tighter": "encurta a cauda",
}


def clamp(value: float) -> int:
    return max(-32767, min(32767, int(value * 32767)))


def write_wav(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(b"".join(struct.pack("<h", clamp(sample)) for sample in samples))


def envelope(index: int, total: int, attack: float, release: float) -> float:
    t = index / RATE
    length = total / RATE
    if t < attack:
        return t / attack if attack else 1.0
    tail = length - release
    if t > tail:
        return max(0.0, (length - t) / release) if release else 0.0
    return 1.0


def noise(index: int, seed: int) -> float:
    x = math.sin((index + 1) * 12.9898 + seed * 78.233) * 43758.5453
    return (x - math.floor(x)) * 2.0 - 1.0


def lowpass(samples: list[float], alpha: float) -> list[float]:
    acc = 0.0
    out = []
    for sample in samples:
        acc += alpha * (sample - acc)
        out.append(acc)
    return out


def highpass(samples: list[float], alpha: float) -> list[float]:
    acc = 0.0
    previous = 0.0
    out = []
    for sample in samples:
        acc = alpha * (acc + sample - previous)
        previous = sample
        out.append(acc)
    return out


def render(seconds: float, voice) -> list[float]:
    total = max(1, int(RATE * seconds))
    return [voice(index, total) for index in range(total)]


def dash(index: int, total: int) -> float:
    t = index / RATE
    whoosh = noise(index, 3) * envelope(index, total, 0.008, 0.12)
    sweep = math.sin(2 * math.pi * (420 - 260 * t) * t) * envelope(index, total, 0.01, 0.1)
    return 0.34 * whoosh + 0.22 * sweep


def graze(index: int, total: int) -> float:
    t = index / RATE
    tick = math.sin(2 * math.pi * 1860 * t) * envelope(index, total, 0.002, 0.05)
    air = noise(index, 11) * envelope(index, total, 0.001, 0.04)
    return 0.18 * tick + 0.08 * air


def collect(index: int, total: int) -> float:
    t = index / RATE
    a = math.sin(2 * math.pi * 523.25 * t) * envelope(index, total, 0.006, 0.16)
    b = math.sin(2 * math.pi * 783.99 * t + 0.3) * envelope(index, total, 0.01, 0.18)
    return 0.28 * a + 0.22 * b


def missed(index: int, total: int) -> float:
    t = index / RATE
    drop = math.sin(2 * math.pi * (196.0 - 80 * t) * t) * envelope(index, total, 0.003, 0.06)
    air = noise(index, 37) * envelope(index, total, 0.001, 0.035)
    return 0.14 * drop + 0.035 * air


def bank(index: int, total: int) -> float:
    t = index / RATE
    chord = (
        math.sin(2 * math.pi * 392.0 * t)
        + 0.7 * math.sin(2 * math.pi * 493.88 * t)
        + 0.5 * math.sin(2 * math.pi * 587.33 * t)
    )
    return 0.22 * chord * envelope(index, total, 0.012, 0.28)


def hit(index: int, total: int) -> float:
    t = index / RATE
    thud = math.sin(2 * math.pi * (110 - 40 * t) * t) * envelope(index, total, 0.004, 0.2)
    crack = noise(index, 7) * envelope(index, total, 0.001, 0.06)
    return 0.42 * thud + 0.2 * crack


def over(index: int, total: int) -> float:
    t = index / RATE
    fall = math.sin(2 * math.pi * (329.63 - 80 * t) * t) * envelope(index, total, 0.02, 0.32)
    fifth = math.sin(2 * math.pi * (246.94 - 50 * t) * t) * envelope(index, total, 0.03, 0.34)
    return 0.26 * fall + 0.18 * fifth


def close(index: int, total: int) -> float:
    t = index / RATE
    tap = math.sin(2 * math.pi * 392.0 * t) * envelope(index, total, 0.003, 0.07)
    click = noise(index, 23) * envelope(index, total, 0.001, 0.025)
    return 0.18 * tap + 0.05 * click


def live(index: int, total: int) -> float:
    t = index / RATE
    rise = math.sin(2 * math.pi * (246.94 + 180 * t) * t) * envelope(index, total, 0.008, 0.10)
    air = noise(index, 29) * envelope(index, total, 0.004, 0.08)
    return 0.22 * rise + 0.06 * air


def stir(index: int, total: int) -> float:
    t = index / RATE
    settle = math.sin(2 * math.pi * (277.18 - 50 * t) * t) * envelope(index, total, 0.006, 0.08)
    air = noise(index, 31) * envelope(index, total, 0.002, 0.06)
    return 0.20 * settle + 0.045 * air


def bed(index: int, total: int) -> float:
    # Ciclos inteiros em 4s: a junta do loop não pede envelope.
    t = index / RATE
    root = math.sin(2 * math.pi * 220.0 * t)
    fifth = math.sin(2 * math.pi * 330.0 * t)
    air = noise(index, 19)
    return 0.12 * root + 0.08 * fifth + 0.02 * air


VOICES = {
    "dash": (0.18, dash, 0.55, 0.18),
    "graze": (0.07, graze, 0.7, 0.35),
    "collect": (0.22, collect, None, None),
    "missed": (0.09, missed, 0.48, 0.32),
    "bank": (0.42, bank, None, None),
    "hit": (0.28, hit, 0.35, 0.22),
    "over": (0.55, over, None, None),
    "close": (0.08, close, 0.62, 0.28),
    "live": (0.14, live, 0.58, 0.24),
    "stir": (0.12, stir, 0.54, 0.26),
    "bed": (4.0, bed, None, 0.12),
}


def normalize(samples: list[float]) -> list[float]:
    peak = max((abs(sample) for sample in samples), default=1.0)
    scale = 0.86 / peak if peak else 0.0
    return [sample * scale for sample in samples]


def design(name: str) -> list[float]:
    seconds, voice, hp, lp = VOICES[name]
    samples = render(seconds, voice)
    if hp is not None:
        samples = highpass(samples, hp)
    if lp is not None:
        samples = lowpass(samples, lp)
    return normalize(samples)


def apply_intent(samples: list[float], intent: str | None) -> list[float]:
    if not intent:
        return samples
    if intent == "brighter":
        return normalize(highpass(detune(samples, 1.18), 0.55))
    if intent == "darker":
        return normalize(lowpass(detune(samples, 0.84), 0.22))
    if intent == "tighter":
        cut = max(8, int(len(samples) * 0.62))
        out = list(samples[:cut])
        fade = max(1, int(len(out) * 0.12))
        for index in range(fade):
            out[-fade + index] *= index / fade
        return normalize(out)
    return samples


def detune(samples: list[float], factor: float) -> list[float]:
    length = max(1, int(len(samples) / factor))
    out = []
    last = len(samples) - 1
    for index in range(length):
        source = index * factor
        low = min(int(source), last)
        high = min(low + 1, last)
        frac = source - low
        out.append(samples[low] * (1.0 - frac) + samples[high] * frac)
    return out


def credits_text(name: str, intent: str | None = None) -> str:
    role = name[:-2] if name.endswith("-b") else name
    kind = "variante para evitar fadiga" if name.endswith("-b") else "design original"
    shift = f" Intenção {intent}: {INTENTS[intent]}." if intent and intent in INTENTS else ""
    return (
        f"{name}.wav — {kind} do starter Canvas Arcade, 2026-09-09.\n"
        "Gerado por tools/design-sfx.py. Autor: Alan Studios Framework. "
        "Licença: CC0-1.0. Sem samples de terceiros, sem jsfxr, sem Kenney, "
        f"sem chiptune.{shift}\n"
        f"Consumidor: src/game/audio.js (papel `{role}`) via src/game/sfx.js.\n"
    )


def write_receipts(names: list[str], merge: bool = False, intent: str | None = None) -> None:
    records = []
    if merge and (OUT / "sources.json").is_file():
        try:
            previous = json.loads((OUT / "sources.json").read_text(encoding="utf-8"))
            kept = previous.get("files") if isinstance(previous, dict) else None
            if isinstance(kept, list):
                skip = set(names)
                records = [
                    item for item in kept
                    if isinstance(item, dict) and item.get("key") not in skip
                ]
        except (OSError, json.JSONDecodeError, TypeError):
            records = []
    note = "design contemporâneo original; não é gravação de campo"
    if intent and intent in INTENTS:
        note = f"{note}; intenção {intent}"
    for name in names:
        (OUT / f"{name}.credits.txt").write_text(credits_text(name, intent), encoding="utf-8")
        records.append({
            "src": f"{name}.wav",
            "key": name,
            "title": f"Canvas Arcade / {name}",
            "author": "Alan Studios Framework",
            "license": "CC0-1.0",
            "origin": "tools/design-sfx.py",
            "note": note,
        })
    (OUT / "sources.json").write_text(
        json.dumps({"schema_version": 1, "files": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    role = None
    intent = None
    index = 0
    while index < len(argv):
        flag = argv[index]
        if flag == "--from" and index + 1 < len(argv):
            role = argv[index + 1].strip()
            index += 2
            continue
        if flag == "--as" and index + 1 < len(argv):
            intent = argv[index + 1].strip()
            index += 2
            continue
        print(
            "uso: python3 tools/design-sfx.py [--from <papel>] [--as brighter|darker|tighter]",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return role or None, intent or None


def write_role(name: str, intent: str | None = None) -> list[str]:
    samples = apply_intent(design(name), intent)
    write_wav(OUT / f"{name}.wav", samples)
    write_wav(OUT / f"{name}-b.wav", detune(samples, 1.07))
    return [name, f"{name}-b"]


def main(argv: list[str] | None = None) -> None:
    role, intent = parse_args(sys.argv[1:] if argv is None else argv)
    if intent and not role:
        print("--as precisa de --from: a intenção desloca um papel que o mixer já toca.", file=sys.stderr)
        raise SystemExit(2)
    if role and role not in ROLES:
        print(f"só --from de papel: {role} não é voz do verbo.", file=sys.stderr)
        raise SystemExit(2)
    if intent and intent not in INTENTS:
        print(f"intenção desconhecida: {intent}. use {'|'.join(INTENTS)}.", file=sys.stderr)
        raise SystemExit(2)
    OUT.mkdir(parents=True, exist_ok=True)
    targets = (role,) if role else ROLES
    names = []
    for name in targets:
        names.extend(write_role(name, intent))
    write_receipts(names, merge=bool(role), intent=intent)
    if role:
        print(f"papel {role}: public/sfx/{role}.wav")
        if intent:
            print(f"intenção {intent} a partir de {role}: {INTENTS[intent]}.")
        else:
            print(f"cópia de {role}: a voz é a mesma até alguém deslocar.")
        return
    print(f"{len(names)} arquivos em {OUT}")


if __name__ == "__main__":
    main()
