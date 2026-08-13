#!/usr/bin/env python3
"""
Decide whether a string extracted from a page is a person's name.

Web extraction reliably produces "Audit Committee", "Accounting Operations" and
"Meet Our Leadership" alongside real names. Filtering at the point of insert lets the
crawler stay permissive while the contact book stays clean.

Import it:      from name_filter import is_person_name
Check by hand:  python3 name_filter.py "Audit Committee" "Cynthia Lagatuz"
"""
import re
import sys

# Words that never appear inside a personal name. Two groups, because they get here two ways:
# org fragments arrive from headings, function words from department labels.
NOT_A_PERSON = re.compile(
    r"\b("
    # organisational
    r"committee|audit|board|council|foundation|association|department|division|"
    r"corporate|corporation|company|trust|holdings?|partners|ventures?|capital|"
    r"systems?|network|clinic|agency|solutions?|technologies|enterprises|"
    r"properties|realty|institute|society|alliance|coalition|team|group|staff|"
    r"office|center|centre|services?|program|project|fund|inc|llc|ltd|corp|gmbh|"
    # functional
    r"operations?|accounting|administration|development|resources?|relations|"
    r"affairs|marketing|sales|support|quality|compliance|billing|payroll|finance|"
    r"financial|human|nursing|medical|health|healthcare|therapy|wellness|"
    r"admissions?|intake|referrals?|scheduling|staffing|engineering|product|"
    # titles
    r"executive|chief|president|director|manager|coordinator|supervisor|"
    r"specialist|assistant|associate|officer|administrator|chairman|chairwoman|"
    r"founder|owner|principal|partner|advisor|consultant|lead|head|"
    r"leadership|management|"
    # page furniture - headings get read as names otherwise
    r"meet|our|your|welcome|about|contact|learn|more|read|click|view|"
    r"privacy|policy|terms|rights|reserved|menu|site|map|home|page|search"
    r")\b", re.I)


def is_person_name(name):
    """True when the string plausibly names one human being."""
    if not name:
        return False
    name = name.strip()
    if len(name) > 40 or NOT_A_PERSON.search(name):
        return False
    toks = [t for t in name.split() if t]
    if not 2 <= len(toks) <= 3:
        return False
    for t in toks:
        core = t.strip(".,'’-")
        if len(core) <= 1:              # middle initial
            continue
        if not re.fullmatch(r"[A-Za-z'’-]+", core):
            return False
    return True


def split_name(s):
    """Return (first, last, display). Handles 'LAST, FIRST M' and 'First Last'."""
    if not s:
        return None, None, None
    s = s.strip()
    if "," in s:
        last, first = [x.strip() for x in s.split(",", 1)]
    else:
        bits = s.split()
        first, last = (bits[0], bits[-1]) if len(bits) > 1 else ("", s)
    first = re.sub(r"\s+[A-Z]\.?$", "", first).strip()
    display = f"{first} {last}".strip() if first else last
    return (first or None), (last or None), (display or None)


def name_key(s):
    """Order-insensitive normalised key, so 'John Smith' and 'Smith, John' dedup."""
    if not s:
        return ""
    s = re.sub(r"[^A-Za-z ]", " ", s.upper())
    return " ".join(sorted(p for p in s.split() if len(p) > 1))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(f"{'PERSON' if is_person_name(arg) else 'REJECT'}  {arg}")
