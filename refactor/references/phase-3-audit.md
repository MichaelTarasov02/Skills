# Phase 3 — Audit

Two audits, run per the mode. Findings ranked by what they cost, not by how much they
offend.

## Clean audit

Establish the project's own baseline first: **read
`skills/enhance/references/conventions.md`** and detect what this codebase does. Clean means
"consistent with here and readable by the next person", not "matches a style guide".

| Look for | The cost when present |
|---|---|
| A function doing several things | every change to one thing risks the others |
| Duplication — the same logic in two or three places | fixes land in one copy |
| Naming that lies | the reader trusts it and is wrong |
| Nesting past two or three levels | the reader holds too much at once |
| A special case buried in a condition | it disappears from view and then from thought |
| Comments explaining *what* | they drift from the code and mislead |
| A parameter nobody passes, a branch nobody reaches | dead weight the reader must still evaluate |
| Mixed levels of abstraction in one function | the reader switches altitude every line |

**Rank by cost to the next change, not by ugliness.** A long function nobody touches
costs less than a short one with a lying name in a hot path. The audit says which, and it
is what makes it more than a list of complaints.

## Performance audit

**Measurement first.** Every finding names the measurement supporting it; a suspicion is
labelled as one. Where nothing is measured yet, delegate to `debug` in `slow` mode before
writing findings.

| Look for | Confirm by |
|---|---|
| A query inside a loop | counting queries for one call |
| A related object touched per row | the same count |
| A derived value recomputed per access | reading, then the timing |
| A list built eagerly where it is scrolled | the render timing at realistic size |
| A round trip per item where one call would do | counting calls |
| Work done before it is needed | what happens if it is deferred |

**Do not report a raw count as a finding.** Narrow: how many of the candidates are on the
path the task complained about? That number is the work.

## Both modes: name the conflicts

Where readability and speed pull apart, say so rather than choosing:

```
Конфликт:   <the readable shape> против <the fast shape>
Разница:    <what the metric costs either way — measured>
Рекомендую: <one>, потому что <…>
```

Most apparent conflicts dissolve under measurement — the readable version turns out to
cost nothing. Report that too; it removes an argument the team would otherwise keep
having.

## Bugs found here are not fixed here

An audit reads code closely and therefore finds bugs. Each is a finding, reported
separately, routed to `resolve-bug`.

Fixing it inside a refactor destroys the property the whole pipeline rests on: that
behaviour is supposed to be identical. A diff containing both is a diff where nobody can
tell which change did what.

## Ends with

```
Режим:        <what was audited>
Найдено:      <ranked by cost to the next change / to the metric>
   <finding> — <cost> — <evidence>
Не находки:   <things that look wrong and are fine, with why>
Конфликты:    <readability against speed, measured>
Баги:         <found, not fixed, routed>
Стоит ли:     <the honest total — sometimes the answer is "не стоит">
```

`Стоит ли` is a real field. A block with three small findings and no measured problem is a
block to leave alone, and saying so is a better outcome than a change nobody needed.
