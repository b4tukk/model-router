# Setting up routing in Codex

Templates live in `assets/codex/` next to this skill.

## What to install

| Template | Goes to | Purpose |
|---|---|---|
| `config.toml` | `~/.codex/config.toml` | Default: Sol on medium; subagents default to Luna on low |
| `quick.config.toml` | `~/.codex/quick.config.toml` | Profile for cheap, mechanical work (`codex -p quick`) |
| `deep.config.toml` | `~/.codex/deep.config.toml` | Profile for planning and audits (`codex -p deep`) |
| `agents/reviewer.toml` | `.codex/agents/` in the project | Sol on xhigh, read-only review |
| `agents/code-searcher.toml` | `.codex/agents/` in the project | Luna on low, search only |

## Steps

1. `~/.codex/` is global. Confirm with the user before touching it, and read any existing `config.toml` first.
2. Merge the keys from the template `config.toml` into the existing file; do not replace the file, since it usually holds unrelated settings.
3. Copy the two profile files if they do not exist.
4. Copy the agent files into the project's `.codex/agents/`.

## Things to know

- Since Codex 0.134.0, each profile is its own file selected with `codex -p <name>`. `[profiles.<name>]` tables inside `config.toml` are no longer read. If the user has old-style profile tables, point this out rather than adding to them.
- A custom agent file sets its own model and effort, and wins over the defaults in `config.toml`.
- Codex has no same-price match for Opus; the closest is Sol on `xhigh`, which is why the reviewer uses it.

Checked on November 9, 2026. Verify against the current Codex config reference if a key is rejected.
