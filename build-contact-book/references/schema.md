# Contact book schema

`scripts/init_contact_book.py` creates it. This file explains the choices that are not
obvious from the DDL.

## Domain-neutral by construction

`organization` and `person` carry a small fixed core plus an `attributes` JSON column.
Beds, headcount, ARR, licence class — whatever this brief cares about goes in `attributes`,
and `external_ids` holds the identifiers that join to other datasets.

A schema change per campaign would make every query campaign-specific and every export a
one-off. The JSON column keeps one query surface across every run.

## Why one person can appear twice

`person` is keyed `(org_id, canonical_role, name_key, source_id)`. Two sources naming
different administrators for one organisation produce two rows, and that is deliberate.

The disagreement is information: usually one register is stale. Collapsing to a single "best"
row throws away the only evidence of which one that is. Resolve it at export time, where the
rule can change without a reload.

## `field_status` is the point of the schema

The table always holds exactly `organisations × target roles` rows. Every combination has a
verdict.

Without it, a missing role is an empty cell, and an empty cell cannot distinguish "searched,
not there" from "never searched". The first is a finding. The second is unfinished work. A
campaign built on the confusion targets the wrong half of the list.

`sources_tried` records which registers were already checked, so the next refresh adds new
sources instead of re-walking the same ones.

## Where `low` confidence comes from

Almost always shared-domain crawling: one corporate website serving forty locations attaches
its executives to all forty. The people are real; the site-level attribution is not.

## `signal` and `match_level`

`match_level` separates `organization` from `parent`. A parent-level signal propagates to
every sibling under that parent, which is often correct and always worth being able to filter
out.

The `UNIQUE (org_id, signal_type, summary, event_date)` key makes signal loading idempotent
alongside everything else.

## Refresh

Re-pull the raw sources, re-run the loaders, re-run `verify-contact-book`. Every loader
upserts, so a refresh updates in place.

Two changes between refreshes are themselves leads: a new name in a role, and a new signal.
Both mean something moved at that organisation, which is a better reason to call than the
original list ever was.
