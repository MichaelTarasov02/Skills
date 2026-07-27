---
name: post-ideas
description: Researches and builds a bank of post topics with fresh, verifiable sources and a contrarian angle for each. Use this when the user wants content ideas, a topic bank, something to write about, help finding fresh angles, or asks what they should post about next. Also use when they want to refresh an existing idea list or check whether a topic has already been covered.
argument-hint: [number of topics] [category focus]
allowed-tools: Read, Write, WebSearch, WebFetch, Bash, Glob, Grep
---

# Post Ideas

Build a topic bank where every entry has a real source and an angle worth arguing. The output feeds `new-post` directly.

## The rule that decides whether this is useful

**A short verified list beats a long fabricated one.**

Under a quota, the failure mode is inventing plausible sources — a real-looking URL, a confident date, a statistic that never existed. This is worse than delivering fewer topics, because it puts the author's credibility behind something that will not survive a reader clicking the link.

So:

- Never cite a URL you did not actually retrieve and read in this session.
- Never state a date you did not see on the retrieved page.
- Never invent engagement numbers. You have no access to feed analytics. Label any popularity signal as a proxy and name where it came from.
- If a source will not verify, drop the topic and say why.

Delivering seven verified topics against a target of ten is success. Delivering ten with two invented links is failure.

## Build the stop-list first

Read the author's existing posts and any current topic bank. List the theses already used.

**Deduplicate by thesis, not by wording.** "Context engineering beats prompting" and "the prompt is only the visible layer" are one topic. Also drop anything so widely repeated it has no tension left — if several mainstream sources state it uncritically, there is nothing to argue.

## Research

Per category, gather more candidates than you need. Look for releases and policy changes, fresh research, public disputes and reversals, and new tools used in non-obvious ways. Record what happened, the date, the URL, and why the author's reader would care.

Freshness matters, but an older story that nobody has interpreted well is worth more than a fresh one everybody has covered. Tag anything outside the window and say why it earned its place.

## Every topic needs tension

State what is considered obvious here, and why that is wrong or incomplete. A general observation — "AI is changing hiring" — is not an angle. If a topic has no tension, cut it rather than shipping it.

## Format

```markdown
### {N}. {Thesis headline — an assertion, not a question}
- **Angle:** what is considered obvious, and why it is wrong or incomplete.
- **Why now:** event + date + working link.
- **For whom:** one specific role.
- **Not a duplicate because:** how it differs from <existing post or topic>.
- **Hook draft:** one or two lines that sit above the fold.
```

## Verify before reporting

Count the headings yourself rather than trusting your own summary. Confirm every topic has a date and a link. List any link that failed to resolve. Report how many candidates you gathered, how many you dropped for duplication, and how many for unverifiable sources.

If a check fails, fix the file, not the report.
