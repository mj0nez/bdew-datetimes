
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
	uv run ruff check .
.PHONY: lint

format:
	uv run ruff format .
.PHONY: format

spell-check:
	uv run codespell --ignore-words=domain-specific-terms.txt src/bdew_datetimes README.md
.PHONY: spell-check

# ci-only targets
ci-format:
	uv run ruff format --check .
	uv run ruff check --select I .
.PHONY: format