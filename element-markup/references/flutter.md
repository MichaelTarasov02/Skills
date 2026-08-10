# Element markup — Flutter

Worked markup for all twelve cases. Read before marking up a mobile element.

Flutter has no DOM and no ARIA. Semantics is a parallel tree built by widgets, and most
Material widgets contribute to it already. The equivalent of "native before ARIA" is
**let the widget speak before wrapping it in `Semantics`**.

## M1 — semantic widget

```dart
// wrong: GestureDetector contributes no semantics
GestureDetector(onTap: _export, child: Text('Export'))

// right: a button widget is announced as a button and is focusable
TextButton(onPressed: _export, child: Text(l10n.exportText))
```

`InkWell` and `GestureDetector` produce a tappable region that a screen reader does not
recognise as a control. Use a button widget, or wrap with
`Semantics(button: true, enabled: true, …)` when the visual cannot be a button.

`onPressed: null` disables and announces disabled. Wrapping an enabled button in a
`Semantics(enabled: false)` to fake it desynchronises the two.

## M2 — accessible name for an icon-only control

```dart
IconButton(
  icon: const Icon(Icons.download),
  tooltip: l10n.exportAssociateListText,   // becomes the semantic label too
  onPressed: _export,
)
```

`tooltip` on `IconButton` supplies the semantic label — one property, both jobs. Where no
tooltip is wanted:

```dart
Semantics(
  label: l10n.exportAssociateListText,
  button: true,
  child: ExcludeSemantics(child: Icon(Icons.download)),
)
```

`ExcludeSemantics` around the icon stops it contributing a second node.

## M3 — images

```dart
Image.network(associate.photoUrl, semanticLabel: l10n.associatePhotoText)  // informative
ExcludeSemantics(child: Image.asset('assets/divider.png'))                 // decorative
```

No `semanticLabel` leaves the image silent, which is right for decoration and wrong for
content. Make the choice explicit with `ExcludeSemantics` so the next reader sees it was
a decision.

## M4 — focus order

Traversal follows the widget tree in reading order. When the visual order diverges —
a `Stack`, or a `Row` reversed for RTL — set it explicitly:

```dart
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(children: [
    FocusTraversalOrder(order: NumericFocusOrder(1), child: fieldA),
    FocusTraversalOrder(order: NumericFocusOrder(2), child: fieldB),
  ]),
)
```

This product ships Hebrew. In RTL the visual order mirrors while the tree does not — any
screen with a horizontal control row needs its traversal checked in an RTL locale, not
assumed.

## M5 — dialog focus

```dart
showDialog(
  context: context,
  barrierDismissible: false,
  builder: (_) => AlertDialog(
    title: Text(l10n.deleteDocumentTitle),
    content: Text(l10n.deleteDocumentBodyText),
    actions: [
      TextButton(onPressed: () => Navigator.pop(context), child: Text(l10n.cancelText)),
      TextButton(onPressed: _confirm, child: Text(l10n.deleteDocumentText)),
    ],
  ),
);
```

`showDialog` traps focus and restores it on pop — do not reimplement either. Android's
system back closes the dialog; if the dialog holds unsaved input, handle it with
`PopScope` rather than letting back discard silently.

`barrierDismissible: false` for destructive confirmations: a stray tap outside should not
count as an answer.

## M6 — visible focus

Focus rings come from the theme, not from each widget:

```dart
ThemeData(
  focusColor: colorScheme.primary.withOpacity(0.12),
  inputDecorationTheme: InputDecorationTheme(
    focusedBorder: OutlineInputBorder(
      borderSide: BorderSide(color: colorScheme.primary, width: 2),
    ),
  ),
)
```

Mobile touch hides the problem: focus is invisible until someone attaches a keyboard or
uses switch access. Check with an external keyboard, not by reasoning about it.

## M7 — announcements

There is no live region. Announce explicitly:

```dart
SemanticsService.announce(
  l10n.associatesFoundText(count),
  Directionality.of(context),
);
```

Passing `Directionality.of(context)` rather than a hard-coded `TextDirection.ltr` is what
makes it correct in Hebrew.

Alternatively, `Semantics(liveRegion: true, child: …)` re-announces when its child's
semantics change — better for a value that updates in place, such as a countdown.

## M8–M10 — analytics

See `references/analytics.md`. Platform note: this app carries
`firebase_analytics: ^11.4.2`, so the layer is applicable. Firebase constrains event
names to 40 characters, parameter names to 40, and 25 parameters per event; names must be
alphanumeric with underscores and cannot start with `firebase_`, `google_` or `ga_`.

## M11 — test id

```dart
IconButton(key: const Key('export-associates'), ...)
```

Flutter tests can find by semantic label — `find.bySemanticsLabel(...)` — which keeps
tests honest about accessibility. Reach for `Key` when the label is localised (and
therefore changes per locale) or absent. With seven locales here, label-based finding is
fragile in tests that run under a non-default locale; a `Key` is the safer default for
those.

## M12 — custom control keyboard contract

Wrap the interaction in a `Shortcuts`/`Actions` pair rather than raw key listeners:

```dart
Shortcuts(
  shortcuts: {
    LogicalKeySet(LogicalKeyboardKey.arrowDown): const NextOptionIntent(),
    LogicalKeySet(LogicalKeyboardKey.arrowUp): const PreviousOptionIntent(),
    LogicalKeySet(LogicalKeyboardKey.enter): const SelectOptionIntent(),
    LogicalKeySet(LogicalKeyboardKey.escape): const DismissIntent(),
  },
  child: Actions(actions: {...}, child: child),
)
```

Escape maps to Flutter's built-in `DismissIntent`, so dismissal behaves consistently with
the rest of the framework.

## VoiceOver and TalkBack differ

They disagree on how much of a merged node they read and on gesture mapping. A label that
reads well on one can be truncated or reordered on the other. `MergeSemantics` around a
composite control (an icon plus label plus value) produces one coherent announcement on
both instead of three fragments; use it, then verify on both.
