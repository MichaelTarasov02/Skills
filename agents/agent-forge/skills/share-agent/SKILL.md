---
name: share-agent
description: This skill should be used when the user wants to give an agent or plugin to other people — colleagues, friends, or the public. Trigger phrases include "share my plugin", "publish this agent", "how do my friends install this", "make a marketplace", "release a new version", "поделиться плагином", "раздать агента", "выпустить версию". Converts a personal skills-directory plugin into a distributable marketplace repo, handles versioning and release tags, and writes the install instructions the recipient will follow.
---

# Share Agent

Turn a personal agent into one other people can install.

## What actually changes

A personal agent lives at `~/.claude/skills/<name>/` and loads as `<name>@skills-dir` with no install step. That path is yours alone — nobody else can reach it. Sharing means moving the same content into a **repository with a marketplace manifest**.

The skills themselves do not change. Only distribution does.

## 1. Pre-flight

Do not ship a broken agent:

```bash
claude plugin validate <path>
```

Confirm it passes, and that `README.md` exists with a working quick start. If verification has not been run, run the `verify-agent` skill first.

## 2. Repository layout

```
my-agents/                          # the repo you will share
├── .claude-plugin/
│   └── marketplace.json            # lists the plugins in this repo
└── plugins/
    └── <agent-name>/
        ├── .claude-plugin/plugin.json
        ├── skills/
        └── README.md
```

Move (or copy) the agent from `~/.claude/skills/<name>/` into `plugins/<agent-name>/`. Keep the internal structure identical.

## 3. Versioning — the rule that silently breaks updates

`version` in `plugin.json` is the cache key. If it is not bumped, `/plugin update` reports "already at the latest version" no matter how many commits were pushed.

Every release: bump `version`, then tag.

```bash
claude plugin tag <path>
```

Creates a `{name}--v{version}` tag and validates that `plugin.json` and the marketplace entry agree.

## 4. Recipient instructions

Write these into the README, tested, not assumed:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install <agent-name>@<marketplace-name>
```

Then, in the README, state plainly:

> Restart Claude Code (or run `/reload-plugins`) after installing — components are not picked up in the current session.

Scope options worth mentioning:

| Scope | Effect |
|---|---|
| `--scope user` | default; just this person |
| `--scope project` | written to `.claude/settings.json`, reaches everyone who clones the repo |
| `--scope local` | gitignored, machine-only |

## 5. Make it configurable for them

An agent hard-wired to your paths, voice or accounts is not shareable. Check for:

- absolute paths pointing into your home directory
- your name, brand or account IDs baked into skill bodies
- credentials or tokens

If any exist, add a `setup-<agent>` skill that interviews the new user and writes their own config file. That is the difference between "my tool" and "our tool".

## 6. Codex recipients

Codex implements the same Agent Skills standard, so individual skills port directly:

```bash
ln -s <repo>/plugins/<agent>/skills/<skill> ~/.codex/skills/<skill>
```

State in the README which Claude-only features (`allowed-tools`, `disable-model-invocation`, `context: fork`) do not apply there, and confirm each shared skill still reads correctly without them.

## Report

- repo layout created, with real paths
- version and tag issued
- exact install commands, verified
- what was de-personalized, and what a new user must configure
- what a recipient should run first to confirm it works
