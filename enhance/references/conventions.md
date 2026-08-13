# Conventions

> **Examples below are shapes, not facts about your codebase.** File names, counts and
> annotations are illustrative. Detect before you follow.

Skim during phase 2, read fully before phase 4. A change written correctly in the wrong
style is a change that reads as foreign for the rest of the file's life.

## Detect, never prescribe

There is no correct convention, only the one in use. Every rule below is a **question you
answer from the code**, not an answer you bring with you.

The reliable method is the same everywhere: **find the nearest sibling and copy its
shape.** Not the nearest file — the nearest file doing the same *kind* of thing. A cubit
copies a cubit, a serializer copies a serializer, a validator copies a validator.

```bash
ls <the directory the change lands in>
find . -name '*<the same kind>*' | head -5
```

Read two. Where they agree, that is the convention. Where they disagree, the newer one
usually wins — check with `git log` before assuming.

**Distinguish a convention from a habit.** Two siblings agreeing on which sections exist
but disagreeing on their order means the sections are a convention and the order is not.
Follow what is consistent; do not manufacture consistency the codebase never had.

Measured on one repository: two screens of the same kind both declared the same five
sections, in two different orders. Enforcing an order there would be inventing a rule and
then obeying it.

## What to establish, in order of how loudly a violation reads

### 1. Naming and file layout

```bash
find . -name '*_<suffix>.*' | wc -l        # for each suffix you see
ls <a feature directory>                    # how a feature is subdivided
```

Measured on one repository: 989 files ending `_widget`, 183 `_page`, 232 `_cubit`, 232
`_state`. Suffixes that consistent are not a habit, they are a contract — a file named
outside the scheme is findable only by whoever added it.

**Pairing is part of the layout.** The same measurement showed cubit and state at exactly
232 each: every one has precisely one state file. Adding one without the other breaks a
1:1 relation that nothing enforces and everything assumes.

### 2. How the same kind of thing is declared

Open the nearest sibling and copy its declaration wholesale:

```dart
part of 'camera_cubit.dart';

enum InitDataStatus { initial, permissionDenied, loading, success, error }

@freezed
abstract class CameraState with _$CameraState {
  const CameraState._();
  const factory CameraState({ ... });
}
```

Four conventions in eight lines: state lives as a `part` of its cubit rather than as its
own library; it is generated rather than hand-written; it exposes a private constructor;
and status is **one enum per operation**, not one shared status field.

A new state written as a plain class with a single `status` field would work, pass review
on a busy day, and be the only one of its kind in two hundred and thirty-two.

### 3. Generated code — check before editing anything it produces

**This is the convention that stops the build rather than reading oddly.** A file whose
twin ends `.freezed.dart`, `.g.dart`, `.generated.*`, `_pb.py`, `*.d.ts` is not written by
hand, and the hand-written source beside it cannot be changed without regenerating.

```bash
find . -name '*.freezed.dart' -o -name '*.g.dart' -o -name '*.generated.*' | wc -l
grep -nE 'build_runner|codegen|generate|protoc' pubspec.yaml package.json Makefile 2>/dev/null
git check-ignore -q <one generated file> && echo "ignored — CI regenerates" || echo "COMMITTED — you must regenerate and commit"
```

Three things follow, and the third is the one that bites:

| Question | Why it decides the plan |
|---|---|
| Which generator | it names the command |
| Is the output committed | committed output means the change is incomplete until regenerated **and committed** — an uncommitted regeneration breaks the build for everyone else |
| Does this change trigger it | adding a field to an annotated class does; changing a method body usually does not |

Measured on one repository: 586 `.freezed.dart` and 338 `.g.dart` files, all committed,
three generators declared. A single added state field there is a two-file change that
looks like a one-file change, and the second file is the one that compiles.

**Hand the command to the developer; do not run it.** Generation rewrites hundreds of
files, and a diff nobody asked for is worse than a missing one:

```
Требуется регенерация: <command>
Затронет:              <path>.freezed.dart — закоммитить вместе с правкой
```

A change to generated source that ships without its regenerated twin does not fail review
— it fails the build, for everybody, after merge.

### 4. Imports

```bash
grep -rh "^import" . --include='<ext>' | sed 's/[^a-z:.].*//' | sort | uniq -c | sort -rn
```

Relative or absolute, and whether internal modules use the package prefix. Mixed counts
mean the project is mid-migration — follow the majority in the directory you are editing,
not the majority overall.

### 5. Error handling

The shape matters more than the choice. Establish from siblings: does the catch report to
monitoring, log, or rethrow? Does it capture the stack? Is failure a state, an exception,
or a nullable return?

A change that throws where everything nearby returns a failure state forces every caller
into a second error path.

### 6. Where things are allowed to live

Which layer may touch the network, which may touch storage, whether a widget may call a
repository directly. Nothing states these; they are visible in what the siblings do not
do.

**Violating a layering rule is the most expensive convention break**, because it is the
one that compiles, passes review, and makes the next change harder.

## Explicit rules beat measured ones — and most of them can be run

```bash
ls .editorconfig analysis_options.yaml .eslintrc* .prettierrc* setup.cfg pyproject.toml
ls .cursorrules AGENTS.md CLAUDE.md 2>/dev/null
cat CONTRIBUTING.md 2>/dev/null | head -40
```

**Then find the command, not just the file.** A linter config is a convention with teeth,
and the project almost always has a script that enforces it:

```bash
grep -E '"(lint|format|analyze|check)' package.json
grep -E 'lint|format' Makefile pyproject.toml 2>/dev/null
```

Measured on one repository: three config files and three scripts — a linter, a formatter,
and a check-only mode. Reading the config tells you the rules; running the check tells you
whether your change obeys them, which is the only version that matters.

Run it in check mode after phase 4, before phase 5 declares anything verified. A change
that fails the project's own formatter is not a style disagreement, it is a broken build
waiting for CI.

## Duplication is the failure this file exists to prevent

**Start with the places the project designated for shared code.** They are usually few
enough to read entirely, and reading an index beats guessing at a name:

```bash
ls src/helpers src/mixins src/utils lib/common 2>/dev/null
ls <the module>/utils* <the module>/helpers* 2>/dev/null
```

Measured on one repository: fourteen files across three shared directories. Listing them
takes a second and answers the question grep only guesses at — grep finds a name you
imagined, the index shows you what is actually there.

Then, for anything not obviously in the index:

```bash
grep -rn '<the operation in words>' <module> | head
grep -rn 'def <likely name>\|function <likely name>\|<likely name>(' <module> | head
```

The second-worst outcome of an enhancement is a helper that already existed forty lines
away. The worst is one that existed and behaved *slightly* differently — now there are two
truths, and the next bug is which one a given call site used.

**Where one exists and does not quite fit:** extend it, or say plainly why it cannot be
extended. Adding a near-twin without that sentence is how a codebase acquires three
date formatters.

## Report what you followed

The plan and the report both name the conventions the change obeys, with the sibling that
established each. This is what lets a reviewer check fit without reading the whole
directory:

```
Соседи:       <files read to establish the shape>
Следую:       <convention → where it is established>
Отступаю:     <any deviation, with the reason — normally empty>
```

A non-empty `Отступаю` needs a sentence per line. Deviating silently is how the next
person concludes there was never a convention.
