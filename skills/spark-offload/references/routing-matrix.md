# Spark Offload Routing Matrix

Use this file when deciding whether to delegate to GPT-5.3-Codex-Spark.

## Strong Yes

| Work type | Why Spark fits | Required parent check |
| --- | --- | --- |
| Generate 3-5 implementation candidates | Wrong variants are cheap to discard | Pick one, inspect logic, run relevant tests |
| Summarize failing logs or CI output | Fast extraction from noisy text | Confirm against raw log lines |
| Search codebase for owners/call paths | Read-heavy and bounded | Open cited files and verify line refs |
| Create fixtures, examples, or docs drafts | Low-risk first-pass writing | Review semantics and style |
| Mechanical change over disjoint files | Parallelizable and easy to diff | Inspect diff and run formatting/tests |
| Extract repeated PDF/document fields | Repetitive and observable | Spot-check against source pages |

## Conditional

| Work type | Use Spark only if | Guardrail |
| --- | --- | --- |
| Small bug fix | The failure mode is already understood | Assign exact files and tests |
| Refactor | Files are disjoint and behavior is covered | One agent per ownership slice |
| Browser or computer-use QA | Action is read-only or explicitly approved | Require visible evidence and stop before irreversible actions |
| External research | Spark only gathers leads or extracts narrow facts | Parent opens/reads sources before citing or synthesizing |
| Large codebase understanding | Spark only maps files, entrypoints, and local evidence | Parent performs architecture judgment |
| Exam/question/artifact analysis | Spark only extracts observable structure | Parent performs final quality/difficulty/meaning judgment |

## No

| Work type | Reason |
| --- | --- |
| Final architecture choice | Needs broad context and tradeoff judgment |
| Deep synthesis or prioritization | Requires strong model judgment over many constraints |
| Security verdict | False negatives are costly |
| Legal/medical/financial/tax recommendation | High-stakes source and reasoning burden |
| Cross-module migration | Coordination overhead can exceed speed benefit |
| Unreviewed code integration | Spark output is not trusted by default |

## Candidate Fanout Template

For quick work, one Spark agent may generate several candidates. For better diversity, spawn 2-4 Spark agents and assign one angle per agent:

1. Minimal patch.
2. Cleaner abstraction.
3. Test-first or compatibility-focused patch.
4. Performance/simple-state variant, only if relevant.

Ask each agent to return:

- One candidate only when agents are split by angle; several candidates only when a single agent owns the whole fanout.
- Changed files or proposed diff.
- Why this variant is better in one sentence.
- Known tradeoffs.
- Exact verification command it ran or recommends.
- Confidence label.

The parent agent compares variants and may combine ideas, but must not merge a candidate without inspection.

## Repetition Template

For repetitive edits:

- Partition by file group.
- Give each agent exact file ownership.
- Tell agents they are not alone in the codebase and must not revert unrelated edits.
- Require a final file list and a short "no unrelated files touched" statement.

The parent agent reviews the aggregate diff and resolves inconsistencies.
