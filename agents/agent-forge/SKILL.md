---
name: agent-forge
description: This skill should be used when the user wants to turn a project, workflow, or prompt chain into an installable agent — a set of skills packaged as a plugin. Trigger phrases include "turn this project into an agent", "make this a plugin", "wrap my prompts into skills", "package this workflow", "сделай из проекта агента", "оберни в плагин", "упакуй промпты в скиллы". Runs the full pipeline: analyzes the project, interviews the user with a form, generates the skills, wraps them in a plugin, installs to Claude Code and Codex, verifies it works, and writes the documentation.
---

# Agent Forge

Turn the current project into an **agent**: a set of skills wrapped in a plugin that can be installed, invoked, and shared.

Run the phases in order. After each phase print a short note and continue automatically. Stop only at the Form (Phase 1) and at genuine forks.

## Hard rules

1. **Never invent.** Verify a file, path, or skill exists before mentioning it.
2. **Packaging preserves behavior.** Do not "improve" the project's logic while wrapping it. Park improvements in a separate list.
3. **One skill, one responsibility.** Two skills doing the same job is a design error — merge them.
4. **Skills for shared state, agents for isolation.** Pipeline stages that share context (voice, theme, policies) must be skills. Use `agents/` only for genuinely independent parallel work.
5. **No placeholders.** Write every file in full. Never "…rest is similar".
6. **Read the reference files instead of guessing format rules:**
   - `references/skill-spec.md` — SKILL.md format, frontmatter, cross-host portability
   - `references/plugin-spec.md` — plugin layout, manifest, install paths, CLI
   - `references/corner-cases.md` — the failure modes that cost hours
   - `references/doc-template.md` — README structure to produce

---

## Phase 0 — Recon the project

Investigate before asking anything:

- repo tree (depth 2–3), `README`, `CLAUDE.md` / `AGENTS.md`
- existing prompts and workflows (`*.prompt.md`, `Prompt*`, `Workflow*`, `Ideas/`)
- already-built skills or plugins (`.claude/skills/`, `.claude-plugin/`)
- scripts and tooling the workflow actually executes
- example outputs — they reveal the real result contract

Output **Project Map**: what the project does, which procedures repeat, which are already formalized as prompts, what belongs in a skill. Flag what is already packaged and must not be touched.

If the project holds no repeatable procedure, say so and stop. Do not force an agent onto nothing.

## Phase 1 — The Form (ask, then wait)

Present the form **pre-filled** from Phase 0 so the user can just confirm. Mark every guess `(proposed)`.

```
=== AGENT ===
1. Agent name (kebab-case):        [proposed: ____]
2. One sentence — what it does:    [proposed: ____]
3. Who it is for:                  [proposed: ____]
4. Trigger phrases (3-5, how a
   person would actually ask):     [proposed: ____]

=== MAIN SKILL (required) ===
5. Name:                           [proposed: ____]
6. What it does, input to output:  [proposed: ____]
7. Input:                          [proposed: ____]
8. Output (files / structure):     [proposed: ____]
9. Definition of done:             [proposed: ____]

=== ADDITIONAL SKILLS (optional) ===
10. Separate skills for other functions? (yes/no)
    For each: name, responsibility, input, output
    [proposed from Phase 0: ____]

=== DISTRIBUTION ===
11. Personal use or share with others? (personal / share)
12. Install to Codex as well? (yes/no)
13. Per-user configuration needed (voice guide, paths, keys)? (yes/no)
```

Rules: if no name is given, invent one from the task context and say plainly that you invented it. If Q10 is "no", a single-skill agent is a valid outcome.

## Phase 2 — Design (show before writing files)

- skill list: name, responsibility, input, output, how it differs from its neighbors
- whether `agents/` are needed — justify by context isolation; default is **no**
- whether a `commands/` entry point is worth it (one-button start)
- whether deterministic steps belong in `scripts/`
- whether a `setup-*` skill is needed (Q13 = yes)

Check for duplicates. Two skills with one function must be merged before anything is written.

## Phase 3 — Generate the skills

Read `references/skill-spec.md` first. For each skill create:

```
<skill-name>/
├── SKILL.md          # required
├── references/       # detail, loaded on demand
├── scripts/          # deterministic code
└── assets/           # templates and output files
```

Frontmatter — portable minimum:

```yaml
---
name: skill-name
description: This skill should be used when ...
---
```

Write `description` in third person with the key use case first, and include the words a person would actually say. Add Claude-Code-only fields (`allowed-tools`, `disable-model-invocation`, `context: fork`, `model`, `agent`) only when genuinely needed, and note they are vendor extensions.

## Phase 4 — Wrap as a plugin

Read `references/plugin-spec.md`. Scaffold with `claude plugin init <agent-name> --with skills`, then replace the generated placeholders with real content.

The manifest lives **only** in `.claude-plugin/plugin.json`; every component directory sits at the plugin root.

## Phase 5 — Install

1. **Claude Code** — `@skills-dir` (personal, zero install) or a marketplace (sharing). See `references/plugin-spec.md`.
2. **Validate** — `claude plugin validate <path>` until clean.
3. **Codex** (if Q12 = yes) — skills are portable under the Agent Skills standard. Copy or symlink each skill to `~/.codex/skills/<skill-name>/SKILL.md`. Confirm the skill still makes sense without Claude-only frontmatter.
4. Record the real paths, verified on disk.

## Phase 6 — Verify it works (evidence, not claims)

1. Show the created tree; confirm every `SKILL.md` exists.
2. `claude plugin validate <path>` — show the output.
3. `claude plugin details <name>` — component inventory and projected token cost.
4. Confirm each skill's YAML parses (broken YAML means empty metadata and a silent auto-trigger).
5. Dry run: take one real input from the project, run the main skill, confirm the output meets Q9.
6. If anything fails, fix the files — never the report.

## Phase 7 — Documentation

Read `references/doc-template.md` and write `README.md` at the plugin root. The **first block must be simple and immediately useful**: what the agent is, quick start, skill table, flags. Then troubleshooting, including the restart and `/reload-plugins` rules from `references/corner-cases.md`.

## Final report

- agent name and what it does
- skills created, with purpose
- where it was installed (real, verified paths)
- Phase 6 results — what was checked and by what evidence
- three commands the user can run right now to try it
- how to share it
- what remains and why
