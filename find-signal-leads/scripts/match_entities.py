#!/usr/bin/env python3
"""
Match names from an external dataset against organisations in the contact book.

Name matching is where lead pipelines quietly break. Organisation names are mostly generic
words, so a loose rule produces confident nonsense: "Palo Alto Networks, Inc." matching
"Palo Alto Post-Acute", "City of Los Angeles" matching "Los Angeles Post Acute". Both are
real failures from the run this script came from, produced by subset matching on the
distinctive tokens alone.

The rule that survived review:
  1. Corporate suffixes are stripped - they carry no meaning.
  2. Tokens appearing in more than GENERIC_DF of all names are generic. They find
     candidates and take no part in the decision.
  3. The decision runs on the FULL token sets, by Jaccard similarity. This is the step
     that rejects the failures above: distinctive tokens can match completely while the
     full names describe different organisations.

Usage:
    python3 match_entities.py contacts.db candidates.jsonl > matches.jsonl

candidates.jsonl: one JSON object per line with at least {"name": "...", "ref": "..."}.
Any other keys are passed through to the output.
"""
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict

GENERIC_DF = 0.015     # token in >1.5% of names is generic
GENERIC_FLOOR = 3      # ...and in at least this many names, so small universes still work
JACCARD_MIN = 0.75     # full-token similarity required to accept
MIN_LEN = 6            # shorter normalised strings are too ambiguous to match

SUFFIX = re.compile(
    r"\b(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LP|LLP|PLC|LTD|"
    r"LIMITED|PARTNERSHIP|DBA|AKA|FKA|THE|GMBH|BV|NV|SA|AG|PTY|"
    r"LIABILITY|DOES|ET AL|AN INDIVIDUAL|TRUST|HOLDINGS?)\b", re.I)


def norm(s):
    if not s:
        return ""
    s = s.upper().replace("&", " AND ")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = SUFFIX.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def toks(s):
    return [t for t in norm(s).split() if len(t) > 1 and not t.isdigit()]


def build_index(conn):
    """Index organisation names and parent names, and learn which tokens are generic."""
    rows = conn.execute(
        "SELECT org_id, name, parent_name FROM organization").fetchall()
    df = Counter()
    for _, name, _ in rows:
        for t in set(toks(name)):
            df[t] += 1
    # A percentage alone marks every token generic when the universe is tiny, which leaves
    # nothing distinctive to anchor on and matches nothing at all.
    cutoff = max(GENERIC_FLOOR, GENERIC_DF * len(rows))
    generic = {t for t, c in df.items() if c >= cutoff}

    exact = defaultdict(set)          # normalised string -> {(org_id, level)}
    by_token = defaultdict(set)       # distinctive token -> {(org_id, level, normalised)}
    for org_id, name, parent in rows:
        for value, level in ((name, "organization"), (parent, "parent")):
            if not value:
                continue
            n = norm(value)
            if not n:
                continue
            exact[n].add((org_id, level))
            for t in toks(value):
                if t not in generic:
                    by_token[t].add((org_id, level, n))
    return exact, by_token, generic, len(rows)


def match(name, exact, by_token, generic):
    """Return [(org_id, level, method, confidence)] for one candidate name."""
    n = norm(name)
    if len(n) < MIN_LEN:
        return []

    hits = [(org_id, level, "exact", "high") for org_id, level in exact.get(n, ())]
    if hits:
        return hits

    full = set(toks(name))
    distinctive = full - generic
    if not distinctive:
        return []                      # only generic words: nothing to anchor on

    seen, out = set(), []
    for t in distinctive:
        for org_id, level, cand_norm in by_token.get(t, ()):
            if (org_id, level) in seen:
                continue
            cand_full = set(toks(cand_norm))
            union = full | cand_full
            if not union:
                continue
            if len(full & cand_full) / len(union) < JACCARD_MIN:
                continue
            if not ((full & cand_full) - generic):
                continue               # overlap was generic words only
            seen.add((org_id, level))
            out.append((org_id, level, "jaccard", "medium"))
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: match_entities.py <contacts.db> <candidates.jsonl>")
    conn = sqlite3.connect(sys.argv[1])
    exact, by_token, generic, n_orgs = build_index(conn)
    print(f"# organisations indexed: {n_orgs}", file=sys.stderr)
    print(f"# generic tokens ignored: {len(generic)}", file=sys.stderr)

    n_in = n_out = 0
    with open(sys.argv[2], encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            n_in += 1
            for org_id, level, method, conf in match(
                    rec.get("name", ""), exact, by_token, generic):
                print(json.dumps({**rec, "org_id": org_id, "match_level": level,
                                  "match_method": method, "confidence": conf},
                                 ensure_ascii=False))
                n_out += 1
    print(f"# candidates: {n_in}, matches: {n_out}", file=sys.stderr)
    conn.close()


if __name__ == "__main__":
    main()
