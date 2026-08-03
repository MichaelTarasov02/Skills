# personal-post

Turn one raw idea into a publish-ready personal LinkedIn post: a full specification with a copy-ready caption, plus a themed carousel and single-page visual exported to PDF and PNG.

You give it an idea. It gives you a folder you can publish from.

```
/personal-post:new-post Junior developers aren't disappearing. Their learning ladder is.
```

## What you get

```
Posts/The Junior Learning Ladder/
├── Post Specification.md      ← strategy, structure, risk notes
├── Post Copy.md               ← both captions, ready to paste
└── Visual/
    └── exports/
        ├── carousel.pdf       ← upload this as a document post
        ├── page-01.png        ← single-image alternative
        └── slide-01..08.png   ← for review
```

## Install

```bash
git clone <this repo> ~/personal-post
cd ~/personal-post && npm install && npx playwright install chromium

claude plugin marketplace add ~/personal-post
claude plugin install personal-post@personal-post
```

**Then restart Claude Code.** Plugins are loaded once at session start, so a
newly installed plugin is invisible to the session you installed it from.

For a one-off trial without installing:

```bash
claude --plugin-dir ~/personal-post
```

## Editing the plugin

Installing **copies** the plugin into `~/.claude/plugins/cache/`, pinned to a git
commit. Editing your working copy does nothing until you publish the change:

```bash
cd ~/personal-post
git add -A && git commit -m "…"
claude plugin marketplace update personal-post
```

Then restart. This trips people up: the edit looks applied because the file on
disk changed, but the running plugin is the cached copy.

While iterating on the prompts themselves, `claude --plugin-dir ~/personal-post`
loads straight from the directory and skips the commit-and-update cycle.

## First run

```
/personal-post:setup-author
```

This interviews you for about fifteen minutes and writes two files into your content repo: `personal-post.yaml` (paths, themes, caption length, risk rules) and a voice guide. If you already have posts you like, point it at them — it will extract your voice from the writing rather than asking you to describe it, which is easier and more accurate.

Then:

```
/personal-post:new-post <your idea>
```

## The four skills

| Skill | What it does |
|---|---|
| `new-post` | The pipeline. Idea → spec → carousel → export. |
| `setup-author` | Creates your profile and voice guide. Run once. |
| `review-post` | QA an existing post. Run before publishing. |
| `new-ideas` | Interviews you, then produces a few post ideas, each a complete form ready to hand to `new-post`. |

## Options

Everything after the command is your idea. Flags are rarely needed.

```
/personal-post:new-post --theme dark <idea>        force a register (light | dark | blue | green | cherry)
/personal-post:new-post --text-only <idea>         skip the visual
/personal-post:new-post https://example.com/post   react to someone else's piece
```

## Why runs come out consistent

Three mechanisms, in order of how much they matter:

**Bundled verification scripts.** `verify_spec.py` checks section completeness, caption length, the watchlist, and invented metrics. `verify_visual.mjs` measures every artboard for frame overflow, dangling connectors, theme mismatch, fill ratio, and whether the single page cropped its closing question. These used to be re-derived by hand every run, and every run missed something different.

**A defect playbook.** `skills/new-post/references/layout-playbook.md` records the layout failures this system has actually hit, with the rule each one produced. One of them cost three separate runs before it was written down. Reading it takes a minute and saves a rebuild.

**A run log.** Each run appends its theme decision, archetypes, and any defect it hit. When a defect shows up twice it gets promoted into the playbook — so the system gets better rather than repeating.

## Making it yours

Edit `personal-post.yaml` for output location, themes, caption length, watchlist, and standing risk rules. Edit your voice guide for how posts sound.

Neither requires touching the plugin, which means you keep taking updates. If you do want to change the method itself, the stage instructions are plain Markdown in `skills/new-post/references/` — edit them directly.

## Sharing it

A colleague clones the repo, runs `setup-author`, and is productive. They never need to understand the internals, and their posts come out in their voice, not yours, because everything author-specific lives in their own config file.

## Requirements

- Node with Playwright available for the export step
- Python 3 for the spec checker (PyYAML optional — it degrades gracefully)

## Layout

```
personal-post/
├── .claude-plugin/plugin.json
├── skills/
│   ├── new-post/
│   │   ├── SKILL.md                    orchestration only
│   │   ├── references/                 stage instructions, visual system, playbook
│   │   ├── scripts/                    export + the two verifiers
│   │   └── assets/                     the CSS and the example profile
│   ├── setup-author/SKILL.md
│   ├── review-post/SKILL.md
│   └── new-ideas/SKILL.md
└── README.md
```

The orchestrator holds sequence and gates. The stage files hold method. Editing a stage file changes every future run without touching anything else.
