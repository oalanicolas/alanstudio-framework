"""Entrada do harness para o acervo em shared/sfx, se existir no laboratório."""
from pathlib import Path
import json
import shlex

import audio


def default_workspace():
    return audio.default_workspace()


DEFAULT_ROOT = default_workspace()
CATALOG_RELATIVE = Path("shared/sfx")
LICENSES = tuple(audio.LICENSES)
QUALITY_BAR = {
    "required": ["origem e licença compatíveis com o uso; direção sonora definida pelo projeto",
                 "arquivo íntegro e decodificável, sem perda adicional na biblioteca",
                 "ouvir o candidato no contexto do jogo"],
    "rejected": [],
    "note": "Triagem documental/técnica não é aprovação artística; preserve a mixagem do jogo.",
}


def quality_bar(root=None):
    policy = audio.audio_policy(root)
    return {**QUALITY_BAR, "rejected": [*policy["excluded_terms"], *policy["excluded_authors"]],
            "policy": policy}


def catalog_dir(root=None):
    return Path(root or DEFAULT_ROOT) / CATALOG_RELATIVE


def load_catalog(root=None):
    return audio.load_catalog(catalog_dir(root))


def studio_assets(root=None):
    base = catalog_dir(root)
    catalog = load_catalog(root)
    return {"sfx": {
        "catalog": str(base / "catalog.json"), "guide": str(base / "README.md"),
        "exists": (base / "catalog.json").is_file(), "policy": audio.audio_policy(root),
        "file_count": len(catalog["sounds"]), "updated": catalog.get("updated"),
        "rule": "Busque em shared/sfx antes de baixar som; ouça e exporte com créditos.",
    }}


def search_catalog(query, root=None, limit=40):
    if not query.strip() or limit < 1:
        raise ValueError("Busca vazia ou limite inválido")
    matches = audio.search(load_catalog(root)["sounds"], query)[:limit]
    return {
        "query": query, "count": len(matches),
        "matches": [{"id": s["id"], "aliases": s.get("aliases", []), "src": s["file"],
                     "title": s["title"], "category": s["category"], "tags": s["tags"],
                     "licenses": sorted({x["license"] for x in s["sources"]}),
                     "authors": sorted({x["author"] for x in s["sources"]})} for s in matches],
        "rule": QUALITY_BAR["note"],
        "next": "Ouça com sfx serve; copie com sfx copy ID --to PASTA. Procure fora só após constatar uma lacuna.",
    }


def copy_entry(entry_id, destination, root=None, sources=None):
    base = catalog_dir(root)
    item = audio.select(load_catalog(root)["sounds"], [entry_id])[0]
    payload = audio.export_payload([item], base, audio.audio_policy(root))
    name = item["id"] + Path(item["file"]).suffix
    destination = Path(destination).resolve()
    if destination.is_relative_to(base.resolve()) or base.resolve().is_relative_to(destination):
        raise ValueError("Destino deve ser separado do acervo")
    target = destination / name
    if target.is_symlink() or (target.exists() and
                              (not target.is_file() or target.read_bytes() != payload[name])):
        raise ValueError("Arquivo de destino diferente; escolha outra pasta")
    record = json.loads(payload["manifest.json"])["files"][0]
    record.update(key=entry_id, from_catalog="shared/sfx")
    receipt = Path(sources) if sources else destination / "sources.json"
    if receipt.resolve().is_relative_to(base.resolve()) or receipt.resolve() == target:
        raise ValueError("Proveniência deve ficar fora do acervo e do arquivo de áudio")
    previous = audio.read_json(receipt) if receipt.exists() else {"files": []}
    if not isinstance(previous.get("files"), list):
        raise ValueError("Manifesto de destino sem lista files")
    entries = previous["files"]
    existing = next((r for r in entries if r.get("id") == item["id"]
                     or r.get("key") == entry_id or r.get("src") == name), None)
    if existing and existing != record:
        raise ValueError("Proveniência de destino diferente; escolha outra pasta")
    if not existing:
        entries.append(record)
    credit_path = destination / (item["id"] + ".credits.txt")
    for path in (receipt, credit_path):
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError("Destino de créditos/proveniência inválido")
    if credit_path.exists() and credit_path.read_bytes() != payload["CREDITS.txt"]:
        raise ValueError("Créditos de destino diferentes; escolha outra pasta")
    destination.mkdir(parents=True, exist_ok=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(payload[name])
    receipt.write_bytes(audio.json_bytes(previous))
    credit_path.write_bytes(payload["CREDITS.txt"])
    return {"copied": str(target), "bytes": item["bytes"], "record": record,
            "sources": str(receipt), "credits": str(credit_path)}


def summarize(root=None):
    catalog = load_catalog(root)
    command = shlex.join(["python3", str(Path(__file__).resolve().with_name("game.py")),
                          "--root", str(Path(root or DEFAULT_ROOT).resolve()), "sfx"])
    groups = {}
    for item in catalog["sounds"]:
        groups[item["category"]] = groups.get(item["category"], 0) + 1
    return {
        "catalog": str(catalog_dir(root) / "catalog.json"),
        "guide": str(catalog_dir(root) / "README.md"),
        "file_count": len(catalog["sounds"]),
        "total_bytes": sum(s["bytes"] for s in catalog["sounds"]),
        "originals": sum(s.get("edition") == "original" for s in catalog["sounds"]),
        "updated": catalog.get("updated"), "quality_bar": quality_bar(root),
        "categories": [{"title": name, "count": count} for name, count in sorted(groups.items())],
        "search": f"{command} search TERMO",
        "listen": f"{command} serve",
        "copy": f"{command} copy ID --to PASTA",
    }


def verify_catalog(root=None):
    result = audio.check(catalog_dir(root), policy=audio.audio_policy(root))
    return {"ok": result["ok"], "problems": result["errors"],
            "file_count": result["sounds"], "warnings": result["warnings"]}


def serve_catalog(root=None, port=8766):
    from functools import partial

    server = audio.ThreadingHTTPServer(("127.0.0.1", port),
                                      partial(audio.CatalogHandler, root=catalog_dir(root), policy=audio.audio_policy(root)))
    print(f"http://127.0.0.1:{port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    print(audio.json_bytes(summarize()).decode(), end="")
