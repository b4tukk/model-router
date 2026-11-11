# Setting up routing in Claude Code

Templates live in `assets/claude/` next to this skill. Copy them; do not retype them.

## What to install

| Template | Goes to | Purpose |
|---|---|---|
| `agents/code-searcher.md` | `.claude/agents/` | Haiku, low effort, read-only search |
| `agents/quick-editor.md` | `.claude/agents/` | Haiku, low effort, renames and boilerplate |
| `agents/implementer.md` | `.claude/agents/` | Sonnet, medium, builds an approved plan |
| `agents/test-runner.md` | `.claude/agents/` | Sonnet, low, writes and runs tests |
| `agents/reviewer.md` | `.claude/agents/` | Opus, high, read-only review of a diff |
| `CLAUDE.routing.md` | appended to the project's `CLAUDE.md` | Tells the main session which subagent to call |
| `settings.example.json` | merged into `.claude/settings.json` | Default model and effort for the main session |

Use `.claude/agents/` in the project for a per-project setup, or `~/.claude/agents/` to have the subagents everywhere. Ask which the user wants; the home directory affects all their projects.

## Steps

1. List the existing `.claude/agents/`, `CLAUDE.md` and `.claude/settings.json`. If a subagent with the same name exists, show the difference and ask before replacing it.
2. Copy the five agent files.
3. Append the contents of `CLAUDE.routing.md` to `CLAUDE.md` (create the file if missing). If a "Model routing" section is already there, update it in place instead of adding a second one.
4. Merge the keys from `settings.example.json` into `.claude/settings.json`, keeping every existing key. The `model` and `effortLevel` keys change the main session's default, which is separate from subagent routing: add them only if the user asked for a default, and say so when you do. Only add `advisorModel` if the user wants the advisor (see below).
5. Tell the user what was written and that new subagents are picked up on the next session start.

## How the pieces fit

- `CLAUDE.md` tells the main session which subagent to call. The model switch itself lives in each subagent's frontmatter (`model`, `effort`).
- `model` accepts `haiku`, `sonnet`, `opus`, `fable`, a full model ID, or `inherit`. `effort` accepts `low` to `max`.
- A subagent has its own small context, so delegating does not invalidate the main session's prompt cache the way `/model` does.

## Commands worth telling the user about

- `/model fable` switches the model and saves it as the default.
- `/effort high` sets the level (`low` to `xhigh`, `max`, or `auto`).
- `/model opusplan` uses Opus while planning, then Sonnet to build.
- Advisor (experimental, needs the Anthropic API): a cheaper model does the work and consults a stronger one. Enable with `/advisor opus`, `"advisorModel"` in settings, or `claude --advisor opus`.

These behaviours were checked on November 9, 2026. If a command or key is rejected, check the current Claude Code docs rather than insisting.
