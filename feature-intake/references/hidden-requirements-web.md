# Hidden requirements — web

Run this checklist in phase 3. Each item is answered, marked not applicable, or becomes a
question or an assumption. The web app here is Vue 3 + ant-design-vue.

## Always asked, rarely written

| Item | The question it hides |
|---|---|
| Permissions | who may see this, who may act; what a user without the right sees instead |
| Empty result | what the screen shows when the query returns nothing |
| Limits | maximum rows, maximum length, maximum file size; what happens at the boundary |
| Pagination | is the result set bounded; what happens at ten thousand rows |
| Sorting and filtering | which columns; does the filter survive a reload |
| Data migration | do existing records need backfilling for this to work |
| Backward compatibility | do older clients still work against the changed API |

## Browser-specific, forgotten most often

| Item | The question it hides |
|---|---|
| Page reload | what survives F5 mid-flow — filters, form input, wizard step |
| Deep link | can this state be linked to and shared; should it be |
| Browser back | what back does mid-form, and what happens to unsaved input |
| New tab | does the feature survive two tabs open on the same record |
| Session expiry | what happens when the token dies mid-action; is input preserved |
| Concurrent edit | two people on one record — last write wins, or something better |
| Export | if the screen shows data, someone will ask to export it |
| Print | reports get printed; `print-js` is already a dependency here |

## Only relevant sometimes

| Item | When it matters |
|---|---|
| Bundle size | the feature pulls in a heavy library |
| SEO | the page is public |
| Timezone | the feature involves times — and this product is full of them |

## Timezone deserves its own line

Any feature touching shifts, breaks or payroll carries a timezone question: is the value
stored in UTC, displayed in the associate's zone, the company's zone, or the viewer's?
The web app already converts through utilities named `convertDateTimeToCurrentTimeZone`,
which means the answer exists in code and is a **fact to look up**, not a question to ask.
