# Component Reference

The markup for every component the system provides. Read this instead of the CSS — the stylesheet is 23 KB and reading it costs the context that should go into the writing.

If a component you need is not here, build it in the post's `styles.css` as the one bespoke object. Do not re-implement something on this list.

## Artboard skeleton

Every slide is this shape. Brackets render in `ivory` and in the coloured family; `graphite` hides them, so including them is harmless either way. The swipe affordance goes on slides 1 and 2 only.

```html
<section class="slide" data-theme="ivory">
  <span class="bracket tl"></span><span class="bracket tr"></span>
  <span class="bracket bl"></span><span class="bracket br"></span>
  <div class="swipe-edge"><span class="chev">›</span>swipe</div>
  <div class="frame">
    <div class="meta"><span><span class="dot"></span>lane</span><span>01 / 08</span></div>
    <div class="fill centre">   <!-- or just "fill" for top-flow -->
      …
    </div>
    <div class="foot"><span>note</span><span><span class="nm">A. Author</span> · 01 / 08</span></div>
  </div>
</section>
```

The single page swaps `.slide` for `.page`, drops the swipe edge, wraps its body in `.sheet` instead of `.fill`, carries the author name once in the top `.meta`, and closes with an `.endnote`.

## Type

`.display` · `.h1` · `.h2` · `.lede` · `.body` · `.small` · `.meta` · `.mono`

`<em>` inside `.display` or `.pull` renders in the theme accent — this is how a hook gets its emphasis without a second colour.

Utilities: `.mt3` `.mt4` `.mt5` `.mb3` `.mb4` (margins) · `.gap3` `.gap4` `.gap5` · `.center` · `.row-2`

## Layout

| Class | Effect |
|---|---|
| `.fill` | body column, flows from the top with real gaps |
| `.fill.centre` | centres the group — for covers and single-object slides |
| `.hero` | on the primary component, grows it to fill the slack (see the playbook first) |
| `.sheet` | single page only, distributes blocks down the whole artboard |

## Components

**Eyebrow** — the pill above a heading. `.acc` tints it with the accent, `.warn` with the risk tone.
```html
<p class="eyebrow acc mb4"><span class="em">🔎</span> label</p>
```

**Chips** — an enumerated field. `.on` marks a chip as active.
```html
<div class="chips"><span class="chip">a</span><span class="chip on">b</span></div>
```

**Strip** — a sequence or pipeline. Use `.nowrap` for four or more nodes so no separator dangles. Node variants: `.on` (filled accent), `.out` (accent outline), `.bad` (risk outline).
```html
<span class="strip-tag acc">label</span>
<div class="strip nowrap">
  <span class="node on">first</span><span class="sep">→</span>
  <span class="node">second</span>
</div>
```

**Stack** — layers, what sits on what. `.inset` indents each layer progressively. `.top` and `.base` mark the ends.
```html
<div class="stack">
  <div class="layer top"><span class="lt">title</span><span class="ld">gloss</span></div>
  <div class="layer base"><span class="lt">title</span><span class="ld">gloss</span></div>
</div>
```

**Pair** — A versus B, side by side. `.side.a` and `.side.b` take different accents.
```html
<div class="pair">
  <div class="side a"><div class="tag">Old</div><div class="ttl">Heading</div>
    <ul><li>point</li></ul></div>
  <div class="side b"><div class="tag">New</div><div class="ttl">Heading</div>
    <ul><li>point</li></ul></div>
</div>
```

**Ledger** — label:value rows, compact enumeration. `.key` accents a row, `.hot` marks it as risk.
```html
<div class="ledger">
  <div class="row key"><span class="k">Label</span><span class="v">Value</span></div>
</div>
```

**Checks** — criteria or tests. `.kill` turns a box to the risk tone. `.cn` is the sub-line.
```html
<div class="checks">
  <div class="check"><span class="box">1</span>
    <span class="ct">Question?<span class="cn">The gloss under it.</span></span></div>
</div>
```

**Scale** — a two-sided trade-off. `.up` takes the accent, `.down` the risk tone.
```html
<div class="scale">
  <div class="arm up"><span class="mk">↑</span><span class="at"><strong>Lead.</strong> Body.</span></div>
  <div class="arm down"><span class="mk">↓</span><span class="at"><strong>Lead.</strong> Body.</span></div>
</div>
```

**Card** — a framed statement. `.acc` and `.warn` change the edge.
```html
<div class="card"><div class="core"><p class="h2">Claim.</p><p class="body">Support.</p></div></div>
```

**Callout** — the caveat or the "but". Left border carries the tone.
```html
<div class="callout"><p class="body">…</p></div>
```

**Pull** — the line the post is remembered by. **One per deck, two at most.**
```html
<p class="pull">The claim, with <em>emphasis</em> on the turn.</p>
```

**Fan** — a node map, converging or diverging. Leaves are small glyph boxes, not labels.
```html
<div class="fan"><div class="hub">source</div><svg>…</svg>
  <div class="leafs"><span class="leaf">1</span></div></div>
```

**Badge** — the qualifier on any illustrative figure. Never present an illustration as a measurement.

**Endnote** — the single page's sign-off. Verify it lands inside the frame; it is silently cropped otherwise.
```html
<div class="endnote"><span class="em">💬</span><span class="q">The question?</span></div>
```

## Emoji — the verified-safe set

Only these render correctly in the headless export:

⚡ 📈 👥 🧭 ⛵ 💬 ⚖️ 🛠️ 🔎 ✅ ⚠️ 🔒 📋 💰 ⚙️ 🧠 🚦 🧩 ❓ 🧪

**Never 🧱** — it renders as an unrelated glyph in the export. This was observed and fixed once already, which is why it is written down.

One per slide title, five to twelve across a deck, always functional rather than decorative.

## Theme names are fixed by the CSS

`data-theme` accepts `ivory`, `graphite`, `cobalt`, `green` and `cherry` only. The last three are one type in three colours and share `content-types/colored.md`. The profile's `themes:` block maps *your* words onto those three, but the values themselves come from the stylesheet. Renaming them there produces artboards with no theme styling at all — and the checker will report the theme as matching, because it compares your spec against your HTML. If you want different names, rename them in the CSS too.
