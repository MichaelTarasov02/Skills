---
name: build-contact-book
description: This skill should be used once sources are verified, to extract organisations and people into a queryable contact book where every fact carries its source, date and confidence, and every missing role is recorded as an explicit gap. Triggers on "build the contact list", "extract the contacts", "put this into a database", "собери контактную книгу", "выгрузи контакты", "сложи в базу". It loads one source per cycle so a rerun updates rows instead of duplicating them.
---

# Build contact book

Two properties make a contact book survive a real campaign.

**Provenance** — every fact carries the source that asserted it, the date, and how much to
trust it. Six months on, that is what separates the rows worth calling from the rows that
rotted.

**Gaps are recorded, not implied.** An empty cell cannot say whether the role was searched
for and missing, or never searched. A `not_found` row listing the sources already tried can.

## Steps

### 1. Initialise

The scripts sit in `scripts/` beside this `SKILL.md`. Resolve that directory once and reuse
it — the install path differs between hosts.

```bash
python3 <skill-dir>/scripts/init_contact_book.py leads/<slug>/contacts.db
```

The schema and the reasoning behind each table live in `references/schema.md` — read it
before adding a column or changing a key.

### 2. Load the anchor source

The **anchor** is the source that defines the universe: the registry listing every
organisation that qualifies. It creates the `organization` rows every other source attaches
to.

Populate the target roles from the brief into `role_target`, one row per role. Everything
downstream counts against this list.

### 3. Load each enrichment source as its own cycle

One source, one function, one entry in `load_log`. Keeping cycles separate is what lets a
single failing source be re-run without touching the rest.

Make every write an upsert against the table's natural key:

```sql
INSERT INTO person (...) VALUES (...)
ON CONFLICT (org_id, canonical_role, name_key, source_id) DO UPDATE SET ...
```

Register the source row **before** inserting people that reference it — `person.source_id` is
a foreign key, and the violation surfaces halfway through a long load otherwise.

### 4. Map raw titles onto the brief's roles

Sources speak their own vocabulary: `W-2 MANAGING EMPLOYEE`, `CORPORATE OFFICER`,
`Authorized Official`, `CFO`. Map each onto a role from the brief and keep the original string
in `raw_title` — the mapping will need revisiting, and the original is the only way back.

Set confidence by how directly the source asserts the role:

| Confidence | The source | Example |
|---|---|---|
| `high` | states the role outright | licence record naming the administrator |
| `medium` | states an adjacent role you inferred from | "managing employee" read as administrator |
| `low` | attaches the person to a parent entity, not this one | a chain executive found on a shared website |

Reserve `low` for research. Outreach runs on `high` and `medium`.

### 5. Reject non-names at the door

Extraction from web pages produces `Audit Committee`, `Accounting Operations`,
`Meet Our Leadership`. Filter at the point of insert, so the crawler can stay permissive and
the book stays clean. `scripts/name_filter.py` holds the check and the token list it uses.

### 6. Write the gaps

For every organisation and every target role, write a `field_status` row. The table always
holds exactly `organisations × roles` rows, so a missing role is impossible to overlook.

| Status | Meaning |
|---|---|
| `found` | at least one named person |
| `mailbox_only` | a role address like `hr@` with no name behind it |
| `not_found` | searched in the sources listed, nothing there |
| `not_applicable` | this role does not exist at this kind of organisation |

### 7. Export

CSV flattened one row per organisation for the campaign tool, CSV one row per person for the
CRM, JSON nested for anything programmatic.

## Getting the roles nobody publishes

Internal roles — scheduler, payroll, HR coordinator — sit in no registry. Two routes remain
and both belong in the book:

- **Company sites.** `scripts/fetch_web.py` crawls team pages, reads `robots.txt` first, and
  accepts only tight name-to-title pairings. Loose proximity matching produces plausible
  garbage that survives review; the three accepted patterns are documented in the script
  header. Expect roughly 7% of domains to yield a name — registries carry the coverage.
- **Role mailboxes.** `hr@`, `scheduling@`, `payroll@` found on those pages go to
  `role_mailbox`. No name attached, and still a working channel.

## Output

```
leads/<slug>/
├── contacts.db
└── exports/
    ├── organizations.csv    one row per organisation, roles in columns
    ├── people.csv           one row per person
    └── contacts.json        nested
```

**Done when** `SELECT COUNT(*) FROM field_status` equals organisations × target roles, every
`person` row has a non-null `source_id` and `confidence`, and a second run of the whole
pipeline leaves every table count unchanged — paste both counts.

Then read `verify-contact-book`, or `find-signal-leads` when the brief named a signal.
