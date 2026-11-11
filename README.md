# model-router

An agent skill that decides which AI model does which part of your work, before the work starts.

Start a project with it. It outlines the project, breaks it into phases, gives each phase the cheapest model that is good enough, runs each phase on that model, and passes a short handoff report between phases so the next model can continue without re-reading everything.

## How a project runs

1. **Outline** - what is being built, the constraints, and what "done" means.
2. **Phases** - each one sized by what it needs and what a silent mistake would cost.
3. **Merge** - neighbouring same-tier phases are combined, because every change of model has a cost. Switches happen only where they pay.
4. **Plan** - written to `.model-router/plan.md` and approved by you.
5. **Run** - each phase runs in a subagent on its model, so the main session stays small and its cache is never thrown away.
6. **Handoff** - each phase ends with a report of about 200 words in `.model-router/handoff/`: decisions, file paths, open risks, next step.
7. **Adjust** - remaining phases are re-sized as the project teaches you what is hard.

For a single task it asks the same question (what is the cheapest model that gets this right first time?), states the answer in one line, and starts the work on that model.

## The tiers

| Tier | Claude | OpenAI | Suited to |
|---|---|---|---|
| Fast | Haiku | Luna | research, search, renames, boilerplate, extraction |
| Balanced | Sonnet | Sol | building a planned feature, tests, drafting |
| Strong | Opus | Sol on xhigh | UI, auth and payments, hard bugs, review |
| Frontier | Fable | Astra | planning, architecture, security audits |

## Also included

- **Usage audit** for when a limit runs out too fast.
- **Cost estimate** per model, with long-context price cliffs and cache discounts applied.
- **Routing setup**: five Claude Code subagents pinned to their own model and effort, a routing block for `CLAUDE.md`, and matching Codex configs.

## Install

Copy the skill folder into your skills directory:

```bash
cp -r skills/model-router ~/.claude/skills/model-router
```

On Windows PowerShell:

```powershell
Copy-Item -Recurse skills\model-router $HOME\.claude\skills\model-router
```

Then ask things like:

- "I'm starting a new project: an invoicing app with Stripe. Plan it and decide which model does what."
- "Which model should I use to refactor our Stripe webhook handler?"
- "My usage is running out too fast, what am I doing wrong?"
- "What would a 150K-token review cost on each model?"

## Layout

```
skills/model-router/
├── SKILL.md                      project workflow, task routing, traps
├── references/
│   ├── routing-tables.md         default model and effort per task type
│   ├── pricing.md                dated prices and models
│   ├── usage-audit.md            how to diagnose wasted usage
│   ├── claude-code-setup.md      how to install the Claude Code setup
│   └── codex-setup.md            how to install the Codex setup
├── scripts/
│   └── estimate_cost.py          cost per model for given token counts
├── assets/
│   ├── templates/                plan and handoff templates
│   ├── prices.json               price snapshot read by the script
│   ├── claude/                   subagents, CLAUDE.md block, settings
│   └── codex/                    config, profiles, agents
└── evals/                        test cases
```

## Keeping it current

Model versions and prices change. Prices were checked on November 9, 2026 and live in two files that should be updated together: `references/pricing.md` and `assets/prices.json`. The subagent templates use tier aliases (`haiku`, `sonnet`, `opus`, `fable`), so they follow new versions without edits.

The tier assignments are a starting point, not a benchmark: test them on your own work.

## License

MIT. See [LICENSE](LICENSE).
