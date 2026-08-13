# Checking text against the red lines

> **Examples below are shapes, not facts about your codebase.** Measure before you quote
> any of them.

Read before phase 6. The rules live in `.dev-agent/red-lines.md`; this file is how to
apply them without drowning the reader in false positives.

## Keyword matching alone has no precision

Measured on one repository, checking the rule *never assert legal compliance on the
product's behalf*:

```
hits on compliance keywords          89
  product claiming about itself       0   ← the actual violation
  quoting a requirement to the user  69   ← correct, and often legally required
  neither — needs reading            20
```

Eighty-nine flags, zero violations. A check with that precision is ignored after its
first run, and then the one real violation ships with it.

## Polarity is the rule, keywords only find candidates

For every red line, the question is **who is claiming what about whom**:

| Direction | Example shape | Verdict |
|---|---|---|
| Product claims about itself | "we are compliant", "your data is safe with us" | violation |
| Product quotes a requirement to the user | "the law requires you to take a meal break" | correct — often mandatory |
| Product disclaims | "there is no guarantee that…" | correct — it is the opposite of a promise |
| Product commits on someone's behalf | "our team will fix this shortly" | violation |

The same keyword sits on both sides of every row. `guarantee` in "we guarantee" is a
violation; in "there is no guarantee" it is the safeguard. A checker that cannot tell them
apart is a random-number generator with opinions.

## Report three buckets, never one list

```
Violations      — the claim, quoted, with the rule it breaks
Correct         — matched a keyword, checked, fine. Count only, not a list
Needs reading   — polarity unclear. These are the ones a human looks at
```

The middle bucket is reported as a number so the reader knows the check ran wide. The
third is the deliverable: a short list of genuinely ambiguous strings beats a long list
that is 78% noise.

## Time promises are the exception — keywords are enough

This is the one rule where matching works, because there is no benign direction:

```
soon · shortly · in the next release · within N days · by tomorrow · later today
we are working on it · our team is on it · will be fixed
```

Measured on the same repository: 13 hits, all real. The most common shape is a success or
error message that reassures by implying a schedule — *"Our team is on it, so please try
again soon"* commits to a timeline nobody agreed to.

## When `red-lines.md` is missing

Say so loudly and check anyway against the two rules that hold in every product: no dates,
and no claims the product makes about itself. Then flag every sentence that commits to
anything, and say the list is incomplete because the product's own rules were unavailable.
