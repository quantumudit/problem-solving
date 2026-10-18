---
platform: labs
concept_area: rag
slug: corrective_rag
phases: 3
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
| phase_02 | knowledge_refinement | Corrective layer -- relevance grading, query rewriting, and fallback retrieval |
| phase_03 | retrieval_evaluation | Evaluate retrieval quality using standard IR metrics (precision, recall, NDCG, MRR) |

## Key Concepts

- Retrieval-Augmented Generation (RAG)
- Document relevance grading
- Query rewriting
- LangGraph stateful graph execution
- FAISS vector store with persistent storage

## Using the Marimo Notebooks

Phase 02 uses [marimo](https://docs.marimo.io) -- a reactive Python notebook where cells
re-execute automatically when their dependencies change. Unlike Jupyter, marimo notebooks are plain `.py` files, making them git-friendly and free of hidden state.

### Installation

```bash
# with uv (recommended)
uv add marimo

# with pip
pip install marimo
```

### Running a notebook

```bash
# from the lab root (replace with the target phase folder)
marimo edit phase_02_knowledge_refinement/notebook.py
marimo edit phase_03_retrieval_evaluation/notebook.py

# or via uv run (no global install needed)
uv run marimo edit phase_02_knowledge_refinement/notebook.py
```

`marimo edit <filename>` opens the notebook in the browser for interactive editing.
If the file does not exist yet, marimo creates a blank notebook at that path automatically.

### VS Code extension

The [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) adds an embedded notebook view, cell execution, and variable explorer directly inside the editor.

Install it from the VS Code marketplace or search for `marimo-team.vscode-marimo` in the Extensions panel.

### Further reading

- Docs: https://docs.marimo.io
