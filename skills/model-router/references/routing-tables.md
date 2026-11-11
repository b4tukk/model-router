# Routing tables

Defaults for common task types. Use them to size a project phase or route a single task. They are starting points, not measured results.

## Coding work

| Task | Model | Effort | Why |
|---|---|---|---|
| Plan a feature | fable | high | Mistakes here are the most expensive to undo |
| Build the planned feature | sonnet | medium | With a plan, the balanced tier is enough |
| Frontend UI | opus | medium | Strongest at web UI work |
| Auth and payments | opus | xhigh | A quiet bug costs money and trust |
| Search the codebase | haiku | low | Reading is cheap work |
| Renames and boilerplate | haiku | low | Mechanical edits; read the diff afterwards |
| Write tests | sonnet | low | Clear target, fast feedback |
| Nasty bug | opus | max | Pay for thinking only when stuck |
| Security audit | fable | xhigh | Use the best available |
| Code review | opus | high | Must differ from the model that wrote the code; Fable if Opus wrote it |

## Work that is not code

| Task | Model | Effort | Why |
|---|---|---|---|
| Preliminary research, gathering sources | haiku | low | Collecting, not judging |
| Summarise, extract, classify, reformat | haiku | low | The answer is already in the input |
| Long or messy input (logs, many files) | haiku | high | Cheap tokens, but give it room to be careful |
| Draft an email, doc or slides from an outline | sonnet | medium | Structure is given; it needs fluent execution |
| Research synthesis, analysis that needs judgement | opus | high | Weighing conflicting sources is not mechanical |
| Strategy, or anything legal or financial that will be acted on | fable | high | Errors compound downstream |
| Checking someone else's draft or analysis | opus | high | A different model from the one that produced it |

## Model and effort together

| | Low effort | High effort |
|---|---|---|
| Cheap model | search, renames, boilerplate | summarise a long log, sort many files |
| Top model | a quick second opinion on a plan | plan a feature, security audit, the bug nobody can find |
