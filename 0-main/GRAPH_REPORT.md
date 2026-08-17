# Graph Report — skill relationships (2026-08-17)

## Summary
- 404 nodes · 2014 edges · 16 communities
- Edges: 741 semantic (carried over from the July run), 1273 statistical (TF-IDF cosine)
- 137 semantic edges dropped — one endpoint no longer exists
- Token cost of this run: 0 — rebuild with `python3 0-main/rebuild-graph.py`

## Communities (12 substantive, 4 thin omitted)

### 0 — Flutter / Gsap / App / React
Size 82 · cohesion 0.112
Nodes: accessibility, accessibility-review, agent-ui, animation-vocabulary, anti-ui-slop, app-store-screenshots, apple-design, artifacts-builder (+74 more)

### 1 — Plan / Interview / Work / Requirements
Size 60 · cohesion 0.115
Nodes: architecture, ask-matt, brainstorming, business-analyst, ce-brainstorm, ce-compound, ce-doc-review, ce-explain (+52 more)

### 2 — Content / Marketing / Linkedin / Video
Size 52 · cohesion 0.146
Nodes: agent-tools, ai-automation-workflows, ai-avatar-video, ai-content-pipeline, ai-marketing-videos, ai-seo, ai-social-media-content, ai-video-generation (+44 more)

### 3 — Sources / Sales / Contact / Research
Size 38 · cohesion 0.144
Nodes: account-research, build-contact-book, call-summary, ce-compound-refresh, ce-product-pulse, ce-sweep, close-management, contact-research (+30 more)

### 4 — Bugs / Git / Tests / Branch
Size 33 · cohesion 0.191
Nodes: agent-browser, ce-babysit-pr, ce-code-review, ce-commit, ce-commit-push-pr, ce-debug, ce-dogfood, ce-polish (+25 more)

### 5 — Writes / Триггеры / Dev-agent / Novel
Size 28 · cohesion 0.172
Nodes: agent-forge, analyze-case, apply-edits, copy, craft, element-markup, enhance, feature-handoff (+20 more)

### 6 — Competitors / Research / Users / Competitor
Size 25 · cohesion 0.22
Nodes: ceo-advisor, competitive-analysis, competitive-brief, competitive-intelligence, competitor-analysis, competitor-profiling, conducting-user-interviews, cto-advisor (+17 more)

### 7 — Image / Pdf / Audio / Text
Size 25 · cohesion 0.19
Nodes: ai-image-generation, ai-voice-cloning, background-removal, better-icons, brandkit, canvas-design, doc, documentation (+17 more)

### 8 — Prompt / Engineering / Prompts / Llm
Size 22 · cohesion 0.199
Nodes: ai-prompt-engineering-safety-review, api-integration-specialist, boost-prompt, cavecrew, caveman, caveman-compress, caveman-stats, ce-optimize (+14 more)

### 9 — Data / Analysis / Charts / Analyze
Size 14 · cohesion 0.451
Nodes: analytics-data-analysis, analyze, build-dashboard, data-context-extractor, data-visualization, excel-analysis, explore-data, google-analytics (+6 more)

### 10 — Resume / Writer / Portfolio / Job
Size 11 · cohesion 0.618
Nodes: case-study-writing, cover-letter-generator, creative-portfolio-resume, executive-resume-writer, portfolio-case-study-writer, reference-list-builder, resume-bullet-writer, resume-formatter (+3 more)

### 11 — Compliance / Contract / Legal / Regulatory
Size 10 · cohesion 0.644
Nodes: brief, compliance-check, compliance-tracking, contract-review, cybersecurity-analyst, legal-advisor, legal-document-analyzer, review-contract (+2 more)

## God nodes (most connected)

1. `flutter-expert` — 30 edges
2. `frontend-design` — 30 edges
3. `content-creation` — 29 edges
4. `web-design-guidelines` — 26 edges
5. `grilling` — 23 edges
6. `copywriting` — 22 edges
7. `to-issues` — 22 edges
8. `senior-frontend` — 21 edges
9. `flutter-building-layouts` — 20 edges
10. `vercel-react-best-practices` — 20 edges

## Bridges (highest betweenness — cross-community connectors)

- `frontend-design` — 0.0374
- `web-design-guidelines` — 0.0294
- `content-creation` — 0.0291
- `task-management` — 0.0238
- `copywriting` — 0.0217

## Knowledge gaps

**5 weakly-connected node(s)** (≤1 edge): `agent-reach`, `ce-retune`, `llm-council`, `task-observer`, `what-leaked-about-you`

A skill with no neighbours is either genuinely unique or described in words nothing else uses — check the description before assuming it is the former.
