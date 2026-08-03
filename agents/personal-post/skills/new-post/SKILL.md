---
name: new-post
description: Turns one raw idea into a publish-ready personal LinkedIn post — a full specification with copy-ready caption, plus a themed carousel and single-page visual exported to PDF and PNG. Use this whenever the user wants to write, draft, or build a personal LinkedIn post, a founder post, a carousel, a document post, or asks to "turn this idea into a post", pastes a raw idea or an article they want to react to, or mentions their personal brand content pipeline. Also use when they ask to redo or extend an existing post in this system.
argument-hint: <raw idea, or an article URL/text> [--theme light|dark|blue] [--text-only]
allowed-tools: Read, Write, Edit, Bash, WebFetch, Glob, Grep
---

# New Post

You take **one text input** and produce a complete, publishable post package. The user should not have to explain the method, name the stages, or paste a workflow. They give you an idea; you run the whole chain.

The value of this skill is not that it writes — any model writes. It is that **run N+1 comes out at the same standard as run N**. Three things buy that: a fixed stage order, bundled verification scripts instead of eyeballing, and a defect playbook that carries forward what previous runs learned the hard way.

## Input

Everything after the command is the idea. Nothing else is required.

```
/personal-post:new-post Junior developers aren't disappearing. Their learning ladder is.
/personal-post:new-post --theme dark <paste of a long dictated idea>
/personal-post:new-post https://example.com/article  ← reacts to someone else's piece
/personal-post:new-post --text-only <idea>           ← skip the visual
```

Flags are optional and rarely needed. Infer everything else and record what you inferred.

## Step 0 — Load the author profile

Read `personal-post.yaml`, looking in this order: the current directory, then the repo root, then `~/.personal-post.yaml`. A repo still holding the pre-rename `founder-post.yaml` is valid — read it, and say once in your report that renaming it to `personal-post.yaml` is the supported name now.

**If no profile exists, stop and run the `setup-author` skill instead.** Everything downstream — voice, output paths, theme routing, risk rules — comes from that file. Without it you would be writing in a stranger's voice into an unknown directory, which is worse than not writing.

The profile gives you: author name and byline, voice guide path, knowledge files, output directory, theme names and routing rules, mention policy, and standing risk constraints. Treat every path in it as relative to the profile's own location.

## Step 1 — Resolve the content type, before anything else

The type decides the entire visual identity — palette, typography, components, density, texture. Getting it wrong is a defect that survives all the way to the exported PDF, so settle it first and write it down. **Read `${CLAUDE_PLUGIN_ROOT}/skills/new-post/references/content-types/index.md` before deciding** — it holds the full routing procedure and the passports for each type.

1. Scan the **user's input** for a type choice: the `--theme` flag (`light` | `dark` | `blue`), a `Theme:` line, or a phrase like "in the dark theme" / "светлая тема" / "синяя тема". Only the user's own words count — option tables in documentation are not a selection.
2. Any concrete value is a **forced override**. Honor it exactly, never re-route. The profile's `themes:` block maps `light`/`dark`/`blue` onto the CSS type names.
3. Absent or `auto` → route by purpose using the profile's `theme_routing` and the orchestrator's table.
4. When a topic straddles two routes, **route on the reader's job**, not the subject matter. Who acts on this post, and what are they doing when they act? This is the single most common routing mistake.
5. Only when steps 3–4 leave a **genuine coin flip**: pick the least-used type by counting existing visual posts per type (text-only posts do not count). The counter never overrides an answer that meaning already produced.

Log it before Stage 1: `theme = <name> · source = forced | auto (<step and reason>)`. Thread that value through unchanged. Stage 3 must not re-decide it.

## Step 2 — Detect the route

- Input tagged `Raw idea:` or `Article:` → obey the tag.
- A URL, a named author or publication, quoted external claims, "this article says…" → **article route**.
- The user's own first-person thinking, experience, or argument → **raw idea route**.

Ask a routing question only when it is a genuine coin flip *and* the answer changes the output materially. Otherwise pick the better-supported route and record why.

## Step 3 — Check for collisions before writing

Read the titles of existing posts in the profile's output directory, plus any topic bank it points at. If the new idea repeats the **thesis** of an existing post, say so and stop for a decision.

Judge by thesis, not by wording. "Context engineering beats prompting" and "the prompt is only the visible layer" are one post. Two posts arguing the same thing to the same reader is the most expensive failure this pipeline can produce, because it costs the author credibility rather than time — and it is invisible unless someone checks.

When the overlap is partial, name the neighbouring post and state how the angle differs. That differentiation belongs in the spec.

## The three stages

Run them in order, in one pass. After each, write a short note and continue automatically — do not wait for approval between stages.

Each stage has its own reference file. Read it when the stage begins, follow it completely, and do not paraphrase its rules back into chat.

| Stage | What it does | Reference |
|---|---|---|
| 1 | idea or article → a filled brief held in context | `references/stage-1-intake.md` |
| 2 | brief → `Post Specification.md` with the copy-ready caption | `references/stage-2-spec.md` |
| 3 | spec → carousel + single page, exported | `references/content-types/<type>.md` + `references/components.md` + `references/stage-3-visual.md` |

Stage 3 is conditional. If the spec's `Visual decision` is `none`, the post is text-first — skip production and say why. That is a complete, valid outcome, not a shortfall.

**Read each knowledge and voice file at most once per run** and reuse it across stages. Re-reading the same voice guide in three stages burns the budget that should go into the writing.

## Output — exactly one folder

```
<output_dir>/<Post Name>/
├── Post Specification.md        ← strategy, structure, risk notes
├── Post Copy.md                 ← what gets pasted into LinkedIn, both versions
└── Visual/                      ← only when the spec calls for a visual
    ├── system.css                ← copy of the plugin's visual-system.css
    ├── styles.css               ← this post's one bespoke object
    ├── carousel.html
    ├── single-page.html
    ├── README.md                ← theme, depth, archetypes, what to upload
    └── exports/
        ├── carousel.pdf         ← this is what gets uploaded
        ├── page-01.png
        └── slide-NN.png
```

`Post Copy.md` carries **two** captions, because the author decides at publishing time which format to post:

- **Carousel version** — the full caption. The deck spreads the argument across slides, so the caption has room to set up the tension and point at the deck.
- **Single-page version** — short. The one artboard already carries the hook, the object, the beats and the question, so a long caption repeats what the reader can see. Roughly half the length.

**That file is the source of truth for both.** The specification's `## Copy-Ready LinkedIn Post` section points at it and does not restate either caption. This is deliberate: two copies of the same text drift, and the drift is invisible until the wrong one gets published.

No brief snapshot, no registry entry, no third copy anywhere.

## Verification — run the scripts, do not eyeball

Gates passing is not QA. The bundled scripts exist because earlier runs kept re-deriving the same checks by hand and kept missing the same defects.

```bash
# after Stage 2
python3 "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/verify_spec.py" "<post folder>"

# after Stage 3, from inside Visual/ — scripts run from the plugin, not copies
node "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/export.mjs"
node "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/verify_visual.mjs"
```

`verify_spec.py` checks section completeness, caption length against the profile's bands, the risky-word watchlist, banned constructions, and invented engagement numbers.

`verify_visual.mjs` measures every artboard for frame overflow, fill ratio, word budget, theme match against the spec, and separators left dangling past the last node.

Then **open the rendered PNGs and look at them.** The scripts catch geometry; they cannot see that a component is stretched hollow or that a slide reads as a small block in a void. Fix and re-export until both the scripts and your eyes pass. Never deliver on "should be fine".

## Close the loop — write the run log

Append one entry to `<output_dir>/../run-log.md` (create it if absent):

```markdown
## <date> · <Post Name>
- theme: <name> (<forced|auto>, <reason>)
- route: <raw|article> · archetypes: <list> · depth: B=<n> → <n> slides
- defects hit: <what broke and the fix>
- new rule: <only if this run taught something not already in the playbook>
```

This is the mechanism that makes the system improve rather than merely repeat. Before Stage 3, skim the last few entries — if a defect appears twice, it belongs in `references/layout-playbook.md` as a rule, not in the log as an anecdote. Promote it there and the next run starts ahead of where this one did.

## Final report

Keep it compact. Stage notes, paths, QA verdict, real risks, one next action. Do not restate the thesis, reader, caption, or visual decision — they are in the file, and repeating them in chat is how a 200-word report becomes 2,000.

Report failures plainly. If a check failed and you fixed it, say what broke. If something still needs a human eye, name it. A report that hides a defect is worth less than no report.
