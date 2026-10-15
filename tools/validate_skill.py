#!/usr/bin/env python3
"""Check that the skill folder is well formed.

  validate_skill.py SKILL_DIR [--evals evals/cases.json]

This checks the rulebook's *structure*: frontmatter, file references, that every pattern
has detection criteria, false-positive guidance, a fix rule, a replacement table and an
example, and that any optional SKILL.md summary table matches references/patterns.md. It does not
read or judge any prose for AI tells.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PATTERN_HEADING_RE = re.compile(r"^### (AT-(\d{2})) · (.+?)\s*$", re.MULTILINE)
SUMMARY_ROW_RE = re.compile(r"^\| (AT-\d{2}) \| (.+?) \| ([12]) \| (.+?) \|\s*$", re.MULTILINE)
PASS_RE = re.compile(r"^\*\*Pass:\*\* ([12]) · \*\*Acts on:\*\* (.+)$", re.MULTILINE)
REFERENCE_RE = re.compile(r"(?<![\w/<>-])((?:references|scripts)/[\w.-]+\.(?:md|py))")
REQUIRED_PARTS = ("**Detect when**", "**Not a tell when**", "**Fix:**", "**Example**")
MIN_TABLE_ROWS = 5
MAX_SKILL_LINES = 500
MAX_DESCRIPTION = 1024


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Minimal YAML frontmatter reader: top-level scalar keys and folded/literal blocks."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with a '---' frontmatter block")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed with '---'")
    block, body = text[4:end], text[end + 5 :]
    fields: dict[str, str] = {}
    key = None
    folded: list[str] = []
    for line in block.splitlines():
        if key and (line.startswith("  ") or not line.strip()):
            folded.append(line.strip())
            continue
        if key:
            fields[key] = " ".join(part for part in folded if part)
            key, folded = None, []
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        name, value = match.groups()
        if value in (">", ">-", "|", "|-"):
            key = name
        else:
            fields[name] = value.strip().strip("\"'")
    if key:
        fields[key] = " ".join(part for part in folded if part)
    return fields, body


def split_patterns(text: str) -> list[tuple[str, int, str, str]]:
    """Return (id, number, name, section text) for each pattern heading."""
    matches = list(PATTERN_HEADING_RE.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(
            (match.group(1), int(match.group(2)), match.group(3), text[match.end() : end])
        )
    return sections


def table_rows(section: str) -> int | None:
    lines = section.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^\|\s*Before\s*\|\s*After\s*\|\s*$", line):
            rows = 0
            for row in lines[index + 2 :]:
                if not row.startswith("|"):
                    break
                rows += 1
            return rows
    return None


def check_patterns(text: str) -> tuple[list[str], dict[str, tuple[str, str, str]]]:
    errors: list[str] = []
    found: dict[str, tuple[str, str, str]] = {}
    sections = split_patterns(text)
    if not sections:
        return ["references/patterns.md has no '### AT-NN · Name' pattern headings"], found
    for expected, (pid, number, name, body) in enumerate(sections, start=1):
        if number != expected:
            errors.append(f"{pid}: expected AT-{expected:02d} here; IDs must be sequential")
        if pid in found:
            errors.append(f"{pid}: duplicate pattern ID")
        pass_match = PASS_RE.search(body)
        if not pass_match:
            errors.append(f"{pid}: missing '**Pass:** N · **Acts on:** ...' line")
            pass_no, acts_on = "?", "?"
        else:
            pass_no, acts_on = pass_match.group(1), pass_match.group(2)
        found[pid] = (name, pass_no, acts_on)
        if "**Status:** retired" in body:
            continue
        for part in REQUIRED_PARTS:
            if part not in body:
                errors.append(f"{pid}: missing {part}")
        rows = table_rows(body)
        if rows is None:
            errors.append(f"{pid}: missing '| Before | After |' replacement table")
        elif rows < MIN_TABLE_ROWS:
            errors.append(f"{pid}: replacement table has {rows} rows; need {MIN_TABLE_ROWS}")
        example = body.split("**Example**", 1)[-1]
        if "Before:" not in example or "After:" not in example:
            errors.append(f"{pid}: example needs both 'Before:' and 'After:'")
    return errors, found


def check_summary(body: str, patterns: dict[str, tuple[str, str, str]]) -> list[str]:
    errors = []
    rows = {m.group(1): (m.group(2), m.group(3), m.group(4)) for m in SUMMARY_ROW_RE.finditer(body)}
    if not rows:
        return errors
    for pid, (name, pass_no, acts_on) in patterns.items():
        if pid not in rows:
            errors.append(f"SKILL.md summary table is missing {pid}")
            continue
        s_name, s_pass, s_acts = rows[pid]
        if s_name != name:
            errors.append(f"{pid}: name differs: SKILL.md {s_name!r} vs patterns.md {name!r}")
        if s_pass != pass_no:
            errors.append(f"{pid}: pass differs: SKILL.md {s_pass} vs patterns.md {pass_no}")
        if not acts_on.startswith(s_acts):
            errors.append(f"{pid}: 'acts on' differs: SKILL.md {s_acts!r} vs {acts_on!r}")
    for pid in rows.keys() - patterns.keys():
        errors.append(f"SKILL.md summary table lists {pid}, which patterns.md does not define")
    return errors


def check_evals(path: Path, known: set[str]) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: cannot read: {exc}"]
    errors = []
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return [f"{path}: needs a non-empty 'cases' list"]
    seen = set()
    for index, case in enumerate(cases):
        label = case.get("id", f"case #{index}")
        for key, kind in (("id", str), ("text", str), ("expect", list), ("must_keep", list)):
            if not isinstance(case.get(key), kind):
                errors.append(f"{path}: {label}: '{key}' must be a {kind.__name__}")
        if label in seen:
            errors.append(f"{path}: duplicate case id {label}")
        seen.add(label)
        for pid in case.get("expect", []) if isinstance(case.get("expect"), list) else []:
            if pid not in known:
                errors.append(f"{path}: {label}: unknown pattern {pid}")
        text = case.get("text", "") if isinstance(case.get("text"), str) else ""
        for fact in case.get("must_keep", []) if isinstance(case.get("must_keep"), list) else []:
            if fact not in text:
                errors.append(f"{path}: {label}: must_keep {fact!r} does not appear in text")
    covered = {pid for case in cases for pid in case.get("expect", []) if isinstance(pid, str)}
    for pid in sorted(known - covered):
        errors.append(f"{path}: no case expects {pid}")
    if not any(case.get("expect") == [] for case in cases):
        errors.append(f"{path}: add at least one false-positive case (expect: [])")
    return errors


def validate(skill_dir: Path, evals: Path | None = None) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_md}: not found"]
    text = skill_md.read_text(encoding="utf-8")
    try:
        fields, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = fields.get("name", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"frontmatter name {name!r} must be lowercase words joined by hyphens")
    if name != skill_dir.resolve().name:
        errors.append(f"frontmatter name {name!r} must match folder name {skill_dir.name!r}")
    description = fields.get("description", "")
    if not description:
        errors.append("frontmatter needs a description")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"description is {len(description)} chars; limit {MAX_DESCRIPTION}")
    if fields.get("license") != "MIT":
        errors.append("frontmatter license must be MIT")
    if len(text.splitlines()) > MAX_SKILL_LINES:
        errors.append(f"SKILL.md is over {MAX_SKILL_LINES} lines; move detail to references/")

    docs = [skill_md, *sorted((skill_dir / "references").glob("*.md"))]
    for doc in docs:
        for ref in sorted(set(REFERENCE_RE.findall(doc.read_text(encoding="utf-8")))):
            if not (skill_dir / ref).is_file():
                errors.append(f"{doc.relative_to(skill_dir)} refers to missing file {ref}")

    patterns_md = skill_dir / "references" / "patterns.md"
    if not patterns_md.is_file():
        errors.append("references/patterns.md: not found")
        return errors
    pattern_errors, patterns = check_patterns(patterns_md.read_text(encoding="utf-8"))
    errors += pattern_errors
    errors += check_summary(body, patterns)
    if evals is not None:
        errors += check_evals(evals, set(patterns))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--evals", type=Path, help="regression cases to check against IDs")
    args = parser.parse_args(argv)
    errors = validate(args.skill_dir, args.evals)
    for error in errors:
        print(f"validate_skill: {error}", file=sys.stderr)
    if errors:
        print(f"validate_skill: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"validate_skill: {args.skill_dir} OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
