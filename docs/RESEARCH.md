# Research Notes

Research date: 2026-06-21.

## Bottom Line

The safest architecture is not "Spark handles easy tasks." The stronger framing is:

> Spark handles low-responsibility, inspectable subproducts; the main model verifies and integrates.

This keeps Spark useful for latency, breadth, and repetition while avoiding the failure mode where a fast model performs deep synthesis that actually needs the stronger main model.

## Sources Used

- [OpenAI Codex Subagents docs](https://developers.openai.com/codex/subagents): Codex supports spawning specialized agents in parallel and custom agents with different model configurations.
- [OpenAI Codex Subagent concepts docs](https://developers.openai.com/codex/concepts/subagents): subagents help move noisy exploration, tests, logs, and summaries out of the main thread and can save time when work is independently parallelizable.
- [OpenAI GPT-5.3-Codex-Spark announcement](https://openai.com/index/introducing-gpt-5-3-codex-spark/): Spark is a research-preview real-time coding model with 128k text-only context at launch, separate limits, and a lightweight working style optimized for targeted edits and rapid iteration.
- [Cerebras Spark best-practices guide](https://www.cerebras.ai/blog/codex-spark-best-practices): Spark's speed rewards deliberate, bounded prompts and tight steering; long complex delegation is a worse fit than focused interaction.
- [`KingGyuSuh/awesome-codex-spark`](https://github.com/KingGyuSuh/awesome-codex-spark): a narrow Spark delegation plugin using structured handoffs and auditable traces for Browser/Computer Use.
- [`Sunwood-ai-labs/codex-spark-eclipse-legion`](https://github.com/Sunwood-ai-labs/codex-spark-eclipse-legion): a Spark subagent skill emphasizing bounded delegation, ownership, and manager/operator split.
- OpenAI Codex GitHub issues around custom agent model selection, including [#11795](https://github.com/openai/codex/issues/11795) and [#14671](https://github.com/openai/codex/issues/14671): useful as limitation evidence that per-agent model behavior can be version-dependent, so model-unavailable or model-inheritance fallback should be explicit.

## Design Decisions

| Finding | Decision |
| --- | --- |
| Official docs support subagents/custom agents and identify exploration/tests/log analysis as good starting points. | Keep Spark offload centered on bounded subproducts. |
| Spark is optimized for real-time targeted work, not necessarily long-horizon synthesis. | Add responsibility ladder and orange/red categories. |
| Public examples emphasize structured handoffs and auditable traces. | Require task/scope/writes/output/stop/confidence/evidence sections. |
| Model availability and per-agent model behavior may vary by Codex version. | Keep fallback behavior explicit and avoid silent success claims. |
| User/session workloads differ. | Add optional analyzer and local profile template, not mandatory personalization. |

## Limits

- No benchmark in this repo proves token or wall-clock savings. The architecture is evidence-informed, not empirically guaranteed.
- Spark availability is account/version dependent.
- Session analysis uses local metadata heuristics and should be treated as a tuning aid, not ground truth.
