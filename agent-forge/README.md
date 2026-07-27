# Agent Forge

Turns any project into an installable agent: a set of skills wrapped in a plugin that you can invoke, verify, and hand to other people.

## Quick start

1. Already installed — it lives at `~/.claude/skills/agent-forge/` and loads as `agent-forge@skills-dir`.
2. **Restart Claude Code** (or run `/reload-plugins`) so all components load.
3. Open a project you want to package and run:

```
/agent-forge
```

It analyzes the project, shows you a pre-filled form, and builds the agent from your answers.

## Skills

| Skill | Use it when | Input → Output |
|---|---|---|
| `/agent-forge` | You want the whole thing built: project → skills → plugin → installed → verified → documented | A project → an installed, working agent + README |
| `/agent-forge:analyze-project` | You want to know *what* it would become, before committing. Creates nothing | A project → Project Map + proposed skill breakdown |
| `/agent-forge:verify-agent` | After building or editing, or when a skill stopped triggering | A plugin path → pass/fail table with evidence |
| `/agent-forge:improve` | Change, extend, or improve an agent that already exists — and reinstall it locally so the new version works right away | An existing agent + what to improve → improved agent, version bumped, reloaded |
| `/agent-forge:share-agent` | Friends or colleagues should be able to install it | A personal agent → marketplace repo + install commands |

No flags. Each skill is driven by conversation, not switches.

## Typical flow

```
/agent-forge:analyze-project     # is this worth packaging?
/agent-forge                     # build it
/agent-forge:verify-agent        # prove it works
/agent-forge:share-agent         # hand it to friends
```

You can start straight at `/agent-forge` — it runs its own recon first.

---

## How it works

`/agent-forge` runs seven phases: recon the project → form → design → generate skills → wrap as plugin → install (Claude Code + Codex) → verify → document.

The format rules live in reference files, loaded only when a phase needs them:

| Reference | Holds |
|---|---|
| `references/skill-spec.md` | SKILL.md format, frontmatter, progressive disclosure, portability |
| `references/plugin-spec.md` | plugin layout, manifest, packaging paths, CLI, Codex install |
| `references/corner-cases.md` | 19 documented failure modes |
| `references/doc-template.md` | README structure for generated agents |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Skill does not trigger | `description` lacks the words you actually say | Ask "what skills are available?"; invoke directly with `/agent-forge` |
| Edited a `SKILL.md`, no effect | — | `SKILL.md` edits apply live. A **new** top-level skills directory needs a restart |
| Edited hooks/agents/MCP, no effect | Those never hot-reload | `/reload-plugins` or restart |
| Skill lost its effect later in the session | Content loads once and is not re-read | Re-invoke it, especially after compaction |
| Plugin does not load | Invalid manifest or wrong layout | `claude plugin validate ~/.claude/skills/agent-forge` |
| Descriptions look truncated | Skill listing budget overflowed | `/doctor`; raise `skillListingBudgetFraction` |

Diagnostics:

```bash
claude plugin list
claude plugin details agent-forge@skills-dir
claude plugin validate ~/.claude/skills/agent-forge
```

## Codex

The four skills follow the [Agent Skills](https://agentskills.io) standard and work in Codex. Link them in:

```bash
ln -s ~/.claude/skills/agent-forge ~/.codex/skills/agent-forge
```

Symlink rather than copy, so one source serves both hosts.

## Share it

`/agent-forge:share-agent` converts this plugin (or any agent you build with it) into a marketplace repo with tested install commands. Remember to bump `version` in `.claude-plugin/plugin.json` on every release — without it, `/plugin update` reports "already at the latest version".

## Sources

Built from the official [Claude Code Skills](https://code.claude.com/docs/en/skills) and [Plugins reference](https://code.claude.com/docs/en/plugins-reference) documentation, the [Agent Skills](https://agentskills.io) standard, and the `plugin-dev`, `skill-creator` and `superpowers:writing-skills` skills.
