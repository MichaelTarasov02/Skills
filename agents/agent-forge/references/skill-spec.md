# Skill specification

Source: [Claude Code — Skills](https://code.claude.com/docs/en/skills), [Agent Skills standard](https://agentskills.io), `plugin-dev:skill-development`.

## What a skill is

A folder containing `SKILL.md`. The file holds YAML frontmatter (metadata) plus markdown instructions. It may bundle scripts, references and assets.

```
skill-name/
├── SKILL.md          # required
├── scripts/          # executable code — deterministic, may run without entering context
├── references/       # docs loaded into context on demand
└── assets/           # files used in the output (templates, fonts, boilerplate)
```

## Progressive disclosure — the reason skills stay cheap

| Level | What loads | Budget |
|---|---|---|
| 1. Metadata (`name` + `description`) | always in context | ~100 words |
| 2. `SKILL.md` body | when the skill triggers | **< 5k words** |
| 3. `references/`, `scripts/`, `assets/` | only when needed | effectively unlimited |

**Rule:** information lives either in `SKILL.md` or in `references/` — never both. Duplication guarantees the two copies drift apart. Keep procedure and workflow in `SKILL.md`; move schemas, detail and examples to `references/`.

If a reference file exceeds ~10k words, include grep patterns in `SKILL.md` so the agent can search instead of loading it whole.

## Frontmatter

### Portable minimum (works across every Agent Skills host)

```yaml
---
name: skill-name
description: This skill should be used when ...
---
```

- `name` — kebab-case, matches the directory name. If omitted it defaults to the directory name.
- `description` — **this is the only thing that decides whether the skill triggers.**

### Writing a description that actually triggers

1. Third person: "This skill should be used when…", not "Use this skill when…".
2. **Key use case first** — the text is truncated at **1,536 characters** in the skill listing.
3. Include the words a person would really say, including other languages if the user works in them.
4. Name the artifacts and formats involved — those words are what the request will match on.

### Claude Code extensions (not portable)

| Field | Effect |
|---|---|
| `allowed-tools` | Pre-approves tools **for the invoking turn only**. Clears on the next message. |
| `disable-model-invocation: true` | Manual `/name` only; the description leaves the listing. |
| `context: fork` | Runs the skill in a forked subagent context. |
| `agent` | Which subagent type to use when `context: fork` is set. |
| `model` | Model override for the rest of the current turn. |

Codex and other hosts ignore these. A skill meant to be portable must still make sense with all of them removed.

## Where skills live

| Location | Path | Scope |
|---|---|---|
| Personal | `~/.claude/skills/<name>/SKILL.md` | all your projects |
| Project | `.claude/skills/<name>/SKILL.md` | this project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | where the plugin is enabled |
| Codex | `~/.codex/skills/<name>/SKILL.md` | Codex sessions |

Precedence: enterprise → personal → project. Plugin skills are namespaced `plugin-name:skill-name` and therefore cannot collide.

A skill directory may be a **symlink** — Claude Code follows it and loads the skill once even if reachable from several locations. This is the cheapest way to share one skill source between Claude Code and Codex.

## Content lifecycle — the rule most authors get wrong

When a skill is invoked its rendered content enters the conversation **once** and stays for the session. The file is **not re-read** on later turns.

Therefore: write **standing instructions** that hold for the whole task, not one-time steps that assume the agent re-reads them. If behavior drifts later in a session, the content is usually still present — strengthen the description and instructions, or enforce with hooks.

## Writing style for skill bodies

- Imperative and procedural. The reader is an agent executing, not a human browsing.
- Number the phases, state the gate for each.
- State what **not** to do — non-goals prevent scope creep.
- Require evidence for completion claims.
- Prefer tables for rules and lookups; they survive compaction better than prose.
