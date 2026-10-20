---
platform: labs
concept_area: rag
slug: advanced_rag
language: [python]
framework: [langgraph, langchain, faiss, azure-openai]
topics: []
date_completed: null
revisit: false
---

## Approach


## What I Learned


## What Tripped Me Up

### Stale vector store after changing chunking or metadata

The FAISS index is persisted to `vector_store/faiss/{slug}/` and loaded from disk on every
later run. When a saved index exists, `FAISS.from_documents` never executes, so whatever
was embedded and stored at build time is what you keep getting back. Two kinds of change
are silently ignored until the index is rebuilt (delete the slug folder):

- **Chunking parameters** -- changing `chunk_size` or `chunk_overlap` changes the chunk
  boundaries and the text that gets embedded, but the saved index still holds the old chunks.
- **`Document` metadata** -- adding or editing metadata (e.g. `chunk_id`) before the vector
  store is built. Metadata is stored inside the index alongside each vector, so a new key
  never shows up in retrieved documents (e.g. in the analysis table) until the rebuild.

Symptom: the code looks right but retrieved chunks do not reflect the change (a missing
`chunk_id`, chunk sizes that do not match the splitter settings).

Rule of thumb: anything that feeds into the build step (splitter settings, chunk text,
metadata) invalidates the index. Delete `vector_store/faiss/{slug}/` after changing it.

## Tricks / New Learnings

### Do not mutate list fields of the graph state inside a node

In the `retrieve` node of `p05_rag_fusion.py`, the question is added to the generated
queries by unpacking into a new list instead of calling `.append`:

```python
all_queries = [*state["queries"], state["question"]]
```

`state["queries"]` is the same list object that the `generate_queries` node wrote into the
state. Calling `state["queries"].append(...)` would change that shared state object
in place instead of returning an update, which causes two problems:

- **Silent side effect** -- `queries` itself would now contain the original question, so the
  later inspection of `resp["queries"]` shows 4 entries instead of the 3 generated ones. A
  second run of the node would add the question again.
- **Fails on non-list values** -- if the field ever holds a tuple (or another immutable
  sequence), `.append` raises `AttributeError: 'tuple' object has no attribute 'append'`.

Unpacking with `[*...]` builds a fresh list, works for any iterable, and leaves the state
untouched. A node should only change state by returning a dict of updates, e.g.
`return {"docs": docs}`.

Note: with a plain list field, `.append` did not raise in a quick test with a LangGraph
`StateGraph` -- it just mutated the state silently. The exact error seen earlier is not
recorded here; add it if it comes up again.


## Revisit Notes
