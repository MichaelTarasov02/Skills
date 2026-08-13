# Three branches

> **Examples below are shapes, not facts about your codebase.** Measure before you quote
> any of them.

Read before phase 3. Everything else in this skill depends on getting this distinction
right, and it is the distinction most bug work never makes.

## The question that separates them

> **What do the rules say should happen, and did it happen?**

Two independent answers, four combinations:

| Rules say | Actually happened | Branch |
|---|---|---|
| X | X, and the user expected X | not a bug at all — misunderstanding of the report |
| X | X, and the user expected Y | **user error**, or **by design** — see below |
| X | Y | **defect** |
| nothing — no rule covers this | anything | **by design**, undefined case: the product never decided |

The fourth row is the quiet one. Nobody wrote a rule, the code does *something*, and that
something became the behaviour by accident. It is not a defect — there is no rule to
contradict — and it is not user error. It is an undecided product question that shipped.

## A rule can cover part of the situation and none of the rest

The trap inside row four. A rule exists, the code follows it, and it answers a different
question from the one the user is asking.

Observed on one investigation: a screen's failure path had a rule — *on error, show a
toast* — and the code followed it exactly. What had no rule was **what the screen shows
afterwards**. The toast disappeared, the table sat empty, and nothing distinguished "no
data" from "the request failed".

Reading the catch block finds a rule and stops. The correct reading is: the rule covers
notification, nothing covers state, and the user's question is about state.

**Ask which layer the expectation is about, then look for a rule at that layer.** A rule
found one layer away is not the rule — and treating it as one turns an undecided product
question into "working as intended".

## Telling user error from by-design

Both mean the system behaved correctly and the person expected otherwise. The difference
is **who is wrong**:

| | User error | By design, wrong for the product |
|---|---|---|
| Would a well-informed user expect this? | no — they misread or misused | **yes** — their expectation is reasonable |
| Does the interface invite the mistake? | possibly, and that is a separate finding | irrelevant |
| Is the rule itself still right? | yes | **no, or no longer** |
| Who decides what happens next | nobody — explain and close | the product owner |

**The test: ask whether a second, careful user would make the same mistake.** If the
expectation is reasonable and the system contradicts it, the rule is the problem, not the
person. Filing that as user error tells someone they are wrong when the product is.

**A user error with a high repeat rate is a design finding.** One person misreading a
screen is user error; the fifth person misreading the same screen is an interface defect
wearing a support ticket. Say so, and route it to `review`.

## Rule combinations are the hardest defects

A defect does not have to live in one place. Two rules, each correct, can combine into
behaviour neither intended — and reading either file alone shows nothing wrong.

Where a product has per-tenant configuration, this is the default shape of a hard bug:
setting A is unusual, setting B is unusual, and only together do they produce the symptom.
The code is right, each rule is right, the combination was never considered.

How to find it:

1. Get the **full** configuration of the account that reported it, not the parts that seem
   relevant
2. Compare against an account where it works
3. The differing settings are the candidate set — and there are usually few
4. Reproduce by changing one at a time

This is why phase 1 asks for the account rather than for more steps. The reporter cannot
tell you which setting differs; they do not know settings exist.

## Evidence each branch requires

Do not name a branch without the evidence its column demands:

| Branch | Minimum evidence |
|---|---|
| User error | the rule, quoted from code or documentation, plus what the user actually did |
| By design | the rule, plus who wrote it and when, plus why it no longer fits |
| Defect | the rule, plus the observed behaviour contradicting it, plus a reproduction |

"It looks like user error" without the quoted rule is a guess that closes a ticket. That
is the most expensive wrong answer available here: it ends the investigation and tells a
customer they were mistaken.

## When the branches are genuinely unclear

Say so. The report carries the candidate branches, the evidence for each, and the single
question that would settle it — usually one the product owner answers in a sentence.

Forcing a verdict to avoid an open question is how "working as intended" gets attached to
things nobody intended.
