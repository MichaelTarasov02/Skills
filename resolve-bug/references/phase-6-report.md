# Phase 6 — Report

One document an engineer can verify without rerunning the investigation, plus whatever
text goes to a human outside the team.

The test: **could a reviewer confirm or refute every claim from this document alone?**
If a claim needs them to trust you, it is missing its evidence.

## The audit

Written in the reader's order — verdict first, method after. A reviewer who agrees with
the verdict may never read past it, and that is a success, not a skimmed report.

```markdown
# <краткое имя проблемы>

## Что это оказалось
<ветка и одна фраза. Если дефект — что именно было сломано>

## Как выглядела проблема
<симптом словами репортёра, verbatim, и что он ожидал>

## Куда смотрели
| Гипотеза | Чем проверяли | Итог |
|---|---|---|
| <механизм> | <команда, файл, лог> | убита: <чем> / подтверждена |

## Что нашли
<причина, с цитатой правила и путём. Что именно противоречило чему>

<для «by design» — правило и почему оно расходится с ожиданием>
<для user error — правило и что сделал пользователь>

## Что изменили
<только для дефекта>

| Файл | Что |
|---|---|

было:
    <фрагмент>
стало:
    <фрагмент>
почему: <строка>

## Как убедились
<воспроизведение до, после, откат, повтор — или прямое «не воспроизводилось,
проверка чтением»>

## Тексты
<the reply, the question to the product owner, or the note — in full, as it will be
 sent, in the reader's language. Drafted here, sent by a person>

## Что осталось
<необъяснённые детали, неисправленное, соседние находки — непустой по умолчанию>
```

**`Что осталось` не имеет права быть пустым молча.** Пустой раздел допустим с одной
фразой, почему покрытие полное. Молчание о пробеле читается как отсутствие пробела, и
следующий читатель считает, что его рассмотрели и отклонили.

## Delegate the check

Before publishing, run the change through `review` in `change` mode. It owns the checklist
— what tasks of this shape forget, regression narrowed to deletions, PII, analytics
integrity — and it will find what a self-review does not.

Its findings go into `Что осталось`, not into a silent second fix.

## The outbound text

Every verdict ends in something for a human who is not an engineer. Delegate the writing
to `copy`; produce it, never send it. **It goes into this report under `## Тексты`, in
full** — a reply that lives only in the chat is a reply that gets rewritten from memory
tomorrow, without the red-lines check, and with nothing showing what this customer was
already told.

| Verdict | Channel | Shape |
|---|---|---|
| User error | reply to the reporter | what happened, why, what to do now, no blame, no date |
| By design | question to the product owner | context, options, recommendation, cost of waiting |
| Defect | reply to the reporter, if they are waiting | what was wrong, that it is fixed, when they will see it — **without a date** |
| Unresolved | reply to the reporter | what is known, what is being checked, what is needed |

For a fixed defect, "when they will see it" means the release mechanism, not a date: *"в
следующей сборке приложения"* is a fact; *"на следующей неделе"* is a promise nobody
authorised.

## Where it lands

The audit goes to `.dev-agent/bugs/<slug>.md` in the product repository. It belongs with
the code because the next person to touch that area needs to know what was already
investigated — and because a diagnosis that lives in a chat log is a diagnosis that gets
repeated.

Name the file for the symptom, not the cause. The next person searches for what they see.

## Ends with

```
Отчёт:        <путь>
Вердикт:      <ветка>
Тексты:       <кому и что подготовлено — не отправлено>
Проверено:    <чем именно>
Осталось:     <непустой список или объяснение пустоты>
```
