# Phase 3 — Plan ⛔ gate

Exactly what changes where, in what order, and what it costs. Specific enough that
someone else could implement it and produce roughly the same diff.

## The plan is a diff described in words

Vague plans produce vague changes. Every line names a file, a place in it, and the change:

```
1. <path>:<function>
   было:    <the current behaviour, one line>
   станет:  <the new behaviour, one line>
   почему:  <which requirement this satisfies>

2. <path>:<function>
   ...
```

**No step says "update the logic".** If a step cannot be written as before → after, it has
not been thought through, and the thinking will happen during implementation, where it is
invisible.

## Order the steps so the code compiles between them

Where possible, each step leaves the project working. This is not ceremony: a change that
only works when complete cannot be reviewed in parts, cannot be paused, and cannot be
partially reverted when one piece turns out wrong.

Signature first, callers second, behaviour last — or additive first, switch second, remove
third.

## Name the conventions you are following

**Read `references/conventions.md`.** The plan states which shape the change copies and
where that shape is established:

```
Соседи:   <the files read>
Следую:   <convention → the sibling that establishes it>
Отступаю: <deviations, with a reason each — normally empty>
```

A reviewer can check fit from these three lines without reading the directory. Without
them they either read everything or trust you.

## Consequences

| Question | Must be answered |
|---|---|
| What else calls this | narrowed to what actually changes, not everything importing the file |
| Does old data change meaning | retroactivity — from phase 2 |
| Does anything cache or freeze this | snapshots, reports, derived columns |
| What breaks for a client that has not updated | only if a contract changes |
| Which tests cover this area | count them; none is a finding that changes phase 5 |

## Gaps in the task, filled and flagged

By the end of planning you know what the ticket did not say: a text, a default, a name, a
case nobody decided. Each is filled with a proposal and marked — never implemented
silently, never handed back empty.

```
Пропуски:  ⚠️ <what was missing> → предлагаю <the proposal> (<basis>)
```

Text goes to `copy`. The engineer approves at the gate rather than writing anything.

## Bottlenecks you will not fix

Anything structurally wrong that the change reveals: named, sized, and explicitly excluded.

```
Замечено:  <what>
Размер:    <rough>
Не делаю:  <because it makes this change unreviewable>
```

The engineer decides whether it becomes a task. Folding it in silently is how a two-file
change becomes a nine-file change nobody can review.

## The gate — this is where every question of the whole run is asked

Phases 1 and 2 collected questions and did not ask them. **They are asked here, once,
batched, each carrying your recommended answer**, so the engineer answers a list in a
minute instead of a question at a time across three interruptions.

```
Вопросы (все за прогон):
- <вопрос> — рекомендую <ответ>, потому что <основание из кода>
Спросил бы раньше: <anything held back that could have changed the plan>
```

`Спросил бы раньше` is what lets the engineer see what was decided on a reading rather
than on an answer. Omitting it makes a carried question indistinguishable from a question
nobody had.

Show the plan. Ask, and wait:

> План такой, вопросы под ним. Правки — точно там? Иду реализовывать?

The engineer knows what the code cannot say: that this function is being replaced next
sprint, that this convention is deliberately being abandoned, that this file has an owner.
Two minutes here is the cheapest review the change will get.

## Ends with

```
Шаги:         <numbered, each before → after → why>
Порядок:      <and whether it compiles between steps>
Соседи:       <conventions followed, with sources>
Регенерация:  <command, if a generated twin is affected — or "не требуется">
Последствия:  <callers, retroactivity, freezing, contracts, tests>
Не делаю:     <bottlenecks named and excluded>
Вопросы:      <all of them, batched, each with a recommendation>
Спросил бы раньше: <what was held back, and what it would have changed>
Открыто:      <anything still undecided — must be empty to proceed>
```
