# Usage audit: where are the tokens going?

Use this when the user's limit runs out too fast or the bill is higher than expected. The aim is to find the one or two habits that account for most of the spend, not to list every possible saving.

## 1. Look before advising

Gather what is actually observable before recommending anything:

- Which model and effort level is the main session on? (In Claude Code, check `.claude/settings.json`, `~/.claude/settings.json`, and ask what `/model` shows.)
- How long do sessions run before being cleared or restarted?
- Does the project have subagents, and do they pin a model, or inherit the main one?
- What kind of work dominates: reading and searching, building, or debugging?
- If the tool offers a usage or cost breakdown, ask the user to share it.

If something cannot be observed, ask one question rather than guessing.

## 2. Check the common causes, most expensive first

| Symptom | What is happening | Fix |
|---|---|---|
| Top model does everything, including file search | Every read is billed at the highest rate | Delegate search and mechanical edits to a fast-tier subagent |
| Effort left on `xhigh` or `max` as the default | Thinking tokens are spent on trivial turns | Default to medium; raise it for the hard task, then lower it |
| Model switched back and forth inside one conversation | Each switch re-reads the whole history uncached | Switch at task boundaries, or delegate to a subagent instead |
| One very long session for unrelated tasks | The whole history is re-sent each turn, and may cross a long-context price cliff | Start a fresh session per task; keep durable facts in `CLAUDE.md` |
| Subagents inherit the main model | Cheap work runs at the expensive rate without anyone noticing | Pin `model` and `effort` in each subagent's frontmatter |
| Cheap model retried many times on a hard task | Paying for several failures and then the strong model anyway | Escalate after one failed attempt |
| Large files or logs pasted in whole | Input tokens dominate | Have a fast-tier subagent read and report the relevant excerpt |
| Same model writes and reviews | Not a cost problem, but review finds less | Review with a different model |

## 3. Recommend

Report in this shape:

1. **Where the usage goes** - one or two sentences, based on what was observed.
2. **Biggest fix** - the single change with the largest effect, and how to make it.
3. **Next fix** - optional second change.
4. **What not to change** - where the expensive model is earning its cost (planning, security-sensitive code), so the user does not over-correct.

If the fix is routing, offer to install the subagent setup (`references/claude-code-setup.md` or `references/codex-setup.md`). To put numbers on a comparison, use `scripts/estimate_cost.py`.
