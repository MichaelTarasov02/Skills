# Phase 2 — Plan ⛔ gate

Say where you will look, what you expect to find there, and what would prove you wrong.
Then stop and let the engineer redirect you.

This phase costs two minutes and regularly saves an hour, because the engineer knows
things no amount of reading finds: that this module was rewritten last month, that this
customer has a configuration nobody else has, that someone already looked here in
February.

## Hypotheses, not a search plan

A list of files you intend to read is not a plan. A hypothesis names a **mechanism** and
predicts something checkable:

```
H1  The shift stays open because the close handler returns early when the
    second meal break is unsigned.
    Would confirm:  the early-return branch exists and the account has the
                    second break required
    Would kill it:  accounts with the same setting close normally
    Look in:        the close path, the per-project time settings
    Cost to check:  one grep and one settings comparison
```

Three to five hypotheses. Fewer means you have already decided; more means you have not
thought yet.

**Every hypothesis names what would kill it.** One that cannot be falsified is a belief,
and beliefs survive contradicting evidence — which is exactly how confident wrong
diagnoses happen.

## Cover all three branches, deliberately

The natural instinct produces three defect hypotheses and nothing else. Force one of each:

| Branch | The hypothesis takes the shape |
|---|---|
| Defect | "the code contradicts rule X because …" |
| By design | "the code follows rule X, and rule X no longer matches what the product wants" |
| User error | "the code follows rule X, the user did Y expecting Z, and the screen makes Y easy" |

If you cannot state the by-design and user-error versions, you have not understood the
rule well enough to call anything a defect.

## Order by cost, not by likelihood

Check cheap-and-decisive before expensive-and-probable. A grep that eliminates two
hypotheses in ten seconds comes before a reproduction that takes an hour, even if the
reproduction targets your favourite theory.

| Cost | Examples |
|---|---|
| Seconds | grep for the rule, read one config value, search the commit history for the error id |
| Minutes | compare two accounts' settings, read one code path end to end, check the release boundary |
| Longer | set up a reproduction, run against a copy of the data, bisect |

## Where to look, by symptom shape

| Symptom | Sources, in order |
|---|---|
| Wrong value shown | the query, then the serialiser, then the screen — the value is usually wrong before it renders |
| Nothing happens on tap or click | the guard on the action, the permission, then the catch block that logged nothing |
| Works for one account, not another | per-tenant settings — compare full configurations, not the parts that seem relevant |
| Worked last week | the release boundary, then what changed outside the code — data volume, expiry, third party |
| Slow | one measurement before any reading; delegate to `debug` in `slow` mode |
| Crash | the stack, from the last frame that belongs to the product |

## Ends with, then stop

```
Hypotheses:   <each with mechanism, what confirms, what kills it, cost>
Order:        <cheap and decisive first, with the reason>
Sources:      <code paths, logs, settings, screens — named, not "the codebase">
Not looking:  <what you are deliberately skipping, and why>
Need:         <access or data you do not have>
```

`Not looking` matters as much as the rest. It lets the engineer say "actually, check
there" — which is the entire point of the gate.

**Wait for an answer.** Passing this gate on assumed agreement wastes the phase.
