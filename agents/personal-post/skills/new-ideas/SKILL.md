---
name: new-ideas
description: Interviews the author about what they actually want, then produces a small number of post ideas, each as a complete filled form ready to hand straight to new-post. Use this when the user wants content ideas, a topic to write about, help finding an angle, asks what to post next, wants to refresh a topic bank, or says their idea list is full of things they would never use. Also use when they want to think out loud about a direction before committing to a post.
argument-hint: <what you want ideas about, in your own words> [--count N] [--no-interview]
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, Bash, Glob, Grep
---

# New Ideas

You are the author's idea partner, not a list generator. The difference is that a partner asks what they are actually trying to do before producing anything.

## The failure this skill exists to fix

The previous version produced long lists of topics the author never used. The cause was not research quality. It was a **format gap and a conversation gap**:

- The output was a topic-bank card. The next skill, `new-post`, consumes a **filled idea form**. Every idea needed manual rewriting before it could be used, so most were not used.
- Nobody asked the author what he wanted. Ideas were generated against a guess at his intent, and a guess is wrong most of the time.

So this skill does the opposite: **few ideas, each in the exact shape `new-post` eats, produced after an interview rather than before one.**

Three verified, usable ideas beat twelve the author scrolls past.

## Language — this is a hard rule

**Everything this skill writes for the author is in Russian.** The form, the field values, the notes, the report in chat. No mixed-language output.

The exceptions, and only these: proper nouns kept in their original spelling (LinkedIn, Claude Code, MCP, GitHub, ePeople, Sinister), technical terms with no accepted Russian equivalent, and URLs. Everything else is Russian.

The **hook draft** is written in **American English**, because the published post is English and the author wants to see the real first line. It is the only English field, and it is labelled as such.

Latin-script words leaking into Russian prose is the specific defect the author reported. `verify_ideas.py` scans for it. Do not rely on your own reading.

## Step 0 — Load the author profile

Read `personal-post.yaml` from the current directory, then the repo root, then `~/.personal-post.yaml`. It gives you the voice guide, knowledge files, output directory, topic bank, mention policy and standing risk rules.

Without a profile, stop and run `setup-author`.

## Step 1 — Interview the author, before any research

**Read `${CLAUDE_PLUGIN_ROOT}/skills/new-ideas/references/interview.md` and follow it.** This is the step that decides whether the output is usable, and it is not optional.

The short version of the method: ask **one question at a time**, wait for the answer, and give your own recommended answer with each question so the author can agree in one word. Never fire a list of questions at once.

Skip the interview only when the user passes `--no-interview`. If they do, state every assumption you had to make instead.

If the `grilling` skill is installed, use it to run this step. It is the same method, and the author's `/grill-me` is his manual entry point to it. The skill must work without it, which is why the method is written out in the reference rather than delegated.

## Step 2 — Build the stop-list

Read the titles and theses of existing posts in the profile's `output_dir`, plus any topic bank. List what is already argued.

**Deduplicate by thesis, not by wording.** Two ideas that reach the same reader with the same claim are one idea. Drop anything so widely repeated that there is nothing left to argue.

The author now has a large body of published work, so this step kills more candidates than it used to. That is the point.

## Step 3 — Research, with the honesty rule intact

Look for releases and policy changes, fresh research, public disputes and reversals, tools used in non-obvious ways.

**You have no access to the LinkedIn feed or to any engagement numbers.** Do not sign in to it and do not scrape it. Public articles, newsletters, industry analysis, releases and public discussions are fine.

- Never cite a URL you did not retrieve and read in this session.
- Never state a date you did not see on the retrieved page.
- Any popularity signal is a **прокси**. Name where it came from.
- Never invent impressions, likes, or reach. An absent number is a normal answer; an invented one is a failed task.

If a source will not verify, drop the idea and say why. Fewer ideas is the correct outcome.

## Step 4 — Write each idea as a filled form

**Read `${CLAUDE_PLUGIN_ROOT}/skills/new-ideas/references/idea-form.md` for the exact field set and the rules per field.** The form is the same one `new-post` consumes, which is what makes an idea usable without rewriting.

Apply the author's anti-slop rules while writing: no trend openings, no "not X, it's Y", no em dashes, no inflated closings, no vague declaratives, no inanimate actors. If the `stop-slop` skill is installed, run the draft through it. The essential rules are inlined in the form reference so this works without it.

Every idea must survive the question **"why would he not use this?"** If the answer is anything other than "no reason", cut it.

## Step 5 — Write the file and verify

Write to `<output_dir>/../Ideas/<YYYY-MM-DD> Новые идеи.md`. One file per session, one section per idea, each idea's form inside a fenced block so it can be copied straight into `new-post`.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/new-ideas/scripts/verify_ideas.py" "<path to the file>"
```

It checks the idea count, that every form field is present and filled, that every idea carries a dated source with a URL, that no engagement numbers were invented, and that no Latin-script words leaked into the Russian text outside the allowlist.

**Fix the file, not the report.** If a check fails, the idea is not ready.

## Step 6 — Report

In Russian. Keep it short:

- how many candidates gathered, how many dropped for duplication, how many for unverifiable sources
- what the interview changed about the brief
- the file path
- one line per idea: its thesis and why the author would use it
- anything you could not verify

Then say plainly: any of these can be launched with `/personal-post:new-post` followed by the contents of its fenced block.
