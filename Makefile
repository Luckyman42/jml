# Run linter
linter:
	uv run ruff check app

# Run linter
linter-fix:
	uv run ruff check app --fix

# Run static type checker
type-checker:
	uv run pyright 

# Run formatter
formatter:
	uv run ruff format app

# Formatter + Linter + type-checker
lint-all: formatter linter type-checker

# Run tests
test: 
	uv run pytest -q

# Install dependencies for developing the project
install-dev-dependencies:
	pip install uv
	uv sync
	uv run pre-commit install
