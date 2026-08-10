# Hidden requirements — mobile

Run this checklist in phase 3, alongside the web one. The mobile app is Flutter, shipping
seven locales.

## Always asked, rarely written

| Item | The question it hides |
|---|---|
| Permissions | who may see and act; and separately, which **OS** permissions the feature needs |
| Offline | what works with no connection; what queues; what is refused outright |
| Sync conflict | the device acted offline and the server disagrees — who wins |
| Empty, error, no access | the same three screens the web needs |
| Limits | list size, upload size, retention on device |
| Data migration | local storage schema changes when the app updates |
| Backward compatibility | older app versions stay in the wild for weeks after release |

## Platform-specific, forgotten most often

| Item | The question it hides |
|---|---|
| OS permission denied | what the feature does when the user says no, and whether it can recover |
| Permission denied permanently | the OS stops asking; the app must route to settings |
| Background | what happens when the app is backgrounded mid-action |
| Killed by the OS | state restoration, and what an interrupted flow resumes to |
| Push | does this feature need a notification; who receives it; what if the token is stale |
| Deep link | does a notification or link open this screen directly, and from a cold start |
| App version floor | does this require a server change that breaks older installs |
| Store review | anything touching payment, location or health has review implications |
| App size | new assets and packages ship to every user |

## Localisation is not optional here

Seven locales, one right-to-left. Every new user-facing string multiplies by seven, and
any layout with tight text breaks in the longer languages and mirrors in Hebrew. Treat a
feature's string count as part of its cost, and say the number.

## Time and location

This product records when and where work happened. Any feature touching either carries
questions that are usually assumed away:

| Item | The question it hides |
|---|---|
| Timezone | stored in UTC, shown in whose zone — associate, company, or device |
| Device clock | what happens when the device time is wrong or manually changed |
| Location permission | foreground versus background, and what the feature does with only foreground |
| Location unavailable | indoors, denied, or hardware off — is the action blocked or recorded without it |

The answers to the storage questions are facts in the backend models. Look them up.
