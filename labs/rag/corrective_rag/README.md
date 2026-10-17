---
platform: labs
concept_area: rag
slug: corrective_rag
phases: 2
link: https://youtu.be/41XDn81nR5c
framework: [langgraph, langchain, faiss, azure-openai]
date_started: 2026-10-17
date_completed: null
---

## Overview

Implementation of corrective RAG with LangGraph. Explores how to build a RAG pipeline
that self-evaluates retrieved documents and applies corrective steps -- such as query
rewriting and fallback retrieval -- when the initial retrieval quality is insufficient.

## Reference

[https://youtu.be/41XDn81nR5c](https://youtu.be/41XDn81nR5c)

## Phases

| # | Slug | Description |
|---|------|-------------|
| phase_01 | basic_rag | Baseline RAG pipeline -- document loading, chunking, embedding, retrieval, and generation |
| phase_02 | knowledge_refinement | Corrective layer -- relevance grading, query rewriting, and fallback retrieval |

## Key Concepts

- Retrieval-Augmented Generation (RAG)
- Document relevance grading
- Query rewriting
- LangGraph stateful graph execution
- FAISS vector store with persistent storage
