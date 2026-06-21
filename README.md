# Codex Spark Offload

`spark-offload` is a Codex skill for delegating low-responsibility work to GPT-5.3-Codex-Spark subagents while the main agent keeps responsibility for planning, verification, integration, and final judgment.

The core idea is not "use the fast model for everything easy." It is a supervisor-worker pattern:

```text
Spark produces cheap, inspectable subproducts.
The main model verifies raw evidence, rejects weak output, and integrates only what survives review.
```

It is useful for:

- generating several code or design candidates,
- repetitive mechanical edits over disjoint files,
- broad but shallow codebase scouting,
- log, test, or CI triage,
- quick documentation, fixture, or migration-note drafts.
- first-pass extraction over repeated documents, PDFs, slides, or batch artifacts.

It is not intended for final architecture, security verdicts, high-stakes decisions, deep synthesis, or unreviewed code integration.

## Responsibility Ladder

| Tier | Spark role | Good examples | Parent responsibility |
| --- | --- | --- | --- |
| Green | Direct low-risk worker | repetitive docs/PDF cleanup, fixture drafts, formatting checks, log summaries | inspect output and run obvious checks |
| Yellow | Candidate or scout | code variants, codebase map, repo/source leads, UI copy options | verify references, choose, and integrate |
| Orange | Evidence extractor only | broad research, large codebase understanding, exam/question analysis, product/game strategy | redo synthesis with the main model |
| Red | Do not delegate | final architecture, security verdicts, financial/legal/medical decisions, release decisions | main model or domain expert only |

This distinction matters. Many tasks look "parallelizable" but still require high-quality synthesis. In those cases Spark should only return raw observations, leads, or candidates.

## Contents

```text
skills/spark-offload/
  SKILL.md
  agents/openai.yaml
  references/
agents/
  spark-candidate.toml
  spark-evidence.toml
  spark-repeater.toml
  spark-scout.toml
scripts/
  analyze-codex-sessions.py
examples/
  routing-profiles/
```

## Install

Copy the skill folder into your Codex user skills directory:

```bash
mkdir -p ~/.codex/skills ~/.codex/agents
cp -R skills/spark-offload ~/.codex/skills/
cp agents/spark-*.toml ~/.codex/agents/
```

Restart Codex or start a new session if the skill or custom agents do not appear immediately.

## Optional Personalization

You can generate a local routing profile from your own Codex session metadata:

```bash
python scripts/analyze-codex-sessions.py --codex-home ~/.codex
```

To write a local-only profile into an installed skill:

```bash
python scripts/analyze-codex-sessions.py \
  --codex-home ~/.codex \
  --write-local-profile ~/.codex/skills/spark-offload/references/local-session-routing.md
```

The analyzer uses aggregate thread metadata by default and does not print thread titles unless you pass `--include-titles`. Do not commit generated local profiles unless you have reviewed them for private data.

## Usage

Invoke the skill explicitly:

```text
Use $spark-offload to generate three alternative implementations for this helper. Keep writes disabled and summarize tradeoffs.
```

Explicit invocation is intended to mean that Spark subagents and parallel delegation are allowed for that turn, within the current runtime's available tools and safety policy.

## Safety Model

Spark output should be treated as cheap search, cheap variation, or a first pass. The parent agent must verify returned claims, inspect patches, run relevant checks, and make the final decision.

Minimum acceptance contract:

- Claims need raw evidence: file path, line, command output, URL, or visible observation.
- Candidates need tradeoffs, risk, and a verification path.
- Writes need exact ownership and parent review.
- Anything without confidence labels is incomplete.

## License

MIT
