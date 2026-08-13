# config.yaml schema

> **Everything below is a shape, never a fact.** Values are placeholders written as
> `<...>`. If you find a concrete framework version, key count or locale list in this
> file, it is a bug in this file — measure the repository instead. A reference that hands
> you a number is handing you a hypothesis.

Read before phase 8, the phase that writes. Eight skills read the produced file. Its shape
is a contract, not a preference.

## Rules

- **Framework majors are mandatory, not optional detail.** `framework: vue` is not an
  answer; the major, the kit's major and the dominant API style are. Every skill that
  emits markup reads these three, and getting the major wrong produces code that does not
  compile while looking plausible.
- Every value carries `source:` — one of `code` / `file` / `user` / `assumption`
- Platform sections are per platform. Never average two platforms into one answer
- A field that could not be determined is present with `null` and `source: unknown`,
  not omitted. An absent key is indistinguishable from a forgotten one
- **`id` and `framework` are the first two keys of every platform block, in that order.**
  The grep contract below depends on it

## Shape

```yaml
version: 1
generated: <YYYY-MM-DD>

product:
  name: <name>
  what: { value: "<one line on what it does>", source: <code|file|user|assumption> }
  users: { value: "<who uses it, in the product's own words>", source: <...> }
  type: { value: <B2B|B2C|internal>, source: <...> }
  industry: { value: <industry|null>, source: <...> }

interface:
  language: { value: <default locale code>, source: <...> }
  locales:
    value: [<codes>]
    source: <...>
    note: "<RTL members; store tags that differ from these codes>"

platforms:
  - id: <mobile|web|desktop|…>
    framework: { value: <framework + major, e.g. flutter / vue2 / vue3 / react18>, source: <...> }
    framework_version: { value: "<exact version from the manifest>", source: <...> }
    kit: { value: "<component kit + major, or null>", source: <...> }
    api_style: { value: <the style actually written>, source: <...>, note: "<the counts that decided it>" }
    root: { value: <path from the repository root>, source: <...> }
    strings:
      where: { value: <path glob, or "inline in templates">, source: <...> }
      library: { value: <i18n library or null>, source: <...> }
      key_count: { value: <n|null>, source: <...> }
      plural: { value: <icu|gettext|null>, source: <...> }
    design_system:
      kind: { value: <own|external_kit|none>, source: <...> }
      evidence: { value: "<the paths or package that decided it>", source: <...> }
      dark_theme: { value: <true|false>, source: <...> }
    state_approach:
      value: { primary: <cubit|flags|store|…>, packages: [<…>] }
      source: <...>
    analytics:
      product: { value: <SDK or null>, source: <...> }
      errors: { value: [<crash reporters>], source: <...> }
      plan: { value: <path or null>, source: <...>, note: "<where you looked>" }

backend:
  framework: { value: <framework>, source: <...> }
  root: { value: <path>, source: <...> }

red_lines:
  - { rule: "<a checkable prohibition>", source: <...> }

asymmetries:
  - { note: "<what differs between platforms>", affects: [<skill names>] }
```

`red_lines` and `asymmetries` are **never omitted**. A project with neither carries an
empty list and a note saying it was looked for — an absent key reads as "not checked", and
`copy` treats a missing `red_lines` as a loud gap rather than as permission.

## Grep contract

Consumers retrieve what they need without parsing YAML. **Every platform lookup is
anchored to the platform block**, because a bare field name matches once per platform and
returns them in file order with nothing saying which is which:

```bash
# WRONG — returns every platform's framework with no way to tell them apart,
# and -A1 lands on a different key depending on what the writer put next.
grep -A1 "framework:" .dev-agent/config.yaml

# WRONG — a fixed window silently truncates. A block one line longer than the
# window loses its tail, and the consumer reads the absence as an answer.
grep -A18 "id: web" .dev-agent/config.yaml

# RIGHT — the whole platform block, however long, bounded by the blank line
sed -n '/- id: web$/,/^$/p'    .dev-agent/config.yaml
sed -n '/- id: mobile$/,/^$/p' .dev-agent/config.yaml

# a single field for one platform
sed -n '/- id: web$/,/^$/p' .dev-agent/config.yaml | grep -m1 "framework:"

# whole-project keys have no platform, so a bare grep is correct for them
grep -A5 "^red_lines:" .dev-agent/config.yaml
grep -A5 "^asymmetries:" .dev-agent/config.yaml
grep -A3 "^interface:" .dev-agent/config.yaml
grep -A3 "^backend:" .dev-agent/config.yaml
```

Consequences for the writer: two-space indentation, no tabs, `value` on the same line as
its key in inline maps, `id` first and `framework` second in every platform block, and
**one blank line after every platform block including the last** — the blank line is what
terminates the range, so a missing one merges two platforms into one answer.

**Never publish a fixed-window lookup for a block whose length you do not control.** The
window is a guess about someone else's future edit, and when it is wrong it fails by
returning less rather than by erroring, which is the failure mode nothing catches.

## Verification — phase 8 is not complete until these run

Run every command above against the file you just wrote and paste the output. Two of them
fail in ways that are invisible without running:

| Failure | What it looks like |
|---|---|
| `red_lines` omitted | the grep returns nothing and exits 1 — a consumer reads this as "no red lines", not as "not recorded" |
| a platform block longer than the anchor window | the tail is silently missing from every consumer's view |

A grep that exits non-zero is a finding about the file, not about the grep.

## Changing the schema

A new key touches every reader. Add it here first, then update the consumers, then re-run
the greps. Editing the writer alone is how the contract quietly breaks.
