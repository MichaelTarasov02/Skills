#!/usr/bin/env python3
"""Verify a New Ideas file before handing it to the author.

Exists because the author's complaint about the previous version was specific and
mechanical: ideas arrived in the wrong shape to use, and English words leaked into
Russian text. Both are cheap to check by machine and expensive to check by eye.

Usage:
    python3 verify_ideas.py "<path to the ideas file>"
    python3 verify_ideas.py "<path>" --expect 3      # assert the idea count
    python3 verify_ideas.py "<path>" --json

Exit code is 0 when every check passes, 1 otherwise, so it can gate a loop.
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Every field the form must carry, in the order new-post reads them.
REQUIRED_FIELDS = [
    "Идея", "Личный контекст", "Тема", "Целевой читатель", "Цель",
    "Наклон обсуждения", "Упоминание компании", "Визуал", "CTA",
    "Риск-ограничения", "Сид оптимизации", "Черновик хука",
]

# Prose sections that must appear above each form.
REQUIRED_SECTIONS = ["Почему автор это использует", "Почему сейчас", "Не дубль потому что"]

# Latin-script tokens that are legitimate inside Russian text: proper nouns,
# product names, and terms with no accepted Russian equivalent. Anything else in
# Latin script is the leak the author reported.
LATIN_ALLOWLIST = {
    # products, companies, platforms
    "linkedin", "claude", "code", "mcp", "github", "gitlab", "epeople", "sinister",
    "openai", "anthropic", "figma", "notion", "slack", "jira", "cursor", "vercel",
    "google", "apple", "microsoft", "meta", "amazon", "aws", "ios", "android",
    # terms without a settled Russian equivalent
    "ai", "saas", "b2b", "b2c", "mvp", "api", "sdk", "ui", "ux", "cto", "ceo",
    "cpo", "hr", "qa", "it", "llm", "rag", "devops", "pm", "roi", "kpi",
    "thought", "leadership", "trade", "off", "tradeoff", "dm", "cta", "seo",
    "none", "optional", "recommended", "required", "text", "markdown",
    "backend", "frontend", "fullstack", "prompt", "agent", "workflow", "product",
    # form scaffolding that stays English by contract
    "en", "ru",
}

ENGAGEMENT_RE = re.compile(
    r"\b[\d][\d\s,.]*\s*(impression|like|reach|view|follower|просмотр|лайк|охват|подписчик)",
    re.I)

URL_RE = re.compile(r"https?://\S+")
DATE_RE = re.compile(
    r"\b(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}"
    r"|\d{4}-\d{2}-\d{2}"
    r"|\d{1,2}\s+(январ|феврал|март|апрел|ма[йя]|июн|июл|август|сентябр|октябр|ноябр|декабр)\w*"
    r"|(январ|феврал|март|апрел|ма[йя]|июн|июл|август|сентябр|октябр|ноябр|декабр)\w*\s+\d{4})\b",
    re.I)


def strip_protected(text: str) -> str:
    """Remove only the spans where Latin script is legitimate.

    Order matters. The hook goes first because it is English by contract. Fence
    markers are dropped as whole lines, but the fenced body is deliberately kept:
    the form fields are exactly where a leak does the most damage. Inline code
    spans are matched single-line so the pattern cannot run across a ``` fence
    and swallow the form with it, which is what an earlier version did.
    """
    text = re.sub(r"^Черновик хука[^:\n]*:.*?(?=\n[А-ЯЁ][^\n:]*:|\n```|\Z)",
                  " ", text, flags=re.S | re.M)
    text = re.sub(r"^\s*```.*$", " ", text, flags=re.M)
    text = URL_RE.sub(" ", text)
    text = re.sub(r"`[^`\n]+`", " ", text)
    # Quoted spans are proper nouns by convention — an English post title cited in
    # "не дубль потому что" is legitimate, and no allowlist can enumerate titles.
    # Quoting is the author's signal that the Latin inside is a name, not a leak.
    text = re.sub(r"[«\"'“‘][^»\"'”’\n]{1,120}[»\"'”’]", " ", text)
    return text


def latin_leaks(text: str):
    """Latin-script words sitting inside Russian prose, outside the allowlist."""
    hits = {}
    for m in re.finditer(r"[A-Za-z][A-Za-z'\-]{2,}", strip_protected(text)):
        w = m.group(0)
        if w.lower().strip("'-") in LATIN_ALLOWLIST:
            continue
        hits[w] = hits.get(w, 0) + 1
    return hits


def split_ideas(text: str):
    """Each idea is a level-2 heading numbered from 1."""
    parts = re.split(r"^##\s+(\d+)\.\s*(.+)$", text, flags=re.M)
    ideas = []
    for i in range(1, len(parts) - 1, 3):
        ideas.append({"n": int(parts[i]), "title": parts[i + 1].strip(), "body": parts[i + 2]})
    return ideas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--expect", type=int, default=None,
                    help="assert this many ideas")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    path = Path(args.target).expanduser()
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    problems, notes = [], []

    ideas = split_ideas(text)
    notes.append(f"ideas: {len(ideas)}")
    if not ideas:
        problems.append("no ideas found — each idea needs a '## N. Тезис' heading")
    if args.expect is not None and len(ideas) != args.expect:
        problems.append(f"found {len(ideas)} ideas, expected {args.expect}")

    for idea in ideas:
        tag = f"idea {idea['n']}"
        body = idea["body"]

        if idea["title"].endswith("?"):
            problems.append(f"{tag}: the thesis is a question, it must be an assertion")

        for sec in REQUIRED_SECTIONS:
            if sec not in body:
                problems.append(f"{tag}: missing section '{sec}'")

        form = re.search(r"```text\n(.*?)\n```", body, re.S)
        if not form:
            problems.append(f"{tag}: no fenced form block — nothing to paste into new-post")
            continue
        form_text = form.group(1)

        # Slice the form on its own field headers rather than with a lookahead
        # per field. A lookahead whose leading \s* swallowed the blank line
        # between fields read the *next* field's value and reported an empty
        # field as filled, which is the one failure this check exists to catch.
        # The header pattern tolerates a parenthetical suffix, e.g. "(EN)".
        headers = [(m.start(), m.end(), m.group(1).strip())
                   for m in re.finditer(
                       r"^([А-ЯЁA-Z][^\n:()]*?)\s*(?:\([^)]*\))?\s*:", form_text, re.M)]
        found = {}
        for i, (s, e, name) in enumerate(headers):
            stop = headers[i + 1][0] if i + 1 < len(headers) else len(form_text)
            found[name] = form_text[e:stop].strip()

        for field in REQUIRED_FIELDS:
            if field not in found:
                problems.append(f"{tag}: form field missing — {field}")
            elif not found[field]:
                problems.append(f"{tag}: form field empty — {field}")
            elif re.fullmatch(r"[\[\]…\.\-\s]*", found[field]):
                problems.append(f"{tag}: form field left as a placeholder — {field}")

        why_now = re.search(r"Почему сейчас:(.*?)(?=\n\*\*|\Z)", body, re.S)
        if why_now:
            seg = why_now.group(1)
            if not URL_RE.search(seg):
                problems.append(f"{tag}: 'Почему сейчас' has no working link")
            if not DATE_RE.search(seg):
                problems.append(f"{tag}: 'Почему сейчас' has no date")

        reader = re.search(r"^Целевой читатель\s*:\s*\n?(.+)$", form_text, re.M)
        if reader and re.search(r"\bи\b|,", reader.group(1)):
            notes.append(f"{tag}: check the reader is one role, not a list")

    for m in ENGAGEMENT_RE.finditer(text):
        problems.append(f"invented engagement figure: '{m.group(0).strip()}'")

    leaks = latin_leaks(text)
    if leaks:
        shown = ", ".join(f"{w}×{n}" if n > 1 else w
                          for w, n in sorted(leaks.items(), key=lambda x: -x[1])[:12])
        problems.append(f"Latin words in Russian text: {shown}")

    if args.json:
        print(json.dumps({"ok": not problems, "notes": notes, "problems": problems},
                         ensure_ascii=False, indent=2))
    else:
        print(f"ideas file: {path}")
        for n in notes:
            print(f"  · {n}")
        print()
        if problems:
            print(f"FAIL — {len(problems)} problem(s):")
            for p in problems:
                print(f"  ✗ {p}")
        else:
            print("PASS — form complete, sources dated and linked, Russian clean")

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
