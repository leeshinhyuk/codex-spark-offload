# Verification Contract

Use this before accepting Spark output into the final answer, patch, or plan.

## Acceptance Rules

Accept Spark output only when it has:

- A bounded task and scope.
- Confidence labels: `known`, `likely`, `uncertain`, or `blocked`.
- Evidence handles for claims the parent may rely on.
- A verification path: command, test, source read, screenshot, diff inspection, or manual check.
- Explicit write ownership when files changed.

Reject or narrow-retry when:

- It gives conclusions without evidence.
- It synthesizes broad strategy instead of returning observations or candidates.
- It touches files outside scope.
- It hides uncertainty.
- It claims source support from search snippets or titles.

## Parent Verification By Output Type

| Spark output | Parent must verify |
| --- | --- |
| Code candidate | inspect diff/sketch, check fit with project constraints, run relevant tests where practical |
| Codebase map | open cited files and verify symbols, entrypoints, and ownership |
| Log/CI triage | compare against raw log lines and rerun the smallest useful command |
| PDF/document extraction | spot-check source pages or original files |
| Research/source leads | open/read sources before citing or deciding |
| UI/browser observation | verify visible state, screenshot note, URL, and non-destructive action scope |

## Responsibility Rule

Spark can reduce search and variation cost. It cannot transfer accountability.

The parent agent owns:

- final architecture,
- final recommendation,
- final patch integration,
- security or safety posture,
- high-stakes judgments,
- final user-facing confidence.
