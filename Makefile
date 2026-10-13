PYTHON ?= python3

.PHONY: check lint test validate install-dev install-skill

## check: everything CI runs (lint, tests, rulebook validator)
check: lint test validate

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

test:
	$(PYTHON) -m pytest -q

validate:
	$(PYTHON) tools/validate_skill.py skills/fix-ai-tell-prose

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

## install-skill: link the skill into your personal Claude Code skills folder
install-skill:
	mkdir -p $(HOME)/.claude/skills
	ln -sfn $(CURDIR)/skills/fix-ai-tell-prose $(HOME)/.claude/skills/fix-ai-tell-prose
	@echo "Linked to $(HOME)/.claude/skills/fix-ai-tell-prose"
