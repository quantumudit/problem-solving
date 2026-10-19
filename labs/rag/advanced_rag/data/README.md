# Data -- advanced_rag

Source documents forming the RAG knowledge base for this lab.
All files are gitignored; only this README is tracked.

---

## Files

### rag-for-nlp-paper.pdf

**Title:** Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
**Authors:** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,
Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, Sebastian Riedel, Douwe Kiela
**Publisher:** NeurIPS 2020 / Meta AI Research
**Download:** https://arxiv.org/pdf/2005.11401

The foundational paper that introduced Retrieval-Augmented Generation (RAG) as a general-purpose
architecture for knowledge-intensive NLP tasks. Proposes combining a parametric memory (a pre-trained
seq2seq model) with a non-parametric memory (a dense vector index over Wikipedia) via a learned
retriever (DPR). Demonstrates that retrieval-augmented models outperform purely parametric models
on open-domain QA, fact verification, and knowledge-grounded generation tasks -- while also being
more interpretable and updatable than storing all knowledge in model weights.
