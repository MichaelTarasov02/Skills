# Element markup — Vue 3 + ant-design-vue

Worked markup for all twelve cases. Read before marking up a web element.

## M1 — semantic element and role

```vue
<!-- wrong: a div pretending -->
<div class="btn" @click="exportList">Export</div>

<!-- right -->
<button type="button" @click="exportList">Export</button>
```

`type="button"` matters: inside a `<form>`, a button without it submits.

With ant-design-vue, `<a-button>` renders a real `<button>` — no `role` needed. Adding
`role="button"` to it is the duplication this rule exists to stop.

## M2 — accessible name for an icon-only control

```vue
<a-button type="text" aria-label="Export associate list" @click="exportList">
  <template #icon><DownloadOutlined aria-hidden="true" /></template>
</a-button>
```

Two halves: the name says the action, and the icon is hidden so it does not add noise.
`aria-label="Download icon"` names the picture instead of the outcome and is wrong.

When a visible label exists, do not replace it with `aria-label` — voice-control users
say what they see:

```vue
<button id="exp">Export</button>
<span aria-labelledby="exp"><!-- nothing extra needed --></span>
```

## M3 — images

```vue
<img :src="associate.photo" :alt="`Photo of ${associate.name}`" />   <!-- informative -->
<img src="/divider.svg" alt="" />                                     <!-- decorative -->
```

Empty `alt` is a decision, not an omission — it tells the screen reader to skip. Missing
`alt` makes it read the file name. Never `alt="image"`.

## M4 — focus order

DOM order is focus order. Reordering visually with CSS `order` or `flex-direction:
row-reverse` desynchronises them, and a keyboard user tabs through a sequence that does
not match what they see. Fix the DOM, not with `tabindex` values above zero.

`tabindex="0"` puts a custom control in the natural order. `tabindex="-1"` makes it
programmatically focusable but skipped. Anything positive is a bug.

## M5 — dialog focus

```vue
<a-modal
  v-model:open="open"
  :title="null"
  aria-labelledby="dlg-title"
  :keyboard="true"
  :mask-closable="false"
  @after-close="restoreFocus"
>
  <h2 id="dlg-title">Delete this document?</h2>
  <template #footer>
    <a-button ref="cancelRef" @click="open = false">Cancel</a-button>
    <a-button danger @click="confirm">Delete document</a-button>
  </template>
</a-modal>
```

`:keyboard="true"` keeps Escape working — it is on by default and is sometimes disabled
without realising Escape goes with it. `after-close` returns focus to the trigger; without
it, focus falls to the document body and a keyboard user restarts from the top of the
page.

## M6 — visible focus

```css
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
```

Removing `outline` without a replacement is the single most common keyboard failure in a
styled app. `:focus-visible` keeps the ring for keyboard users while sparing mouse users
the ring on click — the reason `outline: none` gets written in the first place.

## M7 — live regions

```vue
<div aria-live="polite" aria-atomic="true">
  {{ resultCount }} associates found
</div>
<div role="alert">{{ loadError }}</div>
```

`polite` waits for a pause; `assertive` (and `role="alert"`) interrupts. Filter results are
polite. A failed load is an alert. Marking everything assertive makes the interface shout.

The region must exist in the DOM **before** the text arrives — inserting an already-filled
live region announces nothing.

## M8–M10 — analytics

See `references/analytics.md`. Note for this platform: the Vue app carries no product
analytics SDK, only Sentry. The analytics layer is not applicable here until one exists —
say so rather than inventing an event.

## M11 — test id

```vue
<button data-testid="export-associates">Export</button>
```

Only when role and name are not enough. A button labelled `Export` is already reachable
by `getByRole('button', { name: 'Export' })`; the id adds a second identity that lets the
first one rot.

Legitimate uses: a row in `a-table` (`:data-testid="'row-' + record.associate_number'"`),
a container with no name, a canvas.

## M12 — custom control keyboard contract

For anything without a native equivalent, implement the full APG pattern. A combobox:

| Key | Behaviour |
|---|---|
| `Down` | open the list, move to the first or next option |
| `Up` | move to the previous option |
| `Enter` | select the focused option, close |
| `Escape` | close without selecting, restore the previous value |
| `Home` / `End` | first / last option |
| printable character | jump to the first option starting with it |

```vue
<a-select
  show-search
  aria-label="Filter by company"
  :options="companies"
/>
```

`a-select` implements this already. Before hand-rolling a control, check whether the kit
has it — a hand-rolled combobox that gets four of the seven keys right is worse than the
kit's.
