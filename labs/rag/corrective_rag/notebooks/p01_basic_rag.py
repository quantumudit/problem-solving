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
    # Basic RAG

    A baseline RAG pipeline built with LangGraph. Loads PDF documents, splits and embeds them
    into a FAISS vector store, and wires a `retrieve -> generate` graph to answer questions
    grounded in the retrieved context.

    This phase establishes the foundation that subsequent phases build upon with corrective layers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load Documents

    Load the three ML/DL textbooks using `PyPDFLoader`. Pages are cached to
    `cache/documents.json` on the first run -- subsequent runs skip the expensive PDF
    parsing step and deserialize directly from the cache.
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
    _cache_path = lab_root / "cache" / "documents.json"

    if _cache_path.exists():
        docs = [Document(**item) for item in json.loads(_cache_path.read_text())]
    else:
        _data = lab_root / "data"
        docs = (
            PyPDFLoader(str(_data / "deep_learning_book.pdf")).load()
            + PyPDFLoader(str(_data / "hands_on_ml.pdf")).load()
            + PyPDFLoader(str(_data / "pattern_recognition_and_ml_book.pdf")).load()
        )
        _cache_path.parent.mkdir(parents=True, exist_ok=True)
        _cache_path.write_text(json.dumps([doc.model_dump() for doc in docs]))
    return (docs,)


@app.cell
def _(docs, mo):
    mo.callout(mo.md(f"Loaded **{len(docs)}** pages across 3 PDFs."), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each PDF page becomes a `Document` object with raw text and source metadata (`source`, `page`).
    The three books -- *Deep Learning* (Goodfellow et al.), *Hands-On Machine Learning* (Geron),
    and *Pattern Recognition and Machine Learning* (Bishop) -- together form the knowledge base.
    All subsequent steps (chunking, embedding, retrieval) operate on this collection.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Chunk Documents

    Split the loaded documents into smaller overlapping windows for embedding. Full pages are
    too long to embed meaningfully -- chunking gives the retriever finer-grained units to match
    against a query. A chunk size of 900 characters with 150-character overlap keeps each chunk
    self-contained while preserving context at boundaries.
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
    # Clean the chunk texts to avoid any UnicodeEncodeError (surrogates from PDF extraction)
    for d in chunks:
        d.page_content = d.page_content.encode("utf-8", "ignore").decode(
            "utf-8", "ignore"
        )
    return


@app.cell
def _(chunks, mo):
    mo.callout(mo.md(f"Split into **{len(chunks)}** chunks (chunk_size=900, overlap=150)."), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each chunk is the atomic unit that gets embedded and indexed. A Unicode cleaning pass
    strips surrogates introduced by PDF extraction to prevent encoding errors downstream.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Embeddings

    Set up the Azure OpenAI embeddings model (`text-embedding-3-large`). Credentials
    (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`) are read from `.env` via `python-dotenv`.
    `check_embedding_ctx_length=False` disables the client-side length guard -- the Azure deployment
    handles truncation server-side, so the extra check would raise false errors on longer chunks.
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
    from langchain_openai import OpenAIEmbeddings

    return (OpenAIEmbeddings,)


@app.cell
def _(OpenAIEmbeddings, api_key, base_url):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=api_key,
        base_url=base_url,
        check_embedding_ctx_length=False,
    )
    return (embeddings,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The embeddings model maps text to dense numerical vectors. Semantic similarity between query
    and chunk vectors drives retrieval -- semantically close chunks rank higher than keyword-matched ones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Vector Store

    Build or load a FAISS index from the embedded chunks.
    If a persisted index already exists in `vector_store/`, it is loaded to avoid re-embedding on every run.
    """)
    return


@app.cell
def _():
    from langchain_community.vectorstores import FAISS

    return (FAISS,)


@app.cell
def _(FAISS, chunks, embeddings, lab_root):
    _vector_store_path = lab_root / "vector_store"

    if (_vector_store_path / "index.faiss").is_file():
        vector_store = FAISS.load_local(
            str(_vector_store_path), embeddings, allow_dangerous_deserialization=True
        )
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(str(_vector_store_path))
    return (vector_store,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The FAISS index is now ready. On first run it embeds all chunks and persists the index to `vector_store/`;
    subsequent runs skip re-embedding and load the saved index directly -- saving significant time and cost.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Retriever

    Wrap the vector store as a LangChain retriever.
    Similarity search returns the top `k=4` most relevant chunks for a given query.
    """)
    return


@app.cell
def _(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 4}
    )
    return (retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The retriever wraps the vector store with a search interface. At query time it embeds the question
    and returns the `k` most semantically similar chunks as `Document` objects ready for the generation step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Language Model

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used to generate answers from retrieved context.
    """)
    return


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
    The LLM handles the generation step -- it reads the retrieved context and composes a grounded answer.
    The same instance is reused across all invocations of the graph.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Graph State

    Defines the shared data structure that LangGraph passes between every node in the pipeline.
    All reads and writes happen through this typed dict -- it is the single source of truth at each step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### State Schema

    The shared typed dictionary that LangGraph passes between every node. Each field is
    either written by one node and read by the next, or populated at the start and carried
    through unchanged.

    **Base RAG fields**:
    - `question` -- the user's input query
    - `docs` -- raw chunks returned by the retriever
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
    ## 8. Nodes

    Two node functions implement the baseline RAG pipeline. Each reads from and writes to
    the shared `State` dict. The execution path is linear -- no conditional branching.

    - **`retrieve`** -- fetch the top-k chunks from the vector store
    - **`generate`** -- synthesize an answer from the retrieved chunks using the LLM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8a. Retrieve Node

    Fetches the top `k` semantically similar chunks from the vector store for the given question.
    The raw chunks are passed directly to the `generate` node -- no quality filtering in this phase.
    """)
    return


@app.cell
def _(State, retriever):
    def retrieve(state: State) -> dict:
        return {"docs": retriever.invoke(state["question"])}

    return (retrieve,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8b. Generate Node

    Constructs an answer from the retrieved chunks using the LLM. The system prompt instructs
    the model to answer only from context, reducing hallucination on out-of-context questions.

    All retrieved `docs` are concatenated into a single context string and passed to the prompt
    together with the user's question.
    """)
    return


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate

    return (ChatPromptTemplate,)


@app.cell
def _(ChatPromptTemplate):
    sys_msg = """You are a helpful ML tutor. Answer ONLY using the provided context.
    If the context is empty or insufficient, simply say: "I don't know based on the provided books."
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
    `retrieve` and `generate` implement the full RAG loop: pull context, then synthesize. Both functions
    read from and write to the shared `State` dict that LangGraph passes between nodes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Build the Graph

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
    The compiled graph is a runnable pipeline. Calling `graph.invoke(state)` triggers the full
    `retrieve -> generate` flow and returns the updated state with `answer` populated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe the pipeline's behavior across different question types:**

    | Question | Expected behavior | What to observe |
    |---|---|---|
    | "Explain the bias-variance trade-off" | In-context answer | LLM grounds its answer in retrieved chunks from the textbooks. |
    | "What are the latest major AI news?" | Out-of-context decline | No relevant chunks are retrieved; the LLM should decline to answer. |
    | "How NLP is connected with LLMs?" | Parametric injection risk | The textbooks cover NLP at a foundational level but not LLMs -- the LLM may answer from pretraining knowledge rather than retrieved context. |
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
        value="Explain the bias-variance trade-off",
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
    ## 11. Analysis

    Inspect the intermediate state produced by the pipeline run above -- retrieved documents
    and how much raw context was passed to the LLM unfiltered. All sections below are read-only
    views of `resp`; re-running section 10 refreshes them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Explore Retrieved Documents

    The `k=4` raw chunks retrieved from the vector store. In this baseline phase all chunks
    are passed directly to the LLM without any evaluation or filtering. Expand each to inspect
    the raw content that formed the generation context.
    """)
    return


@app.cell
def _(mo, resp):
    raw_context = "\n\n".join(d.page_content for d in resp["docs"])
    mo.vstack([
        mo.accordion({
            f"Doc {i + 1}": mo.md(d.page_content)
            for i, d in enumerate(resp["docs"])
        }),
        mo.callout(
            mo.md(
                f"**Total raw context:** {len(raw_context):,} characters"
                f" across {len(resp['docs'])} chunks -- passed to the LLM unfiltered."
            ),
            kind="info",
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Parametric Knowledge Injection

    A core limitation of this baseline pipeline. When a question sits at the edge of the
    loaded content -- such as `"How NLP is connected with LLMs?"` -- the textbooks return
    foundational NLP chunks but nothing LLM-specific. Instead of declining, the LLM often
    fills the gap using facts learned during pretraining, not from the retrieved context.

    This behavior is called **parametric knowledge injection**: the model injects its own
    training knowledge into what should be a context-grounded answer. It can appear helpful
    on familiar topics, but the same mechanism causes real problems in production -- the LLM
    fabricates a plausible-sounding answer when no matching document is retrieved.

    **This is the core problem that subsequent phases address** -- by grading retrieved
    documents for relevance and falling back to corrective steps when the vector store
    cannot help.
    """)
    return


if __name__ == "__main__":
    app.run()
