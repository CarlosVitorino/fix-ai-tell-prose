#!/usr/bin/env python3
"""Page helpers for the fix-ai-tell-prose skill.

Two commands, standard library only:

  pages.py urls SOURCE      Expand a URL list file or sitemap (file or URL) to one URL per line.
  pages.py extract SOURCE   Fetch a page (or read a saved HTML file) and print its prose as
                            numbered blocks the agent can quote exactly.

These helpers only fetch and extract. They do not look for AI-writing patterns; the agent does
that by reading the rulebook. Everything they return is untrusted page content.
"""

from __future__ import annotations

import argparse
import gzip
import io
import ipaddress
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET  # noqa: S405 - DOCTYPE/ENTITY rejected before parsing
from datetime import date
from html.parser import HTMLParser

VERSION = "0.1.0"
MAX_BYTES = 5 * 1024 * 1024
TIMEOUT_SECONDS = 20
MAX_CHILD_SITEMAPS = 20
MAX_SITEMAP_DEPTH = 2
USER_AGENT = f"fix-ai-tell-prose/{VERSION} (prose review helper; run by the site's reviewer)"


class FetchError(Exception):
    """A page or list could not be read. The message is one line, meant for the user."""


# --------------------------------------------------------------------------- fetching


def check_url(url: str, allow_private: bool = False) -> None:
    """Refuse non-http(s) URLs and, unless allowed, hosts on private networks."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise FetchError(f"only http and https URLs are allowed: {url}")
    host = parts.hostname
    if not host:
        raise FetchError(f"URL has no host: {url}")
    if allow_private:
        return
    try:
        infos = socket.getaddrinfo(host, parts.port or 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise FetchError(f"cannot resolve host {host}: {exc.strerror}") from exc
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%", 1)[0])
        if not ip.is_global or ip.is_multicast:
            raise FetchError(
                f"refusing {host}: it resolves to a non-public address ({ip}); "
                "use --allow-private for a local staging copy"
            )


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Re-check every redirect target with the same rules as the original URL."""

    def __init__(self, allow_private: bool) -> None:
        super().__init__()
        self.allow_private = allow_private

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl, self.allow_private)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, accept: tuple[str, ...], allow_private: bool = False) -> tuple[bytes, str]:
    """Fetch a URL with size, time, scheme and network limits. Returns (body, charset)."""
    check_url(url, allow_private)
    opener = urllib.request.build_opener(_SafeRedirect(allow_private))
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8",
        },
    )
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as resp:
            ctype = resp.headers.get_content_type()
            if not any(kind in ctype for kind in accept):
                raise FetchError(f"unexpected content type {ctype} from {url}")
            declared = resp.headers.get("Content-Length")
            if declared and declared.isdigit() and int(declared) > MAX_BYTES:
                raise FetchError(f"response from {url} is larger than {MAX_BYTES} bytes")
            body = resp.read(MAX_BYTES + 1)
            charset = resp.headers.get_content_charset() or ""
    except FetchError:
        raise
    except urllib.error.HTTPError as exc:
        raise FetchError(f"HTTP {exc.code} from {url}") from exc
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, FetchError):
            raise exc.reason from exc
        if isinstance(exc.reason, TimeoutError):
            raise FetchError(f"no response from {url} within {TIMEOUT_SECONDS}s") from exc
        raise FetchError(f"cannot reach {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise FetchError(f"no response from {url} within {TIMEOUT_SECONDS}s") from exc
    except OSError as exc:
        raise FetchError(f"cannot read {url}: {exc}") from exc
    if len(body) > MAX_BYTES:
        raise FetchError(f"response from {url} is larger than {MAX_BYTES} bytes")
    return body, charset


def is_url(source: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", source))


def read_source(
    source: str, accept: tuple[str, ...], allow_private: bool = False
) -> tuple[bytes, str]:
    """Read a URL (with fetch limits) or a local file (with the same size limit)."""
    if is_url(source):
        return fetch(source, accept, allow_private)
    if not os.path.isfile(source):
        raise FetchError(f"no such file: {source}")
    if os.path.getsize(source) > MAX_BYTES:
        raise FetchError(f"{source} is larger than {MAX_BYTES} bytes")
    with open(source, "rb") as handle:
        return handle.read(), ""


def decode(body: bytes, charset: str = "") -> str:
    if not charset:
        match = re.search(rb"""<meta[^>]+charset=["']?([\w-]+)""", body[:4096], re.I)
        charset = match.group(1).decode("ascii") if match else "utf-8"
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- extraction

BLOCK_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "figcaption",
    "dt", "dd", "td", "th", "caption", "summary",
}  # fmt: skip
ALWAYS_SKIP = {
    "script", "style", "noscript", "template", "svg", "math", "nav", "form", "button",
    "select", "textarea", "iframe", "canvas", "dialog", "object", "aside",
}  # fmt: skip
# Containers break text into separate blocks but are not block types themselves.
CONTAINER_TAGS = {
    "div", "section", "main", "article", "header", "footer", "ul", "ol", "dl", "table",
    "tr", "tbody", "thead", "tfoot", "figure", "details", "address", "hr", "pre",
}  # fmt: skip
# Starting one of these implicitly closes an open <p>, as browsers do.
CLOSES_P = (BLOCK_TAGS - {"li", "dt", "dd", "td", "th", "caption", "summary", "figcaption"}) | {
    "div", "section", "article", "main", "header", "footer", "ul", "ol", "dl", "table",
    "figure", "details", "address", "pre", "aside", "nav", "form",
}  # fmt: skip
# Starting a tag implicitly closes an open sibling of the listed kinds, up to the boundary.
IMPLIED_CLOSE = {
    "li": ({"li"}, {"ul", "ol"}),
    "dt": ({"dt", "dd"}, {"dl"}),
    "dd": ({"dt", "dd"}, {"dl"}),
    "td": ({"td", "th"}, {"tr", "table"}),
    "th": ({"td", "th"}, {"tr", "table"}),
    "tr": ({"tr", "td", "th"}, {"table", "tbody", "thead", "tfoot"}),
}
CHROME_TAGS = {"header", "footer"}  # site chrome; skipped unless inside main/article
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "source", "track", "wbr",
}  # fmt: skip


class ProseExtractor(HTMLParser):
    """Collect visible prose as (type, text) blocks.

    If the page has a <main> (or role="main"), only text inside it is kept; otherwise the
    first <article>; otherwise the whole body minus header and footer. Navigation, forms,
    scripts and hidden elements are always dropped.
    """

    def __init__(self, scope: str | None) -> None:
        super().__init__(convert_charrefs=True)
        self.scope = scope
        self.scope_done = False
        self.stack: list[tuple[str, bool, bool]] = []  # (tag, skips, opens_scope)
        self.skip_depth = 0
        self.scope_depth = 0
        self.buffer: list[str] = []
        self.blocks: list[tuple[str, str]] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta_description = ""

    def _capturing(self) -> bool:
        if self.skip_depth:
            return False
        return self.scope is None or self.scope_depth > 0

    def _current_block(self) -> str:
        for tag, _, _ in reversed(self.stack):
            if tag in BLOCK_TAGS:
                return tag
        return "text"

    def _flush(self) -> None:
        text = " ".join("".join(self.buffer).split())
        self.buffer = []
        if text:
            self.blocks.append((self._current_block(), text))

    def _opens_scope(self, tag: str, attrs: dict[str, str]) -> bool:
        if self.scope is None or self.scope_done or self.scope_depth:
            return False
        if self.scope == "main":
            return tag == "main" or attrs.get("role") == "main"
        return tag == "article"

    def _skips(self, tag: str, attrs: dict[str, str]) -> bool:
        if tag in ALWAYS_SKIP:
            return True
        if tag in CHROME_TAGS and self.scope_depth == 0:
            return True
        if "hidden" in attrs or attrs.get("aria-hidden") == "true":
            return True
        style = attrs.get("style", "").replace(" ", "").lower()
        return "display:none" in style or "visibility:hidden" in style

    def handle_starttag(self, tag, attrs):
        attr_map = {key: (value or "") for key, value in attrs}
        if tag == "meta":
            if attr_map.get("name", "").lower() == "description":
                self.meta_description = " ".join(attr_map.get("content", "").split())
            return
        if tag == "title" and not self.skip_depth and not self.title_parts:
            self.in_title = True
            return
        if tag in VOID_TAGS:
            if tag == "br":
                self.buffer.append(" ")
            return
        self._close_implied(tag)
        if tag in BLOCK_TAGS or tag in CONTAINER_TAGS:
            self._flush()
        skips = self._skips(tag, attr_map)
        opens = self._opens_scope(tag, attr_map)
        self.stack.append((tag, skips, opens))
        self.skip_depth += skips
        self.scope_depth += opens

    def _close_implied(self, tag: str) -> None:
        closes, boundary = IMPLIED_CLOSE.get(tag, (set(), set()))
        if tag in CLOSES_P:
            closes, boundary = closes | {"p"}, boundary | (CLOSES_P - {"p"})
        for open_tag, _, _ in reversed(self.stack):
            if open_tag in closes:
                self.handle_endtag(open_tag)
                return
            if open_tag in boundary:
                return

    def handle_startendtag(self, tag, attrs):
        if tag == "meta" or tag in VOID_TAGS:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title" and self.in_title:
            self.in_title = False
            return
        if not any(open_tag == tag for open_tag, _, _ in self.stack):
            return
        while self.stack:
            open_tag, skips, opens = self.stack[-1]
            if open_tag in BLOCK_TAGS or open_tag in CONTAINER_TAGS:
                if self._capturing():
                    self._flush()
                else:
                    self.buffer = []
            self.stack.pop()
            self.skip_depth -= skips
            self.scope_depth -= opens
            if opens:
                self._flush()
                self.scope_done = True
            if open_tag == tag:
                break

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        elif self._capturing():
            self.buffer.append(data)

    def close(self):
        super().close()
        if self._capturing():
            self._flush()

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def detect_scope(html: str) -> str | None:
    if re.search(r"<main[\s>]|role\s*=\s*[\"']main[\"']", html, re.I):
        return "main"
    if re.search(r"<article[\s>]", html, re.I):
        return "article"
    return None


def extract(html: str) -> dict:
    parser = ProseExtractor(detect_scope(html))
    parser.feed(html)
    parser.close()
    raw = list(parser.blocks)
    if parser.meta_description:
        raw.insert(0, ("meta-description", parser.meta_description))
    blocks = [
        {"id": f"b{index:03d}", "type": kind, "text": text}
        for index, (kind, text) in enumerate(raw, start=1)
    ]
    return {
        "title": parser.title,
        "words": sum(len(block["text"].split()) for block in blocks),
        "blocks": blocks,
    }


def render_text(page: dict) -> str:
    lines = [
        f"title: {page['title']}",
        f"source: {page['source']}",
        f"retrieved: {page['retrieved']}",
        f"extractor: pages.py {VERSION}",
        f"words: {page['words']}",
        "",
    ]
    lines += [f"[{block['id']} {block['type']}] {block['text']}" for block in page["blocks"]]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- URL lists


def _maybe_gunzip(body: bytes) -> bytes:
    if not body.startswith(b"\x1f\x8b"):
        return body
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise FetchError(f"decompressed sitemap is larger than {MAX_BYTES} bytes")
    return data


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_sitemap(body: bytes) -> tuple[str, list[str]]:
    """Return ("urlset" | "sitemapindex", locations)."""
    if re.search(rb"<!DOCTYPE|<!ENTITY", body, re.I):
        raise FetchError("sitemap declares a DOCTYPE or entities; refusing to parse it")
    try:
        root = ET.fromstring(body)  # noqa: S314 - see DOCTYPE/ENTITY check above
    except ET.ParseError as exc:
        raise FetchError(f"sitemap is not valid XML: {exc}") from exc
    kind = _local_name(root.tag)
    if kind not in ("urlset", "sitemapindex"):
        raise FetchError(f"not a sitemap (root element is <{kind}>)")
    locations = [
        (element.text or "").strip()
        for element in root.iter()
        if _local_name(element.tag) == "loc" and (element.text or "").strip()
    ]
    return kind, locations


def parse_url_list(text: str) -> tuple[list[str], list[str]]:
    """Return (urls, rejected lines) from a one-URL-per-line list."""
    urls, rejected = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if urllib.parse.urlsplit(line).scheme in ("http", "https"):
            urls.append(line)
        else:
            rejected.append(line)
    return urls, rejected


def expand_urls(
    source: str,
    allow_private: bool = False,
    include: str | None = None,
    exclude: str | None = None,
    limit: int | None = None,
    warn=lambda message: None,
) -> list[str]:
    accept = ("xml", "html", "text/plain", "gzip")
    budget = {"children": MAX_CHILD_SITEMAPS}

    def collect(src: str, depth: int) -> list[str]:
        body, charset = read_source(src, accept, allow_private)
        body = _maybe_gunzip(body)
        if not body.lstrip().startswith(b"<"):
            urls, rejected = parse_url_list(decode(body, charset))
            for line in rejected:
                warn(f"skipping line that is not an http(s) URL: {line[:120]}")
            return urls
        kind, locations = parse_sitemap(body)
        if kind == "urlset":
            return locations
        found: list[str] = []
        for child in locations:
            if depth >= MAX_SITEMAP_DEPTH:
                warn(f"not following nested sitemap index beyond depth {depth}: {child}")
                continue
            if budget["children"] <= 0:
                warn(f"child sitemap limit ({MAX_CHILD_SITEMAPS}) reached; skipping {child}")
                continue
            budget["children"] -= 1
            try:
                found += collect(child, depth + 1)
            except FetchError as exc:
                warn(f"could not read child sitemap: {exc}")
        return found

    urls = collect(source, 0)
    include_re = re.compile(include) if include else None
    exclude_re = re.compile(exclude) if exclude else None
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
            warn(f"skipping non-http(s) location: {url[:120]}")
            continue
        if include_re and not include_re.search(url):
            continue
        if exclude_re and exclude_re.search(url):
            continue
        if url in seen:
            continue
        seen.add(url)
        result.append(url)
        if limit is not None and len(result) >= limit:
            break
    return result


# --------------------------------------------------------------------------- CLI


def _warn(message: str) -> None:
    print(f"pages.py: warning: {message}", file=sys.stderr)


def cmd_urls(args: argparse.Namespace) -> int:
    urls = expand_urls(
        args.source,
        allow_private=args.allow_private,
        include=args.include,
        exclude=args.exclude,
        limit=args.limit,
        warn=_warn,
    )
    for url in urls:
        print(url)
    print(f"pages.py: {len(urls)} URLs", file=sys.stderr)
    if not urls:
        _warn("no URLs found")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    body, charset = read_source(args.source, ("html",), args.allow_private)
    page = extract(decode(body, charset))
    page["source"] = args.source
    page["retrieved"] = date.today().isoformat()
    if args.format == "json":
        page["extractor"] = f"pages.py {VERSION}"
        print(json.dumps(page, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(render_text(page))
    if page["words"] < 50:
        _warn(
            f"only {page['words']} words extracted; the page may be rendered by JavaScript "
            "or have little prose"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pages.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("--version", action="version", version=f"pages.py {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    urls = sub.add_parser("urls", help="expand a URL list or sitemap to one URL per line")
    urls.add_argument("source", help="file path or http(s) URL of a sitemap or URL list")
    urls.add_argument("--include", help="keep only URLs matching this regular expression")
    urls.add_argument("--exclude", help="drop URLs matching this regular expression")
    urls.add_argument("--limit", type=int, help="stop after this many URLs")
    urls.set_defaults(func=cmd_urls)

    ext = sub.add_parser("extract", help="print a page's prose as numbered blocks")
    ext.add_argument("source", help="http(s) URL or saved HTML file")
    ext.add_argument("--format", choices=("text", "json"), default="text")
    ext.set_defaults(func=cmd_extract)

    for command in (urls, ext):
        command.add_argument(
            "--allow-private",
            action="store_true",
            help="allow hosts on private or loopback networks (local staging copies)",
        )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if getattr(args, "limit", None) is not None and args.limit < 1:
        print("pages.py: error: --limit must be at least 1", file=sys.stderr)
        return 2
    try:
        return args.func(args)
    except (FetchError, re.error) as exc:
        print(f"pages.py: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
