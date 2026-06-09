set shell := ["pwsh", "-c"]

# Environment variables applied to all recipes
export PYTHONPATH := "."
export PYTHONIOENCODING := "utf-8"

# Default recipe - shows available commands when you run just with no args
default:
    just --list

# Run linter
lint:
    uv run ruff check .

# Run formatter
format:
    uv run ruff format .

# Run linter and formatter
check: lint format

# Run solution for ExcelBI problem
# Examples:
#   just excelbi 06_09_case_stage_progress               # runs solution.py
#   just excelbi 06_09_case_stage_progress pandas        # runs solution_pandas.py
#   just excelbi 06_09_case_stage_progress pandas_v2     # runs solution_pandas_v2.py
#   just excelbi 06_09_case_stage_progress pandas 2025
excelbi slug library="" year="2026":
    uv run .\problems\excelbi\{{ year }}\{{ slug }}\{{ if library == "" { "solution.py" } else { "solution_" + library + ".py" } }}


