# Codex Spark Offload

`spark-offload` is a Codex skill for delegating simple, repetitive, low-risk, or parallelizable work to GPT-5.3-Codex-Spark subagents while the main agent keeps responsibility for planning, verification, integration, and final judgment.

It is useful for:

- generating several code or design candidates,
- repetitive mechanical edits over disjoint files,
- broad but shallow codebase scouting,
- log, test, or CI triage,
- quick documentation, fixture, or migration-note drafts.

It is not intended for final architecture, security verdicts, high-stakes decisions, or unreviewed code integration.

## Contents

```text
skills/spark-offload/
  SKILL.md
  agents/openai.yaml
  references/
agents/
  spark-candidate.toml
  spark-repeater.toml
  spark-scout.toml
```

## Install

Copy the skill folder into your Codex user skills directory:

```bash
mkdir -p ~/.codex/skills ~/.codex/agents
cp -R skills/spark-offload ~/.codex/skills/
cp agents/spark-*.toml ~/.codex/agents/
```

Restart Codex or start a new session if the skill or custom agents do not appear immediately.

## Usage

Invoke the skill explicitly:

```text
Use $spark-offload to generate three alternative implementations for this helper. Keep writes disabled and summarize tradeoffs.
```

Explicit invocation is intended to mean that Spark subagents and parallel delegation are allowed for that turn, within the current runtime's available tools and safety policy.

## Safety Model

Spark output should be treated as cheap search, cheap variation, or a first pass. The parent agent must verify returned claims, inspect patches, run relevant checks, and make the final decision.

## License

MIT
