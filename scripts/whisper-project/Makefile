# Makefile for whisper-subtitles project

.PHONY: help install lint lint-fix format check test clean

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	uv pip install -e ".[dev]"

lint:  ## Check code with ruff
	uv run ruff check whisper_subtitles/ main.py example_usage.py

lint-fix:  ## Auto-fix linting issues
	uv run ruff check --fix whisper_subtitles/ main.py example_usage.py

format:  ## Format code with ruff
	uv run ruff format whisper_subtitles/ main.py example_usage.py

check: lint  ## Run all checks (lint)
	@echo "✅ All checks passed!"

test:  ## Run tests
	pytest

clean:  ## Clean up cache and build files
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:  ## Run the CLI (use: make run ARGS="Guitar.mp4 --translate")
	uv run main.py $(ARGS)

# Examples
example-slovak:  ## Generate Slovak subtitles from Guitar.mp4
	uv run main.py Guitar.mp4

example-english:  ## Generate English subtitles from Guitar.mp4
	uv run main.py Guitar.mp4 --translate

example-preview:  ## Generate with preview
	uv run main.py Guitar.mp4 --preview

