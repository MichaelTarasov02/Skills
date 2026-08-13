# Phase 6 — Report

One document an engineer can verify without redoing the work.

The test: **could a reviewer confirm the change matches its purpose from this alone?**

## Structure

Reader's order — the goal first, the method after. A reviewer who agrees with the first
two sections may never read further, and that is a success.

```markdown
# <краткое имя изменения>

## Зачем
<the business reason, from phase 1 — one paragraph. Not the ticket title>

## Что было и что стало
<behaviour, not code. Two sentences>

## Что нашли по дороге
<contradictions between the ticket and the code, and how each was resolved —
 or that it is still open>

## Спецификация
<the plan, condensed: what changed where, and why each step>

## Как это легло в код
| Файл | Что |
|---|---|

было:
    <fragment>
стало:
    <fragment>
почему: <one line>

<two or three key points only — the rest of the diff is named, not quoted>

## Пропуски в задаче
<what the task did not specify, what was proposed, and what was approved>

## Конвенции
<which shapes were followed, with the sibling that establishes each;
 deviations with reasons>

## Как проверяли
<what was traced, what was read, and — explicitly — what was not verified>

## Требуется до мержа
<regeneration commands, migrations, config changes — anything the change is
 incomplete without. "Ничего" only when it was checked>

## Узкие места рядом
<what was noticed and deliberately not fixed, with rough size>

## Что осталось
<non-empty by default>
```

## The two sections that carry the most and get written the least

**`Что нашли по дороге`.** Every contradiction between ticket and code, and how it was
resolved. This is the section that tells the reviewer a decision was made — silently
choosing one side and not mentioning it is how the choice becomes invisible.

**`Пропуски в задаче`.** What was missing, what was proposed, what was approved. Without
it a filled gap becomes a requirement nobody remembers agreeing to — and it reads exactly
like one that was.

**`Узкие места рядом`.** The duplicated helper, the function that grew too long, the rule
that should be data. Named, sized, not fixed. Without this section they stay unseen until
someone else trips on them; with it they become a decision.

## Delegate the check and the description

Before publishing, run the change through `review` in `change` mode — it owns the
checklist for what changes of this shape forget, and its findings go into `Что осталось`
rather than into a silent second fix.

The PR description is `copy`, team channel. It is a different document from this report:
shorter, aimed at a reviewer deciding what to look at. This report is the record; the PR
description is the invitation.

## Where it lands

`.dev-agent/changes/<slug>.md` in the product repository. It belongs with the code because
the next person to touch this area needs to know why it looks the way it does — and a
rationale that lives in a chat log is a rationale that gets re-litigated.

## Ends with

```
Отчёт:        <path>
Цель:         <achieved | partially — with what is missing>
Изменено:     <files>
До мержа:     <regeneration / migration outstanding, or "ничего — проверено">
Проверено:    <by reading — and what was not>
Осталось:     <non-empty or explained>
Тексты:       <PR description drafted — not sent>
```
