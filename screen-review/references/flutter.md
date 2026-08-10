# Reviewing a Flutter screen

Read before phase 5. There is no browser here, and pretending otherwise produces findings
nobody can trace.

## The honest path

| Step | Evidence it yields |
|---|---|
| read the widget tree | structure, states, what is conditional on what |
| read `ThemeData` and theme extensions | colours, typography, whether tokens or literals |
| golden tests, if present | rendered output without a device |
| simulator screenshot, if a device is available | the closest thing to seeing it |

Say which of these were actually used. A review from widget code alone is legitimate and
useful — it is only misleading when reported as though the screen had been seen.

## Theme

This app has a real theme layer: `lib/theme/data/app_theme.dart`,
`lib/theme/extensions/app_theme_extension.dart`, and `ThemeType { light, dark, system }`
persisted through `SharedPreferences`. **Dark theme exists**, so it is reviewable rather
than absent.

| Check | What goes wrong |
|---|---|
| Colour literals in widgets | `Color(0xFF3B82F6)` inline instead of a theme token — the widget then ignores the dark theme entirely |
| `app_colors.dart` used directly | bypasses the theme; the value is right in light mode and wrong in dark |
| Hard-coded `Colors.white` / `Colors.black` | the two values guaranteed to break one of the two themes |
| Missing extension value | a token defined for light and absent for dark falls back silently |

The strongest dark-theme finding is a list of widgets referencing colours outside the
theme, with paths. It is greppable and unambiguous.

## Contrast

Same thresholds as web. Convert `0xFFRRGGBB` by dropping the alpha. This app's palette is
the same family measured in `references/vue.md`, so the same failures apply — `0xFF3B82F6`
is `#3b82f6` at 3.68:1, below 4.5:1 for normal text.

Check both themes. A pair that passes on white can fail on the dark surface, and dark
surfaces are where inherited palettes usually break.

## Touch targets

Minimum 48×48 logical pixels. `IconButton` defaults to 48 and is safe; a `GestureDetector`
around an `Icon` is whatever the icon is — typically 24, half the minimum. Search for
tappable widgets that are not buttons; that is where the failures are.

## Layout

| Check | What goes wrong |
|---|---|
| `MediaQuery` breakpoints | phone-only assumptions on a tablet |
| `SafeArea` | content under the notch or the home indicator |
| Keyboard | `resizeToAvoidBottomInset`, and whether the focused field stays visible |
| Rotation | what reflows, and whether state survives |
| `Expanded` / `Flexible` | overflow stripes at the smallest supported width |

## Text expansion and RTL — mandatory here

Seven locales, Hebrew among them. This is not a future concern.

| Check | Method |
|---|---|
| Longest string per screen | compare the ARB values across locales for the keys this screen uses; German and French run ~30% longer |
| Overflow | run the screen under the longest locale, not the English one |
| Mirroring | `Directionality(textDirection: TextDirection.rtl)` around the screen in a test |
| Directional padding | `EdgeInsets.only(left:)` does not mirror; `EdgeInsetsDirectional.only(start:)` does — every occurrence of the former in a screen shown in Hebrew is a finding |
| Icons | directional icons (back, next) mirror; non-directional (search, settings) must not |

`EdgeInsets.only(left:)` versus `EdgeInsetsDirectional.only(start:)` is greppable and is
the most common RTL defect in a codebase that added Hebrew after the fact.
