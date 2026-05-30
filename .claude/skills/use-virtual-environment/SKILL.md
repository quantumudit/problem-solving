---
name: use-virtual-environment
description: How to set up and use a Python virtual environment for running solution files that need external packages. Apply when running or testing any solution.py that imports pandas, numpy, or other third-party libraries.
allowed-tools: Bash(uv *) Bash(where python) Bash(python *)
---

# Use Virtual Environment

Most solutions in this repo are standalone and need no setup. This skill applies when
a solution imports external packages (pandas, numpy, etc.) and needs to be run locally.

---

## When You Need This

- StrataScatch solutions that use `pandas`
- edna solutions that use data science libraries
- Any `solution.py` with `import pandas`, `import numpy`, etc.

Pure stdlib solutions (LeetCode algorithm problems) need no virtual environment.

---

## Setup (first time in this repo)

```powershell
# From the repo root
uv venv
```

This creates `.venv/` at the repo root. Run this once -- the same environment
is reused across all solution files.

---

## Adding Packages

```powershell
# Add a package (installs into .venv)
uv add pandas
uv add numpy

# Check what is installed
uv pip list
```

No `pyproject.toml` is required for this repo -- `uv add` creates one automatically
if it does not exist. Do not commit `pyproject.toml` or `.venv/` -- they are
already covered by `.gitignore`.

---

## Running Solutions

Prefer `uv run` -- it uses `.venv` automatically without manual activation:

```powershell
# Run a solution file
uv run python problems/stratascratch/medium/1234_top_earning_sales/solution.py
```

If you need an interactive session:

```powershell
# Activate manually
.venv\Scripts\Activate.ps1        # PowerShell
.venv\Scripts\activate.bat        # CMD

# Then run normally
python solution.py
```

---

## Checking the Environment

```powershell
# Should point to .venv inside the project root
where python
```

---

## Rules

- Always use `uv add <package>` to install -- never `pip install` directly
- Always use `uv run python <file>` to execute -- never bare `python <file>`
- Never commit `.venv/` or generated `pyproject.toml`/`uv.lock` unless explicitly asked
