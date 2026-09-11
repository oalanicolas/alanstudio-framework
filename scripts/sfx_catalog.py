"""Entrada do harness para o acervo em shared/sfx, se existir no laboratório."""
from pathlib import Path
import json
import math
import re
import shlex

import audio


def default_workspace():
    return audio.default_workspace()


DEFAULT_ROOT = default_workspace()
CATALOG_RELATIVE = Path("shared/sfx")
STARTER_SFX = Path(__file__).resolve().parents[1] / "assets/starters/canvas-arcade/public/sfx"
STEM_RECEIPT = ("src", "key", "author", "license", "origin")
# A receita já pede o pico do arquivo. Sem isto o
# summary listava stems e calava o tool.
# Relato no disco não é mix ouvida.
PEAK_FILES = ("tools/peak.mjs", "tools/peak.js", "tools/peak.py")
PEAK_DISK = re.compile(r"Pico do arquivo no disco|não do mix em cena", re.IGNORECASE)


def peak_names_disk(text):
    return bool(text and PEAK_DISK.search(text))


def peak_disk_source(project=None):
    root = Path(project) if project is not None else STARTER_SFX.parent.parent
    for name in PEAK_FILES:
        path = root / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if peak_names_disk(text):
            return name
    return None


# A receita já desloca a voz. Sem isto o
# search achava o stem e calava o tool.
# Arquivo no disco não é mix ouvida.
SFX_FILES = (
    "tools/design-sfx.py",
    "tools/sfx.py",
    "tools/design-sfx.js",
    "tools/sfx.js",
)
SFX_SHIFT = re.compile(r"desloca a voz", re.IGNORECASE)


def sfx_shifts_voice(text):
    return bool(text and SFX_SHIFT.search(text))


def sfx_shift_source(project=None):
    root = Path(project) if project is not None else STARTER_SFX.parent.parent
    for name in SFX_FILES:
        path = root / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if sfx_shifts_voice(text):
            return name
    return None


# O sidecar já carrega os créditos. Sem isto o
# copy levava o caminho e calava o arquivo.
# Créditos no disco não são mix ouvida.
STEM_CREDIT_MARK = re.compile(r"Licen[cç]a\s*:", re.IGNORECASE)


def stem_declares_credits(text):
    return bool(text and STEM_CREDIT_MARK.search(text))


def stem_credits_source(item, folder=None):
    folder = Path(folder or STARTER_SFX)
    src = item.get("src") if isinstance(item, dict) else None
    if not isinstance(src, str) or not src.strip():
        return None
    name = Path(src).stem + ".credits.txt"
    path = folder / name
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if stem_declares_credits(text):
        return name
    return None


# O check já cruza a integridade. Sem isto o
# verify lia ok e calava o hash.
# Hash no disco não é mix ouvida.
CATALOG_CHECK = Path(__file__).resolve().parent / "audio.py"
CATALOG_INTEGRITY = re.compile(r"Integridade inválida")


def catalog_crosses_integrity(text):
    return bool(text and CATALOG_INTEGRITY.search(text))


def verify_integrity_source():
    path = CATALOG_CHECK
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if catalog_crosses_integrity(text):
        return path.name
    return None


# O export já recusa processamento. Sem isto o
# comando copiava bytes e calava a recusa.
# Bytes no disco não são mix ouvida.
CATALOG_PROCESS = re.compile(r"sem processamento adicional", re.IGNORECASE)


def export_refuses_processing(text):
    return bool(text and CATALOG_PROCESS.search(text))


def export_process_source():
    path = CATALOG_CHECK
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if export_refuses_processing(text):
        return path.name
    return None


def receipt_field(row, field):
    # O acervo guarda autor e licença em `sources`. O starter,
    # no topo. Identidade lê os dois sem exigir o mesmo envelope.
    if not isinstance(row, dict):
        return None
    value = row.get(field)
    if field in {"src", "key"} or value not in (None, ""):
        return value
    sources = row.get("sources")
    first = sources[0] if isinstance(sources, list) and sources and isinstance(sources[0], dict) else {}
    if field == "origin":
        return first.get("url") or first.get("origin") or value
    if field in {"author", "license"}:
        return first.get(field) or value
    return value


def same_stem_receipt(existing, record):
    # O init copia o recibo com `note`. O export acrescenta `kind`/`from`.
    # O copy do acervo acrescenta `from_catalog`. Comparar o
    # dicionário inteiro recusava recolocar o WAV que sumiu.
    # Identidade é origem e licença, não o campo extra. Recibo não é licença.
    if not isinstance(existing, dict) or not isinstance(record, dict):
        return False
    return all(receipt_field(existing, field) == receipt_field(record, field) for field in STEM_RECEIPT)
LICENSES = tuple(audio.LICENSES)
QUALITY_BAR = {
    "required": ["origem e licença compatíveis com o uso; direção sonora definida pelo projeto",
                 "arquivo íntegro e decodificável, sem perda adicional na biblioteca",
                 "ouvir o candidato no contexto do jogo"],
    "rejected": [],
    "note": "Triagem documental/técnica não é aprovação artística; preserve a mixagem do jogo.",
}

EMPTY_NEXT = (
    "Acervo vazio. O starter já fala em public/sfx; sfx search "
    "nomeia o stem que casa com o termo, sfx info lê a chave, "
    "sfx verify nomeia os stems sem cruzar o que não existe, "
    "nomeia o stem que o recibo lista e o disco perdeu, "
    "sfx info lê a mesma ausência, "
    "sfx export nomeia a mesma ausência e "
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
    "O recibo que lista um stem e o disco perdeu não é id desconhecido. "
    "Sem id, sem chave e sem recibo de stem perdido, não há ficha. "
    "Cresça com sfx import ARQUIVO --metadata JSON (ffmpeg)."
)
EXPORT_EMPTY = (
    "Acervo vazio. O starter já fala em public/sfx. "
    "sfx export copia bytes e créditos de um id do acervo ou da "
    "chave do stem do starter. O recibo que lista um stem e o "
    "disco perdeu não é id desconhecido. Sem id, sem chave e "
    "sem recibo de stem perdido, não há o que exportar."
)
EXPORT_MISSING = (
    "O recibo lista este stem e o disco perdeu o arquivo. "
    "Não é id desconhecido. Exportar não inventa bytes. "
    "roles --apply e sfx copy recoloca "
    "se origem e licença casam. Nomear não é ouvir."
)
INFO_NEXT = (
    "Ficha lida no disco. Não é mix ouvido. "
    "Ouça no jogo, no papel."
)
INFO_PEAK = (
    " Nomeia o pico que o inspect já mede. "
    "Pico no recibo não é mix ouvida."
)
INFO_LOCAL_NEXT = (
    "Ficha do stem do starter. Não é id do acervo. "
    "Arquivo no disco não é mix ouvido. "
    "Ouça no jogo, no papel."
)
INFO_MISSING_NEXT = (
    "O recibo lista este stem e o disco perdeu o arquivo. "
    "Não é id desconhecido. roles --apply e sfx copy recoloca "
    "se origem e licença casam. Nomear não é ouvir."
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
    "Nomeia o stem que o recibo lista e o disco perdeu. "
    "sfx summary lista os stems. Arquivo no disco não é mix ouvido."
)
VERIFY_NEXT = (
    "Cruzou bytes e fichas do acervo. Não é mix ouvido. "
    "Ouça no jogo, no papel."
)


def quality_bar(root=None):
    policy = audio.audio_policy(root)
    return {**QUALITY_BAR, "rejected": [*policy["excluded_terms"], *policy["excluded_authors"]],
            "policy": policy}


def catalog_dir(root=None):
    return Path(root or DEFAULT_ROOT) / CATALOG_RELATIVE


def local_stems(folder=None):
    # O recibo listava o stem e o verify some se o WAV
    # sumiu. Nomear a ausência não é cruzar nem ouvir.
    folder = Path(folder or STARTER_SFX)
    files = []
    missing = []
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
                key = item.get("key")
                key = key if isinstance(key, str) and key.strip() else Path(src).stem
                path = folder / src
                if not path.is_file() or path.is_symlink():
                    missing.append({
                        "key": key,
                        "src": src,
                        "title": item.get("title") if isinstance(item.get("title"), str) else None,
                        "author": item.get("author") if isinstance(item.get("author"), str) else None,
                        "license": item.get("license") if isinstance(item.get("license"), str) else None,
                        "origin": item.get("origin") if isinstance(item.get("origin"), str) else None,
                    })
                    continue
                files.append({
                    "src": src,
                    "key": key,
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
        "missing": missing,
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
        "missing": local.get("missing", []),
        "heard": False,
    }


def _local_identity_match(item, needle):
    key = audio.fold(item["key"])
    src = audio.fold(item["src"])
    stem = audio.fold(Path(item["src"]).stem)
    return needle in {key, src, stem}


def find_local_stem(entry_id, folder=None):
    needle = audio.fold(entry_id) if isinstance(entry_id, str) else ""
    if not needle:
        return None
    for item in local_stems(folder)["files"]:
        if _local_identity_match(item, needle):
            return item
    return None


def find_local_missing(entry_id, folder=None):
    # O verify já nomeava a ausência. O info dizia id
    # desconhecido e o agente reinventava o papel.
    needle = audio.fold(entry_id) if isinstance(entry_id, str) else ""
    if not needle:
        return None
    for item in local_stems(folder)["missing"]:
        if _local_identity_match(item, needle):
            return item
    return None


# A receita já recusa que arquivo sem papel seja áudio do jogo.
# Sem isto a ficha copiava licença e bytes e calava a recusa.
# Arquivo no disco não é mix.
AUDIO_LOOSE = re.compile(r"sem papel e sem consumidor não é áudio")


def recipe_refuses_loose_file_as_audio(text):
    return bool(text and AUDIO_LOOSE.search(text))


def info_local_loose_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_loose_file_as_audio(text):
        return "recipes/audio.md"
    return None


def info_local_scope():
    scope = (
        "Ficha do stem do starter. "
        "Não ouve e não liga o papel ao mixer."
    )
    if info_local_loose_source():
        scope += (
            " O disco recusa que arquivo sem papel seja áudio do jogo (`lixo`). "
            "Arquivo no disco não é mix."
        )
    return scope


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
        "scope": info_local_scope(),
    }


def local_missing_card(item, empty):
    licenses = [item["license"]] if item.get("license") else []
    authors = [item["author"]] if item.get("author") else []
    return {
        "id": item["key"],
        "key": item["key"],
        "title": item.get("title") or item["key"],
        "src": item["src"],
        "bytes": None,
        "licenses": licenses,
        "authors": authors,
        "origin": item.get("origin"),
        "kind": "starter",
        "missing": True,
        "empty": empty,
        "heard": False,
        "next": INFO_MISSING_NEXT,
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
    report = {
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
    if stem_credits_source(item, folder):
        report["scope"] = (
            "O disco copia os créditos (`.credits.txt`). "
            "Créditos no disco não são mix ouvida."
        )
    return report


def load_catalog(root=None):
    return audio.load_catalog(catalog_dir(root))


# O mapa já recusa que o catálogo ouça. Sem isto o
# context apontava o acervo e calava a recusa.
# Acervo no disco não é mix ouvida.
SOURCES_GUIDE = Path(__file__).resolve().parents[1] / "references/sources.md"
SOURCES_HEAR = re.compile(r"não ouve o starter")


def sources_refuse_hearing(text):
    return bool(text and SOURCES_HEAR.search(text))


def studio_assets_hear_source():
    path = SOURCES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if sources_refuse_hearing(text):
        return "references/sources.md"
    return None


def studio_assets_scope():
    scope = (
        "Aponta o catálogo compartilhado se existir. "
        "Não toca o som e não valida licença."
    )
    if studio_assets_hear_source():
        scope += (
            " O disco recusa que o catálogo ouça o starter (`ouve`). "
            "Acervo no disco não é mix ouvida."
        )
    return scope


def studio_assets(root=None):
    base = catalog_dir(root)
    catalog = load_catalog(root)
    return {"sfx": {
        "catalog": str(base / "catalog.json"), "guide": str(base / "README.md"),
        "exists": (base / "catalog.json").is_file(), "policy": audio.audio_policy(root),
        "file_count": len(catalog["sounds"]), "updated": catalog.get("updated"),
        "rule": "shared/sfx é ADAPT. Sem acervo o catálogo vem vazio; o starter já fala em public/sfx.",
        "scope": studio_assets_scope(),
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
    named = search_local_scope()
    if named:
        local["scope"] = named
    triage = search_match_scope()
    cards = []
    for item in matches:
        card = {
            "id": item["id"],
            "aliases": item.get("aliases", []),
            "src": item["file"],
            "title": item["title"],
            "category": item["category"],
            "tags": item["tags"],
            "licenses": sorted({source["license"] for source in item["sources"]}),
            "authors": sorted({source["author"] for source in item["sources"]}),
        }
        if triage:
            card["scope"] = triage
        cards.append(card)
    report = {
        "query": query, "count": len(matches),
        "empty": empty,
        "matches": cards,
        "local": local,
        "heard": False,
        "rule": QUALITY_BAR["note"],
        "next": nxt,
    }
    if sfx_shift_source():
        report["scope"] = (
            "O disco desloca a voz (`sfx`). "
            "Arquivo no disco não é mix ouvida."
        )
    return report


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
    payload = audio.export_payload([item], base, audio.audio_policy(root))
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
    source = record.get("sources")
    first = source[0] if isinstance(source, list) and source and isinstance(source[0], dict) else {}
    record.update(
        key=as_name or entry_id,
        from_catalog="shared/sfx",
        author=record.get("author") or first.get("author"),
        license=record.get("license") or first.get("license"),
        origin=record.get("origin") or first.get("url") or first.get("origin"),
    )
    receipt = Path(sources) if sources else destination / "sources.json"
    if receipt.resolve().is_relative_to(base.resolve()) or receipt.resolve() == target:
        raise ValueError("Proveniência deve ficar fora do acervo e do arquivo de áudio")
    previous = audio.read_json(receipt) if receipt.exists() else {"files": []}
    if not isinstance(previous.get("files"), list):
        raise ValueError("Manifesto de destino sem lista files")
    entries = previous["files"]
    existing = next((r for r in entries if r.get("id") == item["id"]
                     or r.get("key") in {entry_id, as_name} or r.get("src") == name), None)
    if existing and not same_stem_receipt(existing, record):
        raise ValueError("Proveniência de destino diferente; escolha outra pasta")
    credit_path = destination / (stem + ".credits.txt")
    for path in (receipt, credit_path):
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError("Destino de créditos/proveniência inválido")
    if credit_path.exists() and credit_path.read_bytes() != payload["CREDITS.txt"]:
        raise ValueError("Créditos de destino diferentes; escolha outra pasta")
    already = target.exists() and credit_path.exists() and (
        existing is None or same_stem_receipt(existing, record)
    )
    destination.mkdir(parents=True, exist_ok=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(payload[catalog_name])
    if not existing:
        entries.append(record)
        receipt.write_bytes(audio.json_bytes(previous))
    if not credit_path.exists():
        credit_path.write_bytes(payload["CREDITS.txt"])
    report = {
        "copied": str(target),
        "bytes": item["bytes"],
        "record": record,
        "sources": str(receipt),
        "credits": str(credit_path),
        "kind": "catalog",
        "status": "already_exported" if already else "exported",
        "heard": False,
        "next": EXPORT_NEXT,
    }
    named = copy_catalog_scope()
    if named:
        report["scope"] = named
    consumed = copy_record_scope()
    if consumed:
        report["record"] = dict(record, scope=consumed)
    return report


def summarize(root=None):
    catalog = load_catalog(root)
    command = shlex.join(["python3", str(Path(__file__).resolve().with_name("game.py")),
                          "--root", str(Path(root or DEFAULT_ROOT).resolve()), "sfx"])
    groups = {}
    for item in catalog["sounds"]:
        groups[item["category"]] = groups.get(item["category"], 0) + 1
    empty = len(catalog["sounds"]) == 0
    local = local_stems()
    report = {
        "catalog": str(catalog_dir(root) / "catalog.json"),
        "guide": str(catalog_dir(root) / "README.md"),
        "file_count": len(catalog["sounds"]),
        "empty": empty,
        "total_bytes": sum(s["bytes"] for s in catalog["sounds"]),
        "originals": sum(s.get("edition") == "original" for s in catalog["sounds"]),
        "updated": catalog.get("updated"), "quality_bar": quality_bar(root),
        "categories": [{"title": name, "count": count} for name, count in sorted(groups.items())],
        "local": local,
        "heard": False,
        "search": f"{command} search TERMO",
        "listen": None if empty else f"{command} serve",
        "copy": f"{command} copy ID --to PASTA",
        "import": f"{command} import ARQUIVO --metadata JSON",
        "seed": f"{command} seed",
        "info": f"{command} info ID",
        "export": f"{command} export ID --to PASTA",
        "verify": f"{command} verify",
        "next": EMPTY_NEXT if empty else LISTEN_NEXT,
    }
    if peak_disk_source():
        report["scope"] = (
            "O disco relata o pico do arquivo (`peak`). "
            "Relato no disco não é mix ouvida."
        )
    return report


# A receita já recusa improvisar licença. Sem isto o
# import copiava a conta e calava a recusa.
# Importar no disco não é licença.
AUDIO_RECIPE = Path(__file__).resolve().parents[1] / "recipes/audio.md"
AUDIO_IMPROVISE = re.compile(r"não\s+autoriza improvisar licença")


def recipe_refuses_improvised_license(text):
    return bool(text and AUDIO_IMPROVISE.search(text))


def import_license_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_improvised_license(text):
        return "recipes/audio.md"
    return None


def import_license_scope():
    scope = (
        "Acrescenta entradas ao catálogo. "
        "Não ouve e não concede licença."
    )
    if import_license_source():
        scope += (
            " O disco recusa improvisar licença (`improvisar`). "
            "Importar no disco não é licença."
        )
    return scope


def import_entry(file, metadata, root=None):
    prepared = audio.prepare_import(Path(file), audio.read_json(metadata), audio.import_policy(root))
    result = audio.save_imports([prepared], catalog_dir(root))
    result.update(heard=False, next=IMPORT_NEXT, scope=import_license_scope())
    return result


def receipt_peak(item):
    # O inspect grava o pico no recibo. O info
    # lia id e créditos e calava o número.
    # Pico no recibo não é mix ouvida.
    if not isinstance(item, dict):
        return None
    technical = item.get("technical")
    if not isinstance(technical, dict):
        return None
    peak = technical.get("peak_dbfs")
    if isinstance(peak, bool) or not isinstance(peak, (int, float)):
        return None
    if not math.isfinite(peak):
        return None
    return peak


# A receita já recusa que decode aprove o mix. Sem isto a
# ficha do acervo copiava id e créditos e calava a recusa.
# Ficha no disco não é mix ouvida.
AUDIO_DECODE = re.compile(r"decode não aprova mix")


def recipe_refuses_decode_as_mix(text):
    return bool(text and AUDIO_DECODE.search(text))


def info_catalog_decode_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_decode_as_mix(text):
        return "recipes/audio.md"
    return None


def info_catalog_scope():
    if not info_catalog_decode_source():
        return None
    return (
        "O disco recusa que teste técnico de decode aprove o mix "
        "(`decode`). Ficha no disco não é mix ouvida."
    )


# A receita já recusa que importar e exportar seja ouvir. Sem isto o
# copy do acervo levava bytes e créditos e calava a recusa.
# Cópia no disco não é mix.
AUDIO_HEARING = re.compile(r"Importar e exportar não é ouvir")


def recipe_refuses_export_as_hearing(text):
    return bool(text and AUDIO_HEARING.search(text))


def copy_catalog_hearing_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_export_as_hearing(text):
        return "recipes/audio.md"
    return None


def copy_catalog_scope():
    if not copy_catalog_hearing_source():
        return None
    return (
        "O disco recusa que importar e exportar seja ouvir "
        "(`ouvir`). Cópia no disco não é mix."
    )


# A receita já recusa que o arquivo importado esteja
# sendo consumido. Sem isto o record copiava autor
# e licença e calava a recusa. Recibo no disco não
# é mix.
CONTENT_RECIPE = Path(__file__).resolve().parents[1] / "recipes/content.md"
CONTENT_CONSUMED = re.compile(r"não\s+comprova que está sendo consumido")


def recipe_refuses_import_as_consumed(text):
    return bool(text and CONTENT_CONSUMED.search(text))


def copy_record_consumed_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if recipe_refuses_import_as_consumed(text):
        return "recipes/content.md"
    return None


def copy_record_scope():
    if not copy_record_consumed_source():
        return None
    return (
        "O disco recusa que o arquivo importado esteja sendo consumido "
        "(`consumido`). Recibo no disco não é mix."
    )


# A receita já recusa que o acervo compartilhado seja o primeiro
# ciclo. Sem isto o local do search listava stems e calava a recusa.
# Stem no disco não é mix.
AUDIO_ADAPT = re.compile(r"é ADAPT, não o\s+primeiro ciclo")


def recipe_refuses_catalog_as_first_cycle(text):
    return bool(text and AUDIO_ADAPT.search(text))


def search_local_adapt_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_catalog_as_first_cycle(text):
        return "recipes/audio.md"
    return None


def search_local_scope():
    if not search_local_adapt_source():
        return None
    return (
        "O disco recusa que o acervo compartilhado seja o primeiro ciclo "
        "(`adapt`). Stem no disco não é mix."
    )


# A receita já recusa que avaliação do agente seja aprovação do
# usuário. Sem isto o seed importava a seleção e calava a recusa.
# Seed no disco não é mix.
AUDIO_APPROVAL = re.compile(r"Avaliação do agente não é\s+aprovação do usuário")


def recipe_refuses_agent_as_user_approval(text):
    return bool(text and AUDIO_APPROVAL.search(text))


def seed_approval_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_agent_as_user_approval(text):
        return "recipes/audio.md"
    return None


def seed_catalog_scope():
    if not seed_approval_source():
        return None
    return (
        "O disco recusa que avaliação do agente seja aprovação do usuário "
        "(`aprovação`). Seed no disco não é mix."
    )


# A barra já recusa que a triagem documental aprove a mix.
# Sem isto o match listava licenças e calava a recusa.
# Ficha no disco não é mix.
QUALITY_TRIAGE = re.compile(r"Triagem documental/técnica não é aprovação artística")


def bar_refuses_triage_as_art(text):
    return bool(text and QUALITY_TRIAGE.search(text))


def search_match_triage_source():
    path = Path(__file__).resolve()
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_triage_as_art(text):
        return "scripts/sfx_catalog.py"
    return None


def search_match_scope():
    if not search_match_triage_source():
        return None
    return (
        "O disco recusa que triagem documental/técnica seja aprovação artística "
        "(`triagem`). Ficha no disco não é mix."
    )


# A receita já recusa que variante ausente seja lacuna. Sem isto o
# verify vazio listava stems e calava a recusa.
# Lista no disco não é mix.
AUDIO_GAP = re.compile(r"Variante ausente não é lacuna")


def recipe_refuses_missing_variant_as_gap(text):
    return bool(text and AUDIO_GAP.search(text))


def verify_empty_gap_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_missing_variant_as_gap(text):
        return "recipes/audio.md"
    return None


def verify_empty_scope():
    if not verify_empty_gap_source():
        return None
    return (
        "O disco recusa que variante ausente seja lacuna "
        "(`lacuna`). Lista no disco não é mix."
    )


# A receita já recusa que nomear o 404 seja mix. Sem isto o
# verify listava o stem ausente e calava a recusa.
# Lista no disco não é mix.
AUDIO_404 = re.compile(r"Nomear o 404 não é mix")


def recipe_refuses_naming_404_as_mix(text):
    return bool(text and AUDIO_404.search(text))


def verify_missing_404_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_naming_404_as_mix(text):
        return "recipes/audio.md"
    return None


def verify_missing_scope():
    if not verify_missing_404_source():
        return None
    return (
        "O disco recusa que nomear o 404 seja mix "
        "(`404`). Lista no disco não é mix."
    )


def mark_verify_missing(local):
    named = verify_missing_scope()
    if not named:
        return local
    for item in local.get("missing") or []:
        item["scope"] = named
    return local


# A receita já recusa que o export invente bytes. Sem isto o
# export do stem copiava o WAV e calava a recusa.
# Cópia no disco não é mix.
AUDIO_INVENT = re.compile(r"exportar não inventa bytes")


def recipe_refuses_export_inventing_bytes(text):
    return bool(text and AUDIO_INVENT.search(text))


def export_starter_invent_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_export_inventing_bytes(text):
        return "recipes/audio.md"
    return None


def export_starter_scope():
    if not export_starter_invent_source():
        return None
    return (
        "O disco recusa que o export invente bytes "
        "(`invenção`). Cópia no disco não é mix."
    )


def info_entry(entry_id, root=None, folder=None):
    sounds = load_catalog(root)["sounds"]
    empty = len(sounds) == 0
    if sounds:
        try:
            item = audio.select(sounds, [entry_id])[0]
        except ValueError:
            item = None
        if item:
            card = {
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
            peak = receipt_peak(item)
            if peak is not None:
                card["peak_dbfs"] = peak
                card["next"] = INFO_NEXT + INFO_PEAK
            named = info_catalog_scope()
            if named:
                card["scope"] = named
            return card
    local = find_local_stem(entry_id, folder)
    if local:
        return local_info_card(local, empty)
    lost = find_local_missing(entry_id, folder)
    if lost:
        return local_missing_card(lost, empty)
    if empty:
        raise ValueError(INFO_EMPTY)
    raise ValueError(f"Seleção vazia ou IDs desconhecidos: {entry_id}")


def export_entries(ids, destination, root=None, folder=None):
    sounds = load_catalog(root)["sounds"]
    catalog_items = []
    local_items = []
    missing_items = []
    unknown = []
    for entry_id in ids:
        if sounds:
            try:
                catalog_items.append(audio.select(sounds, [entry_id])[0])
                continue
            except ValueError:
                pass
        local = find_local_stem(entry_id, folder)
        if local:
            local_items.append(local)
            continue
        # O info já nomeava a ausência. O export dizia id
        # desconhecido e o agente reinventava o papel.
        # Recibo sem bytes não é licença nem mix.
        lost = find_local_missing(entry_id, folder)
        if lost:
            missing_items.append(lost)
            continue
        unknown.append(entry_id)
    if missing_items:
        keys = ", ".join(item["key"] for item in missing_items)
        raise ValueError(f"{EXPORT_MISSING} {keys}")
    if unknown:
        if not sounds:
            raise ValueError(EXPORT_EMPTY)
        raise ValueError(f"Seleção vazia ou IDs desconhecidos: {', '.join(unknown)}")
    if catalog_items and local_items:
        raise ValueError("Exporte ids do acervo e stems do starter em destinos separados")
    if catalog_items:
        result = audio.export_files(
            catalog_items, Path(destination), catalog_dir(root), audio.audio_policy(root)
        )
        result.update(
            heard=False,
            next=EXPORT_NEXT,
            ids=[item["id"] for item in catalog_items],
            kind="catalog",
        )
        if export_process_source():
            result["scope"] = (
                "O disco recusa o processamento (`processamento`). "
                "Bytes no disco não são mix ouvida."
            )
        return result
    copied = [copy_local_stem(item, destination, root=root, folder=folder) for item in local_items]
    already = bool(copied) and all(item.get("status") == "already_exported" for item in copied)
    report = {
        "files": len(local_items),
        "status": "already_exported" if already else "exported",
        "destination": str(Path(destination).resolve()),
        "ids": [item["key"] for item in local_items],
        "kind": "starter",
        "heard": False,
        "next": EXPORT_NEXT,
        "copied": [item["copied"] for item in copied],
    }
    named = export_starter_scope()
    if named:
        report["scope"] = named
    return report


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
        prepared.append(
            audio.prepare_import(audio.inside(workspace, local), item, audio.import_policy(root))
        )
    result = audio.save_imports(prepared, catalog_dir(root))
    result.update(heard=False, next=IMPORT_NEXT)
    named = seed_catalog_scope()
    if named:
        result["scope"] = named
    return result


def verify_catalog(root=None, folder=None):
    sounds = load_catalog(root)["sounds"]
    empty = len(sounds) == 0
    local = mark_verify_missing(local_stems(folder))
    if empty:
        report = {
            "ok": False,
            "empty": True,
            "file_count": 0,
            "problems": [],
            "warnings": [],
            "local": local,
            "heard": False,
            "next": VERIFY_EMPTY,
        }
        named = verify_empty_scope()
        if named:
            report["scope"] = named
        return report
    result = audio.check(catalog_dir(root), policy=audio.audio_policy(root))
    report = {
        "ok": result["ok"],
        "empty": False,
        "problems": result["errors"],
        "file_count": result["sounds"],
        "warnings": result["warnings"],
        "local": local,
        "heard": False,
        "next": VERIFY_NEXT,
    }
    if verify_integrity_source():
        report["scope"] = (
            "O disco cruza a integridade (`sha256`). "
            "Hash no disco não é mix ouvida."
        )
    return report


def serve_catalog(root=None, port=8766):
    from functools import partial

    if not load_catalog(root)["sounds"]:
        raise ValueError("Catálogo vazio")
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
