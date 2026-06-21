---
name: spark-offload
description: "Delegate low-responsibility Codex work to GPT-5.3-Codex-Spark subagents while the main agent handles planning, verification, integration, and final judgment. Use when the user explicitly invokes $spark-offload, asks to use Spark for bounded subtasks, wants many code/design candidates, repetitive document/PDF/artifact transformations, broad-but-shallow scouting, evidence extraction, log/test triage, or says subagent/parallel delegation is allowed. Do not use Spark for final architecture, deep synthesis, security verdicts, high-stakes decisions, or unreviewed code integration."
---

# Spark Offload

Use this skill to spend GPT-5.3-Codex-Spark on work that benefits from speed, parallelism, and cheap iteration. The main agent remains accountable for requirements, decomposition, verification, integration, and final decisions.

The governing rule: Spark may produce cheap, inspectable subproducts; the main agent must verify and decide.

Explicit `$spark-offload` invocation is user authorization to use Spark subagents and parallel delegation for this turn, subject to the current runtime tools and safety policy.

## Grounding

This skill is based on the documented Codex pattern of subagents plus custom agents:

- Codex subagents can run specialized agents in parallel and collect consolidated results.
- Custom agent TOML files can pin `model` and `model_reasoning_effort`.
- `gpt-5.3-codex-spark` is appropriate when latency matters more than breadth/depth.
- Subagents cost extra tokens and can be wrong; treat Spark output as raw material.

Read `references/web-findings.md` when you need the research basis or comparable public examples.
Read `references/routing-matrix.md` when delegation boundaries are unclear.
Read `references/verification-contract.md` before accepting Spark output for a final answer or patch.

## Delegation Rule

Prefer Spark offload when all are true:

1. The subtask is concrete and independently checkable.
2. A wrong answer is cheap to discard.
3. The output can be summarized as findings, candidates, diffs, or a bounded patch.
4. The main agent can verify before relying on it.

Do not offload:

- Final architecture, release, legal, financial, medical, security, or safety decisions.
- Cross-cutting edits without clear file ownership.
- Tasks requiring broad long-context synthesis or nuanced prioritization, except for raw evidence extraction.
- Anything the main agent cannot inspect or validate.

## Responsibility Ladder

Use this ladder before delegation:

| Tier | Spark authority | Examples | Main-agent duty |
| --- | --- | --- | --- |
| Green | Can execute bounded work | repetitive docs/PDF cleanup, fixtures, formatting checks, log summaries | inspect result and run obvious checks |
| Yellow | Can produce candidates or scouting notes | implementation variants, codebase map, source/repo leads, UI copy | verify evidence, select, and integrate |
| Orange | Evidence extraction only | broad research, large codebase understanding, exam/question analysis, product/game strategy | redo synthesis and judgment in the main model |
| Red | No delegation | final architecture, security verdict, financial/legal/medical choice, release decision | keep in main thread or expert review |

## Good Spark Work

Use one or more Spark subagents for:

- Repetitive mechanical edits over disjoint files.
- Generating multiple code candidates, implementation sketches, tests, names, or UI copy variants.
- Broad shallow codebase scouting with file and symbol references.
- Log, test, CI, stack trace, or benchmark-output triage.
- Comparing small alternatives against explicit criteria.
- Drafting docs, comments, changelog entries, fixtures, or migration notes for review.
- Producing throwaway prototypes or scratch patches that the main agent may reject.
- Extracting facts from repeated PDFs, documents, slides, logs, or generated artifacts.
- Gathering research/source/repo leads for later main-agent verification.

## Agent Selection

If the runtime supports direct model override, spawn subagents with:

- `model`: `gpt-5.3-codex-spark`
- `reasoning_effort`: `low` for trivial repetition, `medium` for code candidates or triage, `high` only when Spark must trace a nontrivial local path.

If custom agents are available, prefer these names:

- `spark_scout`: read-only exploration, mapping, search, log/test triage.
- `spark_candidate`: multiple code or design candidates; may edit only an explicitly assigned scratch or disjoint write scope.
- `spark_repeater`: repetitive transformations, fixture generation, renames, or mechanical cleanup.
- `spark_evidence`: evidence extraction from sources, documents, logs, questions, or repo slices; no final synthesis.

Use built-in `explorer` or `worker` with `model = "gpt-5.3-codex-spark"` when the custom names are not loaded.

## Prompt Shape

Every Spark handoff must include:

- `Task`: one concrete outcome.
- `Scope`: exact files, commands, URLs, logs, or allowed search space.
- `Allowed writes`: `none`, `scratch only`, or exact disjoint file paths.
- `Output`: required summary shape.
- `Stop condition`: when to stop instead of improvising.
- `Confidence`: require `known`, `likely`, `uncertain`, or `blocked`.
- `Evidence`: require raw support such as file path, line, command output, URL, screenshot note, or exact observed text when relevant.

Template:

```text
Use GPT-5.3-Codex-Spark for this low-risk subtask.
Task: <one concrete task>
Scope: <files/commands/logs/URLs>
Allowed writes: <none|scratch only|exact files>
Output: <bullets/table/diff summary/candidate list>
Stop condition: stop and report blocked if <condition>
Confidence: label each claim or candidate known/likely/uncertain/blocked.
Evidence: include raw support for every claim the parent may rely on.
Do not make final decisions. The parent agent will verify and integrate.
```

## Parallel Patterns

Use parallel Spark agents when work naturally separates:

- Candidate fanout: spawn 2-4 agents, each with a different implementation angle.
- File sharding: one agent per disjoint file group.
- Review sharding: one agent checks tests, one docs, one edge cases.
- Search fanout: one agent maps source code, one checks docs, one checks logs.
- Evidence fanout: one agent extracts facts from documents, one extracts code references, one gathers external leads.

Keep batches small by default. Start with 2-4 agents; exceed that only when the user asks for breadth or the work is highly mechanical.

## Main-Agent Responsibilities

The main agent must:

1. Decompose tasks so Spark agents do not overlap destructively.
2. Keep doing non-overlapping critical-path work while subagents run.
3. Review returned files, diffs, claims, and commands before use.
4. Reject or rerun weak Spark outputs without preserving bad assumptions.
5. Integrate only the best verified result.
6. Tell the user when Spark results were used and what was verified.

Never present Spark output as final just because it is fast. Treat it as cheap search, cheap variation, or cheap first-pass execution.

Reject Spark output by default when it lacks evidence handles, confidence labels, or a verification path.

## Failure Handling

If Spark is unavailable, queued, or blocked:

- Fall back to `gpt-5.4-mini` for light subagent work when available.
- Otherwise do the work in the main thread and mention the fallback.

If Spark output is shallow, contradictory, or overconfident:

- Do not patch around it blindly.
- Ask a narrower Spark follow-up only if cheap and useful.
- Otherwise verify directly with code, tests, docs, or the main model.

## Final Reporting

When this skill materially affects the work, include a compact note:

- Which subtasks were offloaded.
- Which Spark results were accepted, rejected, or modified.
- What verification was run by the main agent.
