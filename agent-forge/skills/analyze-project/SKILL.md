---
name: analyze-project
description: This skill should be used when the user wants to know whether a project can become an agent, and what skills it would contain, without creating any files. Trigger phrases include "what would this look like as an agent", "can this be a plugin", "analyze this project for skills", "dry run the packaging", "что тут можно обернуть в скиллы", "покажи план без создания файлов". Produces a Project Map and a proposed skill breakdown only — a read-only preview of what agent-forge would build.
---

# Analyze Project

Read-only reconnaissance. Answer "what agent would this project become?" **without writing a single file.**

Use this before committing to `agent-forge`, or when deciding whether packaging is worth it at all.

## Hard rule

**Create nothing. Modify nothing.** Read and report. If the user wants it built, they run `agent-forge`.

## Steps

### 1. Map the project

- repo tree, depth 2–3
- `README`, `CLAUDE.md`, `AGENTS.md`
- prompts and workflows: `*.prompt.md`, `Prompt*`, `Workflow*`, `Ideas/`
- existing packaging: `.claude/skills/`, `.claude-plugin/`, `~/.claude/skills/<project>`
- scripts the workflow executes
- example outputs — these define the real result contract

### 2. Find the repeatable procedures

A procedure is a candidate for a skill when it is:

- performed more than once with the same shape
- currently pasted as a prompt or explained from scratch each time
- described by rules the user keeps restating

Ignore one-off work. Ignore code that is already a library.

### 3. Assess honestly

Answer plainly:

- **Is packaging worth it here?** If the project holds no repeatable procedure, say so and stop. A forced agent is worse than none.
- **What is already packaged?** Do not propose rebuilding it.
- **What blocks packaging?** Missing inputs, undocumented tribal rules, external auth.

### 4. Report

```
## Project Map
<what the project does, in two sentences>

## Repeatable procedures found
| Procedure | Where it lives now | Runs how often | Skill candidate |

## Proposed agent
Name (proposed): <kebab-case>
Purpose: <one sentence>

| Skill | Responsibility | Input | Output |

Agents needed: <yes + justification by context isolation | no>
Entry command: <yes/no>
Per-user config: <yes/no — what would be configurable>

## Already packaged (leave alone)
## Blockers
## Verdict
<Worth packaging / Not worth it / Partially — with reasoning>
```

### 5. Hand off

End with exactly one line:

> To build it: run `agent-forge` in this project.
