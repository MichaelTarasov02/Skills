# Phase 1 — Understand

The business rule behind the ticket, before any code is opened.

An enhancement changes behaviour someone depends on. Reading the code first produces a
change that fits the code and misses the reason it exists.

## Three questions, and only the third is asked

| Question | Where the answer is |
|---|---|
| What does the system do now | the code — establish it, do not assume |
| What should it do instead | the ticket, plus what the ticket leaves unsaid |
| **Why** | usually only in someone's head |

The third is the one that decides the change. "Add a column to the report" implemented
without knowing why produces the column and not the decision it was meant to support —
and the follow-up ticket arrives a week later.

**Do not stop the run to ask it.** Write down your best reading of the reason from the
ticket, the code and the surrounding feature, mark it as a reading, and **carry the
question to the phase-3 gate** where it is asked once alongside the plan — see
*One interruption, not three* in `SKILL.md`.

```
Ради чего:  <your reading> — предположение, спрошу на гейте
```

The one case that justifies asking now: when the reason decides whether this is an
enhancement at all. Then it is not a question about the work, it is a question about
whether to do the work, and it cannot wait.

A guessed reason marked as guessed is safe. A guessed reason presented as known is how a
column gets added and the decision it was meant to support does not.

## What the ticket leaves unsaid

Enhancement tickets are short because their author had the context in mind. Reconstruct
what they assumed:

| Unsaid | Why it matters here |
|---|---|
| Which cases the change applies to | "always" is rarely meant; edge cases usually keep the old behaviour |
| What happens to existing records | a rule change is retroactive unless someone says otherwise |
| Who sees the difference | a change visible to one role and not another is two changes |
| Whether the old behaviour must remain reachable | a flag, a setting, or nothing |

**The retroactivity question is the one that gets missed.** Changing how something is
calculated changes it for everything already calculated, unless the code freezes history —
and whether it does is a fact to look up in phase 2, not to assume here.

## Delegate the vague ones

Where the ticket is two lines and the gaps are wide, run `spec` in `task` mode: it owns
the technique for hidden requirements and the three-question budget. Come back with its
intake and continue.

For a genuinely small change with a clear rule, this phase is three sentences and should
be.

## Ends with

```
Сейчас:       <what the system does — to be confirmed against code in phase 2>
Нужно:        <what it should do>
Ради чего:    <the reason — asked, not guessed>
Не сказано:   <the assumptions the ticket makes, listed>
Ретроактивно: <does this change existing records — flagged for phase 2>
```
