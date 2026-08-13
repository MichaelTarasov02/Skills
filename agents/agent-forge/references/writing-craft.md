# Writing craft — how a generated skill must read

`skill-spec.md` keeps a skill from being **malformed**. This file keeps it from being
**ignored**. A skill that parses cleanly and still gets skipped, or gets read and applied
differently on every run, failed here.

The target is a skill that makes the agent take the same **process** every run — not one
that produces the same output.

Vocabulary below is shared with the `writing-for-agents` skill. When it is installed, invoke
it for the full treatment; this file is the generation-time working set.

## The ladder

Three tiers, ranked by how immediately the agent needs the material:

| Tier | What sits there | Loads |
|---|---|---|
| **Step** | an ordered action the skill performs | with `SKILL.md` |
| **In-file reference** | a rule or fact consulted on demand | with `SKILL.md` |
| **Disclosed reference** | a file in `references/`, reached by a pointer | only when the pointer fires |

**Branching test — the whole decision.** Inline what *every* path through the skill needs.
Disclose what only *some* paths reach.

Push too little down and the top bloats. Push too much and the agent cannot find what it
actually needs. In-file reference that belonged in `references/` buries the steps beside it,
and attending to those steps becomes a coin-flip.

**Co-locate** what stays: a rule, its caveat and its example sit under one heading, so
reading one brings its neighbours along. Scattering one meaning across four sections costs
more than length ever does.

## Pointers

A **pointer** is the line that sends the agent to material held outside its context. Its
*wording*, not the file behind it, decides whether that material is ever reached.

A pointer does two jobs: name what the material is, and name the branch that triggers it.

| Weak | Strong |
|---|---|
| "Details in `references/`." | "Read `references/voice.md` at Phase 2, before writing any caption." |
| "See the spec for schemas." | "Hit a schema question → `references/schema.md`." |
| "Consult the style guide." | "Every generated headline gets checked against `references/style.md`." |

Put the pointer **at the step that needs it**, never only in a list at the top. A pointer far
from its moment fires late or not at all.

A must-have file behind a vague pointer is a variance bug. Sharpen the wording first; inline
the material only if sharpening fails.

**The `description` is a pointer too** — the skill's top-level one, and the only thing that
decides whether the skill ever fires. It is loaded in every session whether or not the skill
is used, so it earns harder pruning than anything else you write. The rules for it live in
`skill-spec.md` §"Writing a description that actually triggers".

## Completion criteria

Every step ends on the condition that tells the agent the work is done. Two properties make
it the strongest predictability lever in the file:

- **Checkable** — the agent can tell done from not-done. A fuzzy bound ("understanding
  reached", "the code is clean") invites finishing early, with attention already on the steps
  visible ahead.
- **Demanding** — how much the wording forces. "Every modified model accounted for" drives
  real digging; "produce a change list" does not. Demand is not step-bound: "every rule
  applied" binds a flat body of rules the same way.

Write the bound as something observable: a file that exists, a count that matches, a command
that exits clean, a field that is filled.

| Fuzzy | Sharp |
|---|---|
| "Review the output." | "Every claim in the draft traced to a source line." |
| "Make sure it works." | "`npm test` exits 0 — paste the output." |
| "Understand the codebase." | "Every entry point named, with the file it lives in." |

When a step is irreducibly fuzzy *and* the agent rushes it, split the sequence so the later
steps are out of view — but only across a real context boundary. Hiding fails if the later
steps stay in context.

## Leading words

A **leading word** is one compact concept the model already holds, repeated as a token and
never re-explained. It accumulates a distributed definition across the file and anchors a
whole region of behaviour in the fewest possible tokens.

It anchors twice: in the body, the agent reaches for the same behaviour every time the word
appears; in the `description`, shared language between the user's prompts and the skill makes
it fire more reliably.

Hunt for spelled-out triads and collapse them:

- "fast, deterministic, low-overhead" → *tight*
- "a loop you actually believe in" → *red* (a fuzzy gate becomes a binary observable state)

Prefer a word the model already carries over one you coin — a made-up word recruits no priors
and costs definition tokens to install. The project's own domain words are the best
candidates: they already live in the user's prompts.

A word too weak to beat the default is dead weight. "Be thorough" when the agent is already
thorough-ish changes nothing; the fix is a stronger word, not a different technique.

## Positive phrasing

Steer by naming the target behaviour. A prohibition drags the forbidden behaviour into
context and makes it *more* available, not less — *don't think of an elephant*, and the
elephant is all there is. The negation is a weak modifier that the strongly-activated concept
overruns, so half the time the ban reads as an instruction.

| Instead of | Write |
|---|---|
| "Don't write long comments." | "Write one-line comments." |
| "Never skip validation." | "Validate before every write." |
| "Don't invent file paths." | "Confirm each path on disk before naming it." |

A prohibition earns its place only as a hard guardrail with no positive phrasing available —
and even then it ships paired with the target behaviour, so attention lands on what to do.

## Pruning

Run all four over every generated file before it ships.

1. **Single source of truth.** One meaning, one place. A rule living in both `SKILL.md` and a
   reference will drift, and the duplicate inflates its own rank on the ladder past what it
   deserves. Pick the home, delete the other copy.
2. **The environment is a source of truth too.** `package.json` scripts, the directory
   layout, `--help` output — a line restating a cheap lookup is a copy that goes stale
   silently. Capture instead what no file confesses: the unwritten convention, the reason
   behind a choice, the gotcha no config admits.
3. **No-op test, sentence by sentence.** Does this line change behaviour versus the model's
   default? If not, delete the whole sentence rather than trimming words from it. This is
   where most of the weight goes — be aggressive.
4. **Relevance.** Does the line still bear on what the skill does? Mere exposition, and
   branches that should have been disclosed, both fail here.

Shorter skills are easier to keep true. Adding feels safe and removing feels risky, which is
exactly why skills silt up with stale layers until someone has to core down through them.

## Sprawl

A file can be too long even when every line is live and unique. Attention thins across the
excess and every extra line is one more to keep accurate.

The cure is the ladder, not compression: disclose reference behind pointers, and split by
branch or by sequence so each path carries only what it needs.
