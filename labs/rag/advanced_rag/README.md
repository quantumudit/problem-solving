<p align="center">
  <img src="assets/header.svg" alt="Advanced RAG" width="100%"/>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://www.langchain.com/langgraph"><img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchaincorporate&logoColor=white" alt="LangGraph"/></a>
  <a href="https://docs.marimo.io"><img src="https://img.shields.io/badge/marimo-EE4C2C?style=for-the-badge&logo=gitbook&logoColor=white" alt="marimo"/></a>
  <a href="https://faiss.ai/"><img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="FAISS"/></a>
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
| [FAISS](https://faiss.ai/) | Persistent local vector store for dense similarity search |
| [rank-bm25](https://github.com/dorianbrown/rank_bm25) | BM25 sparse (lexical) retrieval |
| [Cohere Rerank](https://docs.cohere.com/docs/rerank-overview) | Hosted cross-encoder reranker (`langchain-cohere`) |
| [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) | Lightweight local cross-encoder reranker (ONNX, CPU-friendly) |
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
|   |-- documents/
|   |-- models/
|   |-- .gitkeep
|-- data/
|   |-- README.md
|-- notebooks/
|   |-- layouts/
|   |-- p01_bm25_retrieval.py
|   |-- p02_ensemble_retrieval.py
|   |-- p03_reranking.py
|   |-- p04_flash_reranker.py
|   |-- p05_rag_fusion.py
|-- vector_store/
|   |-- faiss/
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
| `cache/` | Auto-generated on first run and gitignored; split into the two subfolders below |
| `cache/documents/` | Serialized loaded documents, one JSON file per collection slug (`rag_paper.json`, `sherlock_holmes.json`) -- avoids re-parsing the source files across sessions |
| `cache/models/` | Reranker model files downloaded on first use (FlashRank, e.g. `ms-marco-MiniLM-L-12-v2`) |
| `data/` | Source documents forming the RAG knowledge base (gitignored) -- see `data/README.md` |
| `notebooks/` | marimo notebooks, one per phase -- open with `marimo edit notebooks/<file>.py` |
| `notebooks/layouts/` | marimo grid layout files for `marimo run` |
| `vector_store/` | Persisted vector stores (gitignored), organised as `vector_store/{backend}/{slug}/` -- e.g. `faiss/rag_paper/`, `faiss/sherlock_holmes/`. The slug matches the document cache file, so notebooks working on the same collection share one index |
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
| 04 | [p04_flash_reranker.py](notebooks/p04_flash_reranker.py) | flash_reranker | TBD |
| 05 | [p05_rag_fusion.py](notebooks/p05_rag_fusion.py) | rag_fusion | TBD |

Phases 01-04 use the RAG paper (`cache/documents/rag_paper.json`, `vector_store/faiss/rag_paper/`);
phase 05 uses the Sherlock Holmes books (`cache/documents/sherlock_holmes.json`,
`vector_store/faiss/sherlock_holmes/`).

### Key Concepts

- Retrieval-Augmented Generation (RAG)
- Hybrid search (dense + sparse retrieval)
- Reranking for retrieval quality improvement (hosted Cohere vs. local FlashRank)
- RAG Fusion (multi-query generation + Reciprocal Rank Fusion)
- LangGraph stateful graph execution
- FAISS vector store with persistent storage

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
COHERE_API_KEY=<your-cohere-api-key>   # only needed for p03_reranking.py
```

### Running

```bash
# open the marimo workspace -- lists all notebooks in the current folder
marimo edit

# open a specific notebook directly
marimo edit notebooks/p01_bm25_retrieval.py

# or via uv run (no global install needed)
uv run marimo edit
uv run marimo edit notebooks/p01_bm25_retrieval.py
```

### VS Code

The [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) adds an embedded notebook view, cell execution, and variable explorer directly inside the editor.

Search for `marimo-team.vscode-marimo` in the Extensions panel.
