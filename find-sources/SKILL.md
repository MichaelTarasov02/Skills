---
name: find-sources
description: This skill should be used after a lead brief exists, to find and probe the open sources that can actually supply the contacts — public registries, regulators, court records, licence databases, company sites. Triggers on "where can I get this data", "what sources exist for", "is this data public", "найди источники", "где взять эти данные", "это есть в открытом доступе". It downloads a sample from every candidate before accepting it, and records the ones that failed alongside the ones that worked.
---

# Find sources

A source is **verified** when it has been probed and returned what it claimed. Everything
else is a candidate, however confident the documentation sounds — documented sources
redirect, gate, return an SPA shell, or quietly dropped the field you need three years ago.

## Steps

### 1. List candidates from the brief

Read `leads/<slug>/brief.md`. Work outward through the ladder, because the earlier tiers are
cheaper, more complete, and legally cleaner:

| Tier | What it holds | Reach for it when |
|---|---|---|
| **Licensing registry** | every regulated entity, plus the named licence holder | the target operates under a licence |
| **Regulator / enforcement** | violations, citations, penalties, inspections | the brief names a compliance signal |
| **Corporate registry** | officers, directors, registered agents | you need the owner |
| **Court records** | lawsuits, judgments, dockets | the brief names a litigation signal |
| **Grant / contract / procurement** | funded organisations and their contacts | the target sells to or takes from government |
| **Provider / membership directory** | practitioners, accreditation, association rosters | the target belongs to a profession |
| **Company sites** | the roles no registry publishes | internal titles are the target |

`references/source-playbook.md` holds the concrete source families per country and per
domain, with the identifier that joins them. Read it while building this list.

### 2. Probe every candidate

Download a sample. For an API, one record. For a file, the header and a row count. For a
search page, one query.

Record what came back, not what was expected:

```bash
curl -sL --max-time 60 "<url>" -o sample.out -w "http=%{http_code} size=%{size_download}\n"
file sample.out && head -c 400 sample.out
```

Four failures are common enough to name, because each looks like success from the outside:

| Symptom | What it means |
|---|---|
| HTML where CSV was promised | the download is behind a JS app; find the API the app calls |
| 200 with an anti-bot body (Imperva, Cloudflare, PerimeterX) | automated access is refused |
| 403 / 401 | the source needs a key — check whether one is free to register |
| Correct format, missing the field you need | the source is real and still useless for this brief |

### 3. Check what the source permits

Read `robots.txt` before any repeated automated request, and honour `Disallow`.

Sources that refuse automation still have legal doors: a public-records request, a free API
key, a paid licence, or a human running the search by hand. Record the door rather than the
refusal — a source marked "blocked" with no route beside it gets rediscovered and re-probed
by the next person.

Working around an anti-bot control is where this skill stops. Record the block and move to the
alternative route.

### 4. Find the join key

Two sources are only worth having together when a key connects them. Look for a licence
number, registration number, tax ID, national provider ID, domain, or a normalised
name-plus-address pair.

Probe the join before committing to it. A key that exists in both files still fails when one
side pads to six digits and the other strips the leading zero — that single mismatch cost
half the match rate in the run this skill came from.

## Output

Write `leads/<slug>/sources.md`:

```markdown
# Sources: <name>
Probed: <ISO date>

## Verified
| Source | URL | Format | Rows | Fields it supplies | Join key | Licence | Probed |
|---|---|---|---|---|---|---|---|

## Rejected
| Source | Why it failed | Alternative route |
|---|---|---|

## Join map
<which key connects which sources, and the normalisation each side needs>
```

**Done when** every candidate appears in exactly one of the two tables, each verified row
carries a row count taken from the downloaded sample, and each rejected row names either an
alternative route or the reason none exists.

Then read `build-contact-book`.
