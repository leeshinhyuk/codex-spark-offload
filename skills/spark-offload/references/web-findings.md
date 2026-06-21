# Web Findings Behind Spark Offload

Research date: 2026-06-21.

## Official anchors

- OpenAI Codex subagents docs: subagents can run specialized agents in parallel and custom agents can use different model configurations. The docs also state that Codex only spawns subagents when explicitly asked, and each subagent consumes its own model/tool work.
- OpenAI Codex subagent concepts docs: parallel agents help keep noisy exploration, tests, logs, and summaries out of the main thread; read-heavy tasks such as exploration, tests, triage, and summarization are recommended starting points. The same docs say `gpt-5.3-codex-spark` is for near-instant text-only iteration when latency matters more than broader capability.
- OpenAI Codex skills docs: skills are reusable workflow packages and can be invoked explicitly with `$skill-name` or implicitly from the skill description.
- OpenAI Codex changelog: GPT-5.3-Codex-Spark is a research-preview fast model with separate model-specific limits during preview and a 128k text-only context window at launch.

## Similar public examples found

- `KingGyuSuh/awesome-codex-spark`: a Codex plugin that delegates concrete Browser Use and Computer Use tasks to GPT-5.3-Codex-Spark with structured handoffs and auditable traces. Useful pattern: structured handoff sections and explicit model-unavailable failure.
- `am-will/codex-skills/parallel-task-spark` on Tessl: a plan-file orchestrator that delegates task waves to parallel Sparky subagents. Useful pattern: dependency-aware waves and parent coordination.
- `agent-offload`: a CLI-based offload tool that installs a skill and can route delegated work to a `codex-spark` profile. Useful pattern: delegated runs produce an output summary that the host agent reviews.
- `VoltAgent/awesome-codex-subagents`: a collection of Codex custom agents that uses `~/.codex/agents/` and `.codex/agents/`, including examples pinning `gpt-5.3-codex-spark`.
- `Agentic Codex Dev Reviewer` skill: uses Spark or mini models for read-only exploration, docs checks, and bounded cleanup while reserving stronger models for final review.

## Design implications

- This skill should not try to replace the official subagent mechanism or run an external orchestrator.
- Explicit `$spark-offload` invocation should be treated as the user's request for delegation/parallelism.
- Spark is best used for cheap variants, first passes, and bounded execution.
- The parent agent must verify all Spark outputs before citation, integration, or final recommendation.
- A small number of opinionated custom agents is better than a broad taxonomy.
