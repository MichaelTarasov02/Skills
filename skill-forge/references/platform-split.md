# Platform split — React and Flutter without forking the skill

Read before phase A4, wherever the two platforms diverge.

## The branch test decides placement

Inline what **every** path through the skill needs. Push behind a pointer what only
**some** paths reach. Applied here: the procedure is identical for both platforms, so it
stays in the body; the mechanics differ entirely, so they go to reference files.

| Tier | Content |
|---|---|
| Body | the procedure, the decision points, the completion criteria — platform-neutral |
| `references/react.md` | how the procedure is carried out in React + TypeScript |
| `references/flutter.md` | how the procedure is carried out in Flutter |

A skill whose body says "for React do X, for Flutter do Y" at every step has forked.
Both halves then drift, and a developer on one platform reads twice the material they
need.

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

A platform file that explains what React is has failed the no-op test.

## Detect before prescribe

Both platforms allow several conventions. The skill establishes which one the repository
already uses, then follows it. Prescribing a convention the codebase does not use makes
the skill's output unusable and its advice untrustworthy.

State the detection explicitly: which file is read, which signal decides.

## Single platform

A repository may hold only one platform. The skill says which it detected and skips the
other, rather than emitting empty sections for a platform that is not there.
