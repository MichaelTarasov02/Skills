# Reviewing a Vue screen

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


Read before phase 5.

## Live first

```
1. start the dev server
2. open the route
3. screenshot at 1440, 768, 375
4. screenshot with the dark theme active, if one exists
5. screenshot with strings expanded ~30%
6. tab through the screen, recording where focus goes
```

Only when the app cannot be started — auth, backend, seed data — fall back to code, and
**say in the review that no screen was seen**. A code review presented as a visual one
misstates the evidence behind every finding.

Expanding strings without a translation: override the locale, or inject longer text
through the store. Guessing which labels would grow is not a substitute — the ones that
break are rarely the ones expected.

## Contrast, computed not eyeballed

Pull the actual values from the stylesheet and compute. Thresholds: **4.5:1** normal
text, **3:1** text ≥18.66px bold or ≥24px, **3:1** UI component boundaries and states.

```python
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True); return (l1+0.05)/(l2+0.05)
```

**Measured for this product's palette on white:**

| Colour | Uses | Ratio | Normal text | UI 3:1 |
|---|---|---|---|---|
| `#10b981` | 130 | **2.54** | fail | fail |
| `#f59e0b` | 57 | **2.15** | fail | fail |
| `#999999` | 32 | 2.85 | fail | fail |
| `#ef4444` | 101 | 3.76 | fail | pass |
| `#3b82f6` | 71 | 3.68 | fail | pass |
| `#2563eb` | 54 | 5.17 | pass | pass |
| `#6b7280` | 52 | 4.83 | pass | pass |

The palette already contains its own fix: `#2563eb` passes where `#3b82f6` fails, and
both are in use. For text and small icons, the darker shade of the same hue is the edit —
no new colour required.

`#10b981` and `#f59e0b` fail even the 3:1 component threshold, so they cannot carry
meaning on white at any size. They need a darker shade, or a non-colour channel beside
them.

## ant-design-vue specifics

| Check | What goes wrong |
|---|---|
| `a-table` at narrow widths | `:scroll="{ x: … }"` gives horizontal scroll only; a table with many columns becomes unusable on a phone rather than reflowing |
| Component defaults | `No Data`, `OK`, `Cancel` shipped unreviewed — a finding, routed to `interface-copy` |
| `:disabled` styling | the kit's disabled grey frequently fails contrast; measure it rather than assuming the kit is compliant |
| Theme override | check whether the kit's tokens were customised; if partly, the screen mixes two palettes |

## Dark theme

Check whether one exists at all before reviewing it. Where the mobile app has a theme and
the web app does not, that asymmetry belongs in the review as a finding in its own right —
a user switching between platforms meets two different products.

## Text expansion and RTL

The Vue app has no i18n layer, so its strings never expand and never mirror. That makes
R11 and R12 not applicable **here** — and worth stating, because the same screens on
mobile carry seven locales including Hebrew. Mark it as not applicable with the reason,
never as a pass.
