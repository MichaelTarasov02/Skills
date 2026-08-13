# Coupling

> **Examples below are shapes, not facts about your codebase.** Counts and paths are
> illustrative. Measure before you quote any of them.

Read before phase 2. Where large changes actually fail.

Adding functionality feels additive. It rarely is: something that already exists needs to
know about the new thing, and the places that need to know are not the places you are
editing. Each is small, each is invisible in the diff, and each is expensive once the
feature has shipped without it.

## The bridges that do not get built

For every new entity, field, state or rule, walk this list. Most rows will be "not
applicable" — the value is in the one or two that are not.

| Existing thing | Question | Cost of missing it |
|---|---|---|
| Lists and reports over this data | do they include the new thing, or silently exclude it | numbers that quietly stop reconciling |
| Filters and search | can users find records by it | the feature exists and is unreachable |
| Exports | is it in the export, and should it be | discovered by a customer, not by you |
| Permissions | who may see and change it | a leak, or a screen that hides what the API returns |
| Existing settings | does any of them change how the new thing behaves | works for you, breaks for one tenant |
| Notifications | should anything now be announced | the feature works and nobody notices it happened |
| Audit and history | is a change to it recorded | discovered during a dispute |
| Deletion and export of user data | what happens to it | a compliance gap |
| The other platform | does it need the same thing | shipped on one, missing on the other |
| Aggregates and counters | do any of them now under-count | wrong numbers, trusted |

**The last row is the quiet one.** A new state that a status count does not know about
makes that count wrong everywhere it appears, and nothing fails.

## Find them mechanically — and follow the value, not only the symbol

Start from the entity and follow it outward. **Do this in every platform root named in
`config.yaml`, not only the one you are editing.**

```bash
grep -rn '<entity>' <root> | grep -E 'serializ|report|export|filter' | head -20
grep -rn '<entity>' <root> | grep -iE 'permission|role|scope' | head
```

**Then do it again with the value.** This is the step that decides whether the search
worked. An enum, a choice field or a status constant couples through the string or number
it serialises to — and that value is what every consumer downstream actually matches on:

```bash
grep -rn 'STATUS_NAME *= *' <models file>          # find the values behind the symbols
grep -rn '"<the value>"' <every root>              # then follow each value
grep -rn '<the value>' --include='*.arb' --include='*.json' --include='*.po' <every root>
```

Measured on one repository: searching the class name of a status enum returned **one
file** — its own definition — and nothing under serializers, reports, permissions or the
client. Searching the values it holds returned three families of user-facing strings in
seven locales, on the other platform. The symbol search concluded "no coupling"; the value
search found the coupling that would have shipped broken.

**An empty candidate set is a finding about the search, not about the code.** Large
functionality with no coupling at all does not exist. When the greps come back empty, the
entity is coupling under a different name — its value, its serialised field name, its
database column, its label — and the next move is to find that name, never to write
"no dependants".

Read what came back. Each candidate is either "needs updating" or "correctly unaffected",
and both answers go in the design.

A candidate set nobody enumerated is a candidate set discovered one item at a time, in
production.

## The reverse direction matters too

Not only "what must know about the new thing" but **"what does the new thing need from
what exists"**:

- a setting it should respect and does not
- a permission model it should fit rather than invent
- an existing base class, builder or pattern it should extend
- a rule it must not contradict

New functionality that invents its own permission check beside an existing permission
system is functionality that will be wrong the first time the permission model changes.

## Size before you decide

Some bridges are worth building now, some are worth a follow-up ticket, and one or two are
worth deciding not to build. That is a decision, and it needs numbers:

```
Мост:      <what needs to know about the new thing>
Где:       <files, count>
Размер:    <rough>
Если не:   <what breaks, and when someone notices>
Рекомендую: сейчас / отдельной задачей / не делать — <because>
```

**"Notices when" is the field that decides.** A bridge whose absence surfaces during a
customer dispute is not the same as one that surfaces as a slightly odd screen, even if
both are two hours of work.

## Ends with

The coupling map goes into the design artifact and is approved with it. A bridge that
appears for the first time during implementation is a bridge that gets skipped, because by
then the estimate has been given.
