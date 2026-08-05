#!/usr/bin/env python3
"""Verify a Post Specification before the visual is built.

Exists because three consecutive runs re-derived these same checks by hand and
each time missed something different. Structure is cheap to check mechanically;
spending judgement on it is waste.

Usage:
    python3 verify_spec.py "<post folder>"           # folder or direct .md path
    python3 verify_spec.py "<post folder>" --json    # machine-readable

Exit code is 0 when every check passes, 1 otherwise, so it can gate a loop.
"""
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Source Idea", "Assumptions", "Personal Brand Fit", "Strategic Interpretation",
    "Post Metadata", "Reader Psychology", "Narrative Angle", "Post Structure",
    "Discussion Strategy", "LinkedIn Optimization Notes", "Copy-Ready LinkedIn Post",
    "Alternate Hooks", "Post Copy Notes", "Visual Specification",
    "Optional Visual Decision", "Optional Visual Brief", "CTA / Closing Move",
    "Risk Notes", "Human Voice QA", "Acceptance Criteria",
]

# Generic AI-tells and unverifiable claims. Overridable via personal-post.yaml.
DEFAULT_WATCHLIST = [
    "delve", "leverage", "robust", "seamless", "holistic", "transformative",
    "game-changer", "game changer", "paradigm", "unlock", "empower",
    "cutting-edge", "comprehensive", "world-class", "revolutioniz",
    "10x", "guaranteed", "future-proof", "multifaceted", "impactful",
]

# Constructions that read as machine-written regardless of vocabulary.
BANNED_PATTERNS = [
    (r"[—–]", "em/en dash — use a period or comma"),
    (r"\bit'?s not [a-z ]{2,30}, it'?s\b", "'not X, it's Y' construction"),
    (r"\bread that again\b", "engagement-bait phrase"),
    (r"\blet that sink in\b", "engagement-bait phrase"),
    (r"^\s*(thoughts|agree)\?\s*$", "generic engagement-bait CTA"),
]

# The trailing \b matters more than it looks. Without it "view" matched inside
# "viewBox", so any spec describing an SVG object was reported as carrying an
# invented engagement figure. This system draws an SVG in almost every post.
ENGAGEMENT_RE = re.compile(
    r"\b[\d][\d\s,.]*\s*"
    r"(impressions?|likes?|reach|views?|followers?"
    r"|просмотр\w*|лайк\w*|охват\w*|подписчик\w*)\b",
    re.I)


# The profile filename, newest first. `founder-post.yaml` is the pre-rename name,
# kept so an older content repo keeps working instead of failing as "no profile".
PROFILE_NAMES = ("personal-post.yaml", "founder-post.yaml")


def load_config(start: Path):
    """Walk upward for the author profile. Absent config is fine — defaults apply."""
    cfg = {}
    for d in [start] + list(start.parents):
        p = next((d / n for n in PROFILE_NAMES if (d / n).exists()), d / PROFILE_NAMES[0])
        if p.exists():
            try:
                import yaml  # optional dependency
                cfg = yaml.safe_load(p.read_text()) or {}
            except Exception:
                # Minimal parse so the check still runs without PyYAML.
                for line in p.read_text().splitlines():
                    m = re.match(r"^\s*(caption_min|caption_max)\s*:\s*(\d+)", line)
                    if m:
                        cfg[m.group(1)] = int(m.group(2))
            break
    else:
        for n in PROFILE_NAMES:
            home = Path.home() / f".{n}"
            if home.exists():
                try:
                    import yaml
                    cfg = yaml.safe_load(home.read_text()) or {}
                except Exception:
                    pass
                break
    return cfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = Path(args.target).expanduser()
    md = target if target.suffix == ".md" else target / "Post Specification.md"
    if not md.exists():
        print(f"FAIL: no specification at {md}")
        sys.exit(1)

    cfg = load_config(md.parent)
    cap_min = int(cfg.get("caption_min", 600))
    cap_max = int(cfg.get("caption_max", 1100))
    short_min = int(cfg.get("caption_short_min", 250))
    short_max = int(cfg.get("caption_short_max", 600))
    watchlist = cfg.get("watchlist", DEFAULT_WATCHLIST)

    text = md.read_text()
    problems, notes = [], []

    # --- required sections -------------------------------------------------
    missing = [s for s in REQUIRED_SECTIONS if f"# {s}" not in text]
    if missing:
        problems.append(f"missing sections ({len(missing)}): {', '.join(missing)}")
    notes.append(f"sections: {len(REQUIRED_SECTIONS)-len(missing)}/{len(REQUIRED_SECTIONS)}")

    # --- the captions ------------------------------------------------------
    # `Post Copy.md` is the source of truth when it exists: it carries the long
    # carousel caption and the short single-page caption, and the specification
    # points at it instead of holding a second copy. Posts written before that
    # file existed keep their caption fenced inside the spec, so the in-spec
    # form stays valid — a check that fails on a shipped post is a broken check,
    # not a finding.
    copy_file = md.parent / "Post Copy.md"

    def audit(label, cap, lo, hi):
        chars, words = len(cap), len(cap.split())
        notes.append(f"{label}: {chars} chars / {words} words")
        if not (lo <= chars <= hi):
            problems.append(f"{label} {chars} chars is outside the {lo}-{hi} band")
        hits = [w for w in watchlist if w.lower() in cap.lower()]
        if hits:
            problems.append(f"watchlist words in {label}: {', '.join(hits)}")
        for pat, why in BANNED_PATTERNS:
            if re.search(pat, cap, re.I | re.M):
                problems.append(f"banned construction in {label}: {why}")
        qs = [l for l in cap.split("\n") if l.strip().endswith("?")]
        if len(qs) > 1:
            problems.append(
                f"{len(qs)} questions in {label} — rhetorical setups read as AI-written")

    caption = ""
    if copy_file.exists():
        ctext = copy_file.read_text()
        notes.append("captions read from Post Copy.md")
        pairs = [("carousel caption", r"##\s*Carousel version.*?\n+```text\n(.*?)\n```",
                  cap_min, cap_max),
                 ("single-page caption", r"##\s*Single-page version.*?\n+```text\n(.*?)\n```",
                  short_min, short_max)]
        for label, pat, lo, hi in pairs:
            cm = re.search(pat, ctext, re.S | re.I)
            if not cm:
                problems.append(f"Post Copy.md: no fenced {label} found")
                continue
            cap = cm.group(1).strip()
            if label.startswith("carousel"):
                caption = cap
            audit(label, cap, lo, hi)
    else:
        m = re.search(r"## Copy-Ready LinkedIn Post\s*\n+```text\n(.*?)\n```", text, re.S)
        if not m:
            problems.append("no fenced copy-ready caption found, and no Post Copy.md")
        else:
            caption = m.group(1).strip()
            audit("caption", caption, cap_min, cap_max)

    # --- invented engagement metrics ---------------------------------------
    for i, line in enumerate(text.split("\n"), 1):
        if ENGAGEMENT_RE.search(line) and "ПРОКСИ" not in line and "proxy" not in line.lower():
            problems.append(f"line {i}: possible invented engagement metric")

    # --- placeholders left behind ------------------------------------------
    for pat in [r"\bTODO\b", r"\bTBD\b", r"\[placeholder", r"\bXXX\b", r"\.\.\.\s*$"]:
        for i, line in enumerate(text.split("\n"), 1):
            if re.search(pat, line, re.I):
                problems.append(f"line {i}: placeholder or truncation left in spec")

    # --- the fields Stage 3 depends on -------------------------------------
    for field in ["Visual decision:", "Visual theme:", "Carousel depth:"]:
        if field not in text:
            problems.append(f"missing '{field}' — Stage 3 reads this")

    vd = re.search(r"Visual decision:\s*(\w+)", text)
    if vd:
        notes.append(f"visual decision: {vd.group(1)}")
    th = re.search(r"Visual theme:\s*(\w+)", text)
    if th:
        notes.append(f"theme: {th.group(1)}")

    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems, "notes": notes}, indent=2))
    else:
        print(f"spec: {md}")
        for n in notes:
            print(f"  · {n}")
        if problems:
            print(f"\nFAIL — {len(problems)} problem(s):")
            for p in problems:
                print(f"  ✗ {p}")
        else:
            print("\nPASS — structure, caption, and watchlist all clean")

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
