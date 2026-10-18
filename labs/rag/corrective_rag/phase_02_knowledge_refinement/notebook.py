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
    # Knowledge Refinement

    ## What Was Built So Far

    In phase_01, the baseline RAG pipeline was assembled:

    - **phase_01 (basic_rag)**: Baseline pipeline -- retrieve top-k chunks from a FAISS vector store, pass them raw to an LLM, generate an answer. No quality checks, no filtering.

    The baseline pipeline trusts whatever the vector store returns. When retrieved chunks contain a mix of relevant and off-topic text -- a natural side-effect of fixed-size text chunking -- the LLM receives noisy context, reducing the quality of the generated answer.

    ---

    ## Why Knowledge Refinement Needed?

    When documents are stored in vector databases, text splitting/chunking is usually performed based on fixed character counts (e.g., 900 characters) rather than semantic topic boundaries.

    Consequently:
    - A retrieved chunk may contain a relevant answer along with irrelevant text from adjacent topics or paragraphs.
    - Passing raw, noisy chunks to the LLM dilutes the prompt context and reduces the overall quality of the generated response.

    ---

    ## The 3-Step Knowledge Refinement Pipeline

    Knowledge Refinement transforms raw document chunks into clean context through three sequential steps

    - **Decomposition:** The retrieved document chunk is split into fine-grained "sentence strips" ($S_1, S_2, \dots, S_k$) at the individual sentence level
    - **Filtration:**
        - Each sentence strip is evaluated individually against the user query using a strict relevance filter
        - The filter determines if the sentence strip directly helps answer the query, assigning a decision (`keep = True` or `keep = False`)
    - **Re-combination:**
        - All strips marked `keep = True` are concatenated back together into a compact, noise-free context block (refined_context)
        - Strips marked `keep = False` are discarded.

    ---

    The **Knowledge Refinement** process is illustrated using an example where a retrieved document chunk contains both relevant and off-topic sentences due to fixed character-based chunking.

    ---

    ### Example Setup

    * **User Question ($q$)**: **"What is gradient descent?"**
    * **Raw Retrieved Document Chunk ($d_1$)**:
      > *"Gradient descent is an optimization algorithm used to minimize a loss function. It iteratively updates parameters in the direction of negative gradient. Neural networks are composed of layers of neurons with non-linear functions. Convolutional neural networks are particularly effective for image processing tasks."*

    **The Problem:** The first two sentences accurately describe gradient descent, but the last two sentences discuss neural network layers and CNNs. This noise occurred because fixed text chunking (e.g., 900 characters) captured trailing text from an adjacent paragraph.

    > Note: Depending upon the set $k$ value we might be getting $k$ number of documents such as $d_1, d_2, \dots, d_k$ and the same 3-step knowledge refinement will be applied to each of the documents. Here, we are just considering one retrieved document chunk for illustration.

    ---

    ### The 3-Step Knowledge Refinement Process

    #### Step 1: Decomposition (Creating Sentence Strips)
    The raw document $d_1$ is split at sentence boundaries into individual **sentence strips** $(S_1, S_2, S_3, S_4)$:

    * **$S_1$**: *"Gradient descent is an optimization algorithm used to minimize a loss function."*
    * **$S_2$**: *"It iteratively updates parameters in the direction of negative gradient."*
    * **$S_3$**: *"Neural networks are composed of layers of neurons with non-linear functions."*
    * **$S_4$**: *"Convolutional neural networks are particularly effective for image processing tasks."*

    ---

    #### Step 2: Filtration (Scoring Each Strip)
    Each sentence strip is evaluated against the query $q$ using a strict relevance filter (such as a fine-tuned T5-Large model or an LLM):

    * **$S_1$** $\rightarrow$ Relevant to gradient descent $\rightarrow$ **Keep (`True`)**
    * **$S_2$** $\rightarrow$ Relevant to gradient descent $\rightarrow$ **Keep (`True`)**
    * **$S_3$** $\rightarrow$ Irrelevant (general neural network architecture) $\rightarrow$ **Discard (`False`)**
    * **$S_4$** $\rightarrow$ Irrelevant (CNN image processing) $\rightarrow$ **Discard (`False`)**

    > Note: The fine-tuned T5-Large model is used by the authors in the paper: [Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884)

    ---

    #### Step 3: Re-combination (Refined Context)
    The strips marked `keep = True` ($S_1$ and $S_2$) are concatenated back together to create the final **refined document context**:

    > **Refined $d_1$ Context:**
    > *"Gradient descent is an optimization algorithm used to minimize a loss function. It iteratively updates parameters in the direction of negative gradient."*

    This clean, noise-free context is then passed to the LLM during answer generation, ensuring higher accuracy and preventing context pollution.
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

    Instantiate the Azure OpenAI chat model (`gpt-6-luna`) used across two roles in this
    pipeline: the relevance filter (keep/discard sentence strips) and the final answer generator.
    A single shared instance keeps the setup simple and ensures consistent behavior across both invocations.
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
    The same LLM instance serves two distinct roles in this pipeline: filtering sentence strips
    (via `filter_chain`) and generating the final answer (via `template | llm`). Reusing one
    instance avoids redundant initialization and ensures consistent model behavior across both invocation types.
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

    **Base RAG fields (same as phase_01):**
    - `question` -- the user's input query
    - `docs` -- raw chunks returned by the retriever
    - `answer` -- final generated answer

    **Knowledge refinement fields (new in phase_02):**
    - `strips` -- all sentence strips produced by decomposing the raw retrieved context
    - `kept_strips` -- the subset of strips the LLM judge marked as relevant to the question
    - `refined_context` -- the final clean context: `kept_strips` joined into a single string, ready for the LLM
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
        strips: List[str]
        kept_strips: List[str]
        refined_context: str
        answer: str

    return (State,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Nodes

    Three node functions implement the knowledge-refined RAG pipeline. Each reads from and
    writes to the shared `State` dict. Unlike phase_01 which passes raw chunks directly to
    the LLM, this pipeline inserts a refinement step between retrieval and generation:

    - **`retrieve`** -- fetch the top-k chunks from the vector store
    - **`refine`** -- decompose raw chunks into sentence strips, filter for relevance, recompose
    - **`generate`** -- synthesize an answer from the refined (noise-free) context
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
    ### 8b. Refine Node

    The core of this phase. Unlike traditional RAG which passes raw retrieved chunks straight to the LLM,
    the `refine` node applies the 3-step knowledge refinement pipeline before generation:
    decompose all retrieved chunks into sentence strips, filter each strip for relevance against the query,
    then recompose the kept strips into a clean context block passed to `generate`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 8b.1 Sentence Level Decomposition

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


@app.cell
def _(decompose_to_sentences):
    sample_text = """
    variance (because the red curves in the left plot look similar) but high bias (because
    the two curves in the right plot are very different). Conversely on the bottom row, for
    which λ is small, there is large variance (shown by the high variability between the
    red curves in the left plot) but low bias (shown by the good ﬁt between the average
    model ﬁt and the original sinusoidal function). Note that the result of averaging many
    solutions for the complex model with M =2 5 is a very good ﬁt to the regression
    function, which suggests that averaging may be a beneﬁcial procedure. Indeed, a
    weighted averaging of multiple solutions lies at the heart of a Bayesian approach,
    although the averaging is with respect to the posterior distribution of parameters, not
    with respect to multiple data sets.
    We can also examine the bias-variance trade-off quantitatively for this example.
    """

    sentence_strips = decompose_to_sentences(sample_text)
    print(sentence_strips)
    return (sentence_strips,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three things happen in order:

    1. **Normalize whitespace:** `re.sub(r"\s+", " ", text).strip()` collapses all newlines, tabs, and multiple spaces into single spaces. PDFs often have erratic whitespace from layout extraction, so this cleans that up before splitting.
    2. **Split on sentence boundaries:** `re.split(r"(?<=[.!?])\s+", text)` splits wherever whitespace follows a `.`, `!`, or `?`. The lookbehind `(?<=[.!?])` says *"split here only if the character before was sentence-ending punctuation"*, so it doesn't split mid-sentence on random whitespace.
    3. **Filter short fragments:** `if len(s) > 20` drops anything shorter than 20 characters. This removes noise like lone section headers, page numbers, or partial lines that survived the split but carry no useful content.

    The output is a `List[str]` of sentence strips -- $S_1, S_2, S_3, \dots$ -- which are then passed one by one to the filtration step to decide which ones are relevant to the user query.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 8b.2 Sentence Filtration

    Step 2 of the pipeline. Each sentence strip is evaluated individually against the user question
    using an LLM as a strict relevance judge returning a structured `KeepDecision` -- `keep=True`
    to retain the strip, `keep=False` to discard it.

    `with_structured_output(KeepDecision)` ensures the LLM always returns a parseable boolean
    response rather than free text, making the decision deterministic and easy to act on.
    """)
    return


@app.cell
def _():
    from pydantic import BaseModel, Field

    return BaseModel, Field


@app.cell
def _(BaseModel, Field):
    class KeepDecision(BaseModel):
        keep: bool = Field(
            ...,
            description="True to retain the sentence strip as relevant to the question; False to discard it.",
        )

    return (KeepDecision,)


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate

    return (ChatPromptTemplate,)


@app.cell
def _(ChatPromptTemplate):
    filter_sys_msg = """You are a strict relevance filter.
    Return keep=true only if the sentence directly helps answer the question.
    Use ONLY the sentence. Output JSON only.
    """

    # Prompt template with role-based message to filter sentence strips
    filter_template = ChatPromptTemplate.from_messages([
        ("system", filter_sys_msg),
        ("human", "Question: {question}\n\nSentence:\n{sentence}")
    ])
    return (filter_template,)


@app.cell
def _(KeepDecision, filter_template, llm):
    # Filter Chain (LLM Judge)
    filter_chain = filter_template | llm.with_structured_output(KeepDecision)
    return (filter_chain,)


@app.cell
def _(filter_chain, mo, sentence_strips):
    sample_q = "Explain the bias-variance trade-off"
    rows = [
        {
            "Strip": s,
            "Decision": "Keep" if filter_chain.invoke({"question": sample_q, "sentence": s}).keep else "Discard",
        }
        for s in sentence_strips
    ]
    mo.vstack([
        mo.md(f"**Question:** _{sample_q}_"),
        mo.ui.table(rows),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Assembling the `refine` Node

    Step 3 -- and the `refine` node function itself. Combines all three steps: decompose all retrieved
    chunks into strips, invoke the filter chain on each strip, then join the kept strips into a single
    `refined_context` string passed downstream to the `generate` node.
    """)
    return


@app.cell
def _(State, decompose_to_sentences, filter_chain):
    def refine(state: State) -> dict:
        q = state["question"]
        docs = state["docs"]

        # Combine retrieved documents into one context string
        context = "\n\n".join(d.page_content for d in docs).strip()

        # Step-1: Decomposition: context --> sentence strips
        strips = decompose_to_sentences(context)

        # Step-2: Filter: keep only relevant strips
        kept = []

        for s in strips:
            if filter_chain.invoke({"question": q, "sentence": s}).keep:
                kept.append(s)

        # Step-3: Recompose: glue kept strips back together (internal knowledge)
        refined_context = "\n".join(kept).strip()

        return {
            "strips": strips,
            "kept_strips": kept,
            "refined_context": refined_context
        }


    return (refine,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8c. Generate Node

    Same structure as in traditional RAG, but instead of raw retrieved chunks it receives the `refined_context`
    produced by the `refine` node -- a compact, noise-free string containing only the relevant sentences.
    The system prompt is also updated to reflect the ML tutor role and the refined input.
    """)
    return


@app.cell
def _(ChatPromptTemplate):
    sys_msg = """You are a helpful ML tutor. Answer ONLY using the provided refined context.
    If the context is empty or insufficient, simply say: "I don't know based on the provided books."
    """
    # Prompt template with role-based messages
    template = ChatPromptTemplate.from_messages(
        [
            ("system", sys_msg),
            ("human", "Question: {question}\n\nRefined Context:\n{refined_context}"),
        ]
    )
    return (template,)


@app.cell
def _(State, llm, template):
    def generate(state: State) -> dict:
        chain = template | llm
        response = chain.invoke({"question": state["question"], "refined_context": state["refined_context"]})
        return {"answer": response.content}

    return (generate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `retrieve`, `refine`, and `generate` together implement the full knowledge-refined RAG loop: pull context,
    clean it, then synthesize. Each function reads from and writes to the shared `State` dict that LangGraph
    passes between nodes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Build the Graph

    Assemble the nodes into a LangGraph `StateGraph` and compile it. Unlike later phases which
    add conditional branching based on retrieval quality, this graph is a straight linear pipeline:

    ```
    START -> retrieve -> refine -> generate -> END
    ```

    Every invocation runs all three nodes in order -- there is no routing or conditional logic.
    The refinement step always runs, regardless of how relevant the retrieved chunks are.
    """)
    return


@app.cell
def _():
    from langgraph.graph import StateGraph, START, END

    return END, START, StateGraph


@app.cell
def _(END, START, State, StateGraph, generate, refine, retrieve):
    builder = StateGraph(State)

    # Add nodes
    builder.add_node("retrieve", retrieve)
    builder.add_node("refine", refine)
    builder.add_node("generate", generate)

    # Add Edges
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "refine")
    builder.add_edge("refine", "generate")
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
    `retrieve -> refine -> generate` sequence and returns the updated state with `strips`,
    `kept_strips`, `refined_context`, and `answer` all populated. Every question runs the
    complete pipeline -- there are no shortcuts or fallback paths.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Run the Pipeline

    Enter a question and click **Run pipeline** to invoke the graph end-to-end.

    **Try these to observe different refinement behaviors:**

    | Question | What to observe |
    |---|---|
    | "Explain the bias-variance trade-off" | Well-covered across all three books -- retrieval is strong and refinement keeps most strips. Clean, focused refined context with modest noise reduction. |
    | "What are attention mechanisms and why are they important in current scenario?" | Partially covered (DL book touches attention, but modern Transformer context is out of scope for these 2016-era books). Refinement discards more strips, producing a shorter but more focused context. |
    | "What are the latest major AI news?" | No retrieved chunk is relevant to recent news -- the filtration step discards almost all strips. The refined context will be near-empty and the LLM will say it doesn't know based on the provided books. |
    """)
    return


@app.cell
def _(graph):
    def process_response(q: str):
        input_state = {
            "question": q,
            "docs": [],
            "strips": [],
            "kept_strips": [],
            "refined_context": "",
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
    mo.md(r"""
    ## 11. Analysis

    Inspect the intermediate state produced by the pipeline run above -- retrieved documents,
    sentence strips, and context size across each stage. All sections below are read-only views
    of `resp`; re-running section 10 refreshes them.
    """)
    return


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
    ### Explore Retrieved Documents

    The `k=4` raw chunks retrieved from the vector store -- before any refinement.
    Expand each to inspect the raw content passed into the `refine` node.
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
    ### Strips Analysis

    Every sentence strip produced by decomposing the **raw context** (all `k=4` retrieved chunks
    joined), annotated with its keep/discard status after the LLM relevance filter. Strips present
    in `kept_strips` are marked **Kept**; the rest are **Discarded**.
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

    The clean, noise-free context produced by the 3-step knowledge refinement -- the only
    text the LLM receives when generating the final answer. The bar chart below shows how
    much context was trimmed: raw retrieval vs. post-refinement character count.
    """)
    return


@app.cell
def _(mo, resp):
    mo.callout(mo.md(resp["refined_context"]), kind="info")
    return


@app.cell
def _(mo, plt, raw_context, resp):
    refined_len = len(resp["refined_context"])
    raw_len = len(raw_context)
    reduction_pct = round((1 - refined_len / raw_len) * 100, 1) if raw_len > 0 else 0.0

    fig_ctx, ax_ctx = plt.subplots(figsize=(4, 3.2))
    ax_ctx.bar(
        ["Raw Context", "Refined Context"],
        [raw_len, refined_len],
        color=["#E45756", "#54A24B"],
    )
    ax_ctx.set_ylabel("Character count")
    ax_ctx.set_title(f"Context size: {reduction_pct}% reduction after refinement")
    ax_ctx.spines["top"].set_visible(False)
    ax_ctx.spines["right"].set_visible(False)
    plt.tight_layout()

    _stats = mo.callout(
        mo.md(
            f"**Refined:** {refined_len:,} chars -- "
            f"**{reduction_pct}% reduction** from raw context ({raw_len:,} chars)."
        ),
        kind="success",
    )
    _display = mo.vstack([_stats, fig_ctx])
    _display
    return


if __name__ == "__main__":
    app.run()
