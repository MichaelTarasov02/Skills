---
name: setup-author
description: Sets up the personal-post pipeline for a new author — creates the personal-post.yaml profile and a voice guide by interviewing the user about how they write and who they write for. Use this when someone installs personal-post and wants to configure it, when the new-post skill reports no author profile was found, when a colleague wants to use this pipeline with their own voice, or when the user asks to change their voice guide, output paths, themes, or risk rules.
argument-hint: [path to your content repo]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Setup Author

Create the two files that make this pipeline belong to one person: `personal-post.yaml` and the voice guide it points at. Everything else in the plugin is author-neutral, which is why a colleague can install it and be productive without reading a single prompt.

## Why interview rather than template

A voice guide filled with plausible defaults produces posts that sound like nobody. The value here is in the specifics — how this person actually argues, what they refuse to claim, which words make them wince. Those cannot be guessed.

Keep it conversational. Fifteen minutes of good answers beats an hour of form-filling.

## If a voice guide already exists

Ask first: has this person already written about their voice, or do they have posts they consider representative? If so, read those instead of asking them to describe themselves in the abstract — people are far better at recognizing their voice than describing it.

Extract from three to five of their strongest posts: sentence rhythm, opening habits, how they close, what proof they reach for, what they never say. Show them what you extracted and ask what is wrong. Correcting a draft is much easier than authoring from blank.

## The interview

Ask in small groups, not as a wall of questions.

**Who they are**
- What do you build, and what do you want to be known for?
- Who is the one reader you are writing for? Push past "founders" toward the specific person who can act on your posts.
- What can you claim that most people in your field cannot?

**How they sound**
- Show me two posts you were happy with, and one that felt off. What was off about it?
- What phrases make you cringe when you see them in your feed?
- Do you write in first person about your own work, or observe from outside?

**What they will not do**
- Any client, employer, or project you cannot name?
- Metrics you are allowed to cite, and metrics you are not?
- Compliance, legal, or medical territory to stay out of?
- Do you mention your company, and how directly?

**Mechanics**
- Where should posts be written to?
- Do you want a light and dark visual register, or one look?
- Roughly how long should a caption run?

## What to write

**`personal-post.yaml`** — copy `${CLAUDE_PLUGIN_ROOT}/skills/new-post/assets/personal-post.example.yaml` and fill it from the answers. Every field commented in that file is real; leave nothing at its placeholder.

**The voice guide** at the path the profile names. Give it these sections:

```
Positioning            who this person is, in one paragraph
Audience               the one reader, plus their emotional state
Voice principles       five to eight, each with a why
Language rules         phrases to use · phrases to avoid
Post archetypes        three to five shapes with their structures
Structure              default length, formatting, opening and closing rules
Discussion strategy    the mechanisms available and how to pick
Human voice            what makes a post feel written by a person
Risk and claims        what needs approval, what is never claimed
QA checklist           what to verify before publishing
```

Write it in whatever language the author thinks in — the guide is a working document, not a deliverable. The posts ship in the language the profile names.

## Verify before declaring done

Do not tell the user it works. Show them:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/verify_spec.py" --help
ls -la personal-post.yaml <voice guide path> <output_dir>
```

Confirm the profile parses, every path in it resolves, and the output directory exists. A profile pointing at a missing voice guide fails on the first real run, which is the worst moment to discover it.

Then offer a dry run: take one small idea and run `new-post` on it. A first post that lands is worth more reassurance than any amount of configuration talk.

## Changing things later

Editing `personal-post.yaml` is the supported path for output location, themes, caption bands, watchlist, and risk rules. Editing the voice guide is the supported path for how posts sound.

Neither requires touching the skill. Say so explicitly — people assume customizing a tool means forking it, and then they never take updates.
