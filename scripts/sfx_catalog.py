"""Entrada do harness para o acervo em shared/sfx, se existir no laboratório."""
from pathlib import Path
import json
import re

import audio


def default_workspace():
    here = Path(__file__).resolve()
    if here.parents[1].name == "framework" and (here.parents[2] / "AGENTS.md").is_file():
        return here.parents[2]
    return Path.cwd()


DEFAULT_ROOT = default_workspace()
CATALOG_RELATIVE = Path("shared/sfx")
STARTER_SFX = Path(__file__).resolve().parents[1] / "assets/starters/canvas-arcade/public/sfx"
STEM_RECEIPT = ("src", "key", "author", "license", "origin")


def same_stem_receipt(existing, record):
    # O init copia o recibo com `note`. O export acrescenta `kind`/`from`.
    # Comparar o dicionário inteiro recusava recolocar o WAV que sumiu.
    # Identidade é origem e licença, não o campo extra. Recibo não é licença.
    if not isinstance(existing, dict) or not isinstance(record, dict):
        return False
    return all(existing.get(field) == record.get(field) for field in STEM_RECEIPT)
LICENSES = tuple(audio.LICENSES)
QUALITY_BAR = {
    "required": ["gravação licenciada ou design sonoro contemporâneo com origem",
                 "arquivo íntegro e decodificável, sem perda adicional na biblioteca",
                 "ouvir o candidato no contexto do jogo"],
    "rejected": ["8-bit", "chiptune", "jsfxr", "sfxr", "bfxr", "bipes retrô",
                 "Kenney arcade como padrão do estúdio"],
    "note": "Triagem documental/técnica não é aprovação artística; preserve a mixagem do jogo.",
}

EMPTY_NEXT = (
    "Acervo vazio. O starter já fala em public/sfx; sfx search "
    "nomeia o stem que casa com o termo, sfx info lê a chave, "
    "sfx verify nomeia os stems sem cruzar o que não existe e "
    "sfx summary lista todos. "
    "Arquivo no disco não é mix ouvido. Desloque com "
    "npm run sfx -- --from <papel> --as brighter. sfx serve não ouve "
    "o que não existe. Para crescer o acervo, sfx import ARQUIVO "
    "--metadata JSON (ffmpeg); importar não é ouvir. Procure fora só "
    "depois de constatar uma lacuna no papel."
)
LISTEN_NEXT = (
    "Ouça com sfx serve; copie com sfx copy ID --to PASTA. "
    "Procure fora só após constatar uma lacuna."
)
MISS_NEXT = (
    "Nenhum id neste termo. O acervo existe: mude o termo ou ouça com sfx serve. "
    "Procure fora só após constatar uma lacuna."
)
LOCAL_HIT_NEXT = (
    "Nenhum id neste termo no acervo. O starter já fala este papel "
    "em public/sfx. Arquivo no disco não é mix ouvido. "
    "Procure fora só após constatar uma lacuna no papel."
)
IMPORT_NEXT = (
    "Importar não é mix ouvido. Ouça no jogo, no papel. "
    "ffmpeg decodifica; sem ele o import recusa. "
    "sfx serve só depois de haver acervo."
)
INFO_EMPTY = (
    "Acervo vazio. O starter já fala em public/sfx. "
    "sfx info lê a ficha de um id do acervo ou a chave do stem do starter. "
    "Sem id e sem chave que case, não há ficha. "
    "Cresça com sfx import ARQUIVO --metadata JSON (ffmpeg)."
)
EXPORT_EMPTY = (
    "Acervo vazio. O starter já fala em public/sfx. "
    "sfx export copia bytes e créditos de um id do acervo ou da "
    "chave do stem do starter. Sem id e sem chave que case, não "
    "há o que exportar."
)
INFO_NEXT = (
    "Ficha lida no disco. Não é mix ouvido. "
    "Ouça no jogo, no papel."
)
INFO_LOCAL_NEXT = (
    "Ficha do stem do starter. Não é id do acervo. "
    "Arquivo no disco não é mix ouvido. "
    "Ouça no jogo, no papel."
)
EXPORT_NEXT = (
    "Exportar preserva bytes e créditos. Não é mix ouvido. "
    "Ouça no jogo, no papel."
)
SEED_MISSING = (
    "selection.json ausente. Seed só importa arquivos locais já selecionados. "
    "Sem seleção, o starter já fala em public/sfx."
)
VERIFY_EMPTY = (
    "Acervo vazio. O starter já fala em public/sfx. "
    "sfx verify cruza bytes e fichas do acervo; sem acervo não há o que cruzar. "
    "sfx summary lista os stems. Arquivo no disco não é mix ouvido."
)
VERIFY_NEXT = (
    "Cruzou bytes e fichas do acervo. Não é mix ouvido. "
    "Ouça no jogo, no papel."
)


def catalog_dir(root=None):
    return Path(root or DEFAULT_ROOT) / CATALOG_RELATIVE


def local_stems(folder=None):
    folder = Path(folder or STARTER_SFX)
    files = []
    sources = folder / "sources.json"
    if sources.is_file():
        data = audio.read_json(sources)
        entries = data.get("files") if isinstance(data, dict) else None
        if isinstance(entries, list):
            for item in entries:
                if not isinstance(item, dict):
                    continue
                src = item.get("src")
                if not isinstance(src, str) or not src.strip():
                    continue
                path = folder / src
                if not path.is_file() or path.is_symlink():
                    continue
                key = item.get("key")
                files.append({
                    "src": src,
                    "key": key if isinstance(key, str) and key.strip() else Path(src).stem,
                    "title": item.get("title") if isinstance(item.get("title"), str) else None,
                    "author": item.get("author") if isinstance(item.get("author"), str) else None,
                    "license": item.get("license") if isinstance(item.get("license"), str) else None,
                    "origin": item.get("origin") if isinstance(item.get("origin"), str) else None,
                    "bytes": path.stat().st_size,
                })
    return {
        "path": str(folder),
        "kind": "starter",
        "exists": folder.is_dir(),
        "file_count": len(files),
        "files": files,
        "heard": False,
    }


def local_match_text(item):
    return audio.fold(" ".join(
        part for part in (
            item.get("key"),
            item.get("src"),
            item.get("license"),
            item.get("origin"),
        ) if isinstance(part, str) and part.strip()
    ))


def match_local_stems(query, folder=None, limit=40):
    local = local_stems(folder)
    terms = [term for term in audio.fold(query).split() if term]
    files = [
        item for item in local["files"]
        if terms and all(term in local_match_text(item) for term in terms)
    ]
    picked = files[:max(1, limit)]
    return {
        "path": local["path"],
        "kind": "starter",
        "exists": local["exists"],
        "file_count": len(picked),
        "files": picked,
        "heard": False,
    }


def find_local_stem(entry_id, folder=None):
    needle = audio.fold(entry_id) if isinstance(entry_id, str) else ""
    if not needle:
        return None
    for item in local_stems(folder)["files"]:
        key = audio.fold(item["key"])
        src = audio.fold(item["src"])
        stem = audio.fold(Path(item["src"]).stem)
        if needle in {key, src, stem}:
            return item
    return None


def local_info_card(item, empty):
    licenses = [item["license"]] if item.get("license") else []
    authors = [item["author"]] if item.get("author") else []
    return {
        "id": item["key"],
        "key": item["key"],
        "title": item.get("title") or item["key"],
        "src": item["src"],
        "bytes": item["bytes"],
        "licenses": licenses,
        "authors": authors,
        "origin": item.get("origin"),
        "kind": "starter",
        "empty": empty,
        "heard": False,
        "next": INFO_LOCAL_NEXT,
    }


def copy_local_stem(item, destination, root=None, sources=None, as_name=None, folder=None):
    folder = Path(folder or STARTER_SFX).resolve()
    src_path = folder / item["src"]
    if not src_path.is_file() or src_path.is_symlink():
        raise ValueError("Stem do starter ausente")
    if as_name and not re.fullmatch(r"[A-Za-z_][\w-]*", as_name):
        raise ValueError("nome de papel inválido")
    stem = as_name if as_name else item["key"]
    name = stem + src_path.suffix
    destination = Path(destination).resolve()
    base = catalog_dir(root)
    if destination == folder:
        raise ValueError("Destino deve ser separado do starter")
    if destination.is_relative_to(base.resolve()) or base.resolve().is_relative_to(destination):
        raise ValueError("Destino deve ser separado do acervo")
    target = destination / name
    data = src_path.read_bytes()
    if target.is_symlink() or (target.exists() and (
        not target.is_file() or target.read_bytes() != data
    )):
        raise ValueError("Arquivo de destino diferente; escolha outra pasta")
    credit_src = folder / (Path(item["src"]).stem + ".credits.txt")
    if credit_src.is_file() and not credit_src.is_symlink():
        credit_bytes = credit_src.read_bytes()
    else:
        credit_bytes = (
            f"{item['src']} — {item.get('title') or item['key']}. "
            f"Autor: {item.get('author') or 'desconhecido'}. "
            f"Licença: {item.get('license') or 'não declarada'}. "
            f"Origem: {item.get('origin') or 'starter'}.\n"
        ).encode()
    credit_path = destination / (stem + ".credits.txt")
    receipt = Path(sources) if sources else destination / "sources.json"
    if receipt.resolve() == target or receipt.resolve().is_relative_to(base.resolve()):
        raise ValueError("Proveniência deve ficar fora do acervo e do arquivo de áudio")
    record = {
        "src": name,
        "key": stem,
        "title": item.get("title") or item["key"],
        "author": item.get("author"),
        "license": item.get("license"),
        "origin": item.get("origin"),
        "kind": "starter",
        "from": "assets/starters/canvas-arcade/public/sfx",
    }
    previous = audio.read_json(receipt) if receipt.exists() else {"files": []}
    if not isinstance(previous.get("files"), list):
        raise ValueError("Manifesto de destino sem lista files")
    entries = previous["files"]
    existing = next((row for row in entries if row.get("key") in {item["key"], stem} or row.get("src") == name), None)
    if existing and not same_stem_receipt(existing, record):
        raise ValueError("Proveniência de destino diferente; escolha outra pasta")
    for path in (receipt, credit_path):
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError("Destino de créditos/proveniência inválido")
    if credit_path.exists() and credit_path.read_bytes() != credit_bytes:
        raise ValueError("Créditos de destino diferentes; escolha outra pasta")
    already = target.exists() and credit_path.exists() and (
        existing is None or same_stem_receipt(existing, record)
    )
    destination.mkdir(parents=True, exist_ok=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(data)
    if not existing:
        entries.append(record)
        receipt.write_bytes(audio.json_bytes(previous))
    if not credit_path.exists():
        credit_path.write_bytes(credit_bytes)
    return {
        "copied": str(target),
        "bytes": item["bytes"],
        "record": record,
        "sources": str(receipt),
        "credits": str(credit_path),
        "kind": "starter",
        "status": "already_exported" if already else "exported",
        "heard": False,
        "next": EXPORT_NEXT,
    }


def load_catalog(root=None):
    return audio.load_catalog(catalog_dir(root))


def studio_assets(root=None):
    base = catalog_dir(root)
    catalog = load_catalog(root)
    return {"sfx": {
        "catalog": str(base / "catalog.json"), "guide": str(base / "README.md"),
        "exists": (base / "catalog.json").is_file(),
        "file_count": len(catalog["sounds"]), "updated": catalog.get("updated"),
        "rule": "shared/sfx é ADAPT. Sem acervo o catálogo vem vazio; o starter já fala em public/sfx.",
    }}


def search_catalog(query, root=None, limit=40):
    if not query.strip() or limit < 1:
        raise ValueError("Busca vazia ou limite inválido")
    sounds = load_catalog(root)["sounds"]
    matches = audio.search(sounds, query)[:limit]
    empty = len(sounds) == 0
    local = match_local_stems(query, limit=limit)
    if empty:
        nxt = EMPTY_NEXT
    elif matches:
        nxt = LISTEN_NEXT
    elif local["files"]:
        nxt = LOCAL_HIT_NEXT
    else:
        nxt = MISS_NEXT
    return {
        "query": query, "count": len(matches),
        "empty": empty,
        "matches": [{"id": s["id"], "aliases": s.get("aliases", []), "src": s["file"],
                     "title": s["title"], "category": s["category"], "tags": s["tags"],
                     "licenses": sorted({x["license"] for x in s["sources"]}),
                     "authors": sorted({x["author"] for x in s["sources"]})} for s in matches],
        "local": local,
        "heard": False,
        "rule": QUALITY_BAR["note"],
        "next": nxt,
    }


def copy_entry(entry_id, destination, root=None, sources=None, as_name=None):
    sounds = load_catalog(root)["sounds"]
    if sounds:
        try:
            audio.select(sounds, [entry_id])
        except ValueError:
            local = find_local_stem(entry_id)
            if local:
                return copy_local_stem(local, destination, root=root, sources=sources, as_name=as_name)
            raise
    else:
        local = find_local_stem(entry_id)
        if local:
            return copy_local_stem(local, destination, root=root, sources=sources, as_name=as_name)
        raise ValueError(EXPORT_EMPTY)
    base = catalog_dir(root)
    item = audio.select(sounds, [entry_id])[0]
    payload = audio.export_payload([item], base)
    catalog_name = item["id"] + Path(item["file"]).suffix
    stem = as_name if as_name else item["id"]
    if as_name and not re.fullmatch(r"[A-Za-z_][\w-]*", as_name):
        raise ValueError("nome de papel inválido")
    name = stem + Path(item["file"]).suffix
    destination = Path(destination).resolve()
    if destination.is_relative_to(base.resolve()) or base.resolve().is_relative_to(destination):
        raise ValueError("Destino deve ser separado do acervo")
    target = destination / name
    if target.is_symlink() or (target.exists() and
                              (not target.is_file() or target.read_bytes() != payload[catalog_name])):
        raise ValueError("Arquivo de destino diferente; escolha outra pasta")
    record = json.loads(payload["manifest.json"])["files"][0]
    record["src"] = name
    record.update(key=as_name or entry_id, from_catalog="shared/sfx")
    receipt = Path(sources) if sources else destination / "sources.json"
    if receipt.resolve().is_relative_to(base.resolve()) or receipt.resolve() == target:
        raise ValueError("Proveniência deve ficar fora do acervo e do arquivo de áudio")
    previous = audio.read_json(receipt) if receipt.exists() else {"files": []}
    if not isinstance(previous.get("files"), list):
        raise ValueError("Manifesto de destino sem lista files")
    entries = previous["files"]
    existing = next((r for r in entries if r.get("id") == item["id"]
                     or r.get("key") in {entry_id, as_name} or r.get("src") == name), None)
    if existing and existing != record:
        raise ValueError("Proveniência de destino diferente; escolha outra pasta")
    if not existing:
        entries.append(record)
    credit_path = destination / (stem + ".credits.txt")
    for path in (receipt, credit_path):
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError("Destino de créditos/proveniência inválido")
    if credit_path.exists() and credit_path.read_bytes() != payload["CREDITS.txt"]:
        raise ValueError("Créditos de destino diferentes; escolha outra pasta")
    destination.mkdir(parents=True, exist_ok=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(payload[catalog_name])
    receipt.write_bytes(audio.json_bytes(previous))
    credit_path.write_bytes(payload["CREDITS.txt"])
    return {"copied": str(target), "bytes": item["bytes"], "record": record,
            "sources": str(receipt), "credits": str(credit_path)}


def summarize(root=None):
    catalog = load_catalog(root)
    groups = {}
    for item in catalog["sounds"]:
        groups[item["category"]] = groups.get(item["category"], 0) + 1
    empty = len(catalog["sounds"]) == 0
    local = local_stems()
    return {
        "catalog": str(catalog_dir(root) / "catalog.json"),
        "guide": str(catalog_dir(root) / "README.md"),
        "file_count": len(catalog["sounds"]),
        "empty": empty,
        "total_bytes": sum(s["bytes"] for s in catalog["sounds"]),
        "originals": sum(s.get("edition") == "original" for s in catalog["sounds"]),
        "updated": catalog.get("updated"), "quality_bar": QUALITY_BAR,
        "categories": [{"title": name, "count": count} for name, count in sorted(groups.items())],
        "local": local,
        "heard": False,
        "search": "python3 scripts/game.py sfx search TERMO",
        "listen": None if empty else "python3 scripts/game.py sfx serve",
        "copy": "python3 scripts/game.py sfx copy ID --to PASTA",
        "import": "python3 scripts/game.py sfx import ARQUIVO --metadata JSON",
        "seed": "python3 scripts/game.py sfx seed",
        "info": "python3 scripts/game.py sfx info ID",
        "export": "python3 scripts/game.py sfx export ID --to PASTA",
        "verify": "python3 scripts/game.py sfx verify",
        "next": EMPTY_NEXT if empty else LISTEN_NEXT,
    }


def import_entry(file, metadata, root=None):
    prepared = audio.prepare_import(Path(file), audio.read_json(metadata))
    result = audio.save_imports([prepared], catalog_dir(root))
    result.update(heard=False, next=IMPORT_NEXT)
    return result


def info_entry(entry_id, root=None):
    sounds = load_catalog(root)["sounds"]
    empty = len(sounds) == 0
    if sounds:
        try:
            item = audio.select(sounds, [entry_id])[0]
        except ValueError:
            item = None
        if item:
            return {
                "id": item["id"],
                "title": item["title"],
                "category": item["category"],
                "tags": item.get("tags", []),
                "style": item.get("style"),
                "src": item.get("file"),
                "bytes": item.get("bytes"),
                "licenses": sorted({source["license"] for source in item.get("sources", [])}),
                "authors": sorted({source["author"] for source in item.get("sources", [])}),
                "kind": "catalog",
                "heard": False,
                "next": INFO_NEXT,
            }
    local = find_local_stem(entry_id)
    if local:
        return local_info_card(local, empty)
    if empty:
        raise ValueError(INFO_EMPTY)
    raise ValueError(f"Seleção vazia ou IDs desconhecidos: {entry_id}")


def export_entries(ids, destination, root=None):
    sounds = load_catalog(root)["sounds"]
    catalog_items = []
    local_items = []
    unknown = []
    for entry_id in ids:
        if sounds:
            try:
                catalog_items.append(audio.select(sounds, [entry_id])[0])
                continue
            except ValueError:
                pass
        local = find_local_stem(entry_id)
        if local:
            local_items.append(local)
            continue
        unknown.append(entry_id)
    if unknown:
        if not sounds:
            raise ValueError(EXPORT_EMPTY)
        raise ValueError(f"Seleção vazia ou IDs desconhecidos: {', '.join(unknown)}")
    if catalog_items and local_items:
        raise ValueError("Exporte ids do acervo e stems do starter em destinos separados")
    if catalog_items:
        result = audio.export_files(catalog_items, Path(destination), catalog_dir(root))
        result.update(
            heard=False,
            next=EXPORT_NEXT,
            ids=[item["id"] for item in catalog_items],
            kind="catalog",
        )
        return result
    copied = [copy_local_stem(item, destination, root=root) for item in local_items]
    already = bool(copied) and all(item.get("status") == "already_exported" for item in copied)
    return {
        "files": len(local_items),
        "status": "already_exported" if already else "exported",
        "destination": str(Path(destination).resolve()),
        "ids": [item["key"] for item in local_items],
        "kind": "starter",
        "heard": False,
        "next": EXPORT_NEXT,
        "copied": [item["copied"] for item in copied],
    }


def seed_catalog(root=None):
    workspace = Path(root or DEFAULT_ROOT)
    selection_path = workspace / CATALOG_RELATIVE / "selection.json"
    if not selection_path.is_file():
        raise ValueError(SEED_MISSING)
    selection = audio.read_json(selection_path)
    sounds = selection.get("sounds")
    if not isinstance(sounds, list) or not sounds:
        raise ValueError("selection.json sem sons")
    prepared = []
    for item in sounds:
        local = item.get("local_path")
        if not isinstance(local, str) or not local.strip():
            raise ValueError("cada som da seleção precisa de local_path")
        prepared.append(audio.prepare_import(audio.inside(workspace, local), item))
    result = audio.save_imports(prepared, catalog_dir(root))
    result.update(heard=False, next=IMPORT_NEXT)
    return result


def verify_catalog(root=None):
    sounds = load_catalog(root)["sounds"]
    empty = len(sounds) == 0
    local = local_stems()
    if empty:
        return {
            "ok": False,
            "empty": True,
            "file_count": 0,
            "problems": [],
            "warnings": [],
            "local": local,
            "heard": False,
            "next": VERIFY_EMPTY,
        }
    result = audio.check(catalog_dir(root))
    return {
        "ok": result["ok"],
        "empty": False,
        "problems": result["errors"],
        "file_count": result["sounds"],
        "warnings": result["warnings"],
        "local": local,
        "heard": False,
        "next": VERIFY_NEXT,
    }


def serve_catalog(root=None, port=8766):
    from functools import partial

    if not load_catalog(root)["sounds"]:
        raise ValueError("Catálogo vazio")
    server = audio.ThreadingHTTPServer(("127.0.0.1", port),
                                      partial(audio.CatalogHandler, root=catalog_dir(root)))
    print(f"http://127.0.0.1:{port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    print(audio.json_bytes(summarize()).decode(), end="")
