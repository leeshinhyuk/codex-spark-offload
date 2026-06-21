# Local Session Routing Example

Copy this file to:

```text
~/.codex/skills/spark-offload/references/local-session-routing.md
```

Then edit it for your own workload. Do not commit a filled local profile unless you have reviewed it for private data.

## My Strong Spark-Offload Patterns

| Pattern | Spark role | Parent verification |
| --- | --- | --- |
| Repeated PDF/document extraction | `spark_evidence` or `spark_repeater` | spot-check source pages |
| Repetitive generated artifact cleanup | `spark_repeater` | inspect diff/output |
| Log/build/CI triage | `spark_scout` | compare with raw logs and rerun |

## My Conditional Patterns

| Pattern | Spark may do | Spark may not do |
| --- | --- | --- |
| Broad research | source leads and narrow extraction | final synthesis or citation |
| Codebase understanding | file map and evidence handles | architecture decision |
| Product/game/design work | candidate variants | final direction |

## My Never-Offload Patterns

- Final architecture decisions.
- Security verdicts.
- High-stakes legal, medical, financial, or release decisions.
- Any work where I cannot inspect the raw evidence.
