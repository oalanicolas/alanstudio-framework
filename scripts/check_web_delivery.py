#!/usr/bin/env python3
"""Check a local static game's actual entrypoint and literal resource URLs.

Complements a browser playthrough; does not certify art, sound playback or rules.
No dependencies, project writes, external requests or JavaScript execution.
"""
import argparse
from collections import deque
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urldefrag
from urllib.request import HTTPRedirectHandler, Request, build_opener


EXTENSIONS = r"(?:m?js|css|woff2?|ttf|otf|png|jpe?g|webp|svg|gif|mp3|wav|ogg|m4a)"
LITERAL = re.compile(r'''["']([^"'\s]+\.''' + EXTENSIONS + r'''(?:[?#][^"'\s]*)?)["']''', re.I)
CSS_URL = re.compile(r'''(?<![\w])url\(\s*["']?([^\s"')]+)["']?\s*\)''', re.I)


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "img", "audio", "video", "source"}:
            if attrs.get("src"):
                self.urls.append(attrs["src"])
        if tag == "video" and attrs.get("poster"):
            self.urls.append(attrs["poster"])
        if tag in {"img", "source"} and attrs.get("srcset"):
            self.urls.extend(part.strip().split()[0] for part in attrs["srcset"].split(",") if part.strip())
        if tag == "link" and attrs.get("href") and set(attrs.get("rel", "").split()) & {"stylesheet", "icon", "preload", "modulepreload"}:
            self.urls.append(attrs["href"])


class SameOriginRedirect(HTTPRedirectHandler):
    def __init__(self, origin):
        self.origin = origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if origin(newurl) != self.origin:
            raise ValueError("redirect outside the requested origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def origin(url):
    parts = urlsplit(url)
    return parts.scheme, parts.netloc


def references(body, suffix):
    text = body.decode("utf-8", errors="replace")
    found = []
    if suffix == ".html":
        parser = ResourceParser()
        parser.feed(text)
        found.extend(parser.urls)
    found.extend(LITERAL.findall(text))
    found.extend(CSS_URL.findall(text))
    return list(dict.fromkeys(found))


def check(project, url, entry="index.html", limit=80):
    parts = urlsplit(url)
    if parts.scheme != "http" or parts.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Use an http:// localhost URL for this local static check")
    project = Path(project).resolve()
    entry_path = (project / entry).resolve()
    if not entry_path.is_relative_to(project):
        raise ValueError("Entry must be inside the project")
    expected = entry_path.read_bytes()
    opener = build_opener(SameOriginRedirect(origin(url)))
    queue = deque([(url, ".html")])
    visited, checks, skipped = set(), [], set()
    while queue:
        current, suffix = queue.popleft()
        if current in visited:
            continue
        if len(visited) >= limit:
            checks.append({"url": current, "error": "resource limit reached; inspection incomplete"})
            break
        visited.add(current)
        item = {"url": current}
        checks.append(item)
        try:
            with opener.open(Request(current), timeout=5) as response:
                item.update(status=response.status, content_type=response.headers.get_content_type())
                textual = suffix in {".html", ".js", ".mjs", ".css"}
                body = response.read(2_000_001) if textual else b""
            if suffix != ".html" and item["content_type"] == "text/html":
                item["error"] = "resource returned HTML instead of its content"
                continue
            if current == url and body != expected:
                item["error"] = "entry differs from the project's file (wrong project/build, or a transforming dev server)"
                continue
            if textual and len(body) > 2_000_000:
                item["error"] = "text resource too large; inspection incomplete"
                continue
            if textual:
                for ref in references(body, suffix):
                    linked = urldefrag(urljoin(current, ref))[0]
                    if origin(linked) != origin(url):
                        skipped.add(linked)
                        continue
                    ext = Path(urlsplit(linked).path).suffix.lower()
                    queue.append((linked, ext))
        except (HTTPError, URLError, TimeoutError, ValueError, OSError) as error:
            item["error"] = str(error)
            if isinstance(error, HTTPError):
                item["status"] = error.code
    return {
        "ok": not any("error" in item for item in checks),
        "project": str(project), "entry": entry, "checks": checks,
        "skipped_external": sorted(skipped),
        "limits": "Static HTML identity and literal URLs only. Dynamic paths, decoding, playback, gameplay and artistic fidelity require runtime inspection.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("url")
    parser.add_argument("--entry", default="index.html")
    args = parser.parse_args()
    try:
        result = check(args.project, args.url, args.entry)
    except (ValueError, OSError) as error:
        result = {"ok": False, "error": str(error)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
