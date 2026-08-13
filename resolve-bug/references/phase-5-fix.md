# Phase 5 — Fix

Only after the verdict is accepted, and only for the defect branch.

## Fix the cause, at its level

| The cause is | Fix belongs |
|---|---|
| a wrong condition | at the condition |
| a value that should never have been null | where the value is produced |
| two rules combining badly | at the combination — usually one of them gains a case, and which one is a decision |
| a missing state | in the state model, not with a null check at the render site |

**A plaster at the symptom is visible as one.** A null check where the value should exist
removes the crash and leaves the wrong value flowing onward, where it produces a different
symptom nobody connects back.

Where the fix needs a design decision — which of two rules yields, what the correct
behaviour even is — that is `spec`, not this phase. Where it is markup, an event or a
performance change, that is `craft`.

## One change, one reason

Everything in the diff traces to the diagnosed cause. A second defect found on the way is
**reported, not included** — a diff carrying two unrelated fixes is unreviewable, and when
it regresses nobody knows which half did it.

Improvements noticed nearby are the same: worth saying, not worth including.

## Reproduce first, then fix, then reproduce again

```
1. make the symptom appear on demand        ← without this, nothing below means anything
2. apply the change
3. the symptom is gone
4. revert the change → the symptom returns
5. re-apply
```

Step 4 is the one that gets skipped and the only one that proves causation. A symptom that
stops when you change something is not the same as a symptom you can turn on and off.

Where the symptom cannot be reproduced, say so plainly and state what the fix rests on
instead — usually reading. A fix on reading alone is legitimate; a fix on reading alone
presented as verified is not.

## Show the change so it can be read without the diff

Two or three key points, before and after, with the reason. Not the whole diff — the parts
that carry the decision:

```
<path>:<line>

было:
    <the code, trimmed to what matters>

стало:
    <the code>

почему:  <what this fixes, in one line>
```

Everything else in the diff is named but not quoted: renames, imports, moved lines. The
reviewer needs to know they exist, not to read them here.

## What the change touches

| Question | Where the answer comes from |
|---|---|
| What else calls this | grep, narrowed to what actually changed — not everything importing the file |
| Does anything depend on the old behaviour | only if something was removed or changed meaning; pure additions break nothing |
| Do the tests cover this area | count them; if there are none, say so — it changes how the fix is verified |
| Does the fix change data | migrations, backfills, and whether it is reversible |

Where tests exist and cover the area, add one that fails before the fix and passes after.
Where they do not, say that the verification is manual and hand the steps to phase 6.

## Ends with

```
Изменено:     <файлы, одной строкой каждый>
Ключевое:     <2–3 фрагмента было/стало с причиной>
Не входит:    <что заметили и не стали трогать>
Задевает:     <зависимости, суженные до изменившегося>
Проверено:    <как — прогон, тест, или чтение с прямым признанием>
```
