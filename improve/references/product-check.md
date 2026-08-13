# The product-analyst pass

> **Examples below are shapes, not facts about your codebase.** Measure before you quote
> any of them.

Read before phase 1. Ten minutes reading the task as a product analyst, before reading any
code.

**Soft by design.** Everything here is raised, never blocked on. The engineer decides what
goes back to the product owner. What this pass must prevent is the other failure: noticing
a contradiction and implementing anyway.

## Four questions, in order

### 1. What is the goal behind the request?

Not what the task asks for — what it is for. "Add a column to the report" has a goal
behind it: someone needs to make a decision they cannot make now.

The goal decides the design. A column added without knowing the decision it supports is a
column that gets followed by three more tickets.

Where the task does not say and nobody is available: state your reading of it explicitly
as a reading. Being wrong about it visibly is fine; being wrong invisibly is what produces
the follow-up tickets.

### 2. Does the described solution actually reach it?

The most valuable question this pass asks, and the one that feels rudest.

A task usually arrives as a solution, not a problem — someone already decided how. Where
the solution does not obviously reach the goal, say so once, with the alternative:

```
Цель, как я её понял: <…>
Описанное решение даёт <…>, но не даёт <…>.
Вариант, который даёт: <…>
Стоит обсудить до начала — или реализую как описано.
```

Then let it go. One flag, one alternative, no argument. The person who wrote the task may
know something you do not, and this pass exists to surface, not to litigate.

### 3. Does it contradict something the product already does?

The expensive one, because it is invisible from the task and obvious from the code.

| Contradiction | How it looks |
|---|---|
| Two rules for the same thing | the new behaviour and an existing setting disagree |
| The same concept, named differently | a new entity that is an existing one under another name — check `lexicon.md` |
| A promise the product already makes | the new behaviour breaks something documented or on screen |
| A recently-made decision reversed | the task undoes something shipped last month, possibly without knowing |

The last one is worth a `git log` on the area. A task reversing a recent deliberate change
usually means two people want different things, and the code cannot settle it.

### 4. Who is affected that the task does not mention?

New functionality lands on a system with existing users, roles, tenants and integrations.

- roles other than the one in the task
- accounts configured unusually
- anything reading the data that is about to change shape
- the other platform, if the product has two

**A feature specified for one platform is a feature that ships on one platform**, and
whether that is intended is a product decision, not an implementation detail.

## How to raise it

One block, at the end of phase 1, in one place:

```
## Стоит обсудить до начала

⚠️ <the issue, one sentence>
   Почему важно: <the consequence of not settling it>
   Мой вариант:  <a recommendation>
   Блокирует:    да / нет — <what can start regardless>
```

`Блокирует: нет` is the common case, and saying it lets the work continue while the
question travels. `Блокирует: да` means the design would be built twice — say that
plainly.

**Empty is the normal outcome and is worth stating as empty.** "Противоречий не нашёл,
проверил: цель, решение, конфликты с существующим, кого задевает" tells the engineer the
pass ran. Silence tells them nothing.
