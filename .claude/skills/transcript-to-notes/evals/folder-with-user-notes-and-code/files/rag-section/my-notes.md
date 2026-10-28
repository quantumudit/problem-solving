My notes (lectures 5-6)

- gotcha: overlap should be smaller than chunk size or you get duplicates everywhere
- chunk_size is in characters for RecursiveCharacterTextSplitter by default, NOT tokens (instructor said tokens loosely)
- RRF formula: score = sum(1 / (k + rank)), k is usually 60

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""],
)
chunks = splitter.split_documents(docs)
for c in chunks:
    c.metadata["source"] = c.metadata.get("source", "unknown")
```

```python
def rrf(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)
```
