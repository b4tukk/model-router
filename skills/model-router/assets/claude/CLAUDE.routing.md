## Model routing
- Search and lookups → code-searcher subagent (Haiku, low)
- Renames, boilerplate, mechanical edits → quick-editor subagent (Haiku, low). Read the diff afterwards.
- Build a planned feature → implementer subagent (Sonnet, medium)
- Tests → test-runner subagent (Sonnet, low)
- UI, auth & payments, hard bugs → this session on Opus (xhigh for auth & payments; max only when stuck)
- Plans and security audits → Fable (/model fable; high, xhigh for audits)
- Code review → reviewer subagent (Opus, high). Never review with the model that wrote the code: if Opus wrote it, review with Fable instead.
