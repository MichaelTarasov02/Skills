# Markup — Vue with a component kit

> **Examples below are shapes, not facts about your codebase.** Counts, kit names and
> syntax are illustrative. Check `config.yaml` for the framework and kit **majors** before
> writing anything — syntax differs between them, and wrong-major markup does not compile
> while looking plausible.

## Measure the baseline before prescribing anything

A zero `aria-label` count reads as catastrophe and usually is not. Component kits carry
semantics: their button renders a real button, and its text content becomes the accessible
name for free.

What matters is how many controls fall **outside** the kit:

```bash
grep -ro 'aria-label' src | wc -l                             # explicit names
grep -ro '<a-button' src | wc -l                              # kit controls
grep -roE '<a-button[^>]*icon="[^"]+"[^>]*/>' src | wc -l     # icon-only: no text, no name
grep -roE '<a-icon[^>]*@click' src | wc -l                    # icon used as a control
grep -roE '<(div|span)[^>]*@click' src | wc -l                # not a control at all
```

Measured on one repository:

```
aria-label                 0
kit buttons             1645   ← named by their text, nothing to do
icon-only kit buttons     15   ┐
clickable icons            8   ├ 55 elements: the entire real gap
clickable div/span        32   ┘
```

Reporting "zero aria-labels, the app is inaccessible" is alarming and useless. Reporting
55 specific elements is a morning's work with a definite end.

## The three shapes outside the kit

### Clickable div or span — the worst of the three

Contributes no role, is not focusable, and does not respond to Enter or Space. Screen
readers announce nothing; keyboard users cannot reach it.

Replace it with the kit's button and, if the visual is wrong, style the button rather than
un-semanticising a div. Adding `role` and `tabindex` reproduces a third of what the button
gives and needs hand-written key handlers for the rest — and Space is the one everyone
forgets.

### Icon used as a control

Same problem, plus the icon component may swallow events. Wrap in the kit's button with
the icon as its content.

### Icon-only button — has a role, lacks a name

The one case where an explicit name is genuinely required:

```html
<a-button icon="download" aria-label="Export associate list" @click="exportList" />
```

**The name says the action, not the picture.** `aria-label="download icon"` names what the
user sees instead of what happens. Take the object from `lexicon.md`; a name using a
`forbidden` synonym is wrong even when it reads well.

When a visible label exists, do not replace it with `aria-label` — voice-control users say
what they see, and a mismatch makes the control unreachable by voice.

## Dialogs

Check the kit major before writing: the prop that opens a dialog, the event that fires on
close, and whether Escape is enabled by default all differ between kit versions. Read one
existing dialog in the codebase and copy its shape — that is faster and more reliable than
recalling the API.

Whatever the version, three things must hold, and the kit usually gives the first two:

- focus moves into the dialog and is trapped there
- Escape closes it
- **focus returns to whatever opened it** — most often missing, and without it a keyboard
  user restarts from the top of the page

## Announcements

With no live region in the codebase, dynamic changes are silent. The region must exist in
the DOM **before** the text arrives — inserting an already-filled live region announces
nothing.

```html
<div aria-live="polite" aria-atomic="true">{{ resultCount }} associates found</div>
<div role="alert">{{ loadError }}</div>
```

`polite` waits for a pause; `alert` interrupts. Filter results are polite, a failed load
is an alert. Marking everything assertive makes the interface shout.

## Focus visibility

```css
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
```

Removing the outline without a replacement is the most common keyboard failure in a styled
app. `:focus-visible` keeps the ring for keyboard users and spares mouse users the ring on
click — which is why the outline was removed in the first place.

## Test identifiers

Only where role and accessible name are not enough: a row in a data grid, a generated
list, a canvas. A button labelled with text is already reachable by role and name, and an
id on top gives the test a second identity that lets the name rot.

## Analytics

No product analytics SDK in this half of the product means the layer is not applicable —
say so rather than proposing an event into an error monitor. Check `config.yaml`.
