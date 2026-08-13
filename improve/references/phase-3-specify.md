# Phase 3 — Specify ⛔ gate

The design turned into steps someone could execute. Approved before any code.

## The specification is a diff described in words

Same rule as the smaller pipelines, more steps:

```
N. <path>:<place>
   было:    <current behaviour or absence>
   станет:  <new behaviour>
   почему:  <which requirement or bridge this satisfies>
```

**No step says "implement the feature".** A step that cannot be written as before → after
has not been thought through, and the thinking will happen during implementation, where
nobody sees it.

Every bridge from the coupling map appears as its own numbered step. A bridge folded into
"and update the related places" is a bridge that gets skipped.

## Decide whether it fits one session

**Read `references/splitting.md`.** Where it does not fit, the specification becomes a
numbered series of self-contained prompts, each leaving the project working.

The split is approved here, with the spec. Discovering mid-implementation that the work
does not fit is how half-built functionality gets merged.

State the decision either way:

```
Влезает в одну сессию: да — <n> шагов, один модуль
                       нет — <m> частей, разбито по <layer | seam>
```

## Order the steps so the project works between them

Additive first, switch second, remove third. Schema before the code that uses it. The
contract before the client. Each step leaves something that builds.

Where a step cannot preserve that, it goes behind a flag and the flag has its own final
step.

## Conventions, named

```
Соседи:   <the files whose shape the new code copies>
Следую:   <convention → where it is established>
Отступаю: <deviations, with a reason each>
```

Delegate the detection to the method in `skills/enhance/references/conventions.md` — it is the
same problem and the same answer. Do not restate it here.

## Tests, planned rather than improvised

Phase 5 writes them; this phase decides what is worth testing:

| Worth a test | Not worth one |
|---|---|
| The rule the feature exists for | glue and wiring |
| A boundary someone will get wrong | a getter |
| A bridge that silently under-counts if broken | a screen's layout |

Where the project has almost no tests, say so — it changes what phase 5 can do and how
much the manual check is worth.

## The gate

Show the specification and the split. Ask:

> Спецификация такая. Разбивка — так? Иду реализовывать?

This is the last cheap moment. After it, changing the shape means changing code.

## Ends with

```
Шаги:         <numbered, before → after → why, bridges as their own steps>
Разбивка:     <one session, or the parts and their seams>
Порядок:      <and that the project works between steps>
Конвенции:    <followed, with sources>
Тесты:        <what is worth testing>
Артефакт:     .dev-agent/features/<slug>/spec.md  (+ part-N.md if split)
```
