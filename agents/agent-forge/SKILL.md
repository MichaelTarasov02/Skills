---
name: agent-forge
description: This skill should be used when the user wants to turn a project, workflow, or prompt chain into an installable agent — a set of skills packaged as a plugin. Trigger phrases include "turn this project into an agent", "make this a plugin", "wrap my prompts into skills", "package this workflow", "сделай из проекта агента", "оберни в плагин", "упакуй промпты в скиллы". Runs the full pipeline: analyzes the project, interviews the user with a form, generates the skills, prunes them against the writing-craft levers, wraps them in a plugin, installs to Claude Code and Codex, verifies it works, and writes the documentation.
---

# Agent Forge

Turn the current project into an **agent**: a set of skills wrapped in a plugin that can be installed, invoked, and shared.

Run the phases in order. Each one ends on a **Done when** line — meet it before moving on. Print a short note after each phase and continue automatically; stop at the Form (Phase 1) and at genuine forks.

Two things decide whether the result is any good, and they are different jobs. The plugin must be **well-formed** — it parses, it validates, it loads. The skills inside must be **well-written** — they fire when they should and drive the same process every run. Phases 3 and 4 own the second one; skipping Phase 4 gets you a valid plugin the agent ignores.

## Standing rules

1. **Confirm before naming.** Every file, path, or skill mentioned in any output exists on disk — check it, then write it down.
2. **Packaging preserves behavior.** Wrap the project's logic exactly as it works today. Collect improvement ideas in a separate list and hand them over in the final report.
3. **One skill, one responsibility.** Two skills doing one job get merged in Phase 2, before anything is written.
4. **Skills share state; agents isolate it.** Pipeline stages that pass voice, theme, IDs or policies between them are skills. Reach for `agents/` only when the work is genuinely independent and parallel.
5. **Write every file complete and runnable as written.**

---

## Phase 0 — Recon the project

Investigate before asking anything:

- repo tree (depth 2–3), `README`, `CLAUDE.md` / `AGENTS.md`
- existing prompts and workflows (`*.prompt.md`, `Prompt*`, `Workflow*`, `Ideas/`)
- already-built skills or plugins (`.claude/skills/`, `.claude-plugin/`)
- scripts and tooling the workflow actually executes
- example outputs — they reveal the real result contract

Output **Project Map**: what the project does, which procedures repeat, which are already formalized as prompts, what belongs in a skill. Flag what is already packaged and leave it untouched.

A project holding no repeatable procedure gets that verdict plainly, and the run stops there. A forced agent is worse than none.

**Done when:** every repeatable procedure found is listed with the file it lives in today, and the already-packaged set is named.

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

Q4 and Q9 carry more weight than the rest. Q4 becomes the `description` — the pointer that decides whether the agent ever fires. Q9 becomes the acceptance bound Phase 7 tests against, so push for something observable rather than "it works".

If no name is given, invent one from the task context and say plainly that you invented it. A "no" on Q10 makes a single-skill agent a valid outcome.

**Done when:** Q1–Q13 are answered or confirmed, and Q9 names something checkable.

## Phase 2 — Design (show before writing files)

- skill list: name, responsibility, input, output, how it differs from its neighbors
- whether `agents/` are needed — justify by context isolation; default is **no**
- whether a `commands/` entry point is worth it (one-button start)
- whether deterministic steps belong in `scripts/`
- whether a `setup-*` skill is needed (Q13 = yes)

For each skill, decide the split now: what every path through it needs (stays in `SKILL.md`) versus what only some paths reach (goes to `references/`). That branching call is cheaper here than after the file is written.

**Done when:** every proposed skill has a one-line responsibility no other skill on the list shares, and each one's `references/` split is decided.

## Phase 3 — Generate the skills

Read both references before writing — they cover different failures:

- `references/skill-spec.md` — format, frontmatter, disclosure budgets, cross-host portability. Read it to keep the skill from being malformed.
- `references/writing-craft.md` — the ladder, pointers, completion criteria, leading words, positive phrasing. Read it to keep the skill from being ignored.

Layout per skill:

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

Write the `description` from Q4 as the skill's top-level pointer: third person, key use case first, carrying the words the user actually says in every language they work in. `references/skill-spec.md` holds the full rules and the character budget.

Add Claude-Code-only fields (`allowed-tools`, `disable-model-invocation`, `context: fork`, `model`, `agent`) only where the skill genuinely needs them; `skill-spec.md` lists what each does and how Codex treats it.

**Done when:** every skill from Phase 2 has a `SKILL.md` on disk whose frontmatter parses, with `name` and `description` non-empty, and every file is complete as written.

## Phase 4 — Prune

Everything written in Phase 3 now gets cut back. This is the phase that separates a plugin that validates from an agent that behaves.

Pass over every generated file:

1. **No-op test, sentence by sentence.** Does this line change behaviour versus what the model does by default? If not, delete the whole sentence rather than trimming it. Most of the weight comes out here — be aggressive.
2. **Single source of truth.** Each rule lives in exactly one file. A rule appearing in both `SKILL.md` and a reference loses one copy; the survivor is its home.
3. **Environment lookups.** Delete lines restating what the agent can read from `package.json`, the directory tree, or `--help`. Keep what no file confesses: the unwritten convention, the reason behind a choice.
4. **Pointer strength.** Every `references/` file is reached by a pointer naming the file, the moment, and the branch — and sitting at the step that needs it, not only in a list at the top.
5. **Completion criteria.** Every step in every generated skill ends on a bound the agent can check. Rewrite the fuzzy ones into something observable.
6. **Negations.** Every prohibition either flips to the target behaviour, or earns its place as a hard guardrail shipped alongside the positive.
7. **Leading words.** Find the spelled-out triads and the sentences gesturing at one idea, and collapse each into a single token the project already uses.

Report the cuts as a table: file, what came out, why. A prune pass that removed nothing means the pass was not run — go back and apply the no-op test properly.

**Done when:** all seven checks have been applied to every generated file, and the cut table is written.

## Phase 5 — Wrap as a plugin

Read `references/plugin-spec.md` for the layout and manifest rules. Scaffold with `claude plugin init <agent-name> --with skills`, then replace the generated placeholders with real content.

The manifest lives **only** in `.claude-plugin/plugin.json`; every component directory sits at the plugin root.

**Done when:** `.claude-plugin/plugin.json` holds real metadata and every component directory sits at the root.

## Phase 6 — Install

1. **Claude Code** — `@skills-dir` (personal, zero install) or a marketplace (sharing). `references/plugin-spec.md` covers both paths.
2. **Validate** — `claude plugin validate <path>` until clean.
3. **Codex** (Q12 = yes) — skills are portable under the Agent Skills standard. Symlink each skill to `~/.codex/skills/<skill-name>/`, so one source serves both hosts. Confirm the skill still reads correctly with the Claude-only frontmatter ignored.
4. Record the real paths, each verified on disk.

**Done when:** `claude plugin validate` exits clean and every recorded path has been listed on disk.

## Phase 7 — Verify it works (evidence, not claims)

1. Show the created tree; confirm every `SKILL.md` exists.
2. `claude plugin validate <path>` — show the output.
3. `claude plugin details <name>` — component inventory and projected token cost.
4. Confirm each skill's YAML parses. Malformed frontmatter loads the body with empty metadata, so `/name` keeps working while auto-triggering silently never fires.
5. **Dry run:** take one real input from the project, run the main skill end to end, and compare the result against Q9. A validator passing is not evidence the agent does its job.
6. When a check fails, fix the files and re-run it. The report states what actually happened.

`references/corner-cases.md` holds the diagnosis for anything that fails here.

**Done when:** every check above has a command and its output attached, and the dry run meets Q9.

## Phase 8 — Documentation

Read `references/doc-template.md` and write `README.md` at the plugin root. The **first block must be simple and immediately useful**: what the agent is, quick start, skill table, flags. Then troubleshooting, drawn from the failure modes this agent can actually reach — `references/corner-cases.md` is the source, and rows that cannot happen here get dropped.

**Done when:** every command in the README has been run and produced what the README claims.

## Final report

- agent name and what it does
- skills created, with purpose
- **what Phase 4 cut** — the table, so the user sees the craft pass happened
- where it was installed (real, verified paths)
- Phase 7 results — what was checked and by what evidence
- three commands the user can run right now to try it
- how to share it
- the parked improvement list from standing rule 2
- what remains and why
