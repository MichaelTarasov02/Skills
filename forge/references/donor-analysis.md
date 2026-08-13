# Donor analysis — how to strip a skill for parts

Read before phase A2. Two people following this on the same donor should reach
comparable conclusions; that comparability is the point.

## Reading order — fixed

1. **Frontmatter.** `description` states which job the donor answers. That job is
   usually not ours. Establish this before the body seduces you.
2. **Body.** The procedure. What the donor actually does, in order.
3. **`references/`.** Where the reusable substance normally lives — rules, templates,
   lookup tables. Richest source per token.
4. **`evals/`, `HISTORY.md`.** Present only in well-built donors. Evals reveal what the
   author considered a correct answer; history reveals what they already tried and
   abandoned.

Skipping straight to the body is the common failure: you inherit a procedure without
noticing it solves a different problem.

## Three verdicts — every fragment gets exactly one

| Verdict | When | Record |
|---|---|---|
| `take as is` | the rule is universal and carries no foreign assumption | quote plus where it landed |
| `rewrite for us` | the idea holds but is bound to another stack, process, or output format | what it was → what it became → why |
| `drop` | different job, already covered, or a no-op | the reason, one line |

A fragment with no verdict has not been analysed. "Read it, took nothing" without a
reason is not a verdict.

## The namesake test

A donor can carry our title and answer someone else's question. Four signals:

1. Its output artifact is not the artifact we need.
2. Its trigger moment sits elsewhere in the lifecycle.
3. Its audience is someone else — a product manager, a designer, an end user.
4. Its "When NOT to Use" points at skills from an unfamiliar lineage, meaning it lives
   inside another process.

One signal is a warning. Two make `rewrite for us` the default, and `take as is` a claim
you now have to defend.

## Foreign assumptions — check before lifting

Before moving any fragment, look for these baked in:

- a specific framework or library
- a specific delivery process, ceremony, or document
- a fixed output format that is not ours
- an interface language other than English
- an executor role that is not a developer

Found one: parameterise it or drop the fragment. Carrying it silently is how a skill
starts giving advice about a stack we do not use.

## Recording

Write to `provenance.md` at the moment of the decision. Deferred recording becomes
recollection, and recollection loses the reasons — which are the only part that helps
when the donor updates.
