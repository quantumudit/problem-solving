# Data -- advanced_rag

Source documents forming the RAG knowledge base for this lab.
All files are gitignored; only this README is tracked.

---

## Files

### rag_for_nlp_paper.pdf (PDF)

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

---

### sherlock_holmes_books/ (TXT collection)

**Author:** Arthur Conan Doyle
**Source:** Project Gutenberg

Four classic Sherlock Holmes works used as a shared fiction knowledge base for retrieval experiments.

#### b01_adv_of_holmes.txt

**Title:** The Adventures of Sherlock Holmes
**Download:** https://www.gutenberg.org/cache/epub/1661/pg1661.txt

A collection of 12 detective stories featuring Sherlock Holmes and Dr. Watson as they investigate
mysterious crimes, uncover hidden motives, and solve complex cases using observation and deduction.

#### b02_memoirs_of_holmes.txt

**Title:** The Memoirs of Sherlock Holmes
**Download:** https://www.gutenberg.org/cache/epub/834/pg834.txt

A collection of 11 detective stories involving unusual crimes, secret identities, suspicious
characters, and intricate mysteries. Includes The Final Problem, one of Holmes's most famous
encounters.

#### b03_hound_of_baskervilles.txt

**Title:** The Hound of the Baskervilles
**Download:** https://www.gutenberg.org/cache/epub/2852/pg2852.txt

A full-length mystery centered on the Baskerville family curse, a terrifying hound, and strange
events on the Dartmoor moors. Holmes and Watson investigate whether the apparent supernatural
threat has a rational explanation.

#### b04_return_of_holmes.txt

**Title:** The Return of Sherlock Holmes
**Download:** https://www.gutenberg.org/cache/epub/108/pg108.txt

A collection of 13 detective stories following Holmes's return to investigative work. Holmes and
Watson tackle new cases involving missing people, stolen treasures, suspicious deaths, and
elaborate schemes.
