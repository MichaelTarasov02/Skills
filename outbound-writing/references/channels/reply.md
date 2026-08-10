# Replying to a user

## Shape

1. What you understood happened — in their words, not the system's
2. What is true about it
3. What they can do now
4. What happens next, without a date

```
You're seeing the associate list stay empty after you pick a date range.

That happens when the report request fails — the error appears briefly and then
the table is left blank, so it looks like there's simply no data.

For now: reload the page and pick the range again. If it stays empty, the data
for that range didn't load rather than being absent.

I've logged the missing error state. Someone will follow up here when it's fixed.
```

## Never

| Never | Because |
|---|---|
| a date or duration | it is the first thing forgotten and the only thing remembered |
| "known issue" | tells them others suffer too and nothing is happening |
| an internal cause — cubit, endpoint, cache | they cannot act on it and it reads as an excuse |
| "working as intended" | if they reported it, the intent is wrong |
| blame the user, however gently | "you may have clicked twice" ends the conversation |

## The apology question

Apologise once, briefly, when the product actually failed them. Do not apologise in every
paragraph — repetition reads as evasion. And do not apologise for something that worked
correctly; explain it instead.

## When there is no answer yet

Say that. A reply that says "I don't have the cause yet, here's what I've ruled out, I'll
come back when I know" is more useful than a confident guess that turns out wrong — which
costs a second message and the reader's trust in the first.

## Reproduction

If the report is unclear, ask for what is missing — and ask for **one** thing. A reply
containing five questions gets none answered. Pick the one that would narrow it most.

Route the answers to `feature-intake`, which turns a complaint into reproduction steps.

## Legal and compliance ground

This product covers meal breaks, disciplinary records and payroll. A reply touching any of
those states what the system recorded, never what the law requires or what the employer
should do.

```
⚖️ Needs review — the reply touches meal-break compliance
```

Quote what the product shows. Interpretation belongs to the employer and their counsel.
