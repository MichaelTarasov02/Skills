#!/usr/bin/env python3
"""
Crawl company sites for the roles no registry publishes.

Reads robots.txt first and honours Disallow. Fetches the homepage plus up to three
team/leadership pages, and accepts only tight name-to-title pairings.

Three accepted patterns, and nothing else:
    A  "Jane Doe, Director of Nursing"      name, separator, title
    B  "Administrator: Jane Doe"            title, separator, name
    C  "Jane Doe" / "Administrator"         name alone, title alone on the next line

Looser proximity matching - a name anywhere near a role word - was tried first and produced
plausible garbage that survives review: real names attached to the wrong role, and headings
read as people. Recall halved when this tightened; precision went from unusable to clean.

Resumable: appends JSONL, skips domains already present.

Usage:
    python3 fetch_web.py domains.txt out.jsonl [--roles roles.json] [--workers 8]

roles.json maps a canonical role to a regex over titles, e.g.
    {"payroll": "\\bpayroll\\b", "hr": "\\bhuman resources?\\b|\\bHR (director|manager)\\b"}
Omit it to use the built-in default set.
"""
import argparse
import gzip
import html
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from name_filter import is_person_name          # noqa: E402

UA = "lead-generation-skill/0.1 (+research; contact via site owner)"
TIMEOUT = 15
MAX_PAGES = 4
PAUSE = 0.4

DEFAULT_ROLES = {
    "payroll": r"\bpayroll\b",
    "hr": r"\b(human resources?|HR (director|manager|coordinator)|personnel|"
          r"director of (human resources|people)|staff development)\b",
    "scheduler": r"\b(scheduler|scheduling (coordinator|manager|director)|"
                 r"staffing (coordinator|manager|specialist))\b",
    "finance": r"\b(controller|comptroller|accountant|accounting (manager|director)|"
               r"business office manager|CFO|chief financial officer|"
               r"(director of finance|finance director)|bookkeeper)\b",
    "executive": r"\b(administrator|executive director|CEO|chief executive|"
                 r"chief operating|COO|president)\b",
    "owner": r"\b(owner|founder|principal|proprietor|managing partner)\b",
}

LINK_HINTS = re.compile(
    r"(our[-_ ]?team|meet[-_ ]?the[-_ ]?team|leadership|management|staff|"
    r"administration|about[-_ ]?us|our[-_ ]?people|directory|contact)", re.I)
NAME_LINE = re.compile(r"^[A-Z][a-z'’\-]{1,20}(\s+[A-Z]\.?)?(\s+[A-Z][a-z'’\-]{1,20})?"
                       r"\s+[A-Z][a-z'’\-]{1,25}$")
SEP = r"\s*[,\|–—:\-]\s*"
MAILTO = re.compile(r"mailto:([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})", re.I)
TAG = re.compile(r"<[^>]+>")
SCRIPT = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.S | re.I)

lock = Lock()
counter = {"n": 0}


def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html", "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read(1_500_000)
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
        ctype = r.headers.get("Content-Type", "")
        if ctype and "html" not in ctype:
            return None, r.geturl()
        return raw.decode("utf-8", errors="replace"), r.geturl()


def lines_of(h):
    h = SCRIPT.sub(" ", h)
    h = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/td|/tr|/span)[^>]*>", "\n", h, flags=re.I)
    h = html.unescape(TAG.sub(" ", h))
    return [re.sub(r"[ \t\xa0]+", " ", ln).strip()[:300]
            for ln in h.split("\n") if ln.strip()]


def role_of(text, patterns):
    for role, rx in patterns.items():
        if rx.search(text):
            return role
    return None


def extract(lines, patterns):
    hits, seen = [], set()

    def add(role, name, ctx, form):
        if is_person_name(name) and (role, name.lower()) not in seen:
            seen.add((role, name.lower()))
            hits.append({"role": role, "name": name.strip(),
                         "context": ctx[:160], "pattern": form})

    for i, ln in enumerate(lines):
        if len(ln) > 120:
            continue
        m = re.match(rf"^(.{{4,40}}?){SEP}(.{{3,70}})$", ln)
        if m:
            left, right = m.group(1).strip(), m.group(2).strip()
            r = role_of(right, patterns)
            if r and not role_of(left, patterns):
                add(r, left, ln, "A")
                continue
            r = role_of(left, patterns)
            if r and not role_of(right, patterns):
                add(r, right, ln, "B")
                continue
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if len(nxt) <= 45 and not role_of(ln, patterns) and NAME_LINE.match(ln):
                r = role_of(nxt, patterns)
                if r:
                    add(r, ln, f"{ln} / {nxt}", "C")
    return hits


def crawl(domain, patterns):
    rec = {"domain": domain, "ok": False, "people": [], "emails": [],
           "pages": [], "error": None}
    body = base = None
    for scheme in ("https://", "http://"):
        try:
            body, base = get(scheme + domain)
            break
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {str(e)[:70]}"
    if not base or body is None:
        return rec

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(base, "/robots.txt"))
    try:
        rp.read()
    except Exception:
        rp = None

    def allowed(u):
        try:
            return rp.can_fetch(UA, u) if rp else True
        except Exception:
            return True

    if not allowed(base):
        rec["error"] = "disallowed by robots.txt"
        return rec

    rec["ok"] = True
    pages, links = [(base, body)], []
    host = urllib.parse.urlparse(base).netloc
    for m in re.finditer(r'href=["\']([^"\'#]+)["\']', body, re.I):
        href = m.group(1)
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        full = urllib.parse.urljoin(base, href)
        if urllib.parse.urlparse(full).netloc == host and LINK_HINTS.search(full) \
                and full not in links:
            links.append(full)

    for url in links[:MAX_PAGES - 1]:
        if not allowed(url):
            continue
        try:
            time.sleep(PAUSE)
            b, final = get(url)
            if b:
                pages.append((final, b))
        except Exception:
            continue

    for url, b in pages:
        rec["pages"].append(url)
        rec["people"].extend(extract(lines_of(b), patterns))
        for em in MAILTO.findall(b):
            em = em.lower()
            if em not in rec["emails"]:
                rec["emails"].append(em)

    seen, ded = set(), []
    for p in rec["people"]:
        k = (p["role"], p["name"].lower())
        if k not in seen:
            seen.add(k)
            ded.append(p)
    rec["people"], rec["emails"] = ded, rec["emails"][:40]
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domains")
    ap.add_argument("out")
    ap.add_argument("--roles")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    raw = json.load(open(a.roles, encoding="utf-8")) if a.roles else DEFAULT_ROLES
    patterns = {k: re.compile(v, re.I) for k, v in raw.items()}

    domains = [d.strip() for d in open(a.domains, encoding="utf-8") if d.strip()]
    done = set()
    if os.path.exists(a.out):
        with open(a.out, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["domain"])
                except Exception:
                    pass
    todo = [d for d in domains if d not in done]
    print(f"domains {len(domains)} | cached {len(done)} | to crawl {len(todo)}")
    if not todo:
        return

    out = open(a.out, "a", encoding="utf-8")
    total = len(todo)

    def work(d):
        rec = crawl(d, patterns)
        with lock:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            counter["n"] += 1
            if counter["n"] % 50 == 0:
                out.flush()
                print(f"  {counter['n']}/{total}", flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        found = sum(1 for r in ex.map(work, todo) if r["people"])
    out.close()
    print(f"done. domains with people: {found}/{total}")


if __name__ == "__main__":
    main()
