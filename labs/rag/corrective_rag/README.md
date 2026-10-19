<p align="center">
  <img src="assets/header.svg" alt="Corrective RAG" width="100%"/>
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

Implementation of corrective RAG with LangGraph. Explores how to build a RAG pipeline that
self-evaluates retrieved documents and applies corrective steps -- such as query rewriting
and web fallback retrieval -- when the initial retrieval quality is insufficient.

The lab progresses across six phases, each building on the previous one. Starting from a
baseline retrieve-and-generate pipeline, the pipeline gains knowledge refinement, retrieval
evaluation, web fallback, query rewriting, and ambiguity handling -- arriving at a full
corrective RAG system capable of handling a range of retrieval failure modes.

### Libraries

The key libraries powering this lab -- from graph orchestration and LLM integration to
vector search, web fallback, and the reactive notebook environment.

| Library | Purpose |
|---|---|
| [LangGraph](https://www.langchain.com/langgraph) | Stateful graph execution with conditional routing between nodes |
| [LangChain](https://python.langchain.com/) | Document loaders, text splitters, embeddings, and vector store integration |
| [langchain-openai](https://python.langchain.com/docs/integrations/llms/azure_openai) | Azure OpenAI chat and embedding models |
| [FAISS](https://faiss.ai/) | In-process vector similarity search (`faiss-cpu`) |
| [langchain-tavily](https://python.langchain.com/docs/integrations/tools/tavily_search) | Web search fallback via Tavily API |
| [marimo](https://docs.marimo.io) | Reactive Python notebooks (plain `.py`, git-friendly) |

> See [requirements.txt](requirements.txt) for the full dependency list.

---

## Data

Three machine learning textbooks serve as the RAG knowledge base. All PDFs are gitignored;
only the data README is tracked.

> See [data/README.md](data/README.md) for download links and full descriptions.

| File | Title | Authors | Publisher |
|---|---|---|---|
| `deep_learning_book.pdf` | Deep Learning | Goodfellow, Bengio, Courville | MIT Press (2016) |
| `hands_on_ml.pdf` | Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow | Aurelien Geron | O'Reilly Media |
| `pattern_recognition_and_ml_book.pdf` | Pattern Recognition and Machine Learning | Christopher M. Bishop | Springer (2006) |

---

## Structure

```
corrective_rag/
|-- assets/
|   |-- header.svg
|-- cache/
|   |-- .gitkeep
|   |-- documents.json
|-- data/
|   |-- deep_learning_book.pdf
|   |-- hands_on_ml.pdf
|   |-- pattern_recognition_and_ml_book.pdf
|   |-- README.md
|-- notebooks/
|   |-- layouts/
|   |   |-- p06_ambiguity_handling.grid.json
|   |-- p01_basic_rag.py
|   |-- p02_knowledge_refinement.py
|   |-- p03_retrieval_evaluation.py
|   |-- p04_web_fallback.py
|   |-- p05_query_rewriting.py
|   |-- p06_ambiguity_handling.py
|-- vector_store/
|   |-- .gitkeep
|   |-- index.faiss
|   |-- index.pkl
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
| `cache/documents.json` | Serialized `Document` objects from PDF loading -- auto-generated on first run, avoids re-parsing PDFs across sessions |
| `data/` | Source PDFs forming the RAG knowledge base (gitignored) -- see `data/README.md` for download links |
| `notebooks/` | marimo notebooks, one per phase -- open with `marimo edit notebooks/<file>.py` |
| `notebooks/layouts/` | marimo grid layout files -- define the web app cell arrangement for notebooks opened with `marimo run` |
| `vector_store/` | Persisted FAISS index (`index.faiss`, `index.pkl`) -- built once in p01 and reused across all phases |
| `.env.example` | Template for required environment variables -- copy to `.env` and fill in credentials |
| `notes.md` | Lab-level notes covering concepts, observations, and implementation details |
| `requirements.txt` | Python dependencies for this lab |

</details>

---

## Phases

| # | Notebook | Slug | What it adds |
|---|---|---|---|
| 01 | [p01_basic_rag.py](notebooks/p01_basic_rag.py) | basic_rag | Baseline pipeline -- load PDFs, chunk, embed into FAISS, retrieve top-k, generate an answer |
| 02 | [p02_knowledge_refinement.py](notebooks/p02_knowledge_refinement.py) | knowledge_refinement | Decompose chunks into sentence strips, filter each strip for relevance, recompose into clean context |
| 03 | [p03_retrieval_evaluation.py](notebooks/p03_retrieval_evaluation.py) | retrieval_evaluation | Score each chunk, classify verdict (`correct`/`incorrect`/`ambiguous`), route conditionally |
| 04 | [p04_web_fallback.py](notebooks/p04_web_fallback.py) | web_fallback | Tavily web search when internal retrieval verdict is `incorrect` |
| 05 | [p05_query_rewriting.py](notebooks/p05_query_rewriting.py) | query_rewriting | LLM rewrites the user query before web search to improve retrieval on the `incorrect` path |
| 06 | [p06_ambiguity_handling.py](notebooks/p06_ambiguity_handling.py) | ambiguity_handling | Handle the `ambiguous` verdict -- partial retrieval recovery before falling back to web search |

### Key Concepts

- Retrieval-Augmented Generation (RAG)
- Document relevance grading and threshold-based verdict classification
- Knowledge refinement -- sentence-level decomposition, filtration, recomposition
- Query rewriting and web search fallback (Tavily)
- LangGraph stateful graph execution with conditional routing
- FAISS vector store with persistent storage
- Ambiguity handling -- partial retrieval recovery on the `ambiguous` path

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
TAVILY_API_KEY=<your-tavily-api-key>
```

### Running

```bash
# open the marimo workspace -- lists all notebooks in the current folder
marimo edit

# open a specific notebook directly
marimo edit notebooks/p01_basic_rag.py
marimo edit notebooks/p02_knowledge_refinement.py
marimo edit notebooks/p03_retrieval_evaluation.py
marimo edit notebooks/p04_web_fallback.py
marimo edit notebooks/p05_query_rewriting.py
marimo edit notebooks/p06_ambiguity_handling.py

# or via uv run (no global install needed)
uv run marimo edit
uv run marimo edit notebooks/p01_basic_rag.py
```

Running `marimo edit` without a filename from the `corrective_rag/` root opens the marimo
workspace at `http://localhost:2718/` -- a file browser that lists all notebooks in the folder
so you can pick and open any phase without typing the full path.

`marimo edit <filename>` opens that specific notebook directly in the browser.

### VS Code

The [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) adds an embedded notebook view, cell execution, and variable explorer directly inside the editor.

Search for `marimo-team.vscode-marimo` in the Extensions panel.

### References

- marimo docs: https://docs.marimo.io
- Reference video: https://youtu.be/41XDn81nR5c
