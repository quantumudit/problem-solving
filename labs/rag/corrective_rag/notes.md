---
platform: labs
concept_area: rag
slug: corrective_rag
phases: 6
link: https://youtu.be/41XDn81nR5c
language: [python]
framework: [langgraph, langchain, faiss, azure-openai, tavily]
topics: [rag, langgraph, retrieval_evaluation, knowledge_refinement, web_search, query_rewriting, ambiguity_handling, faiss, azure_openai]
date_started: 2026-10-17
date_completed: 2026-10-19
revisit: false
---

## Approach

Built corrective RAG incrementally across 6 phases, each adding one corrective layer on top of
the previous. The guiding principle: start with the simplest working pipeline (baseline RAG),
identify its failure mode, and add exactly one corrective mechanism per phase. By phase 6, the
pipeline handles all three retrieval outcomes -- correct, incorrect, and ambiguous -- with
grounded, noise-free answers in each case.

Every phase reuses the same LangGraph `State` TypedDict and node function pattern. New phases
add nodes and conditional edges; they do not restructure earlier work. This additive approach
made it easy to see exactly what each phase contributed.

---

## Learning Progression -- Phase by Phase

### p01 -- Basic RAG

Built the foundation: `retrieve -> generate` with LangGraph. Three ML textbooks (Goodfellow,
Geron, Bishop) loaded via `PyPDFLoader`, chunked at 900 characters with 150-char overlap,
embedded with Azure OpenAI, and stored in a persistent FAISS index. A simple two-node graph
retrieves top-k chunks and passes raw text straight to the LLM.

Key learning: chunking by fixed character count (not semantic boundaries) is fast and practical
but inevitably bundles adjacent off-topic sentences into a single chunk. The LLM receives noisy
context and produces lower-quality answers -- the problem every subsequent phase addresses.

PDF loading is cached to `cache/documents.json` on the first run; subsequent runs skip parsing
and deserialize from the cache directly.

---

### p02 -- Knowledge Refinement

Added a 3-step refinement pass between retrieval and generation: decompose chunks into sentence
strips, filter each strip independently for relevance against the user query, recompose only the
kept strips into a clean `refined_context`.

The filter is an LLM chain that returns `keep=True/False` per strip. Strips marked `False` are
discarded before the context is assembled. The refinement node is reusable -- later phases pass
different document sources (web results, merged pools) through the same node.

Key learning: sentence-level filtration dramatically reduces context noise introduced by
character-based chunking. The 3-step pattern (decompose, filter, recompose) is the backbone of
the whole corrective pipeline and is reused unchanged in every phase that follows.

---

### p03 -- Retrieval Evaluation

Added an LLM-based evaluator that scores each retrieved chunk against the query on a [0.0, 1.0]
scale. Two thresholds divide the score space:

- `LOWER_TH = 0.3` -- minimum bar for relevance; chunks below this are discarded
- `UPPER_TH = 0.7` -- high confidence threshold

Three-way verdict:
- `correct` -- at least one chunk > 0.7; route to `refine -> generate`
- `incorrect` -- all chunks < 0.3; short-circuit with a failure message (dead-end in this phase)
- `ambiguous` -- mixed signals; no chunk > 0.7 but at least one >= 0.3; also a dead-end here

`good_docs` is a key construct introduced here: only chunks that clear `LOWER_TH` are forwarded
to generation, even when the verdict is `correct`. A chunk that helped decide `correct` but
scored below 0.3 is still filtered out.

Key learning: vector nearest-neighbor search always returns k results regardless of relevance.
Without an explicit quality gate, the pipeline blindly trusts whatever the vector store returns.
The evaluator is the first line of defense against retrieval failure.

---

### p04 -- Web Fallback

Replaced the `incorrect` dead-end with a real corrective action. When verdict is `incorrect`,
the pipeline calls the Tavily search API with the user's original query, converts the top web
results into standard `Document` objects (`web_docs`), and passes them through the same `refine`
node used for internal documents. The LLM then generates a grounded answer from clean web context.

Key learning: web snippets are noisy for the same reason chunks are noisy -- they contain filler,
metadata, and off-topic surrounding text. Reusing the existing `refine` node on `web_docs`
costs nothing and keeps context quality consistent regardless of knowledge source. The `ambiguous`
path still short-circuits -- not yet handled.

---

### p05 -- Query Rewriting

Added a `query_rewritter` node before `web_search`. The rewriter is an LLM chain given explicit
instructions: strip conversational filler, retain core search terms, append recency constraints
when the query implies them, and never answer the question -- only reformulate it for a search
engine. The output is stored in `web_query` (a separate state field from the user's `query`).

Key learning: raw user prompts are rarely search-engine-ready. Conversational phrasing and vague
framing produce noisy, off-target Tavily results. A dedicated rewriting step costs one LLM call
and substantially improves web retrieval quality on the `incorrect` path. The `ambiguous` path
still ends in a short-circuit -- the last remaining dead-end.

---

### p06 -- Ambiguity Handling

Resolved the final dead-end. When verdict is `ambiguous`, `good_docs` (partial internal
knowledge) and `web_docs` (external fallback retrieved via query rewriting) are merged into a
single pool before being passed to `refine`. The same `refine -> generate` path runs for all
three verdicts.

The `route` function simplified to a 2-way conditional: `correct` goes straight to `refine`;
everything else (`incorrect` and `ambiguous`) goes through `query_rewritter -> web_search ->
refine -> generate`. The `ambiguous_node` was removed entirely. The `refine` node selects its
document pool based on `state["verdict"]`: `good_docs` for correct, `web_docs` for incorrect,
`good_docs + web_docs` for ambiguous.

Key learning: the ambiguous case does not need a new graph route. The merge happens inside the
`refine` node with a simple conditional on state. LangGraph state management carries both
document pools through the graph transparently -- no extra edges or routing logic required.

---

## What I Learned

- **LangGraph pattern**: `State` TypedDict + node functions (`state: State -> dict`) +
  `add_conditional_edges` is a clean, composable pattern. Nodes stay pure; routing logic lives
  in a separate `route` function returned from a `@app.cell` (not `@app.function`).

- **Threshold-based verdict classification**: Two thresholds (LOWER_TH, UPPER_TH) create a
  clean three-zone scoring system. The verdict determines the pipeline branch; `good_docs`
  filtering is applied independently and always.

- **Refinement is source-agnostic**: The decompose-filter-recompose pipeline does not care
  whether its input comes from FAISS, Tavily, or a merged pool. Passing different document
  sources through the same `refine` node is the key design insight of the whole lab.

- **Query rewriting is cheap and high-leverage**: One additional LLM call before Tavily search
  consistently improves result quality on the `incorrect` path. The rewriter prompt needs to
  be explicit: keyword focus, recency handling, no answering.

- **Context merge for ambiguous**: Concatenating `good_docs + web_docs` before refinement
  gives the LLM both internal domain knowledge and external coverage, producing more complete
  answers than either source alone.

- **marimo reactive cells**: `mo.stop()` gates expensive cells (graph runs, API calls) behind
  a run button. `mo.stat()` + `mo.callout()` make verdict and reason immediately readable.
  `mo.hstack()` / `mo.vstack()` compose multi-panel analysis views cleanly.

---

## What Tripped Me Up

- **`route` must be a `@app.cell`, not `@app.function`**: marimo functions defined with
  `@app.function` are not reactive cells -- they do not participate in the dependency graph.
  The `route` function needs to be returned from a `@app.cell` so it is available as a
  reactive dependency to the graph-building cell.

- **`ambiguous_node` removal in p06**: The ambiguous path was initially wired as a separate
  node in the graph. Removing it required updating both the node list and the conditional edge
  map -- it's easy to miss one of the two.

- **`--` inside SVG XML comments**: The `--` sequence is invalid inside XML comments
  (`<!-- ... -->`). This broke `xml.etree.ElementTree` parsing silently -- the error pointed
  to the wrong line. Always use a comma or space instead of `--` inside SVG comment text.

- **shields.io badge icons**: Not all technology names map to a simple-icons.org slug. Azure
  OpenAI has no icon; marimo has no icon. Workarounds: use `gitbook` for marimo,
  `langchaincorporate` for LangGraph. The only reliable check is simpleicons.org.

---

## Tricks / New Learnings

- **Document caching**: `cache/documents.json` serializes `Document.model_dump()` and
  deserializes with `Document(**item)`. Saves significant time on repeated runs -- PDF loading
  across 3 large textbooks is slow.

- **FAISS persistence**: `vector_store.save_local()` / `FAISS.load_local()` persists the
  index across sessions. Built once in p01, reused unchanged in p02-p06.

- **Surrogate stripping**: PDF text extracted by `PyPDFLoader` sometimes contains lone UTF-8
  surrogates. Encoding each chunk with `encode("utf-8", "ignore").decode("utf-8", "ignore")`
  before embedding prevents `UnicodeEncodeError` at embed time.

- **marimo workspace**: Running `marimo edit` without a filename from the lab root opens a
  workspace file browser at `http://localhost:2718/` listing all notebooks in the folder.
  Faster than typing the full path for each phase.

- **Two-threshold verdict design**: Using `UPPER_TH` and `LOWER_TH` as module-level constants
  makes threshold tuning a single-line change. The original C-RAG paper used a fine-tuned
  T5-Large model for scoring; an LLM prompt works for prototyping at higher cost per call.

---

## Revisit Notes

