#!/bin/bash

set -e  # Exit on error

echo "Installing uv..."
command -v uv &>/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

echo Setting up Virtual Environment...
uv venv

echo "Installing dependencies..."
uv sync --extra dev

echo "Exporting dependencies into requirements.txt file..."
uv export --no-hashes --format requirements-txt > requirements.txt

echo "Setting up pre-commit hooks..."
uv pip install pre-commit && pre-commit install

echo "Setup complete!"
