---
name: find-signal-leads
description: This skill should be used when leads are defined by a problem they already have rather than by what they are — companies sued over wages, hit by an enforcement action, losing a licence, hiring in a rush, or newly funded. Triggers on "companies with lawsuits", "who got fined", "find businesses struggling with", "who is hiring for", "кто судится", "у кого проблемы с", "кого оштрафовали", "найди тех, кто столкнулся с". It ties public event records to organisations in the contact book and reports how much of the market that actually reaches.
---

# Find signal leads

A **signal** is an observable event that makes an organisation worth contacting today. It
turns a directory into a reason to call.

Two things decide whether this works, and both are counter-intuitive.

**Selection bias in the source.** Every signal register captures one slice of reality, chosen
by jurisdiction or reporting threshold. Federal court records skew hard toward large
employers, because that is who gets class actions; the small operators most software is sold
to are litigated against in state courts that publish nothing in bulk. A run that ignores
this produces a technically correct list of the wrong companies.

**Name matching.** Signal records name a legal entity; the contact book names an operating
one. Loose matching between them produces confident nonsense.

## Steps

### 1. Turn the signal into a query

Take field 5 from the brief and express it as something a register can filter on. Most
registers filter on a code, not a phrase.

| Signal | Register | Filter |
|---|---|---|
| Wage or overtime claim | federal court dockets | nature of suit for labour standards |
| Wrongful termination, discrimination | federal court dockets | nature of suit for employment civil rights |
| Regulatory penalty | agency enforcement database | industry code plus date range |
| Licence trouble | licensing authority | status field, revocation and probation lists |
| Hiring surge | job boards, careers pages | posting count over a window |
| New funding | filings, press releases | announcement date |
| Leadership change | filings, press releases | officer change |

When the filter is a code, confirm the code means what you think before pulling volume.

### 2. Pull the register and size it

Pull the whole slice for the geography in the brief, then match. Querying the register once
per organisation is slower, hits rate limits, and misses subsidiaries named differently.

### 3. Match to the contact book

The matcher sits in `scripts/` beside this `SKILL.md`.

```bash
python3 <skill-dir>/scripts/match_entities.py \
    leads/<slug>/contacts.db candidates.jsonl > matches.jsonl
```

The script decides on full-token similarity, not on distinctive tokens alone. That choice is
what stops "Palo Alto Networks" from matching "Palo Alto Post-Acute" — the failure mode this
was built around. `references/matching.md` explains the rule and how to tune the thresholds.

Record every match into `signal` with its `match_level`:

- `organization` — the record names this specific site or entity
- `parent` — the record names the group that controls it, so the signal is corporate

A parent-level match is real and belongs in the book. It also means every sibling under that
parent inherits the signal, which is why the level is stored rather than flattened away.

### 4. Verify the matches by hand

Sample 20 matches at random and read them. Automated matching is where this pipeline fails
silently — a wrong match costs a wasted touch and, worse, credibility on the call.

A sample with any wrong match sends you back to the thresholds. Re-run the sample after
tuning; report the final rate.

### 5. Check the fit before celebrating the count

Group the matched organisations by size and by parent. When the list is dominated by large
groups and public bodies, the register has selection bias against the ICP.

Say so plainly in the report, name the register that would cover the missing segment, and
state what it costs — a public-records request, a paid licence, or manual lookup. A precise
list of the wrong companies is worse than a short list of the right ones, because it looks
like success.

## Output

`leads/<slug>/exports/signal_leads.csv` — one row per organisation, carrying the signal, the
event date, the source URL, and the decision-maker contacts already in the book.

**Done when** the `signal` table holds every accepted match with `match_level` and
`confidence` set, the 20-row manual sample is reported with its error count, and the report
states the share of matched organisations that belong to groups larger than the brief's
target size.

Then read `verify-contact-book`.
