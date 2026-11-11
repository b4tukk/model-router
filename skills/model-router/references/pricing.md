# Models and prices (dated snapshot)

Prices and settings as checked on **November 9, 2026**. Treat everything here as a snapshot and verify against the provider's pricing page before quoting it as current. The same numbers are in `assets/prices.json`, which the cost script reads; update both together.

## Tiers and prices

Price is USD per 1M tokens, input / output.

| Tier | Claude | OpenAI | Price in / out | Suited to |
|---|---|---|---|---|
| Fast | Haiku 5.5 | GPT-6 Luna | $0.10 / $0.50 | search, renames, boilerplate |
| Balanced | Sonnet 5.5 | GPT-6.1 Sol | $2 / $10 | building a planned feature, tests |
| Strong | Opus 5.5 | GPT-6.1 Sol on xhigh | $4 / $20 (Opus) | UI, auth and payments, hard bugs, review |
| Frontier | Fable 5.1 | GPT-6 Astra | $10 / $50 | planning, security audits |

Notes:

- Three pairs cost the same. Opus has no same-price twin at OpenAI; Sol on xhigh is the closest match.
- The Claude Code aliases (`haiku`, `sonnet`, `opus`, `fable`) resolve to the current version of each tier, so the templates use aliases rather than version numbers. If a newer version than the one listed here exists, the alias already points at it; check whether its price changed.

## Price cliffs

- Haiku 5.5 costs $0.50 / $2.50 once a prompt is over 100K tokens (5x), cache reads included.
- OpenAI prompts over 272K input tokens cost 2x input and 1.5x output.
- Cached reads cost 0.05x on Opus and Sonnet, which is why losing the cache by switching models mid-task is expensive.

## The ten coding tasks, both stacks

| # | Task | Claude Code | Codex | Effort |
|---|---|---|---|---|
| 1 | Plan a feature | Fable | GPT-6 Astra | high |
| 2 | Build the feature | Sonnet | GPT-6.1 Sol | medium |
| 3 | Frontend UI | Opus | GPT-6.1 Sol | medium (Sol: xhigh) |
| 4 | Auth and payments | Opus | GPT-6.1 Sol | xhigh |
| 5 | Search the codebase | Haiku | GPT-6 Luna | low |
| 6 | Renames and boilerplate | Haiku | GPT-6 Luna | low |
| 7 | Write tests | Sonnet | GPT-6.1 Sol | low |
| 8 | Nasty bug | Opus | GPT-6.1 Sol | max |
| 9 | Security audit | Fable | GPT-6 Astra | xhigh |
| 10 | Code review | Opus | GPT-6.1 Sol | high (Sol: xhigh) |

- Task 3: Opus 5.5 led WebDev Arena on November 8, 2026 (score 1818); Fable 5.1 was fifth. Rankings move, so re-check before leaning on this.
- Task 4: never the fast tier, and always a review by a different model.
- Task 5: reading on Haiku costs about 40x less per token than on Opus.
- Task 6: keep the cheap model on mechanical edits and read the diff.

## Effort levels

- Claude 5.x and GPT-6 models take `low`, `medium`, `high`, `xhigh` and `max`. Luna also takes `none`.
- In Claude Code, the `effortLevel` setting takes `low` to `xhigh` (no `max`); `/effort` and subagent frontmatter also accept `max`.
- Unset, Claude Code runs Opus on medium.

## The two-dial grid

| | Low effort | High effort |
|---|---|---|
| Cheap model (Haiku, Luna) | search the codebase, renames, boilerplate | summarise a long log, sort many files |
| Top model (Fable, Astra) | a quick second opinion on a plan | plan a feature, security audit, the bug nobody can find |
