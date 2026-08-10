# PII patterns

Read before phase 7. **Every pattern is run and its output pasted — including empty
output.** An unrun search is not a clean result.

**Provenance:** `shiplightai/agent-skills@privacy-review` (418 installs) was recommended
and is **not installed** — installation needs the user's explicit consent. This checklist
was written from the OWASP Logging Cheat Sheet and the GDPR articles that touch code
(erasure and portability). If that skill is installed later, keep one source, not two.

## Why this product raises the stakes

This system records **where and when people work**, plus signed documents, meal-break
compliance and payroll. A log line here is not a debugging artifact — it is a record of
someone's movements and working conditions, sitting in a system with a different access
model from the application database.

## Never in a log

| Category | Examples in this product |
|---|---|
| Contact details | email, phone number, postal address |
| Government identifiers | SSN, document numbers |
| Credentials | passwords, tokens, session ids, **FCM push tokens** |
| Location | latitude, longitude, geocoded addresses |
| Document contents | signature data, uploaded files |
| Compliance detail | who missed a meal break, disciplinary records |

An id that only resolves inside the application database is acceptable. A value that
identifies a person on its own is not.

## Searches

Run all of them. Adjust paths per platform.

```bash
# Flutter — logging density first
grep -rc "log(\|debugPrint(\|print(" lib

# Flutter — sensitive values inside a log call
grep -rnE "(print|debugPrint|log)\(.*(phone|email|ssn|password|token|address|latitude|longitude|location)" lib

# Python — logging density
grep -rc "print(\|logger\.\|logging\." bb core api

# Python — sensitive values in an f-string being logged
grep -rnE "(print|logger\.[a-z]+|logging\.[a-z]+)\(.*(phone|email|ssn|password|token|address|latitude|longitude)" bb core api

# Vue — anything reaching the browser console
grep -rn "console\." src

# Crash and analytics context — what is attached to every report
grep -rnE "setUser|setExtra|setTag|setContext|setUserId" .
```

The f-string form is where most leaks live: `logger.debug(f"...{email}...")` reads as a
message, not as data handling, so it survives review.

## Crash reporting and analytics carry PII too

Sentry and Firebase Crashlytics attach context to every event. `setUser` with an email,
or an extra carrying a phone number, exports that field to a third party on every crash —
a wider disclosure than any log line, and one nobody reviews after it is written once.

Check what is attached globally, not only what a given screen logs.

## Deletion and export

For every new field the feature stores, answer both:

| Question | Why |
|---|---|
| What happens to it when the account is deleted? | erasure; a field nobody wired into deletion outlives the account silently |
| Does it belong in the data export? | portability; a field missing from export is as much a defect as one wrongly included |

Local device storage counts. Data cached on a phone after logout is still retained data.

## Reporting a finding

```
FILE:LINE — what leaks — which category — the edit
lib/main.dart:324 — full FCM token in a log — credential — log only whether a token was
                     received, never its value
```

Flag anything doubtful rather than deciding it. The decision is legal; the finding is not.
