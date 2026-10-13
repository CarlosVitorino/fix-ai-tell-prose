#!/usr/bin/env python3
"""Tally reviewer decisions in fix-ai-tell-prose review files.

  tally.py PATH [PATH ...] [--json] [--strict] [--min-decided N]

PATH is a review file or a folder (searched recursively for *.md). For each pattern it
reports how many proposed fixes were approved, edited, rejected or still pending, and what
share of decided fixes the reviewer accepted. This measures the rulebook, not the pages: it
answers "would a reviewer sign off on these fixes?", per pattern.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

FINDING_RE = re.compile(r"^###\s+F(\d+)\s*[·|:\-–—]\s*(AT-\d{2})\b")
DECISION_RE = re.compile(r"^Decision:\s*(.*?)\s*$", re.IGNORECASE)
SECTION_RE = re.compile(r"^#{1,3}\s")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
DECISIONS = ("approved", "edited", "rejected", "pending")

# Defaults for the per-pattern verdict; see docs/validation-protocol.md.
KEEP_AT = 0.8
STOP_BELOW = 0.6


@dataclass
class Finding:
    file: str
    number: int
    pattern: str
    decision: str  # one of DECISIONS, or "missing" / "invalid"
    raw: str = ""


@dataclass
class Tally:
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    files: int = 0


def parse_review(path: Path) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    warnings: list[str] = []
    current: Finding | None = None
    fence: str | None = None

    def close(finding: Finding | None) -> None:
        if finding is None:
            return
        if finding.decision == "missing":
            warnings.append(f"{path}: F{finding.number} has no Decision line")
        findings.append(finding)

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = marker
            elif marker.startswith(fence[0]) and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        heading = FINDING_RE.match(line)
        if heading:
            close(current)
            current = Finding(str(path), int(heading.group(1)), heading.group(2), "missing")
            continue
        if SECTION_RE.match(line):
            close(current)
            current = None
            continue
        decision = DECISION_RE.match(line)
        if decision and current is not None and current.decision == "missing":
            value = decision.group(1).lower()
            current.raw = decision.group(1)
            if value in DECISIONS:
                current.decision = value
            else:
                current.decision = "invalid"
                warnings.append(
                    f"{path}: F{current.number} has decision {decision.group(1)!r}; "
                    f"expected one of {', '.join(DECISIONS)}"
                )
    close(current)
    return findings, warnings


def collect(paths: list[str]) -> Tally:
    tally = Tally()
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files += sorted(p for p in path.rglob("*.md") if p.is_file())
        elif path.is_file():
            files.append(path)
        else:
            tally.warnings.append(f"{raw}: no such file or folder")
    for path in files:
        findings, warnings = parse_review(path)
        if findings:
            tally.files += 1
        tally.findings += findings
        tally.warnings += warnings
    return tally


def verdict(accepted: int, decided: int, min_decided: int) -> str:
    if decided < min_decided:
        return "too few decisions"
    share = accepted / decided
    if share >= KEEP_AT:
        return "keep"
    if share >= STOP_BELOW:
        return "tighten"
    return "revise or retire"


def summarise(tally: Tally, min_decided: int) -> dict:
    by_pattern: dict[str, Counter] = {}
    for finding in tally.findings:
        by_pattern.setdefault(finding.pattern, Counter())[finding.decision] += 1

    def row(counts: Counter) -> dict:
        decided = counts["approved"] + counts["edited"] + counts["rejected"]
        accepted = counts["approved"] + counts["edited"]
        return {
            "approved": counts["approved"],
            "edited": counts["edited"],
            "rejected": counts["rejected"],
            "pending": counts["pending"],
            "unreadable": counts["missing"] + counts["invalid"],
            "decided": decided,
            "accepted_share": round(accepted / decided, 3) if decided else None,
            "verdict": verdict(accepted, decided, min_decided),
        }

    total = Counter()
    for counts in by_pattern.values():
        total.update(counts)
    overall = row(total)
    overall["verdict"] = (
        "no decisions yet"
        if not overall["decided"]
        else "stop and fix the rulebook"
        if overall["accepted_share"] < STOP_BELOW
        else "continue"
    )
    return {
        "files": tally.files,
        "findings": len(tally.findings),
        "patterns": {key: row(by_pattern[key]) for key in sorted(by_pattern)},
        "overall": overall,
        "warnings": tally.warnings,
    }


def _share(value: float | None) -> str:
    return "—" if value is None else f"{value:.0%}"


def render_markdown(summary: dict) -> str:
    lines = [
        f"Review files: {summary['files']} · Findings: {summary['findings']}",
        "",
        "| Pattern | Approved | Edited | Rejected | Pending | Accepted of decided | Verdict |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    rows = list(summary["patterns"].items()) + [("All", summary["overall"])]
    for name, data in rows:
        lines.append(
            f"| {name} | {data['approved']} | {data['edited']} | {data['rejected']} | "
            f"{data['pending']} | {_share(data['accepted_share'])} | {data['verdict']} |"
        )
    lines += [
        "",
        "Accepted = approved + edited. Verdicts: keep at 80% or more, tighten from 60%,",
        "revise or retire below 60%. The overall run stops below 60%.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tally.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", help="review files or folders")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument(
        "--strict", action="store_true", help="exit 1 if any decision is missing or unreadable"
    )
    parser.add_argument(
        "--min-decided",
        type=int,
        default=5,
        help="decisions a pattern needs before it gets a verdict (default 5)",
    )
    args = parser.parse_args(argv)

    tally = collect(args.paths)
    summary = summarise(tally, args.min_decided)
    for warning in tally.warnings:
        print(f"tally.py: warning: {warning}", file=sys.stderr)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        sys.stdout.write(render_markdown(summary))
    if not tally.findings:
        print("tally.py: warning: no findings found", file=sys.stderr)
    return 1 if args.strict and tally.warnings else 0


if __name__ == "__main__":
    sys.exit(main())
