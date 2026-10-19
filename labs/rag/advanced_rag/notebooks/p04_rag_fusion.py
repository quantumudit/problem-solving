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
    # RAG Fusion

    RAG-Fusion extends retrieval-augmented generation by searching with several related queries instead of relying on only the user’s wording. An LLM generates alternative queries from the original question. The system retrieves a ranked document list for the original query and each alternative; then, combines those lists with **Reciprocal Rank Fusion (RRF)**, and selects the highest-scoring documents as context for answer generation.

    This can improve coverage when relevant information is expressed differently across the source material. It also adds query-generation and retrieval work, and its results depend on the quality of the generated queries and retrieved documents.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Core Concepts

    ### Workflow

    1. Start with the user’s question.
    2. Ask an LLM to generate a small set of alternative queries that preserve the question’s intent.
    3. Retrieve a ranked list of documents for the original query and for each generated query.
    4. Fuse the ranked lists with RRF, treating each document as one result even if it appears in several lists.
    5. Rank documents by their fused scores and select the top results.
    6. Provide the selected documents and original question to the generator to produce an answer.

    ### Reciprocal Rank Fusion (RRF)

    RRF rewards documents that appear near the top of one or more ranked lists. For a document (d):

    $$\operatorname{RRF}(d) = \sum_{q \in Q} \frac{1}{c + \operatorname{rank}_q(d)}$$

    Here, ($Q$) is the set of query result lists, ranks are **1-based**, and a document missing from a list contributes zero for that list. The constant ($c$) is commonly set to 60; it smooths the effect of rank differences and is not a weight.

    **Example:** With ($c=60$), suppose document $A$ ranks 1st in one list and 3rd in another. Its score is:

    $$\frac{1}{60+1} + \frac{1}{60+3} = \frac{1}{61} + \frac{1}{63} \approx 0.03227$$

    If document $B$ appears only at rank 2 in one list, its score is:

    $$\frac{1}{60+2} = \frac{1}{62} \approx 0.01613$$

    $A$ therefore ranks above $B$ after fusion.

    ### Compared with vanilla RAG

    Vanilla RAG typically retrieves documents using one query and passes the top results to the generator. RAG-Fusion runs retrieval for the original query and LLM-generated alternatives, then merges their ranked results with RRF before selecting context.

    The additional query coverage can surface useful documents that a single query misses, at the cost of extra retrieval calls and query-generation latency.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load Documents

    Load the four Sherlock Holmes books using `DirectoryLoader` with `TextLoader`. Documents
    are cached to `cache/sherlock_holmes.json` on the first run -- subsequent runs skip the
    loading step and deserialize directly from the cache.
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

    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain_core.documents import Document

    return DirectoryLoader, Document, TextLoader, json


@app.cell
def _(DirectoryLoader, Document, TextLoader, json, lab_root):
    _cache_path = lab_root / "cache" / "sherlock_holmes.json"

    if _cache_path.exists():
        docs = [Document(**item) for item in json.loads(_cache_path.read_text(encoding="utf-8"))]
    else:
        _data = lab_root / "data"
        docs = DirectoryLoader(
            path=str(_data / "sherlock_holmes_books"),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        ).load()
        _cache_path.parent.mkdir(parents=True, exist_ok=True)
        _cache_path.write_text(
            json.dumps([doc.model_dump() for doc in docs], ensure_ascii=False),
            encoding="utf-8",
        )
    return (docs,)


@app.cell
def _(docs, mo):
    mo.callout(mo.md(f"Loaded **{len(docs)}** documents from the Sherlock Holmes corpus"), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each file is loaded as a `Document` object with raw text and source metadata (`source`).
    The four Sherlock Holmes books -- *The Adventures*, *The Memoirs*, *The Hound of the
    Baskervilles*, and *The Return* -- together form the knowledge base for this phase.
    All subsequent steps operate on this collection.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Chunk Documents

    Split the loaded documents into smaller overlapping windows so the dense vector store
    can operate on finer-grained retrieval units. A chunk size of 900 characters with a
    150-character overlap keeps each chunk self-contained while preserving context at
    paragraph boundaries. Each chunk is also assigned a unique `chunk_id` in its metadata
    -- used by the RRF node to deduplicate documents across multiple retrieval lists.
    """)
    return


@app.cell
def _():
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    return (RecursiveCharacterTextSplitter,)


@app.cell
def _(RecursiveCharacterTextSplitter, docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # Add unique chunk_id to each Document metadata
    for i, doc in enumerate(chunks):
        doc.metadata["chunk_id"] = i
    return (chunks,)


@app.cell
def _(chunks, mo):
    mo.callout(
        mo.md(f"Split into **{len(chunks)}** chunks (chunk_size=900, overlap=150)."),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each chunk is the atomic retrieval unit for the dense retriever. The `chunk_id` assigned
    during splitting is the deduplication key in the RRF node -- it identifies the same chunk
    even when it appears in multiple per-query retrieval lists.
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
    ## 4. Vector Store

    Build or load a FAISS index from the embedded chunks. If a persisted index already
    exists in `vector_store/faiss/sherlock_holmes/`, it is loaded to avoid re-embedding on
    every run -- saving significant time and API cost.
    """)
    return


@app.cell
def _():
    from langchain_community.vectorstores import FAISS

    return (FAISS,)


@app.cell
def _(FAISS, chunks, embeddings, lab_root):
    _vector_store_path = lab_root / "vector_store" / "faiss" / "sherlock_holmes"

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

    The dense retriever embeds every chunk using `text-embedding-3-large` and stores the
    vectors in a FAISS index. At query time the query is embedded and the `k` nearest
    neighbours by cosine similarity are returned. This retriever finds semantically related
    chunks even when the query and document use different words.

    Wrap the FAISS vector store as a LangChain retriever. Similarity search returns the
    top `k=4` most semantically similar chunks for a given query.
    """)
    return


@app.cell
def _(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )
    return (retriever,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Language Model

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
    ## 7. Graph State

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

    **Fields in Naive RAG:**
    - `question` -- the user's input query
    - `docs` -- chunks returned by the retriever for question + queries. In naive RAG its `List[Document]` however, in this case; its `List[List[Documents]]`
    - `answer` -- final generated answer

    **Additional Fields in RAG Fusion:**
    - `queries` -- list of 3 alternative queries generated by the LLM from the original question
    - `fused_docs` -- documents sorted by descending RRF score after fusing all per-query lists
    - `rrf_scores` -- mapping of `chunk_id` to its accumulated RRF score across all query lists
    """)
    return


@app.cell
def _():
    from typing import List, TypedDict

    return List, TypedDict


@app.cell
def _(Document, List, TypedDict):
    class State(TypedDict):
        question: str
        queries: List[str]
        docs: List[List[Document]]
        fused_docs: List[Document]
        rrf_scores: dict[int, float]
        answer: str

    return (State,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Nodes

    Four node functions implement the RAG Fusion pipeline. Each reads from and writes to
    the shared `State` dict. The execution path is linear -- no conditional branching.

    - **`generate_queries`** -- generate 3 alternative queries from the user's original question
    - **`retrieve`** -- run the dense retriever independently for each query (original + generated)
    - **`reciprocal_rank_fusion`** -- merge all per-query ranked lists into a single fused ranking
    - **`generate`** -- synthesize an answer from the top-k fused chunks using the LLM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8a. Query Generator Node

    Generates 3 alternative search queries from the user's original question using the LLM.
    Each alternative preserves the question's intent while exploring different wording and
    related concepts -- expanding retrieval surface before the retrieve node runs.

    The LLM returns a structured `QueryVariants` object enforced by Pydantic: exactly 3
    queries, each between 5 and 200 characters.
    """)
    return


@app.cell
def _():
    from typing import Annotated

    from pydantic import BaseModel, Field, StringConstraints

    return Annotated, BaseModel, Field, StringConstraints


@app.cell
def _(Annotated, StringConstraints):
    Query = Annotated[str, StringConstraints(min_length=5, max_length=200)]
    return (Query,)


@app.cell
def _(BaseModel, Field, Query):
    class QueryVariants(BaseModel):
        queries: list[Query] = Field(
            ...,
            min_length=3,
            max_length=3,
            description="Exactly 3 alternative search queries for the user's question",
        )

    return (QueryVariants,)


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate

    return (ChatPromptTemplate,)


@app.cell
def _(ChatPromptTemplate):
    querygen_msg = """Generate 3 alternative search queries for the question below.
    Preserve its original intent while exploring different wording and relevant concepts.
    """
    querygen_template = ChatPromptTemplate.from_messages(
        [
            ("system", querygen_msg),
            ("human", "Question: {question}"),
        ]
    )
    return (querygen_template,)


@app.cell
def _(QueryVariants, llm, querygen_template):
    querygen_chain = querygen_template | llm.with_structured_output(QueryVariants)
    return (querygen_chain,)


@app.cell
def _(State, querygen_chain):
    def generate_queries(state: State) -> dict:
        out = querygen_chain.invoke({"question": state["question"]})
        return {"queries": out.queries}

    return (generate_queries,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8b. Retrieve Node

    Runs the dense FAISS retriever once for each query in `[*queries, question]` -- 4 calls
    total (3 generated + 1 original). Each call returns up to `k=4` semantically similar
    chunks as a separate ranked list. The result is stored in `docs` as a
    `List[List[Document]]` -- one inner list per query -- and passed to the RRF node.
    """)
    return


@app.cell
def _(State, retriever):
    def retrieve(state: State) -> dict:
        all_queries = [*state["queries"], state["question"]]
        docs = []
        for q in all_queries:
            docs.append(retriever.invoke(q))
        return {"docs": docs}

    return (retrieve,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8c. RRF Node

    Merges all per-query ranked lists into a single fused ranking using Reciprocal Rank
    Fusion. For each document appearance, its RRF contribution is
    $\frac{1}{c + \text{rank}}$ (with $c=60$). A document retrieved by multiple queries
    accumulates contributions from each list -- so a chunk ranked well across several
    queries scores higher than one found by only one.

    `chunk_id` (assigned during chunking) is the deduplication key -- the same chunk
    retrieved for different queries is counted once, with scores summed. The output is
    `fused_docs` (documents sorted by descending RRF score) and `rrf_scores` (a
    `chunk_id -> score` mapping used by the Analysis section).
    """)
    return


@app.cell
def _():
    from collections import defaultdict

    return (defaultdict,)


@app.cell
def _(State, defaultdict):
    def reciprocal_rank_fusion(state: State) -> dict:
        c = 60
        scores = defaultdict(float)
        unique_docs = {}

        for docs in state["docs"]:
            for idx, doc in enumerate(docs, start=1):
                doc_id = doc.metadata.get("chunk_id")
                scores[doc_id] += 1 / (c + idx)
                unique_docs[doc_id] = doc

        ranked_ids = sorted(scores, key=scores.get, reverse=True)

        return {
            "fused_docs": [unique_docs[doc_id] for doc_id in ranked_ids],
            "rrf_scores": dict(scores),
        }

    return (reciprocal_rank_fusion,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8d. Generate Node

    Constructs an answer from the top 5 fused chunks using the LLM. The system prompt
    instructs the model to answer only from context, reducing hallucination on
    out-of-context questions. Only `fused_docs[:5]` are used -- the highest-scoring
    chunks after RRF fusion -- concatenated into a single context string.
    """)
    return


@app.cell
def _(ChatPromptTemplate):
    sys_msg = """You are a helpful AI research assistant. Answer ONLY using the provided context.
    If the context is empty or insufficient, simply say: "I don't know based on the provided context."
    """
    template = ChatPromptTemplate.from_messages(
        [
            ("system", sys_msg),
            ("human", "Question: {question}\n\nContext:\n{context}"),
        ]
    )
    return (template,)


@app.cell
def _(State, llm, template):
    def generate(state: State) -> dict:
        top_docs = state["fused_docs"][:5]
        context = "\n\n".join(d.page_content for d in top_docs)
        response = (template | llm).invoke(
            {
                "question": state["question"],
                "context": context,
            }
        )
        return {"answer": response.content}

    return (generate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `generate_queries`, `retrieve`, `reciprocal_rank_fusion`, and `generate` implement the
    full RAG Fusion loop: expand the query, retrieve per-query, fuse rankings, then synthesize.
    All functions read from and write to the shared `State` dict that LangGraph passes
    between nodes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Build the Graph

    Assemble the nodes into a LangGraph `StateGraph` and compile it. The execution flow
    is linear:

    `START -> query_generator -> retrieve -> rrf -> generate -> END`
    """)
    return


@app.cell
def _():
    from langgraph.graph import END, START, StateGraph

    return END, START, StateGraph


@app.cell
def _(
    END,
    START,
    State,
    StateGraph,
    generate,
    generate_queries,
    reciprocal_rank_fusion,
    retrieve,
):
    builder = StateGraph(State)

    builder.add_node("query generator", generate_queries)
    builder.add_node("retrieve", retrieve)
    builder.add_node("rrf", reciprocal_rank_fusion)
    builder.add_node("generate", generate)

    builder.add_edge(START, "query generator")
    builder.add_edge("query generator", "retrieve")
    builder.add_edge("retrieve", "rrf")
    builder.add_edge("rrf", "generate")
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
    full `query_generator -> retrieve -> rrf -> generate` flow and returns the updated
    state with `answer` populated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe the pipeline's behavior across different question types:**

    | #  | Question                                                                                                                                                        | Category               | What it tests                                                                                        |
    | -- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------- |
    | 1  | How does Sherlock Holmes use observation and deduction to solve mysteries that initially seem impossible?                                                       | General reasoning      | Tests retrieval of passages describing Holmes's investigative methods across multiple stories.       |
    | 2  | What happens in The Final Problem, and why is Professor Moriarty such a formidable opponent for Holmes?                                                         | Specific story         | Tests retrieval from The Memoirs of Sherlock Holmes.                                                 |
    | 3  | What is the legend of the Baskerville hound, and how does Holmes investigate the apparent supernatural threat?                                                  | Novel-specific         | Tests retrieval from The Hound of the Baskervilles.                                                  |
    | 4  | How does Dr. Watson contribute to Holmes's investigations beyond simply recording the cases?                                                                    | Character analysis     | Tests retrieval of Watson's observations, actions, and role across stories.                          |
    | 5  | What clues help Holmes distinguish between a misleading appearance and the actual explanation behind a crime?                                                   | Evidence and deduction | Tests whether retrieval finds concrete evidence rather than generic descriptions.                    |
    | 6  | What happens to Sherlock Holmes before his return in The Return of Sherlock Holmes, and how is his return revealed?                                             | Cross-book continuity  | Tests retrieval across The Memoirs and The Return of Sherlock Holmes.                                |
    | 7  | How do secret identities, disguises, or mistaken assumptions influence the outcome of Holmes's cases?                                                           | Multi-story synthesis  | The model must retrieve examples from more than one story.                                           |
    | 8  | What role do letters, coded messages, documents, or other written clues play in solving Holmes's cases?                                                         | Thematic retrieval     | Tests alternative query wording for different kinds of written evidence.                             |
    | 9  | Compare the apparent supernatural danger in The Hound of the Baskervilles with the rational explanations Holmes seeks. What evidence helps resolve the mystery? | Multi-step reasoning   | Requires both the premise and the investigation's evidence; answers should be grounded in the novel. |
    | 10 | Across the four books, what recurring investigative strategies does Holmes use when physical evidence, witness statements, and initial assumptions conflict?    | Cross-book synthesis   | A challenging test of multi-query retrieval and synthesis across the corpus.                         |
    """)
    return


@app.cell
def _(graph):
    def process_response(q: str):
        input_state = {
            "question": q,
            "queries": [],
            "docs": [],
            "fused_docs": [],
            "rrf_scores": {},
            "answer": "",
        }
        return graph.invoke(input_state)

    return (process_response,)


@app.cell
def _(mo):
    query_input = mo.ui.text_area(
        value="How does Sherlock Holmes use observation and deduction to solve mysteries?",
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

    Inspect the intermediate state produced by the pipeline run above -- generated queries,
    retrieval coverage across all query calls, RRF-fused document scores, and the final
    context passed to the LLM. All sections below are read-only views of `resp`;
    re-running section 8 refreshes them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Generated Queries

    The original question alongside the 3 alternative queries generated by the LLM.
    Each alternative preserves the original intent while exploring different wording and
    related concepts -- together they increase retrieval coverage across the corpus.
    """)
    return


@app.cell
def _(mo, resp):
    _items = [f"**Original:** {resp['question']}"] + [
        f"**Query {i + 1}:** {q}" for i, q in enumerate(resp["queries"])
    ]
    mo.callout(mo.md("\n\n".join(_items)), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retrieval Coverage

    RAG Fusion runs the retriever once per query (3 generated + 1 original = 4 calls).
    Each call returns up to `k=4` chunks -- up to 16 total retrievals, many overlapping.
    RRF deduplicates and re-ranks them into a single fused list. The top 5 fused chunks
    are passed to the LLM.
    """)
    return


@app.cell
def _(mo, resp):
    import matplotlib.pyplot as plt

    _total_retrieved = sum(len(dl) for dl in resp["docs"])
    _unique_fused = len(resp["fused_docs"])
    _passed_to_llm = min(5, _unique_fused)

    _total_chars = sum(len(d.page_content) for dl in resp["docs"] for d in dl)
    _fused_chars = sum(len(d.page_content) for d in resp["fused_docs"])
    _llm_chars = sum(len(d.page_content) for d in resp["fused_docs"][:5])

    _labels = ["Total Retrieved\n(with duplicates)", "Unique Fused", "Passed to LLM"]
    _colors = ["#4C78A8", "#F8A05C", "#54A24B"]

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.5))

    _ax1.bar(_labels, [_total_retrieved, _unique_fused, _passed_to_llm], color=_colors)
    _ax1.set_ylabel("Document count")
    _ax1.set_title("Document count")
    _ax1.spines["top"].set_visible(False)
    _ax1.spines["right"].set_visible(False)

    _ax2.bar(_labels, [_total_chars, _fused_chars, _llm_chars], color=_colors)
    _ax2.set_ylabel("Characters")
    _ax2.set_title("Context length (characters)")
    _ax2.spines["top"].set_visible(False)
    _ax2.spines["right"].set_visible(False)

    plt.tight_layout()

    _fused_doc_pct = round((1 - _unique_fused / _total_retrieved) * 100, 1) if _total_retrieved > 0 else 0.0
    _llm_doc_pct = round((1 - _passed_to_llm / _unique_fused) * 100, 1) if _unique_fused > 0 else 0.0
    _fused_char_pct = round((1 - _fused_chars / _total_chars) * 100, 1) if _total_chars > 0 else 0.0
    _llm_char_pct = round((1 - _llm_chars / _fused_chars) * 100, 1) if _fused_chars > 0 else 0.0

    mo.vstack([
        _fig,
        mo.callout(
            mo.md(
                f"**Docs:** {_total_retrieved} total"
                f" -> {_unique_fused} unique fused (-{_fused_doc_pct}%)"
                f" -> {_passed_to_llm} passed to LLM (-{_llm_doc_pct}% from fused).\n\n"
                f"**Context:** {_total_chars:,} chars total"
                f" -> {_fused_chars:,} fused (-{_fused_char_pct}%)"
                f" -> {_llm_chars:,} passed to LLM (-{_llm_char_pct}% from fused)."
            ),
            kind="info",
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Fused Documents

    The top 5 documents from the RRF-fused ranking -- the exact context passed to the LLM.
    Each accordion label shows the document's rank and its RRF score. Higher scores indicate
    the document appeared near the top across more query result lists.
    """)
    return


@app.cell
def _(mo, resp):
    top_docs = resp["fused_docs"][:5]
    _rrf_scores = resp["rrf_scores"]
    _raw_context = "\n\n".join(d.page_content for d in top_docs)
    mo.vstack([
        mo.accordion({
            f"Doc {i + 1}  |  RRF: {_rrf_scores.get(d.metadata.get('chunk_id'), 0.0):.6f}": mo.md(d.page_content)
            for i, d in enumerate(top_docs)
        }),
        mo.callout(
            mo.md(
                f"**Top 5 fused docs** passed to the LLM."
                f" Total context: {len(_raw_context):,} characters."
            ),
            kind="info",
        ),
    ])
    return (top_docs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Fused Documents Table

    RRF rank, score, source file, and a content snippet for each of the top 5 fused
    documents. Documents that appeared near the top of multiple query result lists
    accumulate higher RRF scores and rank above documents retrieved by only one query.
    """)
    return


@app.cell
def _(mo, resp, top_docs):
    _rrf_scores = resp["rrf_scores"]
    _rows = [
        {
            "Rank": i + 1,
            "Chunk ID": d.metadata.get("chunk_id", ""),
            "RRF Score": round(_rrf_scores.get(d.metadata.get("chunk_id"), 0.0), 6),
            "Source": d.metadata.get("source", "").replace("\\", "/").split("/")[-1],
            "Snippet": d.page_content[:150].replace("\n", " ") + "...",
        }
        for i, d in enumerate(top_docs)
    ]
    mo.ui.table(_rows)
    return


if __name__ == "__main__":
    app.run()
