import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "fix-ai-tell-prose"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def pages():
    return load("pages", SKILL_DIR / "scripts" / "pages.py")


@pytest.fixture(scope="session")
def tally():
    return load("tally", SKILL_DIR / "scripts" / "tally.py")


@pytest.fixture(scope="session")
def validator():
    return load("validate_skill", ROOT / "tools" / "validate_skill.py")
