# Platform split — several platforms without forking the skill

Read before phase A4, wherever platforms diverge.

## The branch test decides placement

Inline what **every** path through the skill needs. Push behind a pointer what only
**some** paths reach. Applied here: the procedure is identical for both platforms, so it
stays in the body; the mechanics differ entirely, so they go to reference files.

| Tier | Content |
|---|---|
| Body | the procedure, the decision points, the completion criteria — platform-neutral |
| `references/<topic>-<platform>.md` | how the procedure is carried out on that platform |

**The platform names are not fixed.** They come from `.dev-agent/config.yaml`, which is
read at run time on a repository this agent has never seen. A skill naming a specific
framework in its body is a skill that is wrong on the next install — and wrong in the way
that compiles.

A skill whose body says "on platform A do X, on platform B do Y" at every step has forked.
Both halves then drift, and a developer on one platform reads twice the material they
need.

## The platform file that does not exist

There will always be one. **A missing platform reference is not a blocker**, and every
skill using this split says what it does instead:

> Read `references/<topic>-<platform>.md`. Where there is no file for this platform, derive
> the specifics from the codebase — read two existing examples of the same kind and copy
> their shape — and **say the advice was derived rather than codified.**

The two are different levels of confidence, and a reader deciding whether to paste
generated markup needs to know which one they have.

## Pointer wording

From the body, always the firing form:

> Read `references/flutter.md` before phase 3.

Never the inert form:

> Platform details are in references.

The wording decides whether the agent reaches the file. This is the single highest-return
rule in the split.

## What belongs in a platform file

Executable specifics, not prose about the platform:

- exact file to read and what to extract from it
- exact API, widget, attribute, or config key
- a worked example for each case the skill handles
- what the platform makes impossible, so the body's step can be skipped honestly

A platform file that explains what the framework is has failed the no-op test.

## Detect before prescribe

Every platform allows several conventions. The skill establishes which one the repository
already uses, then follows it. Prescribing a convention the codebase does not use makes
the skill's output unusable and its advice untrustworthy.

State the detection explicitly: which file is read, which signal decides.

## Single platform

A repository may hold only one platform. The skill says which it detected and skips the
other, rather than emitting empty sections for a platform that is not there.
