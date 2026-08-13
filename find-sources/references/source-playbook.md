# Source playbook

Families of open sources that carry contacts, and the identifier that joins them. Treat every
entry as a **candidate** — probe it before it enters `sources.md`. URLs move; the family
survives.

## What each family actually gives you

Registries publish what a statute forces them to publish: the licence holder and the
responsible officer. Internal staff roles — scheduler, payroll, HR coordinator, office
manager — appear in no registry anywhere, because no law requires disclosing them. Expect to
reach those through company sites, direct contact, or paid enrichment, and say so in the
coverage report rather than presenting the gap as a search failure.

## United States

| Family | Where | Supplies | Join key |
|---|---|---|---|
| Provider registry (healthcare) | NPPES NPI Registry API, free, no key | organisation, authorised official name + title + direct phone | NPI |
| Federal enforcement | agency enforcement portals; many mirror to data.gov | employer, violation, penalty, employees affected | employer name, NAICS |
| Federal courts | CourtListener REST API, free; PACER for filings | parties, counsel, nature of suit, filing date | party name |
| Corporate registry | Secretary of State, per state | officers, directors, registered agent | entity number |
| Federal spending | USAspending API | recipients, award amounts, contacts | UEI, DUNS |
| Regulated facilities | agency-specific licensing files, usually per state | licensee, administrator, address, capacity | licence number, CCN |
| Nonprofits | IRS Form 990 via ProPublica Nonprofit Explorer API | officers, compensation, revenue | EIN |
| Securities filings | SEC EDGAR full-text search API | officers, addresses, filings | CIK |

State corporate registries increasingly sit behind anti-bot controls. When one refuses
automated access, the routes are the official API with a registered key, a public-records
request, or manual lookup for a shortlist.

## European Union / United Kingdom

| Family | Where | Supplies | Join key |
|---|---|---|---|
| Company register | Companies House API (UK, free key); national registers elsewhere | directors, officers, addresses, accounts | company number |
| Cross-border aggregate | OpenCorporates | entity, officers, jurisdiction links | company number |
| Procurement | TED (EU), Contracts Finder (UK) | awarded suppliers, contacts | registration number |
| Beneficial ownership | national UBO registers, access varies by member state | ultimate owners | company number |

GDPR applies to contact data on EU residents regardless of where it was published. Legitimate
interest can cover B2B outreach, and it still requires a balancing assessment, a privacy
notice, and an honoured objection.

## Anywhere

| Family | Supplies | Cost |
|---|---|---|
| Company website team pages | internal titles registries never carry | free, low yield |
| Job postings | hiring signal, hiring manager, tooling in use | free |
| Conference and association rosters | practitioners by speciality | free |
| Press releases and local news | leadership changes, expansions | free |
| Podcast and webinar guest lists | senior people who talk publicly | free |
| Paid enrichment platforms | verified email and direct dial at scale | subscription |

## Yield reality check

Website crawling for internal roles converts poorly. In the run this playbook came from,
2,224 corporate domains produced named people on 144 of them — under 7 percent, and almost
all of those were executives already available in registries.

Budget it accordingly: registries first for coverage, websites for the handful of roles
nothing else carries, paid enrichment when the brief needs a role no public source holds.

## Probe recipes

```bash
# JSON API — does it answer, and with what shape
curl -sL --max-time 30 "<api-url>" | head -c 600

# Bulk file — real format, header, row count
curl -sL --max-time 300 -o s.csv "<file-url>" -w "http=%{http_code}\n"
file s.csv && head -1 s.csv && wc -l < s.csv

# Catalog metadata — find the current download URL instead of guessing it
curl -sL "<catalog-api>/dataset/<id>" | python3 -m json.tool | grep -i download

# Permission check, before any repeated request
curl -s "https://<host>/robots.txt"
```
