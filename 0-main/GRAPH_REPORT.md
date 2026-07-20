# Graph Report - .  (2026-07-10)

## Corpus Check
- Large corpus: 1208 files · ~1,136,335 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 284 nodes · 878 edges · 13 communities
- Extraction: 0% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Content, SEO & Brand Marketing
- Business Strategy & Org Leadership
- Frontend & UI Design
- Planning & Software Architecture
- Sales & Market Research
- Agent Ops & Skill Authoring
- Flutter Mobile Development
- Docs, Media & Asset Generation
- Data Analytics & Finance
- Code Review, QA & Debugging
- Legal, Compliance & Backend Security
- Resume & Career
- Prompt Engineering

## God Nodes (most connected - your core abstractions)
1. `flutter-expert` - 26 edges
2. `content-creation` - 20 edges
3. `senior-frontend` - 18 edges
4. `frontend-design` - 16 edges
5. `copywriting` - 14 edges
6. `analyze` - 13 edges
7. `brainstorming` - 12 edges
8. `code-review` - 12 edges
9. `write-spec` - 12 edges
10. `account-research` - 11 edges

## Surprising Connections (you probably didn't know these)
- `flutter-improving-accessibility` --complements--> `accessibility-review`  [0.6]
  flutter-improving-accessibility/SKILL.md → accessibility-review/SKILL.md
- `audit-website` --complements--> `accessibility-review`  [0.6]
  audit-website/SKILL.md → accessibility-review/SKILL.md
- `lead-research-assistant` --synergizes_with--> `account-research`  [0.75]
  lead-research-assistant/SKILL.md → account-research/SKILL.md
- `founder-sales` --complements--> `account-research`  [0.55]
  founder-sales/SKILL.md → account-research/SKILL.md
- `agent-development` --synergizes_with--> `prompt-engineering`  [0.6]
  agent-development/SKILL.md → prompt-engineering/SKILL.md

## Communities (13 total, 0 thin omitted)

### Community 0 - "Content, SEO & Brand Marketing"
Cohesion: 0.15
Nodes (36): ai-seo, audit-website, brand-guidelines, brand-review, brand-voice-enforcement, competitor-analysis, content-creation, content-creator (+28 more)

### Community 1 - "Business Strategy & Org Leadership"
Cohesion: 0.17
Nodes (28): business-analyst, ceo-advisor, conducting-user-interviews, cto-advisor, founder-sales, job-post-builder, market-sizing-analysis, measuring-product-market-fit (+20 more)

### Community 2 - "Frontend & UI Design"
Cohesion: 0.21
Nodes (27): accessibility-review, artifacts-builder, clarify, colorize, deploy-to-vercel, design-system-patterns, figma, frontend-design (+19 more)

### Community 3 - "Planning & Software Architecture"
Cohesion: 0.20
Nodes (27): architecture, ask-matt, brainstorming, codebase-design, create-plan, decision-mapping, design-an-interface, domain-modeling (+19 more)

### Community 4 - "Sales & Market Research"
Cohesion: 0.18
Nodes (25): account-research, call-summary, competitive-analysis, competitive-brief, competitive-intelligence, competitor-profiling, contact-research, create-an-asset (+17 more)

### Community 5 - "Agent Ops & Skill Authoring"
Cohesion: 0.19
Nodes (24): agent-development, cavecrew, caveman, caveman-compress, caveman-stats, Codex Guide, dispatching-parallel-agents, executing-plans (+16 more)

### Community 6 - "Flutter Mobile Development"
Cohesion: 0.25
Nodes (23): flutter-adding-home-screen-widgets, flutter-animating-apps, flutter-architecting-apps, flutter-building-forms, flutter-building-layouts, flutter-building-plugins, flutter-caching-data, flutter-embedding-native-views (+15 more)

### Community 7 - "Docs, Media & Asset Generation"
Cohesion: 0.23
Nodes (20): ai-image-generation, better-icons, canvas-design, changelog-generator, doc, documentation, documentation-writer, docx (+12 more)

### Community 8 - "Data Analytics & Finance"
Cohesion: 0.26
Nodes (20): analytics-data-analysis, analyze, build-dashboard, close-management, data-context-extractor, data-visualization, Excel Analysis, explore-data (+12 more)

### Community 9 - "Code Review, QA & Debugging"
Cohesion: 0.30
Nodes (19): clean-code, code-review, code-reviewer, customer-escalation, debug, diagnosing-bugs, find-bugs, migrate-to-shoehorn (+11 more)

### Community 10 - "Legal, Compliance & Backend Security"
Cohesion: 0.35
Nodes (14): API Integration Specialist, brief, compliance-check, compliance-tracking, contract-review, cybersecurity-analyst, legal-advisor, legal-document-analyzer (+6 more)

### Community 11 - "Resume & Career"
Cohesion: 0.58
Nodes (11): Cover Letter Generator, Creative Portfolio Resume, Executive Resume Writer, linkedin-profile-optimizer, Portfolio Case Study Writer, Reference List Builder, Resume Bullet Writer, Resume Formatter (+3 more)

### Community 12 - "Prompt Engineering"
Cohesion: 0.51
Nodes (10): ai-prompt-engineering-safety-review, boost-prompt, enhance-prompt, full-output-enforcement, prompt-builder, prompt-engineering, prompt-engineering-patterns, prompt-optimizer (+2 more)

## Knowledge Gaps
- **1 isolated node(s):** `persona-project-manager`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `content-creation` connect `Content, SEO & Brand Marketing` to `Docs, Media & Asset Generation`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `flutter-expert` connect `Flutter Mobile Development` to `Frontend & UI Design`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `senior-frontend` connect `Frontend & UI Design` to `Code Review, QA & Debugging`, `Legal, Compliance & Backend Security`, `Flutter Mobile Development`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **What connects `persona-project-manager` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Content, SEO & Brand Marketing` be split into smaller, more focused modules?**
  _Cohesion score 0.1492063492063492 - nodes in this community are weakly interconnected._