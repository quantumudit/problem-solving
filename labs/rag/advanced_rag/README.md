<p align="center">
  <img src="assets/header.svg" alt="Advanced RAG" width="100%"/>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://www.langchain.com/langgraph"><img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchaincorporate&logoColor=white" alt="LangGraph"/></a>
  <a href="https://docs.marimo.io"><img src="https://img.shields.io/badge/marimo-EE4C2C?style=for-the-badge&logo=gitbook&logoColor=white" alt="marimo"/></a>
  <a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/Chroma-F97316?style=for-the-badge&logo=databricks&logoColor=white" alt="Chroma"/></a>
</p>

<p align="center">
  <a href="#overview">Overview</a> &bull;
  <a href="#data">Data</a> &bull;
  <a href="#structure">Structure</a> &bull;
  <a href="#phases">Phases</a> &bull;
  <a href="#setup">Setup</a>
</p>

---

## Overview

Implementation of advanced retrieval techniques, hybrid search and reranking methodologies.
Explores how to combine multiple retrieval strategies with a LangGraph-orchestrated pipeline
to improve retrieval quality beyond standard dense-only approaches.

### Libraries

| Library | Purpose |
|---|---|
| [LangGraph](https://www.langchain.com/langgraph) | Stateful graph execution with conditional routing between nodes |
| [LangChain](https://python.langchain.com/) | Document loaders, text splitters, embeddings, and vector store integration |
| [langchain-openai](https://python.langchain.com/docs/integrations/llms/azure_openai) | Azure OpenAI chat and embedding models |
| [Chroma](https://www.trychroma.com/) | Persistent vector store with metadata filtering |
| [marimo](https://docs.marimo.io) | Reactive Python notebooks (plain `.py`, git-friendly) |

> See [requirements.txt](requirements.txt) for the full dependency list.

---

## Data

> See [data/README.md](data/README.md) for download links and descriptions.

---

## Structure

```
advanced_rag/
|-- assets/
|   |-- header.svg
|-- cache/
|   |-- .gitkeep
|-- data/
|   |-- README.md
|-- index/
|   |-- .gitkeep
|-- notebooks/
|   |-- layouts/
|   |-- p01_bm25_retrieval.py
|   |-- p02_ensemble_retrieval.py
|   |-- p03_reranking.py
|-- vector_store/
|   |-- .gitkeep
|-- .env.example
|-- .gitignore
|-- notes.md
|-- README.md
|-- requirements.txt
```

<details>
<summary><b>Folder & File Details</b></summary>

<br>

| Path | Description |
|---|---|
| `assets/` | Static images used in this README |
| `cache/` | Serialized document objects -- auto-generated on first run, avoids re-parsing across sessions |
| `data/` | Source documents forming the RAG knowledge base (gitignored) -- see `data/README.md` |
| `index/` | Persistent index artifacts (gitignored) |
| `notebooks/` | marimo notebooks, one per phase -- open with `marimo edit notebooks/<file>.py` |
| `notebooks/layouts/` | marimo grid layout files for `marimo run` |
| `vector_store/` | Persisted Chroma vector store (gitignored) |
| `.env.example` | Template for required environment variables |
| `notes.md` | Lab-level notes covering concepts, observations, and implementation details |
| `requirements.txt` | Python dependencies for this lab |

</details>

---

## Phases

| # | Notebook | Slug | What it adds |
|---|---|---|---|
| 01 | [p01_bm25_retrieval.py](notebooks/p01_bm25_retrieval.py) | bm25_retrieval | TBD |
| 02 | [p02_ensemble_retrieval.py](notebooks/p02_ensemble_retrieval.py) | ensemble_retrieval | TBD |
| 03 | [p03_reranking.py](notebooks/p03_reranking.py) | reranking | TBD |

### Key Concepts

- Retrieval-Augmented Generation (RAG)
- Hybrid search (dense + sparse retrieval)
- Reranking for retrieval quality improvement
- LangGraph stateful graph execution
- Chroma vector store with persistent storage

---

## Setup

All phases use [marimo](https://docs.marimo.io) -- a reactive Python notebook where cells
re-execute automatically when their dependencies change. Unlike Jupyter, marimo notebooks
are plain `.py` files, making them git-friendly and free of hidden state.

### Installation

```bash
# with uv (recommended)
uv add marimo

# with pip
pip install marimo
```

### Environment

Copy `.env.example` to `.env` and fill in your credentials:

```
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=<your-azure-openai-api-key>
```

### Running

```bash
# open the marimo workspace -- lists all notebooks in the current folder
marimo edit

# open a specific notebook directly
marimo edit notebooks/p01_phase_01.py

# or via uv run (no global install needed)
uv run marimo edit
uv run marimo edit notebooks/p01_phase_01.py
```

### VS Code

The [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) adds an embedded notebook view, cell execution, and variable explorer directly inside the editor.

Search for `marimo-team.vscode-marimo` in the Extensions panel.
