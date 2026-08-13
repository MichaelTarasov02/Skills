# Markup — Flutter

> **Examples below are shapes, not facts about your codebase.** Counts and widget names
> are illustrative. Measure before you quote any of them.

Flutter has no DOM and no ARIA. Semantics is a parallel tree that widgets contribute to,
and most Material widgets already do. The equivalent of "native before ARIA" is **let the
widget speak before wrapping it in `Semantics`**.

## Find the leverage before writing a single fix

A codebase with its own component layer has a small number of widgets standing between
hundreds of call sites and the semantics tree. Fixing the widget fixes them all; fixing
call sites one at a time is the same work multiplied.

```bash
grep -rhoE 'class (\w*Button\w*)' --include='*.dart' lib | awk '{print $2}' | sort -u
# then, per candidate:
grep -rho '\bActionCardButtonWidget(' lib | wc -l
```

Measured on one repository:

```
custom button classes            68
ActionCardButtonWidget usages   297   ┐
AlertButtonConfiguration        167   ├ three widgets cover 548 call sites
ActionCardButtonsView            84   ┘

GestureDetector                  29
InkWell                          40
IconButton                       81
Material text buttons             0   ← every button is a custom widget
```

**Report the leverage, not the raw count.** "150 elements lack an accessible name" is
true and useless; "three widgets carry 548 of them" is the same fact turned into a
morning's work.

## The baseline this measurement usually reveals

```
Semantics(         0
semanticLabel      0
ExcludeSemantics   0
SemanticsService   0
tooltip:           0
```

Zero across the board means no accessibility infrastructure exists — not that it was
attempted badly. That changes the recommendation: start with the shared widgets and a
convention, not with an audit of individual screens.

## Three shapes, in order of leverage

### The shared button widget

Whatever it wraps, it must contribute a button role and a name. Where the widget already
takes a label, the name comes free; where it takes only an icon, add a required parameter
rather than an optional one — an optional accessible name is an unfilled accessible name.

```dart
Semantics(
  button: true,
  enabled: onPressed != null,
  label: semanticLabel ?? label,
  child: ExcludeSemantics(child: existingChild),
)
```

`enabled` must track the real callback. A widget that looks disabled while announcing
itself as enabled is worse than one with no semantics at all.

### `IconButton` without a tooltip

`IconButton` gives the role and the tap target; `tooltip` supplies the accessible label
and the long-press hint in one property. Without it the control is announced as a button
with no name.

```dart
IconButton(
  icon: const Icon(Icons.download),
  tooltip: l10n.exportAssociateListText,
  onPressed: _export,
)
```

The label names the **action**, not the icon, and comes from the localisation file — not a
literal, or it will be the only untranslated string on the screen.

### `GestureDetector` and `InkWell`

Neither contributes semantics. A screen reader sees a decorative box. Replace with a
button widget where the visual allows; where it does not, wrap explicitly:

```dart
Semantics(
  button: true,
  label: l10n.someActionText,
  child: ExcludeSemantics(child: GestureDetector(onTap: _tap, child: visual)),
)
```

`ExcludeSemantics` on the child stops it contributing a second, competing node.

## Composite controls

An icon plus a label plus a value announces as three fragments. `MergeSemantics` produces
one coherent announcement, and the two screen readers disagree enough about fragment
ordering that merging is the only way to get a predictable result on both.

## Focus and keyboard

Traversal follows the widget tree in reading order. Where the visual order diverges — a
stack, or a row reversed for right-to-left — set it explicitly with a traversal group.

In a product shipping a right-to-left locale, any screen with a horizontal control row
needs its traversal checked **in that locale**, not assumed from the left-to-right build.

## Announcements

There is no live region. Announce explicitly, and pass the ambient direction rather than a
hard-coded one, or the announcement breaks in right-to-left languages:

```dart
SemanticsService.announce(message, Directionality.of(context));
```

## Test identifiers

`find.bySemanticsLabel` keeps tests honest about accessibility, but a localised label
changes per locale and breaks tests that run under a non-default one. In a multi-locale
product, a `Key` is the safer default for tests and the semantic label stays for users.

## Analytics

Event names come from the tracking plan and objects from `lexicon.md`. Where the platform
has an analytics SDK but no plan, propose the event as a proposal and say the scheme does
not exist yet.
