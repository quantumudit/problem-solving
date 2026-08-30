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

# Run solution for a misc problem by ID prefix
# Examples:
#   just misc 0011               # runs solution.py
#   just misc 0011 pandas        # runs solution_pandas.py
#   just misc 0011 pandas_v2     # runs solution_pandas_v2.py
misc id library="":
    $folder = (Get-ChildItem -Directory ".\problems\misc\{{ id }}_*" | Select-Object -First 1).FullName; uv run "$folder\{{ if library == "" { "solution.py" } else { "solution_" + library + ".py" } }}"

# Run a solution script from a projects/ folder
# Examples:
#   just project misc demographic_data_analysis q01           # runs q01_solution_pandas.py
#   just project misc demographic_data_analysis q01 polars    # runs q01_solution_polars.py
project source challenge q library="pandas":
    uv run .\projects\{{ source }}\{{ challenge }}\scripts\{{ q }}_solution_{{ library }}.py

# Run a SQL solution script from a projects/ folder using DuckDB
# Examples:
#   just project-sql kaggle olympic_history_analysis q01
#   just project-sql kaggle olympic_history_analysis q04 v2
project-sql source challenge q version="":
    uv run .\projects\{{ source }}\{{ challenge }}\scripts\runner.py {{ q }} {{ version }}

# Run a PySpark solution inside Docker (auto-starts container if needed)
# Examples:
#   just excelbi-pyspark 06_09_case_stage_progress
#   just excelbi-pyspark 06_09_case_stage_progress v2
#   just excelbi-pyspark 06_09_case_stage_progress "" 2025
excelbi-pyspark slug version="" year="2026": spark-up
    docker compose exec spark /opt/spark/bin/spark-submit problems/excelbi/{{ year }}/{{ slug }}/{{ if version == "" { "solution_pyspark.py" } else { "solution_pyspark_" + version + ".py" } }}

# --- Docker Desktop ---

# Launch Docker Desktop (run this first if Docker is not running)
docker-start:
    Start-Process "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"

# --- Spark container lifecycle ---

# Build the PySpark image from Dockerfile (run once, or after Dockerfile changes)
spark-build:
    docker compose build

# Start the container in the background
spark-up:
    docker compose up -d

# Build image and start the container
spark-create: spark-build spark-up


# Stop the container (keeps it -- restart with spark-up)
spark-stop:
    docker compose stop

# Stop and remove the container (image is kept)
spark-down:
    docker compose down

# Remove container and the built image (base apache/spark-py image stays cached)
spark-clean:
    docker compose down --rmi local

# Verify the setup: container status + package imports + spark version
spark-verify: spark-up
    docker compose ps
    docker compose exec spark python3 -c "import pandas, polars, rich; print('pandas / polars / rich OK')"
    docker compose exec spark /opt/spark/bin/spark-submit --version
