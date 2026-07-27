# README template for a generated agent

The first block must let someone understand the agent and run it in under 30 seconds. Everything deeper goes below the fold.

````markdown
# <Agent Name>

<One sentence: what it does and for whom.>

## Quick start

1. Install:
   ```bash
   <one command>
   ```
2. **Restart Claude Code** (or run `/reload-plugins`) — new components are not picked up in the current session.
3. Run:
   ```
   /<main-skill>
   ```
   and give it <what exactly>.

## Skills

| Skill | Use it when | Input → Output |
|---|---|---|
| `/<name>` | ... | ... |
| `/<name>` | ... | ... |

## Flags and parameters

| Skill | Flag | Effect |
|---|---|---|
| `/<name>` | `--<flag>` | ... |

*(Omit this section entirely if the agent has no flags — an empty table is worse than none.)*

---

## Configure it for yourself

<Only if a setup-* skill exists.>
```
/<setup-skill>
```
Creates <config file> with <what it holds>.

## How it works

<Flow in one line: `input → skill-a → skill-b → output`.>

| Stage | Skill | Produces |
|---|---|---|

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Skill does not trigger | `description` lacks the words you actually use | Check `/doctor`; invoke directly with `/<name>` |
| Changes to a skill not applied | — | `SKILL.md` edits apply live; a **new** top-level skills directory needs a restart |
| Changes to hooks/agents/MCP not applied | Those do not hot-reload | `/reload-plugins` or restart |
| Skill lost its effect later in the session | Content is loaded once, not re-read | Re-invoke it, especially after compaction |
| Plugin does not load | Invalid manifest or layout | `claude plugin validate <path>` |
| Update never arrives for users | `version` not bumped | Bump `version` in `plugin.json`; restart after updating |

Diagnostics:
```bash
claude plugin list              # what is installed
claude plugin details <name>    # components + projected token cost
claude plugin validate <path>   # manifest and frontmatter
```

## Share it

<Marketplace instructions, or how to copy the directory.>

## Codex

<If installed: which skills are linked into ~/.codex/skills/ and which Claude-only features do not apply there.>
````

## Rules for filling it in

- Every command must be copy-pasteable and verified to run.
- The skill table lists **when to use**, not what the skill contains — the reader is deciding, not studying.
- Never document a flag that does not exist. Check the skill body first.
- Keep troubleshooting to symptoms actually reachable in this agent; delete rows that cannot happen.
