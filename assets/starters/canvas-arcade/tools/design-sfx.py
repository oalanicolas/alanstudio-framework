#!/usr/bin/env python3
"""Gera os seis papéis em public/sfx/. Design contemporâneo, não 8-bit.

Cada voz é seno ou ruído filtrado com envelope. Quadrada, dente e jsfxr
ficam de fora: o piso do estúdio recusa essa estética como padrão.
O arquivo é original deste starter (CC0-1.0). O harness não ouve o resultado.
"""
from __future__ import annotations

import json
import math
import struct
import wave
from pathlib import Path

RATE = 44100
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "sfx"
ROLES = ("dash", "graze", "collect", "bank", "hit", "over")


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


VOICES = {
    "dash": (0.18, dash, 0.55, 0.18),
    "graze": (0.07, graze, 0.7, 0.35),
    "collect": (0.22, collect, None, None),
    "bank": (0.42, bank, None, None),
    "hit": (0.28, hit, 0.35, 0.22),
    "over": (0.55, over, None, None),
}


def design(name: str) -> list[float]:
    seconds, voice, hp, lp = VOICES[name]
    samples = render(seconds, voice)
    if hp is not None:
        samples = highpass(samples, hp)
    if lp is not None:
        samples = lowpass(samples, lp)
    peak = max((abs(sample) for sample in samples), default=1.0)
    scale = 0.86 / peak if peak else 0.0
    return [sample * scale for sample in samples]


def credits_text(name: str) -> str:
    return (
        f"{name}.wav — design original do starter Canvas Arcade, 2026-09-09.\n"
        "Gerado por tools/design-sfx.py. Autor: Alan Studios Framework. "
        "Licença: CC0-1.0. Sem samples de terceiros, sem jsfxr, sem Kenney, "
        "sem chiptune.\n"
        f"Consumidor: src/game/audio.js (papel `{name}`) via src/game/sfx.js.\n"
    )


def write_receipts(names: list[str]) -> None:
    records = []
    for name in names:
        (OUT / f"{name}.credits.txt").write_text(credits_text(name), encoding="utf-8")
        records.append({
            "src": f"{name}.wav",
            "key": name,
            "title": f"Canvas Arcade / {name}",
            "author": "Alan Studios Framework",
            "license": "CC0-1.0",
            "origin": "tools/design-sfx.py",
            "note": "design contemporâneo original; não é gravação de campo",
        })
    (OUT / "sources.json").write_text(
        json.dumps({"schema_version": 1, "files": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in ROLES:
        write_wav(OUT / f"{name}.wav", design(name))
    write_receipts(list(ROLES))
    print(f"{len(ROLES)} papéis em {OUT}")


if __name__ == "__main__":
    main()
