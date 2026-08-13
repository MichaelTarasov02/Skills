# Corner cases

The failure modes that cost hours. Each is grounded in the official docs or verified on disk.

## Triggering

**1. The skill never fires.**
Triggering depends on `description` alone — the body cannot rescue a weak one. Rewrite it by the rules in `skill-spec.md` §"Writing a description that actually triggers", then verify with "what skills are available?".

**2. Descriptions get truncated.**
The skill listing has a budget of ~1% of the context window. When it overflows, Claude Code drops descriptions starting with the least-used skills — stripping the very keywords needed to match. Each entry is capped at **1,536 characters** regardless.
Diagnose: `/doctor`. Raise: `skillListingBudgetFraction` (e.g. `0.02`) or `SLASH_COMMAND_TOOL_CHAR_BUDGET`. Reduce: set low-priority skills to `"name-only"` in `skillOverrides`.

**3. The skill fires too often.**
Narrow the description, or set `disable-model-invocation: true` for manual-only workflows.

**4. Broken YAML fails silently.**
If the frontmatter is malformed, the body still loads but metadata is **empty** — `/name` works while auto-triggering never does. Catch it with `--debug`.

## Reload and lifecycle

**5. Edited `SKILL.md` — applied immediately.**
Claude Code watches skill directories. Adding, editing or removing a skill under `~/.claude/skills/`, the project `.claude/skills/`, or an `--add-dir` skills directory takes effect **in the current session**.

**6. A brand-new top-level skills directory needs a restart.**
If the directory did not exist when the session started, it is not being watched. Restart.

**7. Plugin components other than skills need a reload.**
Changes to `hooks/`, `.mcp.json`, `agents/`, `output-styles/` do **not** hot-reload. Run **`/reload-plugins`** or restart.

**8. The skill "stops working" mid-session.**
Rendered content enters the conversation once and is never re-read. Write standing instructions, not one-time steps. After auto-compaction, re-attached skills share a 25,000-token budget (first 5,000 tokens each), so older skills can drop entirely — re-invoke the important one.

**9. `allowed-tools` expired.**
The grant covers only the turn that invoked the skill. Your next message clears it. For session-wide permission use permission settings instead.

## Structure

**10. Plugin will not load.**
Almost always an invalid manifest or wrong layout. `plugin.json` belongs **only** in `.claude-plugin/`; `skills/`, `agents/`, `commands/`, `hooks/` belong at the plugin **root**. Run `claude plugin validate <path>`.

**11. Paths break.**
All manifest paths must be relative and start with `./`. Inside scripts, hooks and MCP configs use `${CLAUDE_PLUGIN_ROOT}` rather than absolute paths.

**12. Updates never reach users.**
`version` in `plugin.json` is the cache key. Pushing commits without bumping it does nothing — `/plugin update` reports "already at the latest version". After an update lands, a **restart** is required to apply it.

**13. A project-scope `@skills-dir` plugin is invisible.**
It loads only from the `.claude/skills/` of the directory where Claude Code was started, and does not walk up to the repo root. Launch from the repository root, or run `/reload-plugins` after changing directories. It also requires accepting the workspace trust dialog.

**14. Plugin agent refuses to start.**
Plugin-shipped agents may not declare `hooks`, `mcpServers` or `permissionMode`. Remove them.

## Cross-host

**15. The skill works in Claude Code but not Codex.**
Codex implements the base Agent Skills standard only. `allowed-tools`, `disable-model-invocation`, `context: fork`, `agent`, `model` are Claude Code extensions and are ignored. A portable skill must remain correct with all of them stripped.

**16. Two copies drift apart.**
Symlink the skill directory into `~/.codex/skills/` instead of copying, so one source serves both hosts.

## Design

**17. Agents used where skills belong.**
Agents run in an isolated context. A pipeline whose stages share state (voice guide, theme, mention policy, generated IDs) breaks when split across agents. Use skills for shared-state pipelines; agents only for independent parallel work.

**18. Two skills with the same function.**
Guarantees drift and forces every change to be made twice. Merge into one, and note the winner so future edits have a single home.

**19. `SKILL.md` grew past ~5k words.**
Symptoms: the agent skips steps, or applies the file differently each run. Apply the branching test and the pruning passes in `writing-craft.md` — the cure is disclosure and deletion, not compression.

**20. The skill fires and the agent still improvises.**
The body loaded fine; it just does not constrain. Usual causes, in order of frequency: fuzzy completion criteria on each step, reference material sitting behind a vague pointer, and prohibitions that named the unwanted behaviour instead of the wanted one. All three are covered in `writing-craft.md`.
