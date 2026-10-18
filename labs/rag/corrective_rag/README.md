---
platform: labs
concept_area: rag
slug: corrective_rag
phases: 5
link: https://youtu.be/41XDn81nR5c
framework: [langgraph, langchain, faiss, azure-openai]
date_started: 2026-10-17
date_completed: null
---

## Overview

Implementation of corrective RAG with LangGraph. Explores how to build a RAG pipeline that self-evaluates retrieved documents and applies corrective steps -- such as query rewriting and fallback retrieval -- when the initial retrieval quality is insufficient.

## Reference

[https://youtu.be/41XDn81nR5c](https://youtu.be/41XDn81nR5c)

## Phases

| # | Slug | Description |
|---|------|-------------|
| phase_01 | basic_rag | Baseline RAG pipeline -- document loading, chunking, embedding, retrieval, and generation |
| phase_02 | knowledge_refinement | Knowledge refinement -- decompose retrieved chunks into sentence strips, filter for relevance, recompose |
| phase_03 | retrieval_evaluation | Retrieval evaluation -- score each chunk, classify verdict (correct/incorrect/ambiguous), route conditionally |
| phase_04 | web_fallback | Web fallback -- Tavily web search when internal retrieval verdict is `incorrect` |
| phase_05 | query_rewriting | Query rewriting -- LLM rewrites the user query before web search to improve retrieval on the `incorrect` path |

## Key Concepts

- Retrieval-Augmented Generation (RAG)
- Document relevance grading and threshold-based verdict classification
- Knowledge refinement -- sentence-level decomposition, filtration, recomposition
- Query rewriting and web search fallback (Tavily)
- LangGraph stateful graph execution with conditional routing
- FAISS vector store with persistent storage

## Using the Marimo Notebooks

All phases use [marimo](https://docs.marimo.io) -- a reactive Python notebook where cells
re-execute automatically when their dependencies change. Unlike Jupyter, marimo notebooks are plain `.py` files, making them git-friendly and free of hidden state.

Notebooks live in the `notebooks/` folder:

```
notebooks/
├── phase_01_basic_rag.py
├── phase_02_knowledge_refinement.py
├── phase_03_retrieval_evaluation.py
├── phase_04_web_fallback.py
└── phase_05_query_rewriting.py
```

### Installation

```bash
# with uv (recommended)
uv add marimo

# with pip
pip install marimo
```

### Running a notebook

```bash
# from the lab root
marimo edit notebooks/phase_01_basic_rag.py
marimo edit notebooks/phase_02_knowledge_refinement.py
marimo edit notebooks/phase_03_retrieval_evaluation.py
marimo edit notebooks/phase_04_web_fallback.py
marimo edit notebooks/phase_05_query_rewriting.py

# or via uv run (no global install needed)
uv run marimo edit notebooks/phase_01_basic_rag.py
```

`marimo edit <filename>` opens the notebook in the browser for interactive editing.
If the file does not exist yet, marimo creates a blank notebook at that path automatically.

### VS Code extension

The [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) adds an embedded notebook view, cell execution, and variable explorer directly inside the editor.

Install it from the VS Code marketplace or search for `marimo-team.vscode-marimo` in the Extensions panel.

### Further reading

- Docs: https://docs.marimo.io
