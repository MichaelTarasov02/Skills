# Quality rules

Read before phases A4 and A5. Everything here serves **predictability** — the same
process every run.

## Numeric gates

| Gate | Command |
|---|---|
| Body under 5000 words | `wc -w SKILL.md` |
| `description` under 1536 characters | measure it; the listing truncates at that point |
| One meaning, one place | list topics appearing in both body and references; each needs a verdict |

## Structural rules

**Every phase ends on a checkable completion criterion.** The agent must be able to tell
done from not-done. "Produce a change list" fails; "every modified file accounted for"
passes. A vague criterion is an invitation to stop early.

**Standing instructions, not one-time steps.** Rendered content enters the conversation
once and is never re-read. Write rules that hold for the whole task.

**Context pointers carry their trigger.** "Read `references/x.md` before phase N" fires;
"see references for details" does not. The wording decides reliability, not the file.

**Branch test for disclosure.** Inline what every path through the skill needs; push
behind a pointer what only some paths reach.

**Prompt the positive.** Naming a forbidden behaviour makes it more available, not less.
State the target behaviour instead. Keep an outright prohibition only where it is a hard
guardrail, and pair it with what to do in its place.

**Description rules.** Third person. Key use case first. The literal words a person would
say, in English and Russian. Name the artifacts and formats — those words are what the
request matches on.

**Missing-input behaviour is part of the skill.** Every Dev Agent skill reads from
`.dev-agent/`. Each one states what it does when a file it wants is absent: say what is
missing, offer to generate it, continue on flagged assumptions. Silent failure is a
defect.

**Explicit non-goals.** A skill without them expands into its neighbours.

**Every skill carries the `## Answer in the conversation` block, verbatim, plus one line
naming its own headline.** A skill that defines only its artifact leaves the chat output
undefined, and the model fills that space with process narration — which reference it
read, which number it reconciled. The developer then reads a QA log instead of an answer.

**No product-specific finding goes into a reference file as an example.** Real field
names, counts and paths from one repository read as rules and cost every later run the
effort of disproving them — and they go stale silently. Use placeholder shapes
(`<count>`, `<file:line>`), and put the warning banner at the top of any reference file
carrying examples.

**Every skill carries the `## Language` block, verbatim and identical.** This is the one
sanctioned duplication in the agent: there is no shared context file the ten skills can
read, so the rule lives in each. Changing it means changing all ten in one edit — check
with `grep -c '## Language' skills/*/SKILL.md` and expect the same count everywhere.

The rule it encodes: the developer is answered in their own language, product-facing text
follows `config.yaml → interface.language`. Machine-read field values — statuses, keys,
enum-like tokens in artifacts — stay English regardless, because other skills grep them.

## Failure modes — diagnose against this list

| Mode | Test | Cure |
|---|---|---|
| **premature completion** | does any phase criterion permit "close enough"? | sharpen the criterion; only if it is irreducibly fuzzy, split the sequence to hide later phases |
| **duplication** | does a meaning appear twice? | keep one home, replace the other with a pointer |
| **sediment** | does this line still bear on what the skill does? | delete |
| **sprawl** | inside budget but unreadable? | disclose by branch |
| **no-op** | does the line change behaviour versus the default? | delete the whole sentence, do not trim words |
| **negation** | is the rule phrased as a prohibition? | restate as target behaviour |

## Against the excuse

Phase A6 ends in output or in a stated reason it could not run. The excuses that end it
otherwise, and their answers:

| Excuse | Answer |
|---|---|
| "the skill clearly handles this" | run it |
| "covered by section X" | a section is not evidence |
| "should work" | should is not did |
| "no repository available" | say that, name the run as unexecuted |
| "ran it earlier" | paste that output |

## Roster hygiene

Before finishing a skill, check it against the ones already built: two skills with the
same function guarantee drift and force every change to be made twice. Overlap found —
move the function to one home and leave a boundary line in the other.
