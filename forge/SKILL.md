---
name: forge
description: Factory that builds, refines and assembles the Dev Agent skills to one method. Service skill — invoked by name when working on the agent itself.
disable-model-invocation: true
---

# Skill Forge

A skill exists to wrangle **predictability** out of a stochastic system: the same
*process* every run, not the same output. Every rule here serves that. When the word
appears below, it means exactly this.

Three modes. **Forge** builds a new skill. **Refine** improves an existing one against
evidence from a real run. **Assemble** turns the set into an installable plugin.

Refine is the one that runs most. A skill is not finished when it is written; it is
finished when it has survived contact with real tasks, and that contact is what mode C
turns into edits.

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

**Headline for this skill:** what changed, which real failure caused it, and what still
fails its own quality rules.

## The roster

Eight tools and five pipelines. Composition and boundaries are closed; a defect in the
roster is a paragraph in the final report, not a change made in passing.

| | |
|---|---|
| **Tools** | `setup` `spec` `copy` `craft` `review` `debug` `handoff` `forge` |
| **Pipelines** | `resolve-bug` `enhance` `improve` `refactor` `ship-feature` |

**A pipeline routes, carries artifacts and gates. A tool does one job.** A pipeline that
reimplements what a tool owns has produced a second, quietly diverging answer — the
failure this split exists to prevent.

## Fixed decisions — never re-litigate

| | |
|---|---|
| Skill location | `AGENT_REPO/dev-agent/skills/<name>/` |
| Manifest | `.claude-plugin/plugin.json` and nowhere else |
| `SKILL.md` body language | English |
| `description` language | English, plus Russian trigger phrases — the team speaks Russian |
| Product knowledge base | `PRODUCT_REPO/.dev-agent/` — never inside the plugin |
| Every component is a **skill** | they share state through `.dev-agent/`; a subagent's isolated context loses it |

**Platforms are not fixed and never were.** The agent is installed on repositories it has
never seen. Every platform fact — framework, major, kit, API style, where strings live —
is read from `.dev-agent/config.yaml` at run time. A platform named in a skill body is a
bug in that skill: it will be wrong on the next repository, and wrong in the way that
compiles.

## The optional dependency, declared

`agent-forge` covers the general craft of skill authoring. Where it is installed, read it
— never copy it, because a copy drifts the moment it updates.

| Read from `agent-forge` | For |
|---|---|
| `references/skill-spec.md` | skill format, progressive disclosure, `description` rules |
| `references/plugin-spec.md` | plugin layout and manifest — mode B |
| `references/doc-template.md` | agent README — mode B |
| `references/corner-cases.md` | known traps — diagnose from here first |

```bash
ls ~/.claude/skills/agent-forge/references/ 2>/dev/null || echo "absent"
```

**It is not a prerequisite, and this skill must run without it.** Anyone installing
`dev-agent` from the registry has these thirteen skills and nothing else. When it is absent:
say so once, fall back to `references/quality-rules.md` — which is self-contained and
carries every rule this agent actually enforces — and continue. A mode that stops because
an optional donor is missing has turned a convenience into a hard dependency.

---

# Mode A — forge a new skill

**Input:** a statement of what the skill does, plus `PRODUCT_REPO` to try it against.
**Output:** `AGENT_REPO/dev-agent/skills/<name>/` and a coverage report.

### A1 — subject and boundaries

State what the skill does and what it deliberately leaves alone. Then draw one line
against every other skill in the roster: where this one stops and that one starts.

**Read `references/artifact-contract.md` before this phase** — it names the skill's inputs
and who consumes its output.

*Done when:* the boundary table has a row per sibling, each naming the seam in one
sentence.

### A2 — donors

Work through every donor named. Method: **read `references/donor-analysis.md` before this
phase** and follow it. Where no donor is named, say so and build from the boundary table
instead — an invented donor list is worse than none.

*Done when:* `references/provenance.md` carries every donor, each fragment marked
`take as is` / `rewrite for us` / `drop`, and every `drop` carries its reason.

### A3 — specification ⛔ gate

Fill `references/skill-spec-template.md`. Show it. Stop. Wait for an answer.

*Done when:* the filled specification has been shown and answered. A4 stays closed until
then.

### A4 — build

Write `SKILL.md` and every `references/` file. Apply **`references/quality-rules.md`**
throughout, and **`references/platform-split.md`** wherever platforms diverge.

*Done when:* `wc -w SKILL.md` reads under 5000, every reference file exists, and the list
of topics appearing in both body and references is empty or each entry carries a verdict.

### A5 — self-check

Run the finished skill against `references/quality-rules.md` as though someone else wrote
it. Fix what surfaces.

*Done when:* every rule in the checklist has a file-and-line citation showing where it
holds.

### A6 — proving runs

Execute a real task with the skill, against a real repository. A run produces output. A
description of a run produces nothing.

*Done when:* each run has its actual output pasted, or an explicit statement of why it
could not be executed. Never substitute reasoning for a run.

### A7 — coverage report ⛔ gate

Fill the table from `references/coverage-report.md`. Show it. Stop.

*Done when:* every row has evidence from A6, and anything unclosed says so with a reason.

---

# Mode C — refine an existing skill

**Input:** one skill, and a real repository to run it against.
**Output:** edits to that skill, each traceable to a failure that actually happened.

The rule the mode turns on:

> **No edit without a failed run behind it.**

Reading a skill and improving what looks weak produces plausible edits that fix nothing
and occasionally remove something load-bearing. The whole method is: make it fail first.

### C1 — run it for real

Take a task the skill claims, on a repository with real code in it, and follow the skill
**literally** — every reference it says to read, every phase in order, no shortcuts taken
because you already know the answer.

Following it literally is the measurement. Every place you had to decide something the
skill did not decide for you is a finding, and it is invisible if you improvise past it.

*Done when:* the run produced its actual output, and every command it prescribes has been
executed with its output shown.

### C2 — name what went wrong

Between one and five findings. Each carries:

| | |
|---|---|
| **What happened** | the wrong output, the missing instruction, the contradiction — concretely |
| **Where** | file and line in the skill |
| **Cost** | what a developer would have shipped believing it |

Rank by cost, not by how easy the fix is.

**The four failures worth the most:**

| Class | Signature |
|---|---|
| **Silent wrong answer** | the skill produces a confident output that is false, and nothing in the process catches it |
| **Stale cross-reference** | the skill names a file, skill, phase or path that no longer exists |
| **Unowned decision** | the process reaches a fork and says nothing, so the runtime improvises differently every time |
| **Unverifiable claim** | the skill asserts a rule with no command that could check it |

A finding that is none of these is usually a preference. Say so and drop it.

### C3 — fix at the level the failure lives

| The failure was | Fix belongs in |
|---|---|
| The process reached a fork with no rule | `SKILL.md` — it decides the process |
| A recipe produced a wrong number or missed a case | the reference file that owns the recipe |
| A claim could not be checked | add the command that checks it, beside the claim |
| A name went stale | fix it, then add the check that would have caught it |

**Prefer a runnable check to a stronger sentence.** "Be careful about X" has never
prevented X. A command that fails when X happens has.

*Done when:* every finding from C2 has an edit, or an explicit note saying why it was left.

### C4 — verify, on both axes

Two questions, and the second is the one that gets skipped:

1. **Does the fix hold?** Re-run the part of C1 that failed. Paste the output.
2. **Did the fix break something?** Re-run the checks that previously passed.

A fix verified only against the failure it targeted is how iteration three reintroduces
iteration one's defect. **Every later iteration re-runs every earlier iteration's check**,
and the report says which were re-run.

*Done when:* the failed check now passes with its output shown, and every earlier check
still passes.

### C5 — record it

One entry per iteration in `AGENT_REPO/docs/build-history/iterations/<skill>.md`:

```markdown
## Iteration N — <one line>
- **Failure:** <what happened, with the evidence>
- **Class:** silent wrong answer | stale reference | unowned decision | unverifiable claim
- **Fix:** <file:line> — <what changed>
- **Depth:** load-bearing | corrective | cosmetic
- **Re-checked:** <which earlier checks were re-run>
```

**Depth is assessed honestly and is mostly not `load-bearing`.** A run that produces five
load-bearing findings has usually found one and dressed four. `load-bearing` means the
skill produced a wrong answer a developer would have acted on; `corrective` means it
produced a worse answer than it should have; `cosmetic` means it read badly.

Grading everything as critical makes the report useless for deciding what to trust.

---

# Mode B — assemble the plugin

Runs after the skills exist, and again before every release.

**Input:** `AGENT_REPO/dev-agent/skills/*`.
**Output:** an installed, verified `dev-agent` plugin with a README.

### B1 — inventory
Every skill present; every frontmatter parses. Malformed YAML loads the body while leaving
metadata empty, so the skill answers to `/name` and never auto-triggers.

**A colon inside an unquoted `description` is the failure that has actually happened.**
`fast: N+1` in a description parsed as a nested key, and the skill silently vanished from
the install — while `claude plugin validate` passed. Use an em dash, or quote the string.

```bash
for f in skills/*/SKILL.md; do
  python3 -c "import sys,yaml;d=open('$f').read().split('---')[1];print('$f',yaml.safe_load(d).get('name'))"
done
```

*Done when:* every name is printed from parsed frontmatter, not from a directory listing,
and the count matches the roster.

### B2 — contract
Run the staleness check at the foot of `references/artifact-contract.md` first — it fails
loudly when a rename stopped at `SKILL.md`. Then, for each file in the table: name its
writer and its readers, open each reader, and confirm it handles the file being absent.

```bash
PAT='not a blocker, and not a question either'
for s in skills/*/; do s=${s%/}; n=$(basename $s)
  [ "$n" = forge ] && continue          # this file quotes the pattern; it would match itself
  grep -q 'config\.yaml' $s/SKILL.md 2>/dev/null &&
  ! grep -q "$PAT" $s/SKILL.md &&
  echo "no absence path: $n"
done
```

**One exception:** `setup` writes `config.yaml`, so it has no missing-input path to
document — its reads are of its own schema. Anything else printed is a real gap.

**`forge` is skipped explicitly, and the explicit part matters.** This file quotes the
pattern the check searches for, so without the skip it would match itself and report clean
— an exemption by accident rather than by decision. A checker whose own text satisfies its
own condition is a checker that passes for the wrong reason, and that is worth one line of
`continue` rather than a comment saying to ignore it.

*Done when:* the staleness check prints nothing, the absence check prints nothing but the
two exceptions, and every reader has a cited line showing its missing-input path.

### B3 — description collisions
Every description competes for one listing budget. Trigger phrases must not overlap, or
the wrong skill fires.

*Done when:* overlapping triggers are listed and resolved, and each description measures
under 1536 characters.

### B4 — manifest
`.claude-plugin/plugin.json` holds the manifest and nothing else does. Every other
directory sits at the plugin root. All paths relative, starting `./`. The description and
the skill count in it are part of the manifest — a manifest saying "six skills" over
twelve is the first thing a new user reads.

*Done when:* `claude plugin validate <path>` exits clean and its output is shown.

### B5 — documentation
Write `README.md`. Where `agent-forge` is present, follow its `doc-template.md`.

*Done when:* every command in it has been pasted into a shell and run.

### B6 — install
*Done when:* every skill appears in the listing of a fresh session, and the count matches
B1. An install that lands one fewer than expected is B1's YAML failure, not a cache issue.

### B7 — end-to-end
Take one real feature through `spec` → `copy` → `craft` → `review`, then one real bug
through `resolve-bug`.

*Done when:* every `.dev-agent/` artifact the chain should produce exists on disk. This is
the only evidence that twelve skills became one agent.

---

## Reference map

| File | Read it before |
|---|---|
| `references/artifact-contract.md` | A1, B2 |
| `references/donor-analysis.md` | A2 |
| `references/skill-spec-template.md` | A3 |
| `references/quality-rules.md` | A4, A5, C3 |
| `references/platform-split.md` | A4 |
| `references/coverage-report.md` | A7 |
| `references/provenance.md` | when a donor changes upstream |
