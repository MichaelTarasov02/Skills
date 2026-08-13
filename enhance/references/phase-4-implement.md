# Phase 4 — Implement

The plan, applied. Nothing that is not in the plan.

**Read `references/conventions.md` before starting.** Fit is the property this phase is
judged on.

## Follow the plan, and stop when it is wrong

The plan will occasionally turn out wrong — a case it did not anticipate, a caller it did
not see. **Stop and say so.** Do not improvise a solution inside the implementation: a
plan silently diverged from is a plan nobody approved, and the divergence is invisible in
the diff.

One sentence back to the engineer costs less than a change that does something other than
what was agreed.

## Before writing anything, look for it

```bash
grep -rn '<what the helper would do, in words>' <module> | head
grep -rn '<the likely name>' <module> | head
```

The second-worst outcome of this phase is a helper that already existed. The worst is one
that existed and behaved **slightly** differently — now there are two truths, and the next
bug is about which one a call site used.

Where something exists and does not quite fit: extend it, or state plainly why it cannot
be extended. Adding a near-twin without that sentence is how a codebase acquires three
date formatters.

## Copy the shape of the nearest sibling

Not the nearest file — the nearest file doing the same kind of thing. Declaration style,
error handling, naming, where the file lives, what it is a `part` of, which annotations it
carries. Read one, then write yours to match.

A change that works but is the only one of its kind in two hundred is a change that will
be rewritten by whoever notices.

## Clean means readable by the next person, not clever

| | |
|---|---|
| A name says what the thing is | not what it was called in the ticket |
| A function does one thing | if the name needs "and", it is two |
| Nesting stays shallow | early return over another level |
| The special case is visible | not buried in a condition three terms long |
| Comments explain **why** | what is already in the code |

**No commented-out code, no debug output, no leftover flags.** They are the first thing a
reviewer sees and the last thing anyone removes.

## Optimised means not obviously wasteful

Not micro-optimised. The things that matter in a small change:

- no query inside a loop where a single query would do
- no recomputation of something already computed a line above
- no new N+1 introduced by a value read per row

Anything beyond that is `craft`'s `perf` mode, and only against a measurement.

## Where the change is markup or an event

Delegate to `craft`. Accessible names, analytics events and test identifiers have their
own rules and their own leverage question — an element that is an instance of a shared
component gets fixed at the component.

## Ends with

```
Реализовано:  <steps done, mapped to the plan>
Отклонения:   <where the plan was wrong, and what was agreed instead>
Переиспользовано: <what already existed and was extended>
Соседи:       <the files whose shape was copied>
Файлы:        <changed, one line each>
```

`Отклонения` non-empty is normal and healthy. `Отклонения` empty on a change that took
longer than expected usually means something was improvised and not recorded.
