#!/usr/bin/env python3
"""Generate a local Spark offload routing profile from Codex thread metadata.

The script is privacy-first by default:
- uses aggregate thread metadata from state_*.sqlite,
- does not print thread titles unless --include-titles is set,
- writes a local profile only when --write-local-profile is provided.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sqlite3
import textwrap
from pathlib import Path


CATEGORIES = [
    (
        "docs_artifacts",
        re.compile(r"PPT|PDF|문서|한글|hwpx|보고서|브리핑|slide|deck|docx", re.I),
        "Strong Spark fit: repetitive extraction, formatting, drafts, and spot-checkable artifacts.",
    ),
    (
        "logs_build_ci",
        re.compile(r"로그|빌드|에러|CI|test|테스트|install|설정|연결|server|runtime", re.I),
        "Strong Spark fit for triage; parent verifies raw logs and commands.",
    ),
    (
        "codebase_scout",
        re.compile(r"코드|프로젝트|repo|repository|구조|파악|검토|평가|entrypoint|manifest", re.I),
        "Conditional: Spark maps evidence; parent performs architecture judgment.",
    ),
    (
        "research",
        re.compile(r"조사|찾아|논문|오픈소스|유사|인터넷|자료|research|리서치|비교|추천|사례", re.I),
        "Conditional: Spark gathers leads; parent opens sources and synthesizes.",
    ),
    (
        "frontend_game_design",
        re.compile(r"게임|웹|앱|페이지|프론트|디자인|UI|UX|browser|canvas", re.I),
        "Conditional: Spark generates candidates and QA notes; parent decides direction.",
    ),
    (
        "batch_items",
        re.compile(r"문항|수능|KICE|지구과학|생명|미적분|기출|선지|발문|난이도|각각|모든", re.I),
        "Conditional: Spark extracts observable structure; parent judges quality.",
    ),
    (
        "high_stakes",
        re.compile(r"투자|주가|트레이딩|보안|security|법률|의학|세금|release|실거래|주문", re.I),
        "Weak/limited: Spark may extract low-level evidence only; parent decides.",
    ),
]


def newest_state_db(codex_home: Path) -> Path:
    candidates = sorted(codex_home.glob("state_*.sqlite"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise SystemExit(f"No state_*.sqlite found under {codex_home}")
    return candidates[0]


def load_threads(db_path: Path) -> list[sqlite3.Row]:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    try:
        return list(
            con.execute(
                """
                select id, title, model, reasoning_effort, tokens_used, created_at, updated_at
                from threads
                where coalesce(tokens_used, 0) > 0
                """
            )
        )
    finally:
        con.close()


def classify(title: str) -> list[tuple[str, str]]:
    hits = []
    for name, regex, note in CATEGORIES:
        if regex.search(title or ""):
            hits.append((name, note))
    return hits or [("other", "No obvious Spark routing signal.")]


def summarize(rows: list[sqlite3.Row]) -> tuple[dict[str, dict[str, float]], dict[str, list[str]]]:
    summary: dict[str, dict[str, float]] = {}
    examples: dict[str, list[str]] = {}
    for row in rows:
        title = row["title"] or ""
        minutes = max(0.0, ((row["updated_at"] or 0) - (row["created_at"] or 0)) / 60.0)
        for category, _ in classify(title):
            bucket = summary.setdefault(category, {"threads": 0, "tokens": 0, "minutes": 0.0})
            bucket["threads"] += 1
            bucket["tokens"] += row["tokens_used"] or 0
            bucket["minutes"] += minutes
            examples.setdefault(category, [])
            if len(examples[category]) < 5:
                examples[category].append(title[:160].replace("\n", " "))
    return summary, examples


def recommendation(category: str) -> str:
    mapping = {
        "docs_artifacts": "Default to Spark for extraction/repetition; parent spot-checks.",
        "logs_build_ci": "Use Spark early for triage; parent verifies raw logs and reruns.",
        "codebase_scout": "Use Spark only for file maps and evidence handles; parent synthesizes architecture.",
        "research": "Use Spark only for lead generation and narrow extraction; parent opens sources and cites.",
        "frontend_game_design": "Use Spark for variants and QA shards; parent chooses direction.",
        "batch_items": "Use Spark for observable per-item extraction; parent judges quality/difficulty.",
        "high_stakes": "Do not delegate decisions; Spark may extract low-level evidence only.",
        "other": "No default rule; use the base routing matrix.",
    }
    return mapping.get(category, "Use the base routing matrix.")


def render_profile(summary: dict[str, dict[str, float]], include_titles: bool, examples: dict[str, list[str]]) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    rows = sorted(summary.items(), key=lambda kv: kv[1]["tokens"], reverse=True)
    lines = [
        "# Local Spark Offload Profile",
        "",
        f"Generated: {now}",
        "",
        "This file is local tuning material. Review it before sharing or committing.",
        "",
        "## Aggregate Signals",
        "",
        "| Category | Threads | Relative tokens | Minutes | Recommendation |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    total_tokens = max(1, sum(int(v["tokens"]) for v in summary.values()))
    for category, data in rows:
        pct = int(round((data["tokens"] / total_tokens) * 100))
        lines.append(
            f"| {category} | {int(data['threads'])} | {pct}% | {data['minutes']:.1f} | {recommendation(category)} |"
        )
    lines.extend(
        [
            "",
            "## Local Rules",
            "",
            "- Keep Spark on low-responsibility subproducts.",
            "- Require evidence handles and confidence labels.",
            "- Main model performs synthesis, prioritization, final decisions, and patch integration.",
            "- Do not use Spark for high-stakes decisions except narrow evidence extraction.",
        ]
    )
    if include_titles:
        lines.extend(["", "## Example Titles", ""])
        for category, titles in examples.items():
            lines.extend([f"### {category}", ""])
            for title in titles:
                lines.append(f"- {title}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    parser.add_argument("--db", help="Explicit state_*.sqlite path")
    parser.add_argument("--include-titles", action="store_true", help="Include example thread titles in output")
    parser.add_argument("--write-local-profile", help="Write generated markdown to this path")
    args = parser.parse_args()

    codex_home = Path(args.codex_home).expanduser()
    db_path = Path(args.db).expanduser() if args.db else newest_state_db(codex_home)
    rows = load_threads(db_path)
    summary, examples = summarize(rows)
    profile = render_profile(summary, args.include_titles, examples)

    header = textwrap.dedent(
        f"""\
        Analyzed {len(rows)} non-empty Codex threads from {db_path}
        Titles included: {'yes' if args.include_titles else 'no'}
        """
    )
    print(header)
    print(profile)

    if args.write_local_profile:
        output = Path(args.write_local_profile).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(profile)
        print(f"Wrote local profile: {output}")


if __name__ == "__main__":
    main()
