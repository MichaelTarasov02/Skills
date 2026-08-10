#!/usr/bin/env python3
"""List every bespoke object every post has used, so a repeat is a lookup.

    python3 list_objects.py <output_dir>          # e.g. Personal/Posts
    python3 list_objects.py <output_dir> --names  # bare names, one per line

Exists because the uniqueness rule asks whether an object has appeared before,
and answering that by opening thirty-seven `Visual/README.md` files is how a
repeat gets shipped. The rule is only as good as the lookup behind it.

Two sources, in order of trust:

  1. `data-object="…"` attributes in `Visual/carousel.html`. This is what
     `verify_visual.mjs` counts, so it is the truth about what a deck contains.
  2. The `| Bespoke object |` row in `Visual/README.md`, which is where the
     older posts recorded theirs before the attribute existed.

A post that appears only in source 2 predates the marking convention. That is
reported rather than hidden, because "no objects found" and "this post is older
than the rule" are different facts.
"""
import re
import sys
from pathlib import Path

OBJ_ATTR = re.compile(r'data-object\s*=\s*"([^"]+)"')
OBJ_TIER = re.compile(r'data-object-tier\s*=\s*"([^"]+)"')
README_ROW = re.compile(r"\|\s*Bespoke object\s*\|\s*(.+?)\s*\|", re.I)
README_NAME = re.compile(r"`\.?([A-Za-z][\w-]*)`")


def objects_from_html(html: Path):
    """(name, tier) pairs in document order, deduplicated, first tier wins."""
    if not html.exists():
        return []
    text = html.read_text(encoding="utf-8", errors="replace")
    out, seen = [], set()
    # Walk tags so a name and its tier stay associated even when the attributes
    # are written in either order on the same element.
    for tag in re.findall(r"<[^>]*data-object[^>]*>", text):
        m = OBJ_ATTR.search(tag)
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        t = OBJ_TIER.search(tag)
        out.append((m.group(1), t.group(1) if t else "unmarked"))
    return out


def objects_from_readme(readme: Path):
    if not readme.exists():
        return []
    out = []
    for row in README_ROW.findall(readme.read_text(encoding="utf-8", errors="replace")):
        m = README_NAME.search(row)
        if m:
            out.append((m.group(1), row))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    names_only = "--names" in sys.argv
    root = Path(args[0] if args else ".").expanduser()
    if not root.is_dir():
        print(f"no such directory: {root}", file=sys.stderr)
        sys.exit(1)

    rows, legacy, all_names = [], [], set()
    for post in sorted(p for p in root.iterdir() if p.is_dir()):
        vis = post / "Visual"
        marked = objects_from_html(vis / "carousel.html")
        if marked:
            for name, tier in marked:
                rows.append((post.name, name, tier))
                all_names.add(name)
            continue
        for name, gloss in objects_from_readme(vis / "README.md"):
            legacy.append((post.name, name, gloss))
            all_names.add(name)

    if names_only:
        for n in sorted(all_names):
            print(n)
        return

    if rows:
        print("MARKED — counted by verify_visual.mjs\n")
        width = max(len(p) for p, _, _ in rows)
        sig = 0
        for post, name, tier in rows:
            print(f"  {post.ljust(width)}  .{name}  [{tier}]")
            sig += tier == "signature"
        print(f"\n  {len(rows)} objects across "
              f"{len({p for p, _, _ in rows})} posts · {sig} signature")

    if legacy:
        print("\nLEGACY — recorded in README before data-object existed\n")
        width = max(len(p) for p, _, _ in legacy)
        for post, name, gloss in legacy:
            print(f"  {post.ljust(width)}  .{name}")
        print(f"\n  {len(legacy)} objects across {len({p for p, _, _ in legacy})} posts")

    print(f"\nTOTAL DISTINCT NAMES: {len(all_names)}")
    print("A new signature object must not appear above. A supporting object may")
    print("share a family with one of these, but must not re-skin a signature.")


if __name__ == "__main__":
    main()
