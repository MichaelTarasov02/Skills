---
name: verify-agent
description: This skill should be used when the user wants to check that an agent, skill, or plugin actually works — after building one, after editing it, when a skill stopped triggering, or when it triggers but behaves differently every run. Trigger phrases include "check my plugin", "why doesn't my skill trigger", "validate this agent", "is my plugin broken", "my skill gives inconsistent results", "проверь плагин", "почему скилл не срабатывает", "скилл работает по-разному каждый раз", "провалидируй агента". Runs structural validation, frontmatter checks, trigger diagnosis, a writing-craft audit and a dry run, then reports evidence rather than claims.
---

# Verify Agent

Prove an agent works, or find exactly why it does not. Report **evidence**, never assurances.

## Rule

Every claim needs a command and its output. "Looks fine" is not a result. If a check fails, fix the files — never soften the report.

## 1. Structure

```bash
find <plugin-path> -name 'SKILL.md' -o -name 'plugin.json' | sort
```

Confirm:
- `plugin.json` is in `.claude-plugin/` and **nowhere else**
- `skills/`, `agents/`, `commands/`, `hooks/` are at the plugin **root**
- every declared skill directory actually holds a `SKILL.md`

## 2. Manifest and frontmatter

```bash
claude plugin validate <path>
```

Validates the manifest, skill/agent/command frontmatter and `hooks/hooks.json`. **The path argument is required.** Iterate until clean.

## 3. Frontmatter parses

For each `SKILL.md`, confirm the YAML block parses and `name` + `description` are non-empty.

This is the silent killer: malformed YAML loads the body with **empty metadata**, so `/name` still works while auto-triggering never fires. Nothing looks broken until the skill mysteriously never activates.

## 4. Inventory and cost

```bash
claude plugin details <name>
```

Shows the component inventory and projected token cost. Catches two problems: a component that was never picked up, and a skill listing so large it will get truncated.

## 5. Trigger diagnosis (when a skill does not fire)

Work through these in order:

1. Is the plugin enabled? `claude plugin list`
2. Does the skill appear when asking "what skills are available?"
3. Does `description` contain the words the user actually says? This is the usual culprit.
4. Is `disable-model-invocation: true` set? Then only `/name` works, by design.
5. Is the listing budget overflowing? Run `/doctor` — when it overflows, descriptions are dropped starting with the least-used skills.
6. Does the skill need a reload? `SKILL.md` edits apply live; a **new** top-level skills directory needs a restart; `hooks/`, `agents/`, `.mcp.json` need `/reload-plugins`.

## 6. Craft (when the skill fires and the agent still improvises)

Structure and craft fail differently. Everything above proves the skill **loads**; this proves it **constrains**. A skill that validates clean and still produces a different process every run failed here, and no amount of re-validating will show it.

Read `../../references/writing-craft.md`, then score each `SKILL.md`:

| Check | Fails when |
|---|---|
| Completion criteria | a step ends on a bound the agent cannot check ("review the output", "make sure it works") |
| Pointer strength | a `references/` file is reached by "see references" rather than a named file, moment and branch |
| Pointer placement | pointers sit only in a list at the top, far from the step that needs them |
| Positive phrasing | a prohibition names the unwanted behaviour without naming the wanted one |
| Single source of truth | the same rule appears in `SKILL.md` and a reference |
| No-ops | sentences that restate the model's default behaviour |

Report each finding with the file, the line, and the rewrite. Findings here are the usual answer to "it triggers but the results are inconsistent".

## 7. Dry run

Take one **real** input from the project, run the main skill end to end, and compare the output against the agent's stated definition of done. A validator passing is not evidence that the agent does its job.

Run it **twice** on the same input when consistency is the complaint. Two runs taking different processes points straight at section 6, not at the structure.

## 8. Evals (optional, for agents worth trusting)

If `evals/**/case.yaml` or `evals/**/prompt.md` + `graders/*.md` exist:

```bash
claude plugin eval <name>
```

It adds a no-plugin baseline arm, so the result shows whether the agent actually improves the outcome instead of merely existing.

## Report

```
## Verification: <agent-name>

| Check | Result | Evidence |
|---|---|---|
| Structure | pass/fail | <what was found> |
| Manifest validate | pass/fail | <command output> |
| Frontmatter parses | pass/fail | <n/n skills> |
| Inventory + cost | pass/fail | <details output> |
| Craft | pass/fail | <n findings: file:line → rewrite> |
| Dry run | pass/fail | <input used → output produced> |
| Evals | pass/fail/N/A | <scores vs baseline> |

## Problems found
## Fixes applied
## Still broken
```
