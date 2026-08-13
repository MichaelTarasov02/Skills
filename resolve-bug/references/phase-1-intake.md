# Phase 1 — Intake

Turn whatever arrived into facts, and name what is still missing. The phase ends when you
can restate the problem better than the person who reported it.

## What arrives, and what it is worth

| Arrives as | Reliability | First move |
|---|---|---|
| Steps to reproduce | high, if they work | run them |
| A screenshot | high for what is on screen, silent about how it got there | read the state, not the complaint |
| A stack trace or error id | high | search the history for it — it may already be fixed |
| "It doesn't work" | low | this phase is the whole job |
| A forwarded conversation | mixed — the reporter is quoting someone else | find who saw it first |

**Look up before asking.** Roles, limits, defaults, which screens can even produce this
symptom — all in the code. A question whose answer sits in a model file spends the
engineer's patience on nothing.

Delegate the reconstruction to `debug` in `reproduce` mode; it owns the technique for
turning a complaint into steps.

## Six things you need, and where each comes from

| | Question | Ask, or look up |
|---|---|---|
| 1 | Which account, project, role | **ask** — and this is the highest-value question |
| 2 | When it first happened | **ask** — separates deploy from expiry from data growth |
| 3 | Which screen or action | look up from the description, confirm |
| 4 | What they expected | **ask** — and take it seriously; it decides the branch |
| 5 | Every time or sometimes | **ask** — the least-asked, most valuable answer |
| 6 | What the rules say should happen | **look up** — never ask |

Item 6 is the one that makes this skill work. Before the conversation goes further, find
the rule: the setting, the validation, the permission, the documented policy. Everything
after depends on comparing observed behaviour against a rule you can quote.

## The rule is not in the code path that produced the symptom

**This is the failure that quietly destroys the whole pipeline.** You follow the symptom
to the branch that produced it, read the condition, and write it down as the rule. But
that condition *is the behaviour under investigation*. Quoting it as the rule makes
observed and expected identical by construction — and every such investigation ends in
"working as designed", including the ones that are defects.

A rule is something the code is answerable to: a configurable setting, a validation
constraint, a permission, a written policy, a value a customer can change. The `if` that
fired is the answer, not the question.

**Find the settings first, then check which ones the symptom path reads:**

```bash
grep -rn "<the concept from the complaint>" --include='*.py' --include='*.dart' \
  | grep -iE "field|setting|config|option|default|threshold|period|limit"
```

Then, for every setting that turned up, ask the one question that matters:

> **Does the code path that produced the symptom read this setting?**

A configured setting the symptom path never reads is a **defect**, and it is a defect with
a settings screen in front of it — a customer has already set a value that does nothing.
This is the single highest-yield check in the phase, and it is invisible from the code
path alone.

## The strongest statement of a rule is what the product tells the user

**Search the interface strings before the code.** A rule written into a label, a policy
screen or a decline reason is the product's own commitment: someone wrote it deliberately,
someone reviewed it, and in a localised product it was translated into every locale — a
far stronger statement of intent than a condition in a file nobody has opened in a year.

```bash
# localised catalogues
grep -rn "<the concept>" --include='*.arb' --include='*.json' --include='*.po' .
# inline strings, where there is no catalogue
grep -rn "<the concept>" --include='*.vue' --include='*.tsx' --include='*.html' src
```

Read what the strings promise, then check each promise against the code that enforces it.
**Where the product tells the user it does X and the code does not do X, that is a defect
and the investigation is over** — there is nothing to take to the product owner, because
the product already decided and published the decision.

This is the check that most often converts an ambiguous "by design, ask the owner" into a
settled verdict, and it runs in seconds. It also crosses repositories: the rule is
routinely stated in the client and enforced on the server, so search **every** platform
root in `config.yaml`, not the one the symptom appeared on.

## One rule is usually a set

The template below says `The rule`. Where the behaviour has siblings — a start and an end,
an early and a late, a create and a delete — **quote all of them and compare.** The finding
is frequently not in any one rule but in the asymmetry between them: three cases guarded,
the fourth not; two directions with a tolerance, two without.

Quoting the one rule that fired hides the asymmetry completely, and the asymmetry is the
answer. List the siblings, mark which carry the guard and which do not, and ask whether
anything justifies the split. Where nothing does, the missing one is the defect.

**Item 4 decides the branch, so record it verbatim.** Paraphrasing "I expected the shift
to stay open" into "the shift closes incorrectly" has already chosen defect over
by-design.

## What the engineer knows that nothing else does

This is a conversation, not a form. Ask what only they can answer:

- has this area changed recently, and did anyone already look
- is this customer configured unusually
- is this the first report or the fifth
- is there a known workaround being used

The fifth report of the same thing is a different investigation from the first: it has a
pattern, and the pattern is evidence.

## Question budget

**Three questions, batched, not one at a time.** Everything past the third becomes a
stated assumption carrying its cost. An intake that stalls waiting for answers has failed
at the thing it exists for.

Offer options where you can. "Which account?" beats "can you give me more detail", and
"every time, or only sometimes?" beats "how often?".

## Ends with

```
Reported:     <verbatim, including what they expected>
Established:  <facts, each with its source — code path, log line, config value>
The rule:     <the setting, constraint or policy, quoted with its location —
               never the condition that produced the symptom>
Siblings:     <the related rules, each marked guarded / unguarded, or "none">
Unread:       <settings that exist and the symptom path does not consult — or "none checked">
Observed:     <what the code actually did, quoted separately from the rule>
Unknown:      <what is missing, and whether it blocks>
Assumptions:  <anything decided on their behalf, with the cost of being wrong>
```

`The rule` and `Observed` are separate lines because they are separate things. A intake
where they contain the same quotation has not found the rule yet — it has found the code
twice, and phase 4 will read that as agreement.

`The rule` may be empty — and an empty one is itself a finding. Behaviour with no rule
behind it is the fourth row of the branch table: an undecided product question that
shipped, and it goes to the product owner rather than into a fix.

Do not proceed to phase 2 without item 6 answered or explicitly marked absent.
