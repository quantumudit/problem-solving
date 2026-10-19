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
    # Web Fallback with Query Rewriting

    ## What Was Built So Far

    Across the first four phases, the corrective RAG pipeline was assembled step by step:

    - **phase_01 (basic_rag)**: Baseline pipeline -- retrieve top-k chunks from a FAISS vector store, pass them raw to an LLM, generate an answer. No quality checks, no filtering.
    - **phase_02 (knowledge_refinement)**: Added a 3-step refinement pass between retrieval and generation -- decompose chunks into sentence strips, filter each strip for relevance, recompose into a noise-free `refined_context`.
    - **phase_03 (retrieval_evaluation)**: Added an LLM-based retrieval evaluator before refinement. Each chunk is scored $[0.0, 1.0]$ and the pipeline branches on the overall verdict: `correct` proceeds to `refine -> generate`; `incorrect` and `ambiguous` short-circuited with fallback messages.
    - **phase_04 (web_fallback)**: Replaced the `incorrect` dead-end with a real corrective action -- Tavily web search fetches live results when internal retrieval fails; raw web snippets pass through the same `refine` pipeline for a grounded, noise-free answer.

    Phase_04 closed the `incorrect` dead-end, but passed the raw user question directly to Tavily. Conversational, vague, or recency-implied queries (e.g., `"recent AI news"`) produce noisy, off-target web results when sent unmodified to a search API.

    ---

    ## Phase 05: Introduction to Query Rewriting

    ### The Problem with Direct Web Queries

    * **Raw User Queries are Flawed**: Prompts from users are often conversational, vague, under-specified, or missing essential search keywords and time constraints (e.g., a user asking `"recent AI news"` or `"Who was the screenwriter for Death of a Batman"`).
    * **Search Engine Keyword Gap**: Search engines (like Tavily or Google) perform best when given short, keyword-dense, explicitly framed queries. Passing raw, conversational user prompts directly into a search API returns noisy, off-target, or low-quality web snippets.

    ### LLM-Powered Query Rewritter

    Since the user prompts are rarely search-engine-ready; we introduce a dedicated **LLM-powered Query Rewriter node** before performing any web search.

    We provide some specific instruction to the LLM in order to make the raw user query; search-engine-ready. The instruction includes:

    * **Keyword Focus**: Strip conversational filler and retain core search terms.
    * **Recency Constraints**: If a prompt implies recency (e.g., *"recent AI news"*), automatically append explicit date ranges like `"last 30 days"`.
    * **No Answering**: Explicitly instructs the LLM **not** to answer the question, only to rewrite it for search engine optimization.

    **Examples**:
    * **User Prompt**: `"recent AI news"` $\rightarrow$ **Rewritten Web Query**: `"recent AI news last 30 days"`.
    * **User Prompt**: `"Who was the screenwriter for Death of a Batman"` $\rightarrow$ **Rewritten Web Query**: `"Death of a Batman screenwriter wikipedia"`.


    In this case, instead of sending the user query directly to `web_search` node; we provided the search-engine optimized `web_query` to the node.

    The rest of the workflow remains the same post the `web_search` node
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
    # Embeddings
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

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used across four roles in this
    pipeline: the retrieval evaluator (scoring chunks), the query rewriter (producing a
    search-engine-optimized `web_query`), the relevance filter (keep/discard sentence strips
    for either internal or web context), and the final answer generator. A single shared
    instance keeps the setup simple and ensures consistent behavior across all four
    invocations regardless of which knowledge source is active.
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
    The same LLM instance serves four distinct roles in this pipeline: scoring retrieved chunks
    (via `doceval_chain`), rewriting the user query for web search (via `rewritter_chain`),
    filtering sentence strips (via `filter_chain`), and generating the final answer (via
    `template | llm`). Reusing one instance avoids redundant initialization and ensures
    consistent model behavior across all four invocation types.
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
    ### Thresholds

    Two score boundaries that control how the retrieval evaluator classifies chunks:

    - `UPPER_TH = 0.7` -- a chunk scoring above this is considered highly relevant. If at least
      one chunk clears this bar, the overall verdict is `correct` and the pipeline proceeds to refinement.
    - `LOWER_TH = 0.3` -- the minimum bar for a chunk to be included in `good_docs`. Chunks below
      this are discarded even when the verdict is `correct` or `ambiguous`.
    """)
    return


@app.cell
def _():
    UPPER_TH = 0.7
    LOWER_TH = 0.3
    return LOWER_TH, UPPER_TH


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### State Schema

    The shared typed dictionary that LangGraph passes between every node. Each field is
    either written by one node and read by the next, or populated at the start and carried
    through unchanged.

    **Base RAG fields** (same as phase_01):
    - `question` -- the user's input query
    - `docs` -- raw chunks returned by the retriever
    - `answer` -- final generated answer

    **Knowledge refinement fields** (same as phase_02):
    - `strips` -- sentence-level decomposition of the good context
    - `kept_strips` -- strips the LLM judge marked as relevant
    - `refined_context` -- kept strips joined into a clean string for the generator

    **Retrieval evaluation fields** (same as phase_03):
    - `good_docs` -- chunks that scored above `LOWER_TH`; used as input to the refine node
    - `verdict` -- overall routing decision: `correct` / `incorrect` / `ambiguous`
    - `reason` -- one-line explanation of the verdict
    - `doc_scores` -- per-chunk relevance scores in the same order as `docs`
    - `doc_reasons` -- per-chunk reason strings explaining each score

    **Web fallback field** (same as phase_04):
    - `web_docs` -- `Document` objects returned by the Tavily web search; populated only on the `incorrect` path

    **Web Query field (new in phase_05)**:
    - `web_query` -- A search-engine optimized user query
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
        good_docs: List[Document]
        verdict: str
        reason: str
        doc_scores: List[float]
        doc_reasons: List[str]
        strips: List[str]
        kept_strips: List[str]
        refined_context: str
        web_query: str
        web_docs: List[Document]
        answer: str

    return (State,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Nodes

    Six node functions implement the corrective RAG pipeline. Each reads from and writes to
    the shared `State` dict. The execution path branches at `eval_doc` based on the verdict:

    - **`retrieve`** -- fetch the top-k chunks from the vector store
    - **`eval_doc`** -- score each chunk and assign a verdict; routes the graph conditionally
    - **`query_rewritter`** -- rewrite the user query into a search-engine-optimized `web_query` before fetching web results *(new in phase_05)*
    - **`web_search`** -- query Tavily with `web_query` for live web results when verdict is `incorrect`
    - **`refine`** -- decompose context into strips, filter for relevance, recompose; operates on `good_docs` for `correct`, `web_docs` for `incorrect`
    - **`generate`** -- synthesize an answer from the refined context *(correct and incorrect paths)*
    - **`ambiguous`** -- short-circuits with a partial-match message when no chunk clears `UPPER_TH`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8a. Retrieve Node

    Unchanged from traditional RAG -- retrieves the top `k` semantically similar chunks from the vector store
    for the given question. These raw chunks are passed to the `refine` node rather than directly to the LLM.
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
    ### 8b. Retrieval Evaluator Node

    The decision hub of the corrective RAG graph. For each retrieved chunk it invokes an LLM
    judge (`doceval_chain`) that returns a relevance score in $[0.0, 1.0]$ and a short reason.
    After scoring all chunks, the node decides the overall verdict and routes the graph:

    - `correct` -- at least one chunk scored $> 0.7$; proceed to `refine` (using `good_docs`)
    - `incorrect` -- all chunks scored $< 0.3$; route to `web_search`, then `refine` (using `web_docs`), then `generate`
    - `ambiguous` -- mixed signals (some chunks pass `LOWER_TH` but none reach `UPPER_TH`); short-circuit to `ambiguous`

    Regardless of verdict, only chunks scoring $> 0.3$ are kept in `good_docs` for downstream use.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Score-based Document Evaluator

    `DocEvalScore` is the structured output schema for the evaluator LLM. It captures two
    fields per chunk: a float `score` in $[0.0, 1.0]$ (constrained by Pydantic `ge`/`le`)
    and a string `reason` explaining why the score was assigned.
    """)
    return


@app.cell
def _():
    from pydantic import BaseModel, Field

    return BaseModel, Field


@app.cell
def _(BaseModel, Field):
    class DocEvalScore(BaseModel):
        score: float = Field(
            ...,
            ge=0.0,
            le=1.0,
            description="Relevance score for the retrieved chunk in [0.0, 1.0]; 1.0 = fully answers the question, 0.0 = completely irrelevant.",
        )
        reason: str = Field(
            ...,
            description="One-line explanation for the assigned score.",
        )

    return (DocEvalScore,)


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate

    return (ChatPromptTemplate,)


@app.cell
def _(ChatPromptTemplate):
    doceval_sys_msg = """You are a strict retrieval evaluator for RAG.
    You will be given ONE retrieved chunk and a question.
    Return a relevance score in [0.0, 1.0].

    - 1.0: chunk alone is sufficient to answer fully/mostly.
    - 0.0: chunk is irrelevant

    Be conservative with high scores.
    Also return a short reason.
    Output JSON only.
    """

    # Prompt template with role-based message to filter sentence strips
    doceval_template = ChatPromptTemplate.from_messages([
        ("system", doceval_sys_msg),
        ("human", "Question: {question}\n\nDocument Chunk:\n{chunk}")
    ])
    return (doceval_template,)


@app.cell
def _(DocEvalScore, doceval_template, llm):
    # Document Evaluation Chain (LLM Judge)
    doceval_chain = doceval_template | llm.with_structured_output(DocEvalScore)
    return (doceval_chain,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Document Evaluation Node

    `eval_doc` iterates over every chunk in `state["docs"]`, scoring each one independently.
    The per-chunk scores and reasons are stored in `doc_scores` and `doc_reasons` (for the
    exploration table), while chunks that clear `LOWER_TH` are collected into `good_docs`.
    After scoring all chunks, the three-way verdict logic runs and the node returns the
    updated state fields including the routing decision.
    """)
    return


@app.cell
def _(LOWER_TH, State, UPPER_TH, doceval_chain):
    def eval_doc(state: State) -> dict:
        q = state["question"]

        scores = []
        reasons = []
        good = []

        for d in state["docs"]:
            out = doceval_chain.invoke({"question": q, "chunk": d.page_content})
            scores.append(out.score)
            reasons.append(out.reason)
            # for correct case we will refine only docs with score > LOWER_TH
            if out.score > LOWER_TH:
                good.append(d)

        # Verdict is "correct" if atleast one doc > UPPER_TH
        if any(s > UPPER_TH for s in scores):
            return {
                "good_docs": good,
                "verdict": "correct",
                "reason": f"At least one retrieved chunk scored > {UPPER_TH}",
                "doc_scores": scores,
                "doc_reasons": reasons,
            }
        # Verdict is "incorrect" if all docs < LOWER_TH
        if len(scores) > 0 and all(s < LOWER_TH for s in scores):
            why = "No chunk was sufficient."
            return {
                "good_docs": [],
                "verdict": "incorrect",
                "reason": f"All retrieved chunks scored < {LOWER_TH}. {why}",
                "doc_scores": scores,
                "doc_reasons": reasons,
            }
        # Verdict is "ambiguous" for anything in between
        why = "Mixed relevance signals"
        return {
            "good_docs": good,
            "verdict": "ambiguous",
            "reason": f"No chunk scored > {UPPER_TH}, but not all were < {LOWER_TH}. {why}",
            "doc_scores": scores,
            "doc_reasons": reasons,
        }

    return (eval_doc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8c. Refine Node

    The knowledge refinement stage, now handling two different knowledge sources depending on
    which path the graph took:

    - **`correct` path**: refines `good_docs` -- the internal chunks that cleared `LOWER_TH`.
    - **`incorrect` path**: refines `web_docs` -- the raw web search results fetched by Tavily.

    In both cases the same 3-step pipeline runs: decompose into sentence strips, filter each
    strip for relevance against the query, recompose kept strips into `refined_context`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 8c.1 Sentence Level Decomposition

    Step-1 of the knowledge refinement pipeline -- breaking raw retrieved document chunks
    into individual sentence strips.
    """)
    return


@app.cell
def _():
    import re

    return (re,)


@app.cell
def _(List, re):
    def decompose_to_sentences(text: str) -> List[str]:
        """sentence-level decomposer that extracts strips from a given text"""
        text = re.sub(r"\s+", " ", text).strip()
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s for s in (s.strip() for s in sentences) if len(s) > 20]

    return (decompose_to_sentences,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three things happen in order:

    1. **Normalize whitespace:** collapses all newlines, tabs, and multiple spaces into single spaces.
    2. **Split on sentence boundaries:** splits wherever whitespace follows `.`, `!`, or `?`.
    3. **Filter short fragments:** drops anything shorter than 20 characters.

    The output is a `List[str]` of sentence strips -- $S_1, S_2, S_3, \dots$ -- passed one by one to the filtration step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 8c.2 Sentence Filtration

    Step 2 of the pipeline. Each sentence strip is evaluated individually against the user question
    using an LLM as a strict relevance judge returning a structured `KeepDecision` -- `keep=True`
    to retain the strip, `keep=False` to discard it.
    """)
    return


@app.cell
def _(BaseModel, Field):
    class KeepDecision(BaseModel):
        keep: bool = Field(
            ...,
            description="True to retain the sentence strip as relevant to the question; False to discard it.",
        )

    return (KeepDecision,)


@app.cell
def _(ChatPromptTemplate):
    filter_sys_msg = """You are a strict relevance filter.
    Return keep=true only if the sentence directly helps answer the question.
    Use ONLY the sentence. Output JSON only.
    """
    filter_template = ChatPromptTemplate.from_messages([
        ("system", filter_sys_msg),
        ("human", "Question: {question}\n\nSentence:\n{sentence}"),
    ])
    return (filter_template,)


@app.cell
def _(KeepDecision, filter_template, llm):
    filter_chain = filter_template | llm.with_structured_output(KeepDecision)
    return (filter_chain,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Assembling the `refine` Node

    Step 3 -- and the `refine` node function itself. The only change from phase_03 is the
    context source: the node checks `state["verdict"]` and joins `good_docs` on the `correct`
    path or `web_docs` on the `incorrect` path. Everything downstream -- decomposition,
    filtration, recomposition -- is identical regardless of source.
    """)
    return


@app.cell
def _(State, decompose_to_sentences, filter_chain):
    def refine(state: State) -> dict:
        q = state["question"]


        if state["verdict"] == "correct":
            context = "\n\n".join(d.page_content for d in state["good_docs"]).strip()
        else:
            context = "\n\n".join(d.page_content for d in state["web_docs"]).strip()

        # Step-1: Decomposition
        strips = decompose_to_sentences(context)

        # Step-2: Filtration
        kept = []
        for s in strips:
            if filter_chain.invoke({"question": q, "sentence": s}).keep:
                kept.append(s)

        # Step-3: Recompose
        refined_context = "\n".join(kept).strip()

        return {
            "strips": strips,
            "kept_strips": kept,
            "refined_context": refined_context,
        }

    return (refine,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8d. Query Rewriter Node

    New in phase_05. Triggered on the `incorrect` path, immediately before the web search.
    Receives `state["question"]` and invokes `rewritter_chain` to produce a search-engine-
    optimized `web_query` stored back in the state:

    - Strips conversational filler and retains core search keywords.
    - Adds explicit recency constraints when the question implies freshness
      (e.g., `"recent AI news"` -> `"recent AI news last 30 days"`).
    - Never answers the question -- the output is a rewritten query string only.

    The rewritten `web_query` is then consumed by the `web_search` node instead of the raw
    `question`, improving result relevance on the `incorrect` path.
    """)
    return


@app.cell
def _(BaseModel, Field):
    class WebQuery(BaseModel):
        query: str = Field(
            ...,
            description="Short keyword-dense search query (6-14 words) optimized for a web search engine; do not answer the question.",
        )


    return (WebQuery,)


@app.cell
def _(ChatPromptTemplate, WebQuery, llm):
    rewritter_instruction = """Rewrite the user question into a web search query composed of keywords.
    Rules:
    - Keep it short (6-14 words).
    - If the question implies reecency (e.g., recent/latest/last week/last month); add a constraint like (last 30 days).
    - Do NOT answer the question.
    - Return JSON with a single key: query
    """

    rewritter_template = ChatPromptTemplate.from_messages([
        ("system", rewritter_instruction),
        ("human", "Question: {question}")
    ])

    rewritter_chain = rewritter_template | llm.with_structured_output(WebQuery)
    return (rewritter_chain,)


@app.cell
def _(State, rewritter_chain):
    def query_rewritter(state: State) -> dict:
        response = rewritter_chain.invoke({"question": state["question"]})
        return {"web_query": response.query}

    return (query_rewritter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8e. Web Search Node

    Triggered only on the `incorrect` path, after `query_rewritter`. Uses the **Tavily API**
    to search the web with the rewritten `web_query` (falling back to the raw `question` if
    `web_query` is empty) and converts the top results into `Document` objects stored in
    `web_docs`. Each document carries the result's `title` and `url` as metadata alongside
    the full text `content`, making the source traceable in the exploration view.
    """)
    return


@app.cell
def _():
    from langchain_tavily import TavilySearch

    return (TavilySearch,)


@app.cell
def _(TavilySearch, os):
    tavily_key = os.getenv("TAVILY_API_KEY")

    tavily = TavilySearch(
        name="web_search", 
        max_results=5, 
        topic="general", 
        api_key=tavily_key
    )
    return (tavily,)


@app.cell
def _(Document, State, tavily):
    def web_search(state: State) -> dict:
        q = state.get("web_query") or state["question"] # fallback to user question if empty
        response = tavily.invoke({"query": q})

        web_docs = []
        for r in response.get("results") or []:
            title = r.get("title", "")
            url = r.get("url", "")
            content = r.get("content", "") or r.get("snippet", "")
            text = f"TITLE: {title}\nURL: {url}\nCONTENT: {content}"
            web_docs.append(Document(page_content=text, metadata={"url":url, "title": title}))
        return {"web_docs": web_docs}

    return (web_search,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8f. Generate Node

    Same structure as in traditional RAG, but receives the `refined_context` produced by the
    `refine` node -- a compact, noise-free string containing only the relevant sentences,
    whether those came from internal `good_docs` or external `web_docs`.
    """)
    return


@app.cell
def _(ChatPromptTemplate):
    sys_msg = """You are a helpful ML tutor. Answer ONLY using the provided refined context.
    If the context is empty or insufficient, simply say: "I don't know based on the provided books."
    """
    template = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        ("human", "Question: {question}\n\nRefined Context:\n{refined_context}"),
    ])
    return (template,)


@app.cell
def _(State, llm, template):
    def generate(state: State) -> dict:
        chain = template | llm
        response = chain.invoke({
            "question": state["question"],
            "refined_context": state["refined_context"],
        })
        return {"answer": response.content}

    return (generate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `retrieve`, `eval_doc`, `query_rewritter`, `web_search`, `refine`, and `generate` together
    implement the full corrective RAG loop: pull context, evaluate it, rewrite the query and
    fetch from the web if needed, refine what remains, then synthesize. Each function reads from
    and writes to the shared `State` dict that LangGraph passes between nodes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8g. Routing & Fallback Node

    The `route` function reads `state["verdict"]` and returns the name of the next node to run.
    LangGraph uses this as the edge condition for `add_conditional_edges`.

    - `correct` -> `refine` (uses `good_docs`)
    - `incorrect` -> `query_rewritter` -> `web_search` -> `refine` (uses `web_docs`) -> `generate`
    - `ambiguous` -> `ambiguous_node` (short-circuit; returns a partial-match message)

    `ambiguous_node` is the only remaining pure fallback in this phase. In a full C-RAG
    implementation the `ambiguous` path would merge `good_docs` with web results before
    refining -- that extension is left for a future phase.
    """)
    return


@app.cell
def _(State):
    def ambiguous_node(state: State) -> dict:
        return {"answer": f"Ambiguous: {state['reason']} "}

    return (ambiguous_node,)


@app.function
def route(state: State) -> str:
    if state["verdict"] == 'correct':
        return "refine"
    elif state["verdict"] == "incorrect":
        return "query_rewritter"
    else:
        return "ambiguous"


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Build the Graph

    Assemble the nodes into a LangGraph `StateGraph` and compile it. The graph has a
    conditional branch at `eval_doc` that routes to one of three paths based on the verdict:

    ```
    START -> retrieve -> eval_doc --(correct)---> refine -> generate -> END
                                  --(incorrect)--> query_rewritter -> web_search -> refine -> generate -> END
                                  --(ambiguous)--> ambiguous -> END
    ```

    The key difference from phase_04 is the `incorrect` path: instead of routing directly to
    `web_search`, it now passes through `query_rewritter` first -- the LLM rewrites the raw
    user question into a search-engine-optimized `web_query` before Tavily is called.
    `add_conditional_edges` wires the `route` function to the three possible next nodes.
    """)
    return


@app.cell
def _():
    from langgraph.graph import StateGraph, START, END

    return END, START, StateGraph


@app.cell
def _(
    END,
    START,
    State,
    StateGraph,
    ambiguous_node,
    eval_doc,
    generate,
    query_rewritter,
    refine,
    retrieve,
    web_search,
):
    builder = StateGraph(State)

    builder.add_node("retrieve", retrieve)
    builder.add_node("eval_doc", eval_doc)
    builder.add_node("query_rewritter", query_rewritter)
    builder.add_node("web_search", web_search)
    builder.add_node("refine", refine)
    builder.add_node("generate", generate)
    builder.add_node("ambiguous", ambiguous_node)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "eval_doc")

    builder.add_conditional_edges(
        "eval_doc", route,
        {"refine":"refine", "query_rewritter": "query_rewritter", "ambiguous": "ambiguous"}
    )

    builder.add_edge("query_rewritter", "web_search")
    builder.add_edge("web_search", "refine")
    builder.add_edge("refine", "generate")
    builder.add_edge("generate", END)
    builder.add_edge("ambiguous", END)

    graph = builder.compile()
    return (graph,)


@app.cell
def _(graph):
    graph
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The compiled graph encodes the full corrective RAG pipeline with conditional routing.
    `graph.invoke(state)` always runs `retrieve` and `eval_doc`; the path after that depends
    on the verdict. Both `correct` and `incorrect` paths run `refine` and `generate` -- the
    difference is the context source (`good_docs` vs `web_docs`). Only `ambiguous` short-circuits
    without generating a grounded answer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe each routing path:**

    | Question | Expected verdict | What to observe |
    |---|---|---|
    | "Explain the bias-variance trade-off" | `correct` | Internal retrieval succeeds -- `good_docs` are refined and used for generation. Web Docs section will be empty. |
    | "What are attention mechanisms and why are they important in current scenario?" | `ambiguous` | Mixed relevance -- some chunks pass `LOWER_TH` but none exceed `UPPER_TH`. Routes to `ambiguous` node; no refinement or generation runs. |
    | "What are the latest major AI news?" | `incorrect` | Internal retrieval fails completely. Routes to `query_rewritter` -> `web_search` -> `refine` -> `generate`. Query Rewriting section shows the original vs rewritten query; Web Docs section populates with Tavily results. |

    > **Note:** Strip analysis and refined context are populated for both `correct` and `incorrect`
    > verdicts (both paths run `refine`). For `ambiguous`, the `refine` node is skipped -- strips
    > and refined context remain empty and those sections will show no data.
    """)
    return


@app.cell
def _(graph):
    def process_response(q: str):
        input_state = {
            "question": q,
            "docs": [],
            "good_docs": [],
            "web_docs": [],
            "verdict": "",
            "reason": "",
            "doc_scores": [],
            "doc_reasons": [],
            "strips": [],
            "kept_strips": [],
            "refined_context": "",
            "web_query": "",
            "answer": "",
        }
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

    Inspect the intermediate state produced by the pipeline run above -- verdict and reason,
    query rewriting (on the `incorrect` path), retrieved documents, web search results (if
    triggered), sentence strips, and context size across each stage. All sections below are
    read-only views of `resp`; re-running section 10 refreshes them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verdict & Reason

    The retrieval evaluator's overall decision for this run -- the `verdict` string and the
    `reason` explaining which threshold condition was met. The verdict determines which pipeline
    path ran; the reason reflects the aggregate scoring across all retrieved chunks.
    """)
    return


@app.cell
def _(mo, resp):
    _verdict = resp.get("verdict", "")
    _reason = resp.get("reason", "")
    _kind_map = {"correct": "success", "incorrect": "danger", "ambiguous": "warn"}
    _kind = _kind_map.get(_verdict, "neutral")
    mo.vstack([
        mo.stat(label="Verdict", value=_verdict.upper() if _verdict else "N/A"),
        mo.callout(mo.md(f"**Reason:** {_reason}"), kind=_kind),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Query Rewriting

    Compares the original user question with the search-engine-optimized `web_query` produced
    by the `query_rewritter` node. Only populated on the `incorrect` path -- the rewriter runs
    before Tavily is called. On `correct` and `ambiguous` paths, `web_query` remains empty.
    """)
    return


@app.cell
def _(mo, resp):
    original_q = resp.get("question", "")
    rewritten_q = resp.get("web_query", "")
    if not rewritten_q:
        _display = mo.callout(
            mo.md("Query rewriting was not triggered -- verdict was not `incorrect`."),
            kind="neutral",
        )
    else:
        _display = mo.vstack([
            mo.hstack([
                mo.stat(
                    label="Original Question",
                    value=original_q,
                ),
                mo.stat(
                    label="Rewritten Web Query",
                    value=rewritten_q,
                ),
            ]),
            mo.callout(
                mo.md(
                    f"**Original:** `{original_q}`  \n"
                    f"**Rewritten:** `{rewritten_q}`  \n"
                    f"Length: {len(original_q)} chars -> {len(rewritten_q)} chars"
                    f" ({'+' if len(rewritten_q) >= len(original_q) else ''}"
                    f"{len(rewritten_q) - len(original_q)} chars)."
                ),
                kind="info",
            ),
        ])
    _display
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Explore Web Documents

    Web results fetched by Tavily when the verdict was `incorrect`. Each result shows the
    title, source URL, and raw content snippet as returned by the API -- before any refinement.
    Only populated on the `incorrect` path; empty for `correct` and `ambiguous` verdicts.
    """)
    return


@app.cell
def _(mo, resp):
    web_context = "\n\n".join(d.page_content for d in resp["web_docs"])
    if not resp["web_docs"]:
        _display = mo.callout(
            mo.md("No web search was triggered -- verdict was not `incorrect`."),
            kind="neutral",
        )
    else:
        _display = mo.vstack([
            mo.accordion({
                f"Web Result {i + 1} -- {d.metadata.get('title', '')}": mo.md(d.page_content)
                for i, d in enumerate(resp["web_docs"])
            }),
            mo.callout(
                mo.md(
                    f"**{len(resp['web_docs'])} web results** fetched via Tavily."
                    f" Total web context: {len(web_context):,} characters."
                ),
                kind="warn",
            ),
        ])
    _display
    return (web_context,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Explore Retrieved Documents

    The `k=4` raw chunks retrieved from the vector store -- before any evaluation or refinement.
    Expand each to inspect the raw content passed into the `eval_doc` node.
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
                f" across {len(resp['docs'])} chunks."
            ),
            kind="info",
        ),
    ])
    return (raw_context,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Chunk Retrieval Analysis

    Each retrieved chunk scored individually by the evaluator. **Good Doc?** marks chunks
    that passed the lower threshold ($> 0.3$) and were retained in `good_docs` for refinement.
    """)
    return


@app.cell
def _(mo, raw_context, resp):
    good_pages = {d.page_content for d in resp["good_docs"]}
    good_context = "\n\n".join(d.page_content for d in resp["good_docs"])

    chunk_rows = [
        {
            "Chunk": f"Doc {i + 1}",
            "Score": round(resp["doc_scores"][i], 3) if i < len(resp["doc_scores"]) else "N/A",
            "Good Doc?": "Yes" if d.page_content in good_pages else "No",
            "Reason": resp["doc_reasons"][i] if i < len(resp["doc_reasons"]) else "",
        }
        for i, d in enumerate(resp["docs"])
    ]

    total_docs = len(resp["docs"])
    good_docs_n = len(resp["good_docs"])
    good_pct = round(good_docs_n / total_docs * 100, 1) if total_docs > 0 else 0.0
    raw_chars = len(raw_context)
    good_chars = len(good_context)
    char_reduction_pct = round((1 - good_chars / raw_chars) * 100, 1) if raw_chars > 0 else 0.0

    _stats = mo.callout(
        mo.md(
            f"**{good_docs_n} of {total_docs} chunks** passed retrieval evaluation"
            f" -- **{good_pct}% are good docs**. "
            f"Good context: {good_chars:,} chars vs {raw_chars:,} raw"
            f" ({char_reduction_pct}% reduction)."
        ),
        kind="info",
    )
    _display = mo.vstack([mo.ui.table(chunk_rows), _stats])
    _display
    return (good_context,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strips Analysis

    Every sentence strip produced by the `refine` node, annotated with its keep/discard status
    after the LLM relevance filter. The source context depends on the verdict:

    - **correct** -- strips are decomposed from `good_docs` (internally retrieved chunks above
      the lower threshold)
    - **incorrect** -- strips are decomposed from `web_docs` (Tavily web search results)
    - **ambiguous** -- `refine` is skipped; this table will be empty

    Strips present in `kept_strips` are marked **Kept**; the rest are **Discarded**.
    """)
    return


@app.cell
def _(mo, resp):
    kept_set = set(resp["kept_strips"])
    strip_rows = [
        {"Strip": s, "Status": "Kept" if s in kept_set else "Discarded"}
        for s in resp["strips"]
    ]
    _table = mo.ui.table(strip_rows)
    _table
    return


@app.cell
def _(mo, resp):
    import matplotlib.pyplot as plt

    total_strips = len(resp["strips"])
    kept_strips_n = len(resp["kept_strips"])
    kept_pct = round(kept_strips_n / total_strips * 100, 1) if total_strips > 0 else 0.0

    fig_strips, ax_strips = plt.subplots(figsize=(4, 3.2))
    ax_strips.bar(
        ["Total Strips", "Kept Strips"],
        [total_strips, kept_strips_n],
        color=["#4C78A8", "#54A24B"],
    )
    ax_strips.set_ylabel("Number of Strips")
    ax_strips.set_title(f"{kept_strips_n}/{total_strips} strips kept ({kept_pct}% useful)")
    ax_strips.spines["top"].set_visible(False)
    ax_strips.spines["right"].set_visible(False)
    plt.tight_layout()

    _strip_stats = mo.callout(
        mo.md(
            f"**{kept_strips_n} of {total_strips} strips** were relevant to the query"
            f" -- **{kept_pct}% useful**, {round(100 - kept_pct, 2)}% discarded as noise."
        ),
        kind="info",
    )
    _display = mo.vstack([_strip_stats, fig_strips])
    _display
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Refined Context

    The clean, noise-free context produced by the `refine` node -- the only text the LLM
    receives when generating the final answer. The bar chart below shows how context size
    shrinks across the pipeline; the stages shown depend on which path was taken:

    - **correct path** -- Raw retrieval -> Good context (eval filter) -> Refined context
      (sentence filter). Three bars; both filters reduce noise.
    - **incorrect path** -- Raw retrieval (failed internally) -> Web context (Tavily) ->
      Refined context (sentence filter). Three bars; web context replaces good context.
    - **ambiguous path** -- `refine` is skipped; refined context is empty.
    """)
    return


@app.cell
def _(mo, resp):
    mo.callout(mo.md(resp["refined_context"]), kind="info")
    return


@app.cell
def _(good_context, mo, plt, raw_context, resp, web_context):
    verdict = resp["verdict"]
    refined_len = len(resp["refined_context"])
    raw_len = len(raw_context)

    if verdict == "ambiguous":
        _display = mo.callout(
            mo.md(
                "Verdict was **ambiguous** -- `refine` was skipped."
                " No refined context to compare."
            ),
            kind="neutral",
        )
    elif verdict == "correct":
        good_len = len(good_context)
        eval_reduction_pct = round((1 - good_len / raw_len) * 100, 1) if raw_len > 0 else 0.0
        refine_reduction_pct = round((1 - refined_len / good_len) * 100, 1) if good_len > 0 else 0.0
        total_reduction_pct = round((1 - refined_len / raw_len) * 100, 1) if raw_len > 0 else 0.0

        fig_ctx, ax_ctx = plt.subplots(figsize=(5, 3.5))
        ax_ctx.bar(
            ["Raw Context", "Good Context", "Refined Context"],
            [raw_len, good_len, refined_len],
            color=["#E45756", "#F8A05C", "#54A24B"],
        )
        ax_ctx.set_ylabel("Character count")
        ax_ctx.set_title("Context size -- correct path")
        ax_ctx.spines["top"].set_visible(False)
        ax_ctx.spines["right"].set_visible(False)
        plt.tight_layout()

        _stats = mo.callout(
            mo.md(
                f"**Raw:** {raw_len:,} chars"
                f" -> **Good:** {good_len:,} chars (-{eval_reduction_pct}% via eval)"
                f" -> **Refined:** {refined_len:,} chars (-{refine_reduction_pct}% via refinement)."
                f" Total reduction: **{total_reduction_pct}%**."
            ),
            kind="success",
        )
        _display = mo.vstack([_stats, fig_ctx])
    else:
        web_len = len(web_context)
        refine_reduction_pct = round((1 - refined_len / web_len) * 100, 1) if web_len > 0 else 0.0

        fig_ctx, ax_ctx = plt.subplots(figsize=(5, 3.5))
        ax_ctx.bar(
            ["Raw (failed)", "Web Context", "Refined Context"],
            [raw_len, web_len, refined_len],
            color=["#E45756", "#4C78A8", "#54A24B"],
        )
        ax_ctx.set_ylabel("Character count")
        ax_ctx.set_title("Context size -- incorrect path (web fallback)")
        ax_ctx.spines["top"].set_visible(False)
        ax_ctx.spines["right"].set_visible(False)
        plt.tight_layout()

        _stats = mo.callout(
            mo.md(
                f"Internal retrieval failed (raw: {raw_len:,} chars, no good docs)."
                f" **Web:** {web_len:,} chars fetched via Tavily"
                f" -> **Refined:** {refined_len:,} chars (-{refine_reduction_pct}% via refinement)."
            ),
            kind="warn",
        )
        _display = mo.vstack([_stats, fig_ctx])

    _display
    return


if __name__ == "__main__":
    app.run()
