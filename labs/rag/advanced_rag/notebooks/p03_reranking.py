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
    # RAG: Hybrid Retrieval with Reranking

    A RAG pipeline built with LangGraph that combines hybrid retrieval with a neural
    reranking stage. It loads a PDF document, splits it into chunks, retrieves candidate
    documents using a BM25 + FAISS ensemble, and then reranks those candidates using
    Cohere's cross-encoder API.

    The highest-scored chunks are passed to the generation stage to produce an answer
    grounded in the most relevant retrieved context.

    This phase extends the hybrid retrieval pipeline by introducing **reranking**, which
    refines the ordering of retrieved candidates before they are used for answer generation.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reranking

    **Reranking** is a retrieval refinement technique that takes an initial set of candidate
    documents and reorders them according to their relevance to a user query. Unlike a
    retriever, which searches a corpus to find candidate documents, a reranker evaluates
    an existing shortlist to identify the most relevant results.

    In a RAG pipeline, reranking is applied after hybrid retrieval, where BM25 and dense
    vector retrieval provide complementary candidate documents. A neural reranker evaluates
    the relationship between the query and each candidate chunk to produce a refined ranking.

    ### How It Works

    1. Retrieve candidate chunks using BM25 and dense vector retrieval.
    2. Combine the candidates using an ensemble retrieval strategy (RRF).
    3. Send the query and candidate chunks to the reranking model.
    4. Calculate relevance scores for each query-chunk pair.
    5. Sort the chunks by their relevance scores.
    6. Select the top-ranked chunks.
    7. Pass the selected context to the LLM to generate an answer.

    ### Reranking with Cohere

    - **Cohere Rerank:** A hosted reranking API that uses a cross-encoder to score each
      candidate chunk against the query. Unlike bi-encoders used in dense retrieval, a
      cross-encoder reads the query and document *together* -- capturing fine-grained
      interaction between them that retrieval-time embeddings cannot express.
    - **Relevance scores:** Each returned chunk carries a `relevance_score` in its metadata.
      These scores reflect query-document relevance as assessed by the cross-encoder. They
      are not probabilities and should not be interpreted as a confidence that the chunk
      contains a correct answer.
    - **Top-N selection:** Only the top-N highest-scored chunks are returned for downstream
      generation, reducing noise in the LLM's context window.

    ### Why Use Reranking?

    - **Improved ordering:** Promotes more relevant chunks that may have ranked lower in the
      initial RRF output.
    - **Cross-encoder precision:** Captures query-document interaction that neither BM25 nor
      bi-encoder embeddings can model.
    - **Reduced context noise:** Filters the candidate set down to only the most relevant
      chunks before passing them to the LLM.
    - **Complementary to hybrid retrieval:** Hybrid retrieval maximizes recall; reranking
      maximizes precision from that candidate set.

    ### Hybrid Retrieval vs. Reranking

    - **Hybrid retrieval** finds candidate documents by combining multiple retrieval methods.
      Its goal is **recall** -- surface as many potentially relevant chunks as possible.
    - **Reranking** evaluates those candidates against the query and re-orders them by
      relevance. Its goal is **precision** -- promote the most useful chunks to the top.

    Reranking does not recover documents that were absent from the initial candidate set.
    Its effectiveness therefore depends on the quality and coverage of the first-stage
    retrieval.

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
    # Add unique chunk_id to each Document metadata
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
    Each chunk is the atomic retrieval unit shared by both retrievers. A Unicode cleaning
    pass strips surrogates introduced by PDF extraction to prevent encoding errors in both
    the BM25 index and the embedding step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Ensemble Retriever

    Two retrievers are built from the same set of chunks and combined via RRF to produce
    a candidate set for the reranker. The ensemble's job is **recall** -- surface as many
    potentially relevant chunks as possible before the reranker filters them down.

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
    via `python-dotenv` and reused by the language model in section 5.
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
    Reciprocal Rank Fusion (RRF). The merged candidate set -- up to 8 chunks when there is
    no overlap -- is passed to the reranker in the next section for precision refinement.
    """)
    return


@app.cell
def _():
    from langchain_classic.retrievers import EnsembleRetriever

    return (EnsembleRetriever,)


@app.cell
def _(EnsembleRetriever, dense_retriever, sparse_retriever):
    ensemble_retriever = EnsembleRetriever(
        retrievers=[sparse_retriever, dense_retriever],
        weights=[0.5, 0.5],
        c=60,
    )
    return (ensemble_retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Reranker

    The reranker sits between the ensemble retriever and the LLM. It takes the candidate
    chunks produced by RRF and re-scores each one against the query using a cross-encoder,
    then returns only the top-N highest-scored chunks. This two-stage design keeps the
    retrieval step fast (BM25 + FAISS) while using the more expensive cross-encoder only
    on a small shortlist.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4a. Cohere Reranker

    `CohereRerank` is a hosted cross-encoder that scores each candidate chunk against the
    query by reading them *together* in a single forward pass. This gives the model access
    to token-level interaction between query and document -- something bi-encoder embeddings
    cannot capture because they encode query and document independently.

    - **`model="rerank-v3.5"`:** Cohere's latest reranking model, optimized for relevance
      scoring across multilingual content.
    - **`top_n=4`:** number of chunks to return after reranking. The model scores all
      incoming candidates and keeps only the top 4. Each returned chunk carries a
      `relevance_score` in its metadata.
    - **`cohere_api_key`:** credentials read from `.env` via `COHERE_API_KEY`.
    """)
    return


@app.cell
def _():
    from langchain_cohere import CohereRerank

    return (CohereRerank,)


@app.cell
def _(os):
    cohere_api_key = os.getenv("COHERE_API_KEY")
    return (cohere_api_key,)


@app.cell
def _(CohereRerank, cohere_api_key):
    reranker = CohereRerank(
        model="rerank-v3.5",
        top_n=4,
        cohere_api_key=cohere_api_key
    )
    return (reranker,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4b. Compression Retriever

    `ContextualCompressionRetriever` wires the reranker as a post-processing step on top
    of any base retriever. It passes the base retriever's output through the
    `base_compressor` and returns the compressor's filtered, reranked result.

    In this pipeline:
    - **`base_retriever`** (`ensemble_retriever`): runs BM25 + FAISS and returns up to
      4-8 candidate chunks via RRF
    - **`base_compressor`** (`reranker`): scores all candidates and returns the top
      `top_n=4` by relevance score

    The result -- `retriever` -- is a single object that the `retrieve` node can invoke
    like any other LangChain retriever. The full hybrid + rerank pipeline is transparent
    to the graph.
    """)
    return


@app.cell
def _():
    from langchain_classic.retrievers import ContextualCompressionRetriever

    return (ContextualCompressionRetriever,)


@app.cell
def _(ContextualCompressionRetriever, ensemble_retriever, reranker):
    retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=ensemble_retriever,
    )
    return (retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Language Model

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used to generate answers from
    the retrieved context. Credentials are already loaded from section 3b.
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
    ## 6. Graph State

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
    - `docs` -- top-N chunks returned by the Cohere reranker, ordered by relevance score
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
    ## 7. Nodes

    Two node functions implement the RAG pipeline. Each reads from and writes to the
    shared `State` dict. The execution path is linear -- no conditional branching.

    - **`retrieve`** -- invoke the compression retriever to get the top reranked chunks
    - **`generate`** -- synthesize an answer from the reranked chunks using the LLM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7a. Retrieve Node

    Invokes the `ContextualCompressionRetriever` with the question. Internally this
    triggers the full hybrid + rerank pipeline in sequence:

    1. `ensemble_retriever` runs BM25 and FAISS in parallel and merges results via RRF.
    2. The Cohere reranker scores all candidate chunks against the query.
    3. The top `top_n=4` reranked chunks are returned, each with a `relevance_score` in
       its metadata.

    The reranked chunks are passed directly to the `generate` node.
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
    ### 7b. Generate Node

    Constructs an answer from the reranked chunks using the LLM. The system prompt
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
    ## 8. Build the Graph

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
    ## 9. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe the pipeline's behavior across different question types:**

    | Question | Type | Expected behavior |
    |---|---|---|
    | "What are the two main components of the RAG model?" | Basic | Grounded answer; reranker should confidently promote the chunk that directly names the components. |
    | "What is the difference between RAG-Sequence and RAG-Token?" | Basic | The reranker should surface the defining paragraph over surrounding context chunks. |
    | "Which knowledge source is used by the RAG models?" | Basic | Answer in the retrieval architecture section; reranker should rank it above less specific chunks. |
    | "How does RAG combine parametric and non-parametric memory?" | Technical | Requires synthesizing across sections; tests whether reranking promotes the most synthesis-relevant chunks. |
    | "What role does the DPR question encoder play in retrieval?" | Technical | Specific technical detail; reranker should promote the DPR-specific passage over tangentially related chunks. |
    | "How does RAG marginalize over retrieved documents when generating answers?" | Technical | Dense technical content; tests whether the cross-encoder identifies the marginalization passage over adjacent text. |
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
    ## 10. Analysis

    Inspect the intermediate state produced by the pipeline run above -- the reranked
    chunks, their Cohere relevance scores, and how much context was passed to the LLM.
    All sections below are read-only views of `resp`; re-running section 9 refreshes them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retrieved Documents

    The top `top_n=4` chunks returned by the Cohere reranker, ordered by relevance score.
    These are the final chunks passed to the LLM. Each chunk carries a `relevance_score`
    in its metadata assigned by the cross-encoder. Expand each to inspect the content that
    formed the generation context.
    """)
    return


@app.cell
def _(mo, resp):
    _raw_context = "\n\n".join(d.page_content for d in resp["docs"])
    mo.vstack([
        mo.accordion({
            f"Doc {i + 1}  |  Score: {round(d.metadata.get('relevance_score', 0.0), 4)}": mo.md(d.page_content)
            for i, d in enumerate(resp["docs"])
        }),
        mo.callout(
            mo.md(
                f"**Total raw context:** {len(_raw_context):,} characters"
                f" across {len(resp['docs'])} chunks -- passed to the LLM."
            ),
            kind="info",
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Chunk Ranking

    Cohere relevance scores for each reranked chunk. Unlike RRF, these scores reflect the
    cross-encoder's direct assessment of how well each chunk addresses the query. Higher
    scores indicate stronger relevance. Scores are not probabilities and are not normalized
    -- they are comparable within a single query run but not across different queries.
    """)
    return


@app.cell
def _(mo, resp):
    _rows = [
        {
            "Rank": i + 1,
            "Relevance Score": round(d.metadata.get("relevance_score", 0.0), 4),
            "Page": d.metadata.get("page", ""),
            "Snippet": d.page_content[:150].replace("\n", " ") + "...",
        }
        for i, d in enumerate(resp["docs"])
    ]
    mo.ui.table(_rows)
    return


if __name__ == "__main__":
    app.run()
