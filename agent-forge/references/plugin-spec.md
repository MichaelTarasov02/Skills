# Plugin specification

Source: [Plugins reference](https://code.claude.com/docs/en/plugins-reference), `plugin-dev:plugin-structure`.

## The four entities — do not confuse them

| Entity | What it is | Context | Invoked by |
|---|---|---|---|
| **Skill** | folder + `SKILL.md`; procedural knowledge | **shared with the user** | model (via `description`) or user (`/name`) |
| **Agent** | subagent with its own system prompt | **isolated** | model delegates |
| **Command** | flat `.md`; slash command | shared | user only |
| **Plugin** | manifest + all of the above | — | installed |

> "Agents are FOR autonomous work, commands are FOR user-initiated actions."

**Design consequence:** stages that share state (voice, theme, policies, IDs) must be **skills**. An agent's isolated context loses that state. Reach for `agents/` only when work is genuinely independent and parallelizable.

## Directory layout

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json       # manifest — ONLY here
├── skills/<name>/SKILL.md
├── commands/<name>.md
├── agents/<name>.md
├── hooks/hooks.json
├── scripts/
├── bin/                  # added to the Bash tool PATH while enabled
├── .mcp.json
└── README.md
```

**The manifest goes in `.claude-plugin/`. Every other directory sits at the plugin root, never inside `.claude-plugin/`.** This is the single most common structural failure.

A `CLAUDE.md` at the plugin root is *not* loaded as context. Ship instructions as skills instead.

## Manifest

`name` is the only required field, kebab-case. The manifest itself is optional — without it components are auto-discovered and the name comes from the directory.

```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "What the agent does",
  "author": { "name": "Author" },
  "keywords": ["..."],
  "skills": ["./"]
}
```

- All component paths are **relative and start with `./`**.
- For absolute paths inside scripts, hooks and MCP configs use `${CLAUDE_PLUGIN_ROOT}`.
- `"skills": ["./"]` makes the plugin root itself a skill, alongside `skills/`.
- Unrecognized top-level fields are ignored, so one manifest can carry metadata for other ecosystems.

## Two packaging paths

| Path | How | When |
|---|---|---|
| **`@skills-dir`** | `claude plugin init <name> [--with skills agents hooks mcp]` scaffolds at `~/.claude/skills/<name>/`. Auto-loads next session as `<name>@skills-dir` — **no marketplace, no install step** | personal use, fast iteration |
| **Marketplace** | repo + `.claude-plugin/marketplace.json`, then `claude plugin install <name>@<marketplace> [--scope user\|project\|local]` | sharing with others |

`--with` accepts: `skills`, `agents`, `hooks`, `mcp`, `lsp`, `output-style`, `channel`.

Scope decides which settings file records it: `project` writes to `.claude/settings.json` and reaches everyone who clones the repo.

## Plugin agents

```markdown
---
name: agent-name
description: What this agent specializes in and when to invoke it
model: sonnet
tools: Read, Grep
---
System prompt.
```

Supported: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation` (only `"worktree"`).

**Forbidden for plugin-shipped agents, for security:** `hooks`, `mcpServers`, `permissionMode`.

Agents appear in @-mention as `plugin-name:agent-name`.

## CLI (verified on Claude Code 2.1.201)

| Command | Purpose |
|---|---|
| `claude plugin init <name>` | scaffold at `~/.claude/skills/<name>/` |
| `claude plugin validate <path>` | validate manifest + skill/agent frontmatter + hooks — **path is required** |
| `claude plugin details <name>` | component inventory and projected token cost |
| `claude plugin list` | what is installed |
| `claude plugin install <plugin>` | install from a marketplace |
| `claude plugin enable/disable <name>` | toggle |
| `claude plugin update <plugin>` | update — **restart required to apply** |
| `claude plugin eval <target>` | run `evals/**/case.yaml` with a no-plugin baseline arm |
| `claude plugin tag <path>` | create a `{name}--v{version}` release tag |

## Codex installation

Codex implements the same Agent Skills standard: `~/.codex/skills/<name>/SKILL.md` with `name` + `description` frontmatter.

Install a skill for Codex by copying or symlinking the skill directory:

```bash
ln -s ~/.claude/skills/<plugin>/skills/<skill> ~/.codex/skills/<skill>
```

Claude-only frontmatter fields are ignored there. Verify the skill still reads correctly without them. The plugin wrapper itself (`agents/`, `hooks/`, `.mcp.json`) is Claude Code machinery; Codex has its own plugin system under `~/.codex/plugins/`.
