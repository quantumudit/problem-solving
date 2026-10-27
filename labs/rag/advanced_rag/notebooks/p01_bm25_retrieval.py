import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # RAG: Sparse Retrieval

    A baseline RAG pipeline built with LangGraph. Loads a PDF document, splits it into
    chunks, and builds a BM25 sparse retriever in memory. The pipeline wires a
    `retrieve -> generate` graph to answer questions grounded in the retrieved context.

    This phase establishes the foundational step that shows how to perform keyword-based
    retrieval without embeddings or a vector store.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sparse Retrieval

    Sparse retrieval -- also called **keyword-based retrieval**, **lexical retrieval**, or
    **term-based retrieval** -- is an information retrieval approach that finds relevant
    documents by matching terms in a user query against terms present in a document
    collection.

    The name "sparse" comes from the internal representation: documents and queries are
    encoded as high-dimensional vectors where most values are zero (only matched vocabulary
    terms carry non-zero weights). This contrasts with **dense retrieval**, where every
    dimension of a low-dimensional embedding vector carries a non-zero value.

    Sparse retrieval focuses on **lexical matching** rather than semantic similarity. The
    retrieval system evaluates how well the words in the query match the words in each
    document. Unlike dense retrieval, it does not require an embedding model or a vector
    database.

    ### How It Works

    1. Collect and preprocess documents.
    2. Split documents into chunks if working with long documents.
    3. Build an index using a sparse retrieval algorithm.
    4. Process the user query.
    5. Score and rank documents based on term relevance.
    6. Return the top-k relevant documents to the RAG pipeline.
    7. Pass the retrieved context to the LLM to generate an answer.

    ### Common Sparse Retrieval Techniques

    - **TF-IDF:** Represents documents using term frequency and inverse document frequency,
      helping identify terms that are important to a document relative to the corpus.
    - **BM25:** A probabilistic ranking function that scores documents based on query-term
      matches, term frequency, document length, and corpus statistics. The most widely used
      sparse retrieval algorithm in practice.
    - **Boolean Retrieval:** Retrieves documents according to logical conditions involving
      terms, such as `AND`, `OR`, and `NOT`.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load Documents

    Load the RAG paper using `PyPDFLoader`. Pages are cached to `cache/documents/rag_paper.json`
    on the first run -- subsequent runs skip the expensive PDF parsing step and
    deserialize directly from the cache.
    """)
    return


@app.cell
def _():
    import warnings
    from pathlib import Path

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    lab_root = Path(__file__).parent.parent
    return (lab_root,)


@app.cell
def _():
    import json

    from langchain_community.document_loaders import PyPDFLoader
    from langchain_core.documents import Document

    return Document, PyPDFLoader, json


@app.cell
def _(Document, PyPDFLoader, json, lab_root):
    _cache_path = lab_root / "cache" / "documents" / "rag_paper.json"

    if _cache_path.exists():
        docs = [Document(**item) for item in json.loads(_cache_path.read_text())]
    else:
        _data = lab_root / "data"
        docs = PyPDFLoader(str(_data / "rag_for_nlp_paper.pdf")).load()
        _cache_path.parent.mkdir(parents=True, exist_ok=True)
        _cache_path.write_text(json.dumps([doc.model_dump() for doc in docs]))
    return (docs,)


@app.cell
def _(docs, mo):
    mo.callout(mo.md(f"Loaded **{len(docs)}** pages from the PDF"), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each PDF page becomes a `Document` object with raw text and source metadata (`source`,
    `page`). The paper -- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
    (Lewis et al., 2020) -- forms the sole knowledge base for this phase. All subsequent
    steps operate on this collection.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Chunk Documents

    Split the loaded pages into smaller overlapping windows so the BM25 retriever can
    match finer-grained units against a query. A chunk size of 900 characters with a
    150-character overlap keeps each chunk self-contained while preserving context at
    paragraph boundaries.
    """)
    return


@app.cell
def _():
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    return (RecursiveCharacterTextSplitter,)


@app.cell
def _(RecursiveCharacterTextSplitter, docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900, chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)
    return (chunks,)


@app.cell
def _(chunks):
    # Add a unique chunk_id to each Document's metadata, then strip surrogates
    # introduced by PDF extraction to prevent encoding errors downstream.
    for i, d in enumerate(chunks):
        d.metadata["chunk_id"] = i
        d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")
    return


@app.cell
def _(chunks, mo):
    mo.callout(mo.md(f"Split into **{len(chunks)}** chunks (chunk_size=900, overlap=150)."), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each chunk is the atomic retrieval unit. A Unicode cleaning pass strips surrogates
    introduced by PDF extraction to prevent encoding errors in the BM25 index.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. BM25 Retriever

    Build a BM25 retriever directly from the document chunks. BM25 operates entirely
    in memory -- no embedding model, no vector database, and no external index store
    are needed. The retriever is configured to return the top `k=4` chunks for any
    given query.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How BM25 Works

    BM25 (Best Matching 25) is a probabilistic ranking function that scores each chunk
    against a query using three signals:

    - **Term Frequency (TF):** Counts how often a query term appears in a chunk. BM25
      applies **term-frequency saturation** -- repeated occurrences yield diminishing
      score increases rather than scaling indefinitely.
    - **Inverse Document Frequency (IDF):** Upweights rare terms that appear in few
      chunks across the corpus, and downweights common terms that appear everywhere.
    - **Document-Length Normalization:** Adjusts for chunk length so longer chunks do
      not gain an unfair advantage simply from containing more words.

    Together these signals rank chunks by how precisely and distinctively they match
    the query terms, rather than by raw term overlap.
    """)
    return


@app.cell
def _():
    from langchain_community.retrievers import BM25Retriever

    return (BM25Retriever,)


@app.cell
def _(BM25Retriever, chunks):
    retriever = BM25Retriever.from_documents(chunks, k=4)
    return (retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `BM25Retriever.from_documents` tokenizes all chunks and builds the BM25 index in one
    call. At query time it scores every chunk against the query terms and returns the top
    `k` results as `Document` objects -- ready to pass into the generation step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Language Model

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used to generate answers from
    the retrieved context.
    """)
    return


@app.cell
def _():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    return (os,)


@app.cell
def _(os):
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url = os.getenv("AZURE_OPENAI_ENDPOINT")
    return api_key, base_url


@app.cell
def _():
    from langchain_openai import ChatOpenAI

    return (ChatOpenAI,)


@app.cell
def _(ChatOpenAI, api_key, base_url):
    llm = ChatOpenAI(
        model="gpt-6-luna",
        api_key=api_key,
        base_url=base_url,
    )
    return (llm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The LLM handles the generation step -- it reads the retrieved context and composes a
    grounded answer. The same instance is reused across all invocations of the graph.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Graph State

    Defines the shared data structure that LangGraph passes between every node in the
    pipeline. All reads and writes happen through this typed dict -- it is the single
    source of truth at each step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### State Schema

    The shared typed dictionary that LangGraph passes between every node. Each field is
    either written by one node and read by the next, or populated at the start and carried
    through unchanged.

    **Fields:**
    - `question` -- the user's input query
    - `docs` -- chunks returned by the retriever (with BM25 scores in metadata)
    - `answer` -- final generated answer
    """)
    return


@app.cell
def _():
    from typing import TypedDict, List

    return List, TypedDict


@app.cell
def _(Document, List, TypedDict):
    class State(TypedDict):
        question: str
        docs: List[Document]
        answer: str

    return (State,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Nodes

    Two node functions implement the RAG pipeline. Each reads from and writes to the
    shared `State` dict. The execution path is linear -- no conditional branching.

    - **`retrieve`** -- fetch the top-k keyword-matched chunks from the BM25 index
    - **`generate`** -- synthesize an answer from the retrieved chunks using the LLM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6a. Retrieve Node

    Fetches the top `k` keyword-matched chunks from the BM25 index for the given question.
    After retrieval, the BM25 score for each chunk is written into its metadata under
    `bm25_score` so the Analysis section can surface it later.

    The raw chunks are passed directly to the `generate` node -- no quality filtering in
    this phase.
    """)
    return


@app.cell
def _(State, retriever):
    def retrieve(state: State) -> dict:
        query = state["question"]
        docs = retriever.invoke(query)

        scores = retriever.vectorizer.get_scores(
            retriever.preprocess_func(query)
        )

        for doc in docs:
            idx = retriever.docs.index(doc)
            doc.metadata["bm25_score"] = float(scores[idx])

        return {"docs": docs}

    return (retrieve,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6b. Generate Node

    Constructs an answer from the retrieved chunks using the LLM. The system prompt
    instructs the model to answer only from context, reducing hallucination on
    out-of-context questions.

    All retrieved `docs` are concatenated into a single context string and passed to
    the prompt together with the user's question.
    """)
    return


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate

    return (ChatPromptTemplate,)


@app.cell
def _(ChatPromptTemplate):
    sys_msg = """You are a helpful AI research assistant. Answer ONLY using the provided context.
    If the context is empty or insufficient, simply say: "I don't know based on the provided context."
    """
    template = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ])
    return (template,)


@app.cell
def _(State, llm, template):
    def generate(state: State) -> dict:
        context = "\n\n".join(d.page_content for d in state["docs"])
        response = (template | llm).invoke({
            "question": state["question"],
            "context": context,
        })
        return {"answer": response.content}

    return (generate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `retrieve` and `generate` implement the full RAG loop: pull context, then synthesize.
    Both functions read from and write to the shared `State` dict that LangGraph passes
    between nodes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Build the Graph

    Assemble the nodes into a LangGraph `StateGraph` and compile it.
    The execution flow is linear: `START -> retrieve -> generate -> END`.
    """)
    return


@app.cell
def _():
    from langgraph.graph import StateGraph, START, END

    return END, START, StateGraph


@app.cell
def _(END, START, State, StateGraph, generate, retrieve):
    builder = StateGraph(State)

    builder.add_node("retrieve", retrieve)
    builder.add_node("generate", generate)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    graph = builder.compile()
    return (graph,)


@app.cell
def _(graph):
    graph
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The compiled graph is a runnable pipeline. Calling `graph.invoke(state)` triggers the
    full `retrieve -> generate` flow and returns the updated state with `answer` populated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe the pipeline's behavior across different question types:**

    | Question | Type | Expected behavior |
    |---|---|---|
    | "What are the two main components of the RAG model?" | Basic | Grounded answer; both components are named explicitly in the paper. |
    | "What is the difference between RAG-Sequence and RAG-Token?" | Basic | Clear distinction in the paper; BM25 should retrieve the right sections via term match. |
    | "Which knowledge source is used by the RAG models?" | Basic | Answer found in the retrieval architecture section. |
    | "How does RAG combine parametric and non-parametric memory?" | Technical | Requires synthesizing across multiple sections; tests multi-chunk retrieval quality. |
    | "What role does the DPR question encoder play in retrieval?" | Technical | Specific technical detail; BM25 should surface it via keyword match on "DPR". |
    | "How does RAG marginalize over retrieved documents when generating answers?" | Technical | Dense technical content; tests whether keyword match can locate the right passage. |
    | "Explain how a diesel engine works." | Unrelated | No relevant chunks; LLM should decline to answer. |
    | "What causes thunderstorms?" | Unrelated | No relevant chunks; LLM should decline to answer. |
    """)
    return


@app.cell
def _(graph):
    def process_response(q: str):
        input_state = {"question": q, "docs": [], "answer": ""}
        return graph.invoke(input_state)

    return (process_response,)


@app.cell
def _(mo):
    query_input = mo.ui.text_area(
        value="What are the two main components of the RAG model?",
        label="Your question",
        full_width=True,
    )
    run_btn = mo.ui.run_button(label="Run pipeline")
    mo.vstack([query_input, run_btn])
    return query_input, run_btn


@app.cell
def _(mo, process_response, query_input, run_btn):
    mo.stop(not run_btn.value)
    resp = process_response(query_input.value)
    return (resp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Answer
    """)
    return


@app.cell
def _(mo, resp):
    mo.callout(mo.md(resp["answer"]), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Analysis

    Inspect the intermediate state produced by the pipeline run above -- retrieved chunks,
    their BM25 scores, and how much raw context was passed to the LLM unfiltered. All
    sections below are read-only views of `resp`; re-running section 8 refreshes them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retrieved Documents

    The `k=4` chunks returned by the BM25 index. In this baseline phase all chunks are
    passed directly to the LLM without any quality filtering. Expand each to inspect the
    raw content that formed the generation context.
    """)
    return


@app.cell
def _(mo, resp):
    _raw_context = "\n\n".join(d.page_content for d in resp["docs"])
    mo.vstack([
        mo.accordion({
            f"Doc {i + 1}  |  BM25: {round(d.metadata.get('bm25_score', 0.0), 2)}": mo.md(d.page_content)
            for i, d in enumerate(resp["docs"])
        }),
        mo.callout(
            mo.md(
                f"**Total raw context:** {len(_raw_context):,} characters"
                f" across {len(resp['docs'])} chunks -- passed to the LLM unfiltered."
            ),
            kind="info",
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### BM25 Scores

    BM25 scores for each retrieved chunk. Higher scores indicate a stronger keyword match
    between the query and the chunk. Scores are not normalized -- they are comparable
    within a single query run but not across different queries.
    """)
    return


@app.cell
def _(mo, resp):
    _rows = [
        {
            "Rank": i + 1,
            "BM25 Score": round(d.metadata.get("bm25_score", 0.0), 4),
            "Page": d.metadata.get("page", ""),
            "Snippet": d.page_content[:150].replace("\n", " ") + "...",
        }
        for i, d in enumerate(resp["docs"])
    ]
    mo.ui.table(_rows)
    return


if __name__ == "__main__":
    app.run()
