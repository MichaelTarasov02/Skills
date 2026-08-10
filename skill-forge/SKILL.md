---
name: skill-forge
description: Factory that builds the nine Dev Agent skills to one method, and assembles them into the dev-agent plugin. Service skill — invoked by name from the build prompts.
disable-model-invocation: true
---

# Skill Forge

A skill exists to wrangle **predictability** out of a stochastic system: the same
*process* every run, not the same output. Every rule here serves that. When the word
appears below, it means exactly this.

Two modes. **Forge** builds one Dev Agent skill. **Assemble** turns the finished nine
into an installable plugin.

## Language

Answer in the language the request was written in. Findings, explanations, questions,
reports and section headings you produce for a developer follow their language — Russian
request, Russian answer.

**Text destined for the product's users is exempt.** Interface strings, release notes,
store listings and email stay in the product's interface language, taken from
`.dev-agent/config.yaml` → `interface.language`, whatever language the request used.
Mixing the two — an English report about Russian button labels, or the reverse — is the
failure this rule prevents.

## Answer in the conversation, not only in the file

The developer reads the chat. The artifact is for the skills downstream. Lead with what
was asked, in this order:

1. **The answer** — what to do, as a recommendation, not a menu
2. **What blocks it** — decisions only they can make, each carrying your recommended
   option and the reason for it
3. **The cost of being wrong** — for anything decided on their behalf
4. **Where the detail lives** — one line naming the artifact

Never open with what you verified, which reference files you read, or how you reconciled
your own numbers. That is the record of your process, not the answer to their question.
Evidence belongs attached to the claim it supports, never in the headline.

A developer who reads only the first ten lines must be able to act.

**Headline for this skill:** what was built and what failed its own quality rules.

## What this skill does not do

`agent-forge` already covers the general craft. Read its files, never copy them —
a copy drifts the moment `agent-forge` updates.

| Read from `agent-forge` | For |
|---|---|
| `references/skill-spec.md` | skill format, progressive disclosure, `description` rules |
| `references/plugin-spec.md` | plugin layout and manifest — mode B |
| `references/doc-template.md` | agent README — mode B |
| `references/corner-cases.md` | known traps — diagnose from here first |

Improving an already-built skill is `agent-forge:improve`. Verifying a finished agent is
`agent-forge:verify-agent`. Publishing is `agent-forge:share-agent`. This skill builds.

## Fixed decisions — never re-litigate

| | |
|---|---|
| Skill roster | the nine in `AGENT_REPO/USE-CASES.md` plus `project-onboarding`. Composition and boundaries are closed |
| Platforms | React + TypeScript (web) and Flutter (mobile), equal weight |
| Product UI language | English |
| `SKILL.md` body language | English |
| `description` language | English and Russian trigger phrases — the team speaks Russian |
| Skill location | `AGENT_REPO/dev-agent/skills/<name>/` |
| Product knowledge base | `PRODUCT_REPO/.dev-agent/` — never inside the plugin |
| Every component is a **skill** | the nine share state through `.dev-agent/`; a subagent's isolated context loses it |

Spot a real defect in the roster: write one paragraph in the final report and carry on
with the current one.

---

# Mode A — forge one skill

**Input:** a build prompt `NN-<skill>.md` from `AGENT_REPO/prompts/`, plus `USE-CASES.md`
and `PRODUCT_REPO`.
**Output:** `AGENT_REPO/dev-agent/skills/<name>/` and a coverage report.

### A1 — subject and boundaries

State what the skill does and what it deliberately leaves alone. Then draw one line
against every other skill in the roster: where this one stops and that one starts.

**Read `references/artifact-contract.md` before this phase** — it names the skill's
inputs and who consumes its output.

*Done when:* the boundary table has a row per sibling skill, each naming the seam in one
sentence.

### A2 — donors

Work through every donor the build prompt lists. Method: **read
`references/donor-analysis.md` before this phase** and follow it.

*Done when:* `references/provenance.md` carries every donor, each fragment marked
`take as is` / `rewrite for us` / `drop`, and every `drop` carries its reason.

### A3 — specification ⛔ gate

Fill `references/skill-spec-template.md`. Show it. Stop. Wait for an answer.

*Done when:* the filled specification has been shown and answered. A4 stays closed
until then.

### A4 — build

Write `SKILL.md` and every `references/` file. Apply
**`references/quality-rules.md`** throughout, and **`references/platform-split.md`**
wherever React and Flutter diverge.

*Done when:* `wc -w SKILL.md` reads under 5000, every reference file exists, and the
list of topics appearing in both body and references is empty or each entry carries a
verdict.

### A5 — self-check

Run the finished skill against `references/quality-rules.md` as though someone else
wrote it. Fix what surfaces.

*Done when:* every rule in the checklist has a file-and-line citation showing where it
holds.

### A6 — proving runs

Execute every run the build prompt lists under Верификация. A run produces output. A
description of a run produces nothing.

*Done when:* each listed run has its actual output pasted, or an explicit statement of
why it could not be executed. Never substitute reasoning for a run.

### A7 — coverage report ⛔ gate

Fill the table from `references/coverage-report.md`: one row per use case ID in the
build prompt. Show it. Stop.

*Done when:* every ID has a row, every row has evidence from A6, and anything unclosed
says so with a reason.

---

# Mode B — assemble the plugin

Runs once, after all nine skills exist.

**Input:** `AGENT_REPO/dev-agent/skills/*`.
**Output:** an installed, verified `dev-agent` plugin with a README.

### B1 — inventory
All nine present; every frontmatter parses. Malformed YAML loads the body while leaving
metadata empty, so the skill answers to `/name` and never auto-triggers — check, don't
assume.
*Done when:* nine names printed from parsed frontmatter, not from directory listing.

### B2 — contract
For each file in `references/artifact-contract.md`: name its writer and its readers, then
open each reader and confirm it handles the file being absent.
*Done when:* every reader has a cited line showing its missing-input path.

### B3 — description collisions
Nine descriptions compete for one listing budget. Trigger phrases must not overlap, or
the wrong skill fires.
*Done when:* overlapping triggers are listed and resolved, and each description measures
under 1536 characters.

### B4 — manifest
`.claude-plugin/plugin.json` holds the manifest and nothing else does. Every other
directory sits at the plugin root. All paths relative, starting `./`.
*Done when:* `claude plugin validate <path>` exits clean and its output is shown.

### B5 — documentation
Write `README.md` from `agent-forge/references/doc-template.md`.
*Done when:* every command in it has been pasted into a shell and run.

### B6 — install
*Done when:* all nine skills appear in the listing of a fresh session.

### B7 — end-to-end
Take one real feature through `feature-intake` → `screen-blueprint` → `interface-copy` →
`element-markup` → `screen-review` → `feature-handoff` → `outbound-writing`.
*Done when:* every `.dev-agent/` artifact the chain should produce exists on disk. This
is the only evidence that nine skills became one agent.

---

## Reference map

| File | Read it before |
|---|---|
| `references/artifact-contract.md` | A1, B2 |
| `references/donor-analysis.md` | A2 |
| `references/skill-spec-template.md` | A3 |
| `references/quality-rules.md` | A4, A5 |
| `references/platform-split.md` | A4 |
| `references/coverage-report.md` | A7 |
| `references/provenance.md` | when a donor changes upstream |
