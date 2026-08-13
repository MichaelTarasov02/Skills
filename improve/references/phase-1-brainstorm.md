# Phase 1 — Brainstorm ⛔ soft gate

Understand the task and the goal behind it. No code yet.

**Read `references/product-check.md` first** and run its four questions. That pass is what
makes this phase more than a summary of the ticket.

## Load the context properly

Large tasks arrive with more material than small ones — a description, a discussion, a
design, related tickets, sometimes a document. Read all of it before forming a view.

| Source | What it gives that others do not |
|---|---|
| The task itself | the requested solution |
| The discussion around it | what was rejected, and why |
| Linked or related tickets | whether this is one of several |
| A design, if there is one | the parts nobody described in words |
| `.dev-agent/lexicon.md` | whether the new concept already has a name |

**The discussion is worth more than the task.** A ticket records a conclusion; the
discussion records the options and why they lost — and one of those is usually about to be
proposed again.

## Restate the task better than it arrived

The output of this phase is a description of the work the person who wrote the ticket
would recognise and improve on:

```
Цель:         <what this is for — the outcome, not the feature>
Кому:         <who benefits, and who else is affected>
Что делаем:   <the functionality, in behaviour terms>
Чего не:      <explicit boundaries — what this is not>
Успех:        <how anyone would know it worked>
```

`Чего не` is the field that prevents scope drift. Large tasks grow between the ticket and
the merge, and the growth is invisible without a written boundary.

`Успех` is the field phase 5 checks against. Without it, "done" means "the code is
written".

## Brainstorm the shape, briefly

Not the design — that is phase 2. Here: what are the two or three ways this could work at
all, and which is worth designing?

```
Подход A: <one line>  — <what it costs, what it buys>
Подход B: <one line>  — <…>
Рекомендую A, потому что <…>
```

Where one approach is obviously right, say so in a sentence and move on. Where two are
genuinely close, that is a decision for the gate.

## The soft gate

```
## Стоит обсудить до начала
<from product-check — or "проверил, противоречий не нашёл">

## Подход
<the recommendation>

Продолжаю проектирование — или сначала уточним?
```

**Soft: the work continues unless the engineer stops it.** Raise, recommend, proceed. What
this phase must never do is notice a contradiction and implement anyway.
