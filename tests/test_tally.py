import json

from conftest import FIXTURES

REVIEWS = FIXTURES / "reviews" / "site-a"


def test_parse_review_reads_decisions(tally):
    findings, warnings = tally.parse_review(REVIEWS / "home.md")
    assert [(f.number, f.pattern, f.decision) for f in findings] == [
        (1, "AT-02", "approved"),
        (2, "AT-09", "edited"),  # case-insensitive
        (3, "AT-09", "rejected"),  # first Decision line wins; "-" separator accepted
        (4, "AT-03", "pending"),
    ]
    assert warnings == []


def test_parse_review_flags_bad_and_missing_and_ignores_fences(tally):
    findings, warnings = tally.parse_review(REVIEWS / "about.md")
    assert [(f.number, f.decision) for f in findings] == [
        (1, "invalid"),
        (2, "missing"),
        (3, "approved"),
    ]
    assert len(warnings) == 2
    assert all("F9" not in w for w in warnings)


def test_summary_counts_and_verdicts(tally):
    summary = tally.summarise(tally.collect([str(REVIEWS)]), min_decided=1)
    assert summary["files"] == 2  # index.md has no findings
    assert summary["findings"] == 7
    at02 = summary["patterns"]["AT-02"]
    assert (at02["approved"], at02["unreadable"], at02["verdict"]) == (2, 1, "keep")
    at09 = summary["patterns"]["AT-09"]
    assert (at09["edited"], at09["rejected"], at09["accepted_share"]) == (1, 1, 0.5)
    assert at09["verdict"] == "revise or retire"
    assert summary["patterns"]["AT-03"]["verdict"] == "too few decisions"
    overall = summary["overall"]
    assert (overall["decided"], overall["accepted_share"]) == (4, 0.75)
    assert overall["verdict"] == "continue"


def test_verdict_thresholds(tally):
    assert tally.verdict(4, 5, 5) == "keep"
    assert tally.verdict(3, 5, 5) == "tighten"
    assert tally.verdict(2, 5, 5) == "revise or retire"
    assert tally.verdict(4, 4, 5) == "too few decisions"


def test_overall_stop(tally):
    findings = [tally.Finding("f", n, "AT-01", "rejected") for n in range(3)]
    findings.append(tally.Finding("f", 4, "AT-01", "approved"))
    summary = tally.summarise(tally.Tally(findings=findings, files=1), min_decided=1)
    assert summary["overall"]["verdict"] == "stop and fix the rulebook"


def test_cli_markdown(tally, capsys):
    assert tally.main([str(REVIEWS / "home.md")]) == 0
    out = capsys.readouterr().out
    assert "| AT-09 | 0 | 1 | 1 | 0 | 50% |" in out
    assert out.count("| All |") == 1


def test_cli_json_and_strict(tally, capsys):
    assert tally.main([str(REVIEWS), "--json", "--strict"]) == 1
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["overall"]["pending"] == 1
    assert "tally.py: warning:" in captured.err


def test_cli_missing_path(tally, capsys):
    assert tally.main(["nowhere"]) == 0
    assert "no such file" in capsys.readouterr().err


def test_worked_example_in_review_format_is_parseable(tally, tmp_path):
    """The example in references/review-format.md must parse with zero warnings."""
    from conftest import SKILL_DIR

    text = (SKILL_DIR / "references" / "review-format.md").read_text()
    start = text.index("## Worked example")
    body = text[start:].split("````markdown\n", 1)[1].split("\n````", 1)[0]
    review = tmp_path / "example.md"
    review.write_text(body)
    findings, warnings = tally.parse_review(review)
    assert warnings == []
    assert [f.pattern for f in findings] == ["AT-02", "AT-07", "AT-09"]
    assert {f.decision for f in findings} == {"pending"}
