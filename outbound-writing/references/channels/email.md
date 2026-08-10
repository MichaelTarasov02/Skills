# Transactional email

## Parts

| Part | Budget | Job |
|---|---|---|
| Subject | ~45 chars | what happened, no cleverness |
| Preheader | ~90 chars | the sentence after the subject in the inbox list |
| Body | as short as the facts allow | what happened, what it means, one action |
| CTA | one | the single thing to do |
| Plain-text version | mirrors the body | half of enterprise mail clients block images |

The preheader is the most-wasted field in transactional email: left empty, clients fill it
with whatever markup comes first, usually "View this email in your browser".

## One action

Transactional mail carries one action. A second link competes with the first and lowers
both. If two things genuinely need doing, they are two emails or one email plus a screen
that holds both.

The CTA names the outcome — `Sign the document`, not `Click here` and not `Learn more`.

## Without images

Write so the email works with images blocked. That means: no meaning carried by an image
alone, alt text on every image that carries any, and a plain-text version that is a real
message rather than a stripped shell.

## Identity and trust

A work product's email lands beside payroll and HR mail, where users are alert to
phishing. Say which company and which account it concerns, state why they are receiving
it, and never ask for credentials — legitimate mail sends people to the app, it does not
collect.

## Locales

Seven. An email template with a hard-coded English fragment around a translated body is
the common defect — check the wrapper, not only the message.

Hebrew reverses direction: the template needs `dir="rtl"` support, not only translated
strings.

## Never in an email

Amounts and document contents unless the email exists specifically to deliver them; any
other person's data; and any date by which something will be fixed.
