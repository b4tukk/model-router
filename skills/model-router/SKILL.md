---
name: model-router
description: Start a project or a task by deciding which AI model does which part of it. Breaks a project into phases, assigns each phase the cheapest model and effort level that is good enough, runs each phase on that model, and passes a short handoff report between phases so the next model can continue without re-reading everything. Use this at the start of any new project, feature or multi-step job, whenever the user asks which model to use for a task, wants to cut token cost or make a usage limit last longer, asks about effort levels, compares Haiku / Sonnet / Opus / Fable or Luna / Sol / Astra, asks what a task will cost, or wants subagents pinned to different models - even if they never say "routing" or "switch".
---

# Model router

Decide which model does which work before the work starts, then run each piece on the cheapest model that will get it right the first time.

There are two modes. Pick by the size of the request:

- **Project mode** - a new project, feature or anything with several distinct stages. Follow "Running a project" below.
- **Task mode** - one self-contained job. Follow "Running a single task".

Model names and prices go stale quickly. The dated numbers are in `references/pricing.md` and `assets/prices.json`.

## The four tiers

| Tier | Claude alias | OpenAI | Suited to |
|---|---|---|---|
| Fast | `haiku` | Luna | research, reading, searching, mechanical edits, bulk extraction |
| Balanced | `sonnet` | Sol | executing a clear plan, tests, routine drafting |
| Strong | `opus` | Sol on xhigh | UI, money and auth code, hard bugs, review |
| Frontier | `fable` | Astra | planning, architecture, security audits |

For a task type not obvious from this table, read `references/routing-tables.md`. If the user names a model that is not listed here, ask which tier it belongs to rather than guessing, and add it to `assets/prices.json` if they want it kept.

## Running a project

The point of this workflow is that the expensive model only touches the parts that need it, and that changing models costs almost nothing. Both depend on keeping the main session small and passing short written handoffs instead of long conversation history.

### 1. Outline

Agree the outline with the user before anything else: what is being built, for whom, the constraints (stack, deadline, budget), and what "done" means. Ask only what you cannot infer. Keep it to a few lines; this is a brief, not a specification.

### 2. Break into phases and size each one

List the phases in order. For each, decide:

- **What it needs** - is it reading and gathering, executing a known plan, or making judgement calls?
- **What a silent mistake would cost** - money, security, data loss, or rework of later phases pushes the tier up.
- **Model and effort** - the cheapest tier that satisfies both answers.

A typical shape, to adapt rather than copy:

| Phase | Tier | Why |
|---|---|---|
| Preliminary research, reading docs, surveying the codebase | Fast | The answers already exist; this is gathering |
| Architecture and plan | Frontier | Errors here are inherited by every later phase |
| Scaffolding, boilerplate | Fast | Mechanical |
| Feature implementation from the plan | Balanced | The decisions are already made |
| Auth, payments, data migrations, UI polish | Strong | Quiet bugs are expensive |
| Tests | Balanced | Clear target, fast feedback |
| Review | Strong or Frontier | A different model from the one that wrote the code |

### 3. Merge phases to limit switches

Every change of model has a cost: a handoff must be written and the next model must read it and re-open the files it needs. So switch only where it pays.

- Merge neighbouring phases that land on the same tier into one.
- Fold a small phase into its neighbour instead of switching for it. Starting a subagent has a fixed overhead of its own, whatever the model, so a tiny phase run separately can cost more than doing it on a pricier model in place. If a phase is only a few tool calls, the handoff costs more than the saving; let the current model do it, unless the risk calls for a stronger one.
- Order phases so that same-tier work sits together where the dependencies allow.
- Moving up for risk is always justified. Moving down is only worth it for a sizeable block of work.

A small project often ends up as three or four phases. That is the right outcome, not a shortcut.

### 4. Write the plan and get approval

Write the plan to `.model-router/plan.md` using `assets/templates/plan.md`. Show the user the phase table and wait for approval before starting, since this fixes where their usage goes.

### 5. Run each phase on its model

The main session is the coordinator. It holds the plan and the handoffs, and nothing else, so it stays cheap whatever model it is on.

For each phase, in order:

1. Start a subagent on the phase's model and effort. In Claude Code, use the matching pinned subagent if the project has one (see "Setting up routing"), otherwise pass the model when spawning the subagent.
2. Give it a brief containing only: the phase goal, the "done when" line, the previous handoff, and the file paths it needs. Do not paste the conversation or the whole plan.
3. Tell it to finish by writing its handoff (step 6) and to return only a few lines.
4. Mark the phase done in `plan.md`.

A subagent has its own small context, so the main session's cache is never invalidated and no history is re-read at a new model's price. This is why delegating is preferred over switching the session model.

Some phases need the user in the loop (shaping the architecture, reviewing UI). Those run in the main session. If the main session is on the wrong model for that phase, write the handoff first, then ask the user to switch with `/model <alias>` and `/effort <level>` at that boundary, ideally in a fresh session that starts from the plan and the latest handoff. You cannot change the session's model yourself; say so plainly rather than pretending the switch happened.

### 6. Handoff report

Each phase ends by writing `.model-router/handoff/NN-phase-name.md` from `assets/templates/handoff.md`. The next model reads this instead of the history, so its length is paid for on every later phase that reads it.

- Under about 200 words. State decisions and results, not how you got there.
- Point to files by path instead of quoting their contents.
- When the phase's result is itself a long list (rules, findings, options), write that list to its own file and point to it from the handoff, so readers that do not need the detail do not pay for it.
- Record what the next phase must not redo or re-decide.
- List open questions and known risks, because those are what a fresh model cannot recover on its own.
- Each handoff replaces the need to read earlier ones. Carry forward what still matters and drop the rest.

### 7. Adjust as you learn

Re-size the remaining phases after each one. If a phase's model fails with full context, move that phase up one tier after a single failed attempt and note it in the plan. If a phase turned out simpler than expected, move the similar later phases down.

## Running a single task

1. Ask the routing question: what is the cheapest model and effort that will get this right first time? Use the two questions below, or `references/routing-tables.md` for common task types.
2. State the decision in one line: model, effort, reason.
3. Start the work on that model. If it differs from the current session's model, delegate to a subagent on the chosen model. If the task is only a few tool calls, do it in the current session; a handoff would cost more than it saves.
4. If the task needs the main session on another model, tell the user which `/model` and `/effort` to set, and to do it before starting rather than midway.

The two questions:

1. **What does a silent mistake cost?** Money, security, data loss or a decision someone will act on means strong or frontier, however small the task looks. For auth and payment code specifically, use Opus on xhigh.
2. **Is it mechanical or does it need judgement?** Reading, moving and repeating is fast-tier work. Deciding is not.

## Two dials: model and effort

Effort controls how many tokens the model spends thinking before it answers. It is usually the better first lever.

- Turn effort up first when the answer was shallow.
- Change the model when it had the full context and was still wrong.
- A cheap model on high effort suits bulk work that needs care.
- Step back down afterwards. Leaving a session on max effort or the frontier model after the hard part is over is the most common way the savings disappear.

## Three traps that make routing cost more

1. **Paying twice after a cheap fail.** If the fast model fails, the user pays for that try and then for the stronger model's. Route by risk up front, and escalate after one failed try, not three.
2. **Switching models mid-task kills the cache.** The prompt cache is per model, so after a mid-conversation switch the whole history is re-read at full price. Switch between phases, or delegate to a subagent.
3. **Price cliffs.** Some models cost several times more per token once the prompt passes a size threshold (see `references/pricing.md`). Judge cost per solved task, not price per token.

## Other things this skill covers

- **Estimating cost.** Run `python scripts/estimate_cost.py --input <tokens> --output <tokens>` to compare every model, or add `--model` and `--cached`. Present the result as a rough comparison from a dated snapshot.
- **Diagnosing wasted usage.** When a limit runs out too fast, read `references/usage-audit.md` and find where the tokens go before recommending anything.
- **Setting up routing.** To install pinned subagents so phases can be delegated by name, read `references/claude-code-setup.md` (templates in `assets/claude/`) or `references/codex-setup.md` (templates in `assets/codex/`). Merge into existing config instead of overwriting, and confirm before touching anything under the user's home directory.
- **Review.** Never have the model that wrote a change review it. Review normally goes to Opus because Sonnet wrote the code; when Opus wrote it, send the review to Fable.

## Honesty about the numbers

The tier assignments are a reasonable starting point, not a benchmark. Say so when the user treats them as fact, and adjust the plan to what actually happens in their project.
