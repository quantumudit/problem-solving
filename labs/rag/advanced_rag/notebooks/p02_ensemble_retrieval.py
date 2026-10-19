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
    # RAG: Hybrid Retrieval

    A hybrid RAG pipeline built with LangGraph. Loads a PDF document, splits it into
    chunks, and combines a BM25 sparse retriever with a FAISS dense retriever using an
    ensemble strategy. The pipeline wires a `retrieve -> generate` graph to answer
    questions grounded in the retrieved context.

    This phase introduces **hybrid retrieval** by fusing keyword-based matching with
    semantic similarity search. Using LangChain's `EnsembleRetriever` with Reciprocal
    Rank Fusion (RRF), the pipeline combines rankings from both retrievers to improve
    retrieval coverage over either approach used alone.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hybrid Retrieval

    **Hybrid retrieval** combines two or more retrieval approaches to improve the relevance
    and coverage of retrieved documents. In a typical RAG pipeline it pairs **sparse
    retrieval** (BM25) with **dense retrieval** (vector embeddings).

    Sparse retrieval excels at matching exact terms, technical keywords, identifiers, and
    named entities. Dense retrieval can find conceptually related content even when the
    query and document use different wording. Combining them addresses the blind spots of
    each approach when used independently.

    ### How It Works

    1. Load and split documents into chunks.
    2. Build a sparse index using BM25.
    3. Generate embeddings for the document chunks and store them in a vector store.
    4. Process the user query through both retrievers independently.
    5. Combine the ranked results from both retrievers using Reciprocal Rank Fusion (RRF).
    6. Return the top-k fused documents to the RAG pipeline.
    7. Pass the retrieved context to the LLM to generate an answer.

    ### Components of Hybrid Retrieval

    - **Sparse Retriever (BM25):** Matches query terms against document terms and ranks
      chunks using lexical relevance scores.
    - **Dense Retriever:** Embeds queries and chunks into vector representations and
      retrieves chunks based on semantic similarity.
    - **Ensemble Retriever:** Combines the rankings from multiple retrievers, allowing
      lexical and semantic signals to complement each other.
    - **Reciprocal Rank Fusion (RRF):** Merges rankings by combining the reciprocal rank
      of each document from each retriever. This avoids directly comparing raw BM25 scores
      with vector similarity scores, which have different scales and distributions.

    ### Why Combine Sparse and Dense Retrieval?

    - **Exact terminology:** BM25 reliably retrieves chunks containing specific technical
      terms, model names, or identifiers that a dense retriever may miss.
    - **Semantic matching:** Dense retrieval finds conceptually relevant chunks that use
      synonyms or different phrasing that BM25 would score as zero.
    - **Improved coverage:** Combining both approaches captures useful chunks that either
      retriever would miss individually.
    - **Complementary signals:** RRF balances exact lexical matches against semantic
      relevance without requiring score normalization.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load Documents

    Load the RAG paper using `PyPDFLoader`. Pages are cached to `cache/rag_paper.json`
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
    _cache_path = lab_root / "cache" / "rag_paper.json"

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

    Split the loaded pages into smaller overlapping windows so both the BM25 index and
    the dense vector store can operate on finer-grained retrieval units. A chunk size of
    900 characters with a 150-character overlap keeps each chunk self-contained while
    preserving context at paragraph boundaries.
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
    # Strip surrogates introduced by PDF extraction to prevent encoding errors downstream.
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
    Each chunk is the atomic retrieval unit shared by both retrievers. A Unicode cleaning
    pass strips surrogates introduced by PDF extraction to prevent encoding errors in both
    the BM25 index and the embedding step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Retrievers

    Two retrievers are built from the same set of chunks and later combined by the ensemble:

    - **Sparse Retriever (BM25):** lexical matching, no embedding required
    - **Dense Retriever (FAISS):** semantic matching via vector embeddings
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3a. Sparse Retriever: BM25

    BM25 (Best Matching 25) is a probabilistic ranking function that scores each chunk
    against a query using term frequency, inverse document frequency, and document-length
    normalization. It operates purely on token overlap -- no embeddings or vector store
    are needed.

    `BM25Retriever.from_documents` tokenizes all chunks and builds the index in one call.
    At query time it scores every chunk and returns the top `k` results as `Document`
    objects.
    """)
    return


@app.cell
def _():
    from langchain_community.retrievers import BM25Retriever

    return (BM25Retriever,)


@app.cell
def _(BM25Retriever, chunks):
    sparse_retriever = BM25Retriever.from_documents(chunks, k=4)
    return (sparse_retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3b. Dense Retriever: FAISS

    The dense retriever embeds every chunk using `text-embedding-3-large` and stores the
    vectors in a FAISS index. At query time the query is embedded and the `k` nearest
    neighbours by cosine similarity are returned. This retriever finds semantically related
    chunks even when the query and document use different words.

    Credentials (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`) are read from `.env`
    via `python-dotenv` and reused by the language model in the next section.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Embeddings

    Set up the Azure OpenAI embeddings model (`text-embedding-3-large`).
    `check_embedding_ctx_length=False` disables the client-side length guard -- the Azure
    deployment handles truncation server-side, so the extra check would raise false errors
    on longer chunks.
    """)
    return


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
    #### Vector Store

    Build or load a FAISS index from the embedded chunks. If a persisted index already
    exists in `vector_store/faiss/rag_paper/`, it is loaded to avoid re-embedding on every
    run -- saving significant time and API cost.
    """)
    return


@app.cell
def _():
    from langchain_community.vectorstores import FAISS

    return (FAISS,)


@app.cell
def _(FAISS, chunks, embeddings, lab_root):
    _vector_store_path = lab_root / "vector_store" / "faiss" / "rag_paper"

    if (_vector_store_path / "index.faiss").is_file():
        vector_store = FAISS.load_local(
            str(_vector_store_path), embeddings, allow_dangerous_deserialization=True
        )
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
        _vector_store_path.mkdir(parents=True, exist_ok=True)
        vector_store.save_local(str(_vector_store_path))
    return (vector_store,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Retriever

    Wrap the FAISS vector store as a LangChain retriever. Similarity search returns the
    top `k=4` most semantically similar chunks for a given query.
    """)
    return


@app.cell
def _(vector_store):
    dense_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )
    return (dense_retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3c. Ensemble Retriever

    `EnsembleRetriever` runs both retrievers independently and merges their results using
    **Reciprocal Rank Fusion (RRF)**. Because BM25 scores and vector similarity scores
    have different scales, RRF operates on rank positions rather than raw scores -- making
    the fusion scale-independent.

    #### Reciprocal Rank Fusion

    Each document receives a fused score computed as:

    $$\operatorname{RRF}(d) = \sum_{r \in R} \frac{w_r}{c + \operatorname{rank}_r(d)}$$

    Where:
    - $w_r$ -- the retriever's weight (controls its proportional influence on the final ranking)
    - $c$ -- a rank-fusion constant that controls how steeply rank contributions fall off
      with position (LangChain default: `c=60`)
    - $\operatorname{rank}_r(d)$ -- the document's position in that retriever's ranked list (1-indexed)

    Documents appearing near the top in both retrievers receive the highest fused scores.
    Documents found by only one retriever can still rank well if their rank in that list
    is high enough.

    #### Weight Configuration

    Weights control how much each retriever influences the final RRF ranking. They must
    always **sum to 1.0** -- the list order matches the `retrievers` list, so
    `weights=[0.5, 0.5]` means `[sparse_weight, dense_weight]`.

    - `0.5 / 0.5` -- equal contribution; neither retriever dominates
    - `0.7 / 0.3` -- sparse-heavy; lexical matches drive the ranking
    - `0.3 / 0.7` -- dense-heavy; semantic similarity drives the ranking

    **Recommended starting points by task type:**

    | Task / Corpus Type | Sparse (BM25) | Dense | Rationale |
    |---|---|---|---|
    | General / unknown query distribution | 0.5 | 0.5 | Balanced starting point; adjust after evaluation |
    | Technical docs, code, API references | 0.7 | 0.3 | Exact term matches (function names, identifiers) are critical |
    | Research papers, academic content | 0.4 | 0.6 | Concepts are expressed with varied terminology; semantic match helps more |
    | Conversational / open-domain QA | 0.3 | 0.7 | Queries rarely match document wording; dense retrieval dominates |
    | Mixed corpus (prose + technical content) | 0.5 | 0.5 | Neutral balance; adjust once you observe retrieval failures |
    | Small corpus (< 500 chunks) | 0.6 | 0.4 | BM25 generalizes well on small corpora; dense models need more data to shine |

    #### Expected Document Count

    Each retriever independently returns up to its own `k` documents. The ensemble merges
    both result sets and ranks all **unique** documents by RRF score. There is no separate
    output `k` -- the final chunk count depends entirely on how much the two result sets
    overlap.

    - **Maximum** = $k_{\text{sparse}} + k_{\text{dense}}$ -- when the two result sets share
      no documents at all (zero overlap)
    - **Minimum** = $\max(k_{\text{sparse}},\ k_{\text{dense}})$ -- when one retriever's
      results are a complete subset of the other's (full overlap)

    In practice the count usually falls somewhere between the two bounds. Higher overlap
    means both retrievers agree on relevance; lower overlap means they complement each other
    and together surface a wider set of candidates for the LLM.

    | k (BM25) | k (Dense) | Min chunks | Max chunks |
    |---|---|---|---|
    | 4 | 4 | 4 | 8 |
    | 2 | 4 | 4 | 6 |
    | 4 | 2 | 4 | 6 |
    | 3 | 5 | 5 | 8 |

    This notebook uses `k=4` for both retrievers, so the LLM receives between **4 and 8**
    chunks per query depending on result-set overlap.
    """)
    return


@app.cell
def _():
    from langchain_classic.retrievers import EnsembleRetriever

    return (EnsembleRetriever,)


@app.cell
def _(EnsembleRetriever, dense_retriever, sparse_retriever):
    retriever = EnsembleRetriever(
        retrievers=[sparse_retriever, dense_retriever],
        weights=[0.5, 0.5],
        c=60,
    )
    return (retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Language Model

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used to generate answers from
    the retrieved context. Credentials are already loaded from the previous section.
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
    - `docs` -- chunks returned by the ensemble retriever, ranked by RRF
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

    - **`retrieve`** -- fetch the top-k chunks from the ensemble retriever
    - **`generate`** -- synthesize an answer from the retrieved chunks using the LLM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6a. Retrieve Node

    Invokes the ensemble retriever with the question. Internally, `EnsembleRetriever` runs
    BM25 and FAISS in parallel, applies RRF to merge their ranked lists, and returns the
    top-k fused `Document` objects. The merged chunks are passed directly to the `generate`
    node -- no further filtering in this phase.
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
    | "What is the difference between RAG-Sequence and RAG-Token?" | Basic | Clear distinction in the paper; the ensemble should retrieve the right sections via both term match and semantic overlap. |
    | "Which knowledge source is used by the RAG models?" | Basic | Answer found in the retrieval architecture section. |
    | "How does RAG combine parametric and non-parametric memory?" | Technical | Requires synthesizing across multiple sections; tests whether RRF surfaces a better combined chunk set than either retriever alone. |
    | "What role does the DPR question encoder play in retrieval?" | Technical | Specific technical detail; BM25 should surface it via "DPR" keyword, dense retriever via semantic context. |
    | "How does RAG marginalize over retrieved documents when generating answers?" | Technical | Dense technical content; tests whether the ensemble retrieves the marginalization passage better than sparse alone. |
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

    Inspect the intermediate state produced by the pipeline run above -- the chunks
    returned by the ensemble retriever and how much raw context was passed to the LLM
    unfiltered. All sections below are read-only views of `resp`; re-running section 8
    refreshes them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retrieved Documents

    The chunks returned by the ensemble retriever after RRF fusion. All chunks are passed
    directly to the LLM without further filtering. Expand each to inspect the raw content
    that formed the generation context.
    """)
    return


@app.cell
def _(mo, resp):
    _raw_context = "\n\n".join(d.page_content for d in resp["docs"])
    mo.vstack([
        mo.accordion({
            f"Doc {i + 1}": mo.md(d.page_content)
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
    ### Chunk Ranking

    RRF rank order of the retrieved chunks. The ensemble does not expose a single numeric
    score per chunk -- the rank reflects the fused position after combining BM25 and
    FAISS rankings. Lower rank = higher relevance.
    """)
    return


@app.cell
def _(mo, resp):
    _rows = [
        {
            "Rank": i + 1,
            "Page": d.metadata.get("page", ""),
            "Snippet": d.page_content[:150].replace("\n", " ") + "...",
        }
        for i, d in enumerate(resp["docs"])
    ]
    mo.ui.table(_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What's Next: Reranking

    RRF produces a good merged ranking but it is purely position-based -- it fuses rank
    order signals from BM25 and FAISS without ever reading the chunk content against the
    query. A chunk ranked high by both retrievers rises to the top, but there is no
    guarantee it is the most relevant chunk for that specific question.

    **Reranking** adds a second pass on top of the fused set. A cross-encoder model reads
    the query and each candidate chunk *together* -- as a single input -- and outputs a
    relevance score for the pair. Because both the query and the chunk are visible at once,
    the cross-encoder captures nuanced query-document interaction that neither BM25 nor a
    bi-encoder embedding model can express.

    The typical flow in a reranked hybrid pipeline:

    1. Retrieve a wider candidate set using the ensemble (e.g., top 10-20 chunks via RRF).
    2. Pass all candidates through a reranker model.
    3. Re-sort by the reranker's relevance scores.
    4. Feed only the top-k reranked chunks to the LLM.

    This is explored in **Phase 3**, where a reranker is applied on top of the RRF output
    to produce a tighter, more query-relevant final context before generation.
    """)
    return


if __name__ == "__main__":
    app.run()
