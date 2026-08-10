# States in Flutter

Read before phase 1.

## Find the existing convention first

| Look for | Tells you |
|---|---|
| `lib/features/*/` — cubit, bloc, or notifier files | the state approach the team chose |
| sealed classes or `freezed` unions in a feature's state file | states are modelled as a closed set — the strong case |
| `FutureBuilder` / `StreamBuilder` in widgets | states handled per-widget via `AsyncSnapshot` |
| bare `bool isLoading` in a `StatefulWidget` | flag-based, same trap as the web side |

This repository organises by feature under `lib/features/` with cubits present
(`switch_project_cubit` among them). Open the cubit of a neighbouring feature and match
its state shape — that is the convention the screen must join.

## Closed state sets

Where the codebase already models state as a sealed union, the blueprint names one
variant per matrix row:

```dart
sealed class ShiftListState {}
class Loading         extends ShiftListState {}
class Loaded          extends ShiftListState { final List<Shift> shifts; }
class EmptyNoShifts   extends ShiftListState {}
class EmptyFiltered   extends ShiftListState {}
class NoAccess        extends ShiftListState {}
class LoadFailed      extends ShiftListState { final bool canRetry; }
```

Two empty variants rather than one is the whole point: the compiler then forces the UI to
handle them separately, which prose never does.

Where the codebase uses flags, say which flag combination renders which state — the code
cannot express it, so the blueprint must.

## Screen structure

| Concern | Where it is decided |
|---|---|
| Safe area, notch, system bars | `Scaffold`, `SafeArea` |
| Keyboard covering fields | `resizeToAvoidBottomInset`, scroll behaviour on focus |
| Pull to refresh | `RefreshIndicator` — decide whether the screen has one |
| Rotation | whether the screen supports landscape, and what reflows |
| Back | system back on Android, gesture on iOS, and what an unsaved form does with it |

Android's system back has no visual affordance and cannot be removed. A form with unsaved
input needs an answer for it; on web the same question is the browser back button.

## Offline

Connectivity handling belongs in the state set, not in a banner bolted on top. Answer:
what is served from local storage, what is blocked, how the user learns connectivity
returned.

## Placement

`lib/navigation/` holds the route definitions. The Placement section names the route, its
guard, the entry points that reach it, and where popping the screen lands.

## Locale pressure on layout

Seven locales including Hebrew. Any state whose text is close to its container's width in
English will overflow in German or French and mirror in Hebrew. Note it in Boundary data,
where it belongs — it is a data boundary, not a translation task.
