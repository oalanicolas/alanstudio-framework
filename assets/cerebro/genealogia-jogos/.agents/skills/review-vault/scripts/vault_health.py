#!/usr/bin/env python3
"""Read-only Obsidian vault health report using only Python's standard library."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def visible_markdown_files(vault: Path) -> list[Path]:
    return sorted(
        path
        for path in vault.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(vault).parts)
    )


def clean_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    return target[:-3] if target.lower().endswith(".md") else target


def analyze(vault: Path) -> dict[str, object]:
    notes = visible_markdown_files(vault)
    canvases = sorted(
        path
        for path in vault.rglob("*.canvas")
        if not any(part.startswith(".") for part in path.relative_to(vault).parts)
    )
    linkable_files = notes + canvases
    by_path = {
        path.relative_to(vault).with_suffix("").as_posix(): path
        for path in linkable_files
    }
    by_name: dict[str, list[Path]] = defaultdict(list)
    for path in linkable_files:
        by_name[path.stem].append(path)

    outgoing: dict[Path, list[str]] = {}
    incoming: Counter[Path] = Counter()
    broken: list[dict[str, str]] = []
    total_links = 0

    for path in notes:
        text = path.read_text(encoding="utf-8", errors="replace")
        targets = [clean_target(match) for match in WIKILINK.findall(text)]
        targets = [target for target in targets if target]
        outgoing[path] = targets
        total_links += len(targets)

        for target in targets:
            resolved = by_path.get(target)
            if resolved is None and "/" not in target:
                matches = by_name.get(target, [])
                resolved = matches[0] if len(matches) == 1 else None
            if resolved is None:
                broken.append(
                    {
                        "source": path.relative_to(vault).as_posix(),
                        "target": target,
                    }
                )
            elif resolved.suffix == ".md":
                incoming[resolved] += 1

    connection_count = {
        path: len(outgoing[path]) + incoming[path]
        for path in notes
    }
    orphans = [path for path, count in connection_count.items() if count == 0]
    weak = [path for path, count in connection_count.items() if count == 1]
    hubs = sorted(connection_count.items(), key=lambda item: (-item[1], item[0].name))[:10]

    relative = lambda path: path.relative_to(vault).as_posix()
    return {
        "vault": str(vault),
        "notes": len(notes),
        "links": total_links,
        "broken_links": broken,
        "orphan_notes": [relative(path) for path in orphans],
        "weakly_connected_notes": [relative(path) for path in weak],
        "hubs": [
            {"note": relative(path), "connections": count}
            for path, count in hubs
        ],
    }


def print_markdown(report: dict[str, object]) -> None:
    print("# Saúde do cofre")
    print()
    print(f"- Notas: {report['notes']}")
    print(f"- Links: {report['links']}")
    print(f"- Links quebrados: {len(report['broken_links'])}")
    print(f"- Notas isoladas: {len(report['orphan_notes'])}")
    print(f"- Notas com uma conexão: {len(report['weakly_connected_notes'])}")
    print()
    if report["broken_links"]:
        print("## Links quebrados")
        for item in report["broken_links"]:
            print(f"- {item['source']} → `{item['target']}`")
        print()
    if report["orphan_notes"]:
        print("## Notas isoladas")
        for note in report["orphan_notes"]:
            print(f"- {note}")
        print()
    if report["weakly_connected_notes"]:
        print("## Uma conexão")
        for note in report["weakly_connected_notes"]:
            print(f"- {note}")
        print()
    print("## Principais hubs")
    for hub in report["hubs"]:
        print(f"- {hub['note']}: {hub['connections']} conexões")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisa um cofre Obsidian sem alterá-lo.")
    parser.add_argument("vault", type=Path, help="Caminho do cofre Obsidian")
    parser.add_argument("--json", action="store_true", help="Imprime JSON")
    args = parser.parse_args()

    vault = args.vault.expanduser().resolve()
    if not vault.is_dir():
        parser.error(f"cofre não encontrado: {vault}")

    report = analyze(vault)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_markdown(report)


if __name__ == "__main__":
    main()
