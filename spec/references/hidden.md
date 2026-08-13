# Hidden requirements

Run in phase 3, **once per platform the change touches** — the sections below are separate
checklists, not one list with variations. A feature that ships on two platforms runs two.

Each item is answered, marked not applicable, or becomes a question or an assumption.

**Read the platform's major from `.dev-agent/config.yaml` before using the platform
sections.** They name framework behaviour, and behaviour differs by major. This file never
names a version, because a version written here is wrong on the next repository and wrong
in the way that looks plausible.

---

## Any platform

| Item | The question it hides |
|---|---|
| Permissions | who may see this, who may act; what a user without the right sees instead |
| Empty result | what the screen shows when the query returns nothing |
| Error and no-access | the two states that share a screen with empty and are never designed with it |
| Limits | maximum rows, length, file size; what happens **at** the boundary, not past it |
| Data migration | do existing records need backfilling for this to work |
| Backward compatibility | do older clients still work against the changed API |
| Concurrent change | two people on one record — last write wins, or something better |

---

## Web

| Item | The question it hides |
|---|---|
| Pagination | is the result set bounded; what happens at ten thousand rows |
| Sorting and filtering | which columns; does the filter survive a reload |
| Page reload | what survives a refresh mid-flow — filters, form input, wizard step |
| Deep link | can this state be linked to and shared; should it be |
| Browser back | what back does mid-form, and what happens to unsaved input |
| New tab | does the feature survive two tabs open on the same record |
| Session expiry | what happens when the token dies mid-action; is input preserved |
| Export | if the screen shows data, someone will ask to export it |
| Print | reports get printed — check whether a print library is already a dependency |
| Bundle size | only when the feature pulls in a heavy library |
| SEO | only when the page is public |

---

## Mobile

| Item | The question it hides |
|---|---|
| OS permissions | which the feature needs, and what it does when the user says no |
| Permission denied permanently | the OS stops asking; the app must route to settings |
| Offline | what works with no connection; what queues; what is refused outright |
| Sync conflict | the device acted offline and the server disagrees — who wins |
| Background | what happens when the app is backgrounded mid-action |
| Killed by the OS | state restoration, and what an interrupted flow resumes to |
| Push | does this feature need a notification; who receives it; what if the token is stale |
| Deep link | does a notification open this screen directly, and from a cold start |
| App version floor | does this require a server change that breaks older installs |
| Store review | anything touching payment, location or health has review implications |
| App size | new assets and packages ship to every user |
| On-device storage | local schema changes when the app updates; what is retained and for how long |

---

## Localisation, where the product is localised

Read the locale set from `config.yaml` before answering. **Every new user-facing string
multiplies by the number of locales**, and the number is part of the feature's cost — say
it.

Two questions the count alone does not raise:

- **Is any locale right-to-left?** If so, every new layout mirrors, and tight horizontal
  arrangements are the ones that break.
- **Do the longer languages fit?** A label sized to the default language truncates in the
  languages that need more words for the same idea.

Where a platform is localised and the other is not, that asymmetry is in `config.yaml` and
it means the same feature has different costs on each. Say both.

---

## Time and location, where the product records either

| Item | The question it hides |
|---|---|
| Timezone | stored in what, shown in whose zone — the subject's, the organisation's, or the viewer's |
| Device clock | what happens when the device time is wrong or manually changed |
| Location permission | foreground versus background, and what the feature does with only foreground |
| Location unavailable | indoors, denied, or hardware off — is the action blocked, or recorded without it |

**These are facts, not questions.** The storage answers are in the backend models and the
display answers are in whatever conversion utility the client already uses:

```bash
grep -rn "utc\|timezone\|tzinfo\|DateTimeField" <backend> | grep -v migrations | head
grep -rniE "converttime|totimezone|timezone" <client roots> | head
```

Asking a person what the product already decided, and wrote down in code, spends the one
thing this skill has a budget of.
