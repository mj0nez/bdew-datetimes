

dev:
	uv sync
.PHONY: dev

build:
	uv build
.PHONY: build


build-check:
	uv publish --dry-run -t _token_ dist/*
.PHONY: build-check

release:
	uv publish
.PHONY: release

tests:
	uv run pytest tests
.PHONY: tests

typing:
	uv run mypy --strict src/bdew_datetimes tests
.PHONY: typing

lint:
	uv run --group linting pylint bdew_datetimes
.PHONY: lint

format:
	uv run black .
	uv run isort .
.PHONY: format

spell-check:
	uv run codespell --ignore-words=domain-specific-terms.txt src/bdew_datetimes README.md
.PHONY: spell-check

# ci-only targets
black:
	uv run black . --check
.PHONY: black

isort:
	uv run isort . --check
.PHONY: isort
