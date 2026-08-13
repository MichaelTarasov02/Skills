# Scanning a backend

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths are illustrative. Measure before you quote any of them.

Skipping the backend leaves two things blind: the data domain in `spec`, and half the
product's vocabulary. Model field names are the code-side language, and the front end
usually inherits it.

## Identify the framework

| Marker | Framework | Where the schema lives |
|---|---|---|
| `manage.py`, `settings.py` | Django | `**/models.py` |
| `alembic/`, `Base = declarative_base()` | SQLAlchemy | model modules, `alembic/versions/` |
| `prisma/schema.prisma` | Prisma | one file |
| `entity/*.ts` with decorators | TypeORM / NestJS | entity files |
| `*.sql` under `migrations/` | raw SQL | migration history |

If none match, say so rather than guessing — the data mode of `spec` will ask instead.

## The schema is the domain model

```bash
find . -name models.py -not -path "*/migrations/*" | head -20
grep -c "^class .*models.Model" $(find . -name models.py | head -1)
```

For each significant model record: its name, its fields, its foreign keys, and whether it
is written by users or by the system. Names here are the canonical developer-side
vocabulary; compare them against the UI strings to find synonym sets across layers.

**Fields whose name and meaning disagree are the richest finding.** A field named for one
concept holding another is a defect that outlives everyone who remembers it, and the
front end will have copied the wrong name.

## What the schema tells you that nothing else does

| Question | Where the answer is |
|---|---|
| Is this entity one thing or two? | separate models versus one with a type flag |
| Who may see what? | permission models, scoping foreign keys, row-level filters |
| What is legally load-bearing? | fields with audit trails, signed documents, immutable snapshots |
| What must never be renamed? | anything referenced by historical records that must stay reproducible |
| What is derived versus recorded? | computed properties versus stored columns |

The last one matters more than it looks. A stored column that is actually derived is a
consistency bug waiting to happen; a derived value the product treats as recorded cannot
be audited.

## Migrations carry the history

```bash
ls */migrations/*.py | wc -l
git log --oneline -- '*/migrations/' | head -10
```

Recent migrations show where the model is still moving. A table nobody has migrated in
years is stable; one migrated last week is contested, and `spec` should say so before
proposing changes to it.

## Roles and permissions

Do not assume a role exists because the product talks about it. Check whether roles are
a fixed enum, free-text names, or a permission set with no role object at all. A skill
that writes an acceptance criterion naming a role that does not exist has produced an
untestable criterion.

```bash
grep -rniE "class .*(Role|Permission)" --include=models.py . | head
```

## Logging and PII

Note the logging call style and whether personal fields reach it. `review` runs the full
search later; `setup` only records where logs are written and with what.

## Vocabulary extraction

Same idea as the front-end scan, different source: model class names, field names, and
choice labels. These are what developers say. The UI strings are what users read. The gap
between the two lists is the synonym set worth reporting.
