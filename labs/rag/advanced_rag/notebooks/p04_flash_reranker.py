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
    # RAG: Dense Retrieval with FlashRank Reranking

    FlashRank is a lightweight library for reranking retrieved documents in a retrieval-augmented generation (RAG) pipeline. After an initial search returns candidate passages, a reranker scores each query-passage pair and sorts the candidates by estimated relevance. The generator can then use the highest-ranked passages as context.

    FlashRank provides compact reranking models that can run locally, including on CPU. This can avoid a hosted reranking API, though latency and ranking quality depend on the selected model, hardware, and candidate set. Reranking adds work after retrieval, so it is most useful when the initial search can return a broad candidate pool and the final context should be more selective.

    This notebook builds a LangGraph RAG pipeline over the RAG paper (PDF). A FAISS dense retriever fetches `k=10` candidate chunks, a local FlashRank cross-encoder reranks them, and the top 4 chunks are passed to the LLM to generate a grounded answer. It is the local-reranker counterpart of `p03_reranking.py`, which uses a hybrid retriever and the hosted Cohere reranker.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Core Concept

    ### Where reranking fits

    1. Receive the user's question.
    2. Run an initial retriever, such as vector search, to collect candidate passages (for example, the top 10).
    3. Score each candidate against the question with FlashRank.
    4. Sort candidates by reranker score and keep the desired number (for example, the top 3).
    5. Pass the selected passages and original question to the generator.

    The candidate counts are configuration choices, not fixed requirements. Reranking can reorder and filter retrieved passages; it does not recover a passage that the initial retriever did not return.

    ### Bi-encoder retrieval and cross-encoder reranking

    | Method | How it scores relevance | Typical role |
    | --- | --- | --- |
    | Bi-encoder | Encodes the query and each passage separately, then compares their vectors. | Fast first-stage search over a large collection. |
    | Cross-encoder | Reads the query and passage together and produces a relevance score for that pair. | More detailed second-stage ranking of a smaller candidate set. |

    Because a cross-encoder evaluates query-passage pairs, it generally costs more per candidate than comparing precomputed vectors. Applying it to a shortlist keeps the work manageable. The returned score is a ranking signal; it should not automatically be interpreted as a calibrated probability.

    ### FlashRank vs. Cohere Rerank

    Both rerankers plug into LangChain's `ContextualCompressionRetriever` the same way (`FlashrankRerank` and `CohereRerank`), so switching is a small change. `p03_reranking.py` uses Cohere; this notebook uses FlashRank.

    | Aspect | FlashRank | Cohere Rerank |
    | --- | --- | --- |
    | Deployment | Runs locally in-process (ONNX Runtime, CPU-friendly). | Hosted API call. |
    | Credentials and cost | No API key; open-source library. The cost is local compute. | Requires `COHERE_API_KEY`; usage-based billing. |
    | Data handling | Query and passages stay on the machine. | Query and passages are sent to an external service. |
    | Models | Small models chosen by name, from ~4MB to ~150MB (for example `ms-marco-MiniLM-L-12-v2`). | Managed model selected by name (for example `rerank-v3.5`); weights are not available. |
    | Setup | Downloads the model on first run into `cache_dir`. | Nothing to download; needs network access. |
    | Latency | Depends on CPU, model size, and number of candidates; no network round trip. | Network round trip plus provider processing time. |
    | Languages | MS MARCO models are English-focused; `ms-marco-MultiBERT-L-12` covers 100+ languages. | `rerank-v3.5` is multilingual. |
    | Ranking quality | Depends on the chosen model; larger models are slower. | Managed, larger model; quality varies by domain. |
    | Best fit | Offline, privacy-sensitive, low-cost, or serverless setups. | Teams that prefer a managed service and can send data to a vendor. |

    Ranking quality differs by domain and query type, so compare both on your own data before choosing.

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

    Split the loaded pages into smaller overlapping windows so the dense vector store
    can operate on finer-grained retrieval units. A chunk size of
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
    Each chunk is the atomic retrieval unit for the dense retriever. A unique integer
    `chunk_id` is added to every chunk's metadata so chunks can be traced through
    retrieval and reranking. The same pass strips surrogates introduced by PDF extraction
    to prevent encoding errors in the embedding step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Embeddings

    Set up the Azure OpenAI embeddings model (`text-embedding-3-large`).
    `check_embedding_ctx_length=False` disables the client-side length guard -- the Azure
    deployment handles truncation server-side, so the extra check would raise false errors
    on longer chunks.

    Credentials (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`) are read from `.env`
    via `python-dotenv` and reused by the language model in section 7.
    """)
    return


@app.cell
def _():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    return (os,)


@app.cell
def _():
    from langchain_openai import OpenAIEmbeddings

    return (OpenAIEmbeddings,)


@app.cell
def _(os):
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url = os.getenv("AZURE_OPENAI_ENDPOINT")
    return api_key, base_url


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
    ## 4. Vector Store

    Build or load a FAISS index from the embedded chunks. If a persisted index already
    exists in `vector_store/faiss/rag_paper/`, it is loaded to avoid re-embedding on every
    run -- saving significant time and API cost.

    The persisted index stores each chunk's metadata, including `chunk_id`. If the
    chunking logic changes, delete `vector_store/faiss/rag_paper/` so the index is rebuilt.
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
    ## 5. Retriever

    Wrap the FAISS vector store as a LangChain retriever. At query time the question is
    embedded with `text-embedding-3-large` and the `k=10` nearest chunks by vector distance
    are returned. FAISS defaults to L2 distance; for normalized OpenAI embeddings the
    ranking is equivalent to cosine similarity. This finds semantically related chunks even
    when the query and document use different words.

    `k=10` is deliberately larger than the final context size. The dense retriever is the
    **recall** stage: it produces a broad candidate pool that the reranker in section 6
    narrows down to the top 4 chunks.
    """)
    return


@app.cell
def _(vector_store):
    dense_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )
    return (dense_retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Reranker

    The reranker sits between the dense retriever and the LLM. It takes the 10 candidate
    chunks returned by FAISS and re-scores each one against the query using a cross-encoder,
    then returns only the top 4 highest-scored chunks. This two-stage design keeps the
    retrieval step fast (FAISS dense search) while using the more expensive cross-encoder
    only on a small shortlist.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6a. FlashRank Reranker

    #### Why FlashRank?

    FlashRank is an ultra-lite Python library for reranking search and retrieval results.

    - **Ultra-lite:** No heavy dependencies. Runs on CPU, and the default reranking model is only ~4MB.
    - **Fast:** Speed depends on the number of tokens in the query and passages, and on the model depth.
    - **Cost-efficient:** Well suited to serverless deployments with tight memory and time limits.
    - **Cross-encoder based:** Ships distilled cross-encoder models such as `ms-marco-TinyBERT-L-2-v2` and `ms-marco-MiniLM-L-12-v2`.
    - **Low overhead:** Designed for minimal latency in user-facing applications.

    #### Model Choices

    Calling `Ranker()` without a model name uses the default `ms-marco-TinyBERT-L-2-v2` (~4MB), a very fast model with competitive ranking precision.

    Alternatively, pass a model name explicitly. Some options:

    - **Small (~34MB):** slightly slower, better ranking precision. Example: `ms-marco-MiniLM-L-12-v2`
    - **Medium (~110MB):** slower still. Example: `rank-T5-flan`, a T5-based reranker
    - **Large (~150MB):** slower, supports 100+ languages. Example: `ms-marco-MultiBERT-L-12`

    FlashRank also ships specialised models (for example e-commerce search and Arabic) and an LLM-based listwise reranker (`rank_zephyr_7b_v1_full`) that is several GB and not suited to lightweight setups.

    **This notebook uses `ms-marco-MiniLM-L-12-v2`**: a good balance between ranking precision and size for a small candidate pool of 10 chunks.

    #### Configuration

    - **`Ranker(model_name, cache_dir)`:** loads the ONNX model. On the first run the model is downloaded into `cache_dir` (here `cache/models/`, which is gitignored); later runs load it from disk.
    - **`FlashrankRerank(top_n=4)`:** the LangChain wrapper. It scores all 10 candidates and keeps the top 4. Each returned chunk carries a `relevance_score` in its metadata, and its original metadata (including `chunk_id`) is preserved.
    - **`score_threshold`:** optional minimum score for a chunk to be returned. It defaults to `0.0` and is not used here.
    """)
    return


@app.cell
def _():
    from flashrank import Ranker

    return (Ranker,)


@app.cell
def _(Ranker, lab_root):
    model = "ms-marco-MiniLM-L-12-v2"
    client = Ranker(model_name=model, cache_dir=str(lab_root / "cache" / "models"))
    return client, model


@app.cell
def _():
    from langchain_community.document_compressors import FlashrankRerank

    return (FlashrankRerank,)


@app.cell
def _(FlashrankRerank, client, model):
    reranker = FlashrankRerank(
        client=client,
        model=model,
        top_n=4,
    )
    return (reranker,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6b. Compression Retriever

    `ContextualCompressionRetriever` wires the reranker as a post-processing step on top
    of any base retriever. It passes the base retriever's output through the
    `base_compressor` and returns the compressor's filtered, reranked result.

    In this pipeline:
    - **`base_retriever`** (`dense_retriever`): the FAISS dense retriever that returns
      the top `k=10` most semantically similar chunks
    - **`base_compressor`** (`reranker`): FlashRank scores all 10 candidates and returns
      the top `top_n=4` by relevance score

    The result -- `retriever` -- is a single object that the `retrieve` node can invoke
    like any other LangChain retriever. The full retrieval + rerank pipeline is transparent
    to the graph.
    """)
    return


@app.cell
def _():
    from langchain_classic.retrievers import ContextualCompressionRetriever

    return (ContextualCompressionRetriever,)


@app.cell
def _(ContextualCompressionRetriever, dense_retriever, reranker):
    retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=dense_retriever,
    )
    return (retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Language Model

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used to generate answers from
    the retrieved context. Credentials are already loaded from section 3.
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
    ## 8. Graph State

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
    - `docs` -- top-N chunks returned by the FlashRank reranker, ordered by relevance score
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
    ## 9. Nodes

    Two node functions implement the RAG pipeline. Each reads from and writes to the
    shared `State` dict. The execution path is linear -- no conditional branching.

    - **`retrieve`** -- invoke the compression retriever to get the top reranked chunks
    - **`generate`** -- synthesize an answer from the reranked chunks using the LLM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9a. Retrieve Node

    Invokes the `ContextualCompressionRetriever` with the question. Internally this
    triggers the full retrieval + rerank pipeline in sequence:

    1. The FAISS dense retriever returns the top `k=10` most semantically similar chunks.
    2. FlashRank scores all 10 candidate chunks against the query using a cross-encoder.
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
    ### 9b. Generate Node

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
    ## 10. Build the Graph

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
    ## 11. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe the pipeline's behavior across different question types:**

    | Question | Type | Expected behavior |
    |---|---|---|
    | "What are the two main components of the RAG model?" | Basic | Grounded answer; reranker should rank the chunk that directly names the components first. |
    | "What is the difference between RAG-Sequence and RAG-Token?" | Basic | The reranker should surface the defining paragraph over surrounding context chunks. |
    | "Which knowledge source is used by the RAG models?" | Basic | Answer in the retrieval architecture section; reranker should rank it above less specific chunks. |
    | "How does RAG combine parametric and non-parametric memory?" | Technical | Requires synthesizing across sections; tests whether reranking promotes the most synthesis-relevant chunks. |
    | "What role does the DPR question encoder play in retrieval?" | Technical | Specific technical detail; reranker should promote the DPR-specific passage over tangentially related chunks. |
    | "How does RAG marginalize over retrieved documents when generating answers?" | Technical | Dense technical content; tests whether the cross-encoder identifies the marginalization passage over adjacent text. |
    | "Explain how a diesel engine works." | Unrelated | Retrieval still returns 10 candidates and the reranker keeps 4, but their scores should be low; LLM should decline to answer. |
    | "What causes thunderstorms?" | Unrelated | Retrieval still returns 10 candidates and the reranker keeps 4, but their scores should be low; LLM should decline to answer. |
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
    ## 12. Analysis

    Inspect the intermediate state produced by the pipeline run above -- the reranked
    chunks, their FlashRank relevance scores, and how much context was passed to the LLM.
    All sections below are read-only views of `resp`; re-running section 11 refreshes them.
    """)
    return


@app.cell
def _():
    import altair as alt
    import pandas as pd

    return alt, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retrieved Documents

    The top `top_n=4` chunks returned by the FlashRank reranker, ordered by relevance score.
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

    FlashRank relevance scores for each reranked chunk, with the chunk's `chunk_id`, source
    page, and a short snippet. The scores reflect the cross-encoder's direct assessment of
    how well each chunk addresses the query; higher means stronger relevance. They fall
    between 0 and 1 but are not calibrated probabilities -- compare them within a single
    query run rather than across different queries.
    """)
    return


@app.cell
def _(mo, resp):
    rows = [
        {
            "Rank": i + 1,
            "Relevance Score": round(d.metadata.get("relevance_score", 0.0), 4),
            "Chunk ID": d.metadata.get("chunk_id", ""),
            "Page": d.metadata.get("page", ""),
            "Snippet": d.page_content[:150].replace("\n", " ") + "...",
        }
        for i, d in enumerate(resp["docs"])
    ]
    mo.ui.table(rows)
    return (rows,)


@app.cell
def _(pd, rows):
    df = pd.DataFrame(rows)
    return (df,)


@app.cell
def _(alt, df):
    _chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(field='Chunk ID', type='nominal'),
            y=alt.Y(field='Relevance Score', type='quantitative', stack=True),
            color=alt.Color(field='Relevance Score', type='quantitative', scale={
                'scheme': 'blues'
            }),
            tooltip=[
                alt.Tooltip(field='Rank'),
                alt.Tooltip(field='Relevance Score', format=',.2f'),
                alt.Tooltip(field='Chunk ID'),
                alt.Tooltip(field='Page'),
                alt.Tooltip(field='Snippet')
            ]
        )
        .properties(
            title='Relevance Score by Chunk ID',
            height=290,
            width='container',
            config={
                'axis': {
                    'grid': False
                }
            }
        )
    )
    _chart
    return


@app.cell
def _(alt, df):
    _chart = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X(field='Page', type='nominal'),
            y=alt.Y(aggregate='count', type='quantitative', title='Chunk Count'),
            color=alt.Color(aggregate='count', type='quantitative'),
            tooltip=[
                alt.Tooltip(field='Page', format=',.2f'),
                alt.Tooltip(aggregate='count'),
                alt.Tooltip(aggregate='count')
            ]
        )
        .properties(
            title='Relevant Chunk Count by PDF Document Page',
            height=290,
            width='container',
            config={
                'axis': {
                    'grid': True
                }
            }
        )
    )
    _chart
    return


if __name__ == "__main__":
    app.run()
