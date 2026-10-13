import json
import shutil

import pytest
from conftest import ROOT, SKILL_DIR


@pytest.fixture
def skill_copy(tmp_path):
    target = tmp_path / "fix-ai-tell-prose"
    shutil.copytree(SKILL_DIR, target)
    return target


def edit(path, old, new):
    text = path.read_text()
    assert old in text, f"fixture text not found: {old!r}"
    path.write_text(text.replace(old, new, 1))


def test_shipped_skill_is_valid(validator):
    assert validator.validate(SKILL_DIR, ROOT / "evals" / "cases.json") == []


def test_cli_ok(validator, capsys):
    assert validator.main([str(SKILL_DIR), "--evals", str(ROOT / "evals" / "cases.json")]) == 0
    assert "OK" in capsys.readouterr().out


def test_frontmatter_parsing(validator):
    fields, body = validator.parse_frontmatter(
        "---\nname: x\ndescription: >-\n  one\n  two\nlicense: MIT\n---\n# Body\n"
    )
    assert fields == {"name": "x", "description": "one two", "license": "MIT"}
    assert body == "# Body\n"


def test_name_must_match_folder(validator, skill_copy):
    edit(skill_copy / "SKILL.md", "name: fix-ai-tell-prose", "name: Fix_Prose")
    errors = validator.validate(skill_copy)
    assert any("lowercase" in e for e in errors)
    assert any("match folder" in e for e in errors)


def test_license_required(validator, skill_copy):
    edit(skill_copy / "SKILL.md", "license: MIT", "license: Proprietary")
    assert any("license" in e for e in validator.validate(skill_copy))


def test_missing_reference_file(validator, skill_copy):
    (skill_copy / "references" / "voice-calibration.md").unlink()
    errors = validator.validate(skill_copy)
    assert any("missing file references/voice-calibration.md" in e for e in errors)


def test_pattern_parts_are_required(validator, skill_copy):
    patterns = skill_copy / "references" / "patterns.md"
    edit(patterns, "**Not a tell when**\n\n- The word is literal", "- The word is literal")
    errors = validator.validate(skill_copy)
    assert errors == ["AT-03: missing **Not a tell when**"]


def test_short_table_is_rejected(validator, skill_copy):
    patterns = skill_copy / "references" / "patterns.md"
    edit(patterns, "| Results may vary and might not always be guaranteed. | Results vary. |\n", "")
    row = "| This may potentially reduce your costs. | This can reduce your costs. |\n"
    edit(patterns, row, "")
    errors = validator.validate(skill_copy)
    assert errors == ["AT-05: replacement table has 3 rows; need 5"]


def test_ids_must_be_sequential(validator, skill_copy):
    edit(skill_copy / "references" / "patterns.md", "### AT-04 ·", "### AT-14 ·")
    errors = validator.validate(skill_copy)
    assert any("expected AT-04" in e for e in errors)
    assert any("summary table is missing AT-14" in e for e in errors)


def test_summary_must_match_patterns(validator, skill_copy):
    edit(skill_copy / "SKILL.md", "| AT-08 | Brochure language | 2 |", "| AT-08 | Sales talk | 1 |")
    errors = validator.validate(skill_copy)
    assert any("AT-08: name differs" in e for e in errors)
    assert any("AT-08: pass differs" in e for e in errors)


def test_retired_pattern_skips_content_checks(validator, skill_copy):
    patterns = skill_copy / "references" / "patterns.md"
    text = patterns.read_text()
    start = text.index("### AT-13")
    retired = "### AT-13 · Generic upbeat conclusions\n\n**Pass:** 2 · **Acts on:** one sighting\n"
    patterns.write_text(text[:start] + retired + "\n**Status:** retired\n")
    assert validator.validate(skill_copy) == []


def test_eval_checks(validator, tmp_path):
    cases = {
        "cases": [
            {"id": "a", "text": "Price is $5.", "expect": ["AT-01", "AT-99"], "must_keep": ["$6"]},
            {"id": "a", "text": "x", "expect": ["AT-01"], "must_keep": []},
        ]
    }
    path = tmp_path / "cases.json"
    path.write_text(json.dumps(cases))
    errors = validator.check_evals(path, {"AT-01", "AT-02"})
    assert any("unknown pattern AT-99" in e for e in errors)
    assert any("'$6' does not appear" in e for e in errors)
    assert any("duplicate case id a" in e for e in errors)
    assert any("no case expects AT-02" in e for e in errors)
    assert any("false-positive" in e for e in errors)
