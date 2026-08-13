# Phase 6 — Report

One document an engineer can verify without redoing the work. Longer than the enhancement
report, because there was design and deeper analysis.

## Structure

Reader's order: what and why first, method after.

```markdown
# <название фичи>

## Зачем
<the goal from phase 1 — the outcome, not the feature. One paragraph>

## Что появилось
<the functionality in behaviour terms, two or three sentences>

## Что обсуждали до начала
<the product-check findings and how each was resolved — or that it ran clean>

## Как спроектировали
<where it lives, what it extends, and why that place>

## Связанность
| Что | Обновили | Почему / почему нет |
|---|---|---|
<every coupling candidate, including the ones correctly unaffected>

## Спецификация
<the steps, condensed — and the split, if there was one>

## Как легло в код
| Файл | Что |
|---|---|

было:
    <fragment>
стало:
    <fragment>
почему: <one line>

<three or four key points; the rest named, not quoted>

## Пропуски в задаче
<what the task did not specify, what was proposed, and what was approved>

## Конвенции
<shapes followed, with the sibling establishing each; deviations with reasons>

## Как проверяли
<tests written and run with output; spec traced; **goal checked** and how>

## Узкие места рядом
<noticed, sized, not fixed>

## Что осталось
<non-empty by default>
```

## The three sections that carry the most

**`Связанность`.** The coupling table, with the unaffected rows kept. It is the evidence
that the ripple was enumerated rather than encountered — and the row someone disagrees
with is the most useful thing in the document.

**`Пропуски в задаче`.** What the task did not say, what was proposed, what was approved.
Without it, filled gaps become requirements nobody remembers agreeing to.

**`Как проверяли`, goal line.** Tests passing and the specification complete are the easy
answers. Whether the thing it was built for now works is the question, and a report that
skips it has reported on the wrong thing.

## Delegate the check and the texts

Run the change through `review` in `change` mode before publishing; its findings go into
`Что осталось`, not into a silent second fix.

The PR description is `copy`, team channel — shorter, aimed at a reviewer deciding what to
look at. The release note is `copy`, user channel. Neither is this report; this is the
record, they are the announcements.

## Where it lands

`.dev-agent/features/<slug>/report.md`, beside the specification and the parts. The whole
folder is the feature's history: what was wanted, how it was designed, what was built, what
was checked.

## Close the handover

Where the work was split, this report is written after the **last** part. Delete
`.dev-agent/features/<slug>/progress.md` — a finished feature that still looks mid-flight
sends every later session down the resume path in `SKILL.md` and it starts by trying to
continue something that is done.

Where this report covers a part rather than the whole, say so in the first line and leave
`progress.md` in place.

## Ends with

```
Отчёт:        <path>
Охват:        <вся работа | часть N из M>
Цель:         <achieved | partially — with what is missing>
Изменено:     <files, count; bridges, count>
Тесты:        <written / run / result>
Передача:     <progress.md deleted, or left with what remains>
Осталось:     <non-empty or explained>
Тексты:       <PR description and release note drafted — not sent>
```
