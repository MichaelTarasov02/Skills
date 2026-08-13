#!/usr/bin/env python3
"""
Create an empty contact book.

Domain-neutral by design: `organization` and `person` carry a small fixed core plus an
`attributes` JSON column for whatever the current brief needs. A schema change per campaign
would make every downstream query campaign-specific.

Usage:  python3 init_contact_book.py leads/<slug>/contacts.db
"""
import json
import os
import sqlite3
import sys

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- Every source that ever wrote into this book, with the date it was pulled.
CREATE TABLE IF NOT EXISTS source (
    source_id    TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    url          TEXT,
    tier         TEXT,            -- registry|regulator|court|corporate|directory|website|manual
    data_date    TEXT,            -- the cut-off the source itself claims
    retrieved_at TEXT NOT NULL,   -- when we pulled it
    record_count INTEGER,
    licence      TEXT,
    notes        TEXT
);

-- The universe. One row per organisation the brief qualifies.
CREATE TABLE IF NOT EXISTS organization (
    org_id       TEXT PRIMARY KEY,   -- natural key from the anchor source
    name         TEXT NOT NULL,
    legal_name   TEXT,
    org_type     TEXT,
    country      TEXT,
    region       TEXT,
    city         TEXT,
    postal_code  TEXT,
    address      TEXT,
    website      TEXT,
    email        TEXT,
    phone        TEXT,
    size_metric  TEXT,              -- headcount, beds, revenue - whatever the brief sizes by
    parent_name  TEXT,              -- operator or group, when one exists
    parent_count INTEGER,           -- how many organisations that parent controls
    external_ids TEXT,              -- {"npi": "...", "ccn": "...", "company_number": "..."}
    attributes   TEXT,              -- brief-specific fields, JSON
    source_id    TEXT REFERENCES source(source_id),
    updated_at   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_org_type   ON organization(org_type);
CREATE INDEX IF NOT EXISTS idx_org_region ON organization(region);
CREATE INDEX IF NOT EXISTS idx_org_parent ON organization(parent_name);

-- Roles the brief asks for. Everything downstream counts against this list.
CREATE TABLE IF NOT EXISTS role_target (
    role        TEXT PRIMARY KEY,   -- canonical, kebab-case
    label       TEXT,
    priority    INTEGER DEFAULT 0,
    description TEXT
);

-- One row = one source's claim about one person in one organisation.
-- Two sources naming different people for the same role both stay: the disagreement is
-- information, and collapsing it hides which source went stale.
CREATE TABLE IF NOT EXISTS person (
    person_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id         TEXT NOT NULL REFERENCES organization(org_id),
    canonical_role TEXT NOT NULL,
    raw_title      TEXT,            -- the source's own wording, kept for re-mapping
    full_name      TEXT NOT NULL,
    first_name     TEXT,
    last_name      TEXT,
    name_key       TEXT,            -- normalised, for dedup
    email          TEXT,
    phone          TEXT,
    linkedin       TEXT,
    attributes     TEXT,
    source_id      TEXT NOT NULL REFERENCES source(source_id),
    source_date    TEXT,
    confidence     TEXT NOT NULL CHECK (confidence IN ('high','medium','low')),
    updated_at     TEXT NOT NULL,
    UNIQUE (org_id, canonical_role, name_key, source_id)
);

CREATE INDEX IF NOT EXISTS idx_person_org  ON person(org_id);
CREATE INDEX IF NOT EXISTS idx_person_role ON person(canonical_role);

-- Always organisations x target roles rows. A gap you can query is a gap you can close.
CREATE TABLE IF NOT EXISTS field_status (
    org_id        TEXT NOT NULL REFERENCES organization(org_id),
    role          TEXT NOT NULL REFERENCES role_target(role),
    status        TEXT NOT NULL CHECK (status IN
                    ('found','mailbox_only','not_found','not_applicable')),
    person_count  INTEGER NOT NULL DEFAULT 0,
    best_source   TEXT,
    best_conf     TEXT,
    sources_tried TEXT,
    checked_at    TEXT NOT NULL,
    PRIMARY KEY (org_id, role)
);

CREATE INDEX IF NOT EXISTS idx_fs_role_status ON field_status(role, status);

-- A role address with nobody's name on it still reaches the role.
CREATE TABLE IF NOT EXISTS role_mailbox (
    org_id        TEXT NOT NULL REFERENCES organization(org_id),
    role          TEXT NOT NULL,
    email         TEXT NOT NULL,
    source_id     TEXT NOT NULL REFERENCES source(source_id),
    discovered_at TEXT NOT NULL,
    PRIMARY KEY (org_id, role, email)
);

-- The observable fact that makes an organisation a lead today.
CREATE TABLE IF NOT EXISTS signal (
    signal_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id      TEXT NOT NULL REFERENCES organization(org_id),
    signal_type TEXT NOT NULL,      -- litigation|enforcement|funding|hiring|licence|news
    summary     TEXT,
    detail      TEXT,
    event_date  TEXT,
    url         TEXT,
    match_method TEXT,              -- how this was tied to the organisation
    match_level  TEXT,              -- organization | parent
    confidence  TEXT NOT NULL CHECK (confidence IN ('high','medium','low')),
    source_id   TEXT NOT NULL REFERENCES source(source_id),
    recorded_at TEXT NOT NULL,
    UNIQUE (org_id, signal_type, summary, event_date)
);

CREATE INDEX IF NOT EXISTS idx_signal_org  ON signal(org_id);
CREATE INDEX IF NOT EXISTS idx_signal_type ON signal(signal_type);

-- One row per source per run. Makes a partial load visible instead of silent.
CREATE TABLE IF NOT EXISTS load_log (
    run_id      TEXT NOT NULL,
    cycle       TEXT NOT NULL,
    source_id   TEXT,
    rows_in     INTEGER,
    rows_out    INTEGER,
    started_at  TEXT,
    finished_at TEXT,
    notes       TEXT
);
"""


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: init_contact_book.py <path/to/contacts.db>")
    path = sys.argv[1]
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fresh = not os.path.exists(path)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    conn.close()
    print(f"{path}: {'created' if fresh else 'already present, schema applied'}")
    print("tables:", ", ".join(tables))


if __name__ == "__main__":
    main()
