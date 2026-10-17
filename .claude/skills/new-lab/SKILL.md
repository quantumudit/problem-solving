---
name: new-lab
description: >
  Scaffold a new labs/ project -- creates the branch, folder structure, README.md,
  notes.md, and entry-point files for a single-phase or multi-phase AI/ML learning
  project. Use this whenever the user says "new lab", "start a lab", "scaffold a lab",
  or names a concept (e.g. "start a RAG chatbot lab", "new LangGraph memory project").
  Always invoke before creating any files under labs/.
argument-hint: "[concept_area] [slug]"
---

Today's date: !`date +%Y-%m-%d`

Scaffold a new lab project under `labs/`. Follow the steps below in order.
Never skip ahead. Every git action requires explicit user approval before running.

---

### Step 1 -- Collect lab metadata

Check what is already known from `$ARGUMENTS` or the conversation. Ask only for what
is missing, in one message if possible:

1. **Concept area** -- snake_case category:
   common values: `rag`, `agents`, `memory`, `langgraph`, `embeddings`,
   `fine_tuning`, `multi_agent`, `prompt_engineering`, `evaluation`
   (free-form if none of these fit)

2. **Slug** -- snake_case project name e.g. `youtube_rag_chatbot`, `ltm_langgraph`

3. **Description** -- one or two sentences: what this lab implements and what concept
   it explores

4. **Single-phase or multi-phase?**
   - Single: one `main.py` (and/or `notebook.ipynb`) at the project root
   - Multi: numbered phase subfolders; ask how many phases and a short slug for each
     e.g. phase 1 = `trim_messages`, phase 2 = `delete_messages`

5. **Framework(s)** -- list of libraries e.g. `langchain`, `langgraph`, `openai`,
   `anthropic`, `chroma`, `faiss`, `streamlit`, `fastapi` (free-form)

6. **Reference URL** -- YouTube link, blog post, or paper; empty string if none

7. **Entry-point format** -- for each phase (or the single phase):
   - `script` -- `main.py` only
   - `notebook` -- `notebook.ipynb` only
   - `both` -- `main.py` and `notebook.ipynb`

8. **Shared data folder needed?** -- yes/no; creates `data/` at the project root

---

### Step 2 -- Confirm branch name and folder path

Derive:
- **Branch:** `labs/{concept_area}/{slug}`
- **Folder:** `labs/{concept_area}/{slug}/`

Show the user:
```
Branch:  labs/{concept_area}/{slug}
Folder:  labs/{concept_area}/{slug}/
```

Ask: "Does this look right?"
Wait for confirmation or correction before proceeding.

---

### Step 3 -- Create branch

Only after user confirms, show the exact commands and ask permission:

```
git checkout main
git checkout -b labs/{concept_area}/{slug}
```

Wait for explicit approval. Do not create the branch until the user says yes.

---

### Step 4 -- Create folder structure

Show the planned structure and ask permission to create it.

**Single-phase:**
```
labs/{concept_area}/{slug}/
├── README.md
├── notes.md
├── main.py          (if script or both)
├── notebook.ipynb   (if notebook or both)
└── data/            (if shared data needed)
```

**Multi-phase:**
```
labs/{concept_area}/{slug}/
├── README.md
├── notes.md
├── data/                          (if shared data needed)
├── phase_01_{phase_slug}/
│   ├── main.py                    (if script or both)
│   └── notebook.ipynb             (if notebook or both)
├── phase_02_{phase_slug}/
│   ...
```

Run:
```
mkdir -p labs/{concept_area}/{slug}
```
And for multi-phase, one `mkdir -p` per phase folder, and `mkdir -p .../data` if needed.

---

### Step 5 -- Create README.md

Create at `labs/{concept_area}/{slug}/README.md`:

```markdown
---
platform: labs
concept_area: {concept_area}
slug: {slug}
phases: {null for single-phase, integer for multi-phase}
link: {reference_url}
framework: [{framework1}, {framework2}]
date_started: {today}
date_completed: null
---

## Overview

{description}

## Reference

{If link is non-empty: "[{reference title or URL}]({link}) -- brief note on how this differs from the reference, if at all."}
{If no link: "None"}

## Phases

| # | Slug | Description |
|---|------|-------------|
{one row per phase: | phase_01 | {phase_slug} | {brief} |}

(Omit the Phases section entirely for single-phase projects.)

## Key Concepts

- {concept derived from description or framework}
- {add more as known}
```

Fill in the Overview from the description the user gave. Derive a brief reference
title from the URL if one was provided (use the URL itself if the title is unknown).
Leave Key Concepts as a short starter list -- the user will expand them.

---

### Step 6 -- Create notes.md

Create at `labs/{concept_area}/{slug}/notes.md`:

```markdown
---
platform: labs
concept_area: {concept_area}
slug: {slug}
language: [python]
framework: [{framework1}, {framework2}]
topics: []
date_completed: null
revisit: false
---

## Approach


## What I Learned


## What Tripped Me Up


## Tricks / New Learnings


## Revisit Notes

```

Leave all body sections blank -- the user fills these in as they work through the lab.

---

### Step 7 -- Create entry-point files

**main.py** (when format is `script` or `both`):

For single-phase, create at `labs/{concept_area}/{slug}/main.py`.
For multi-phase, create one per phase at `labs/{concept_area}/{slug}/phase_##_{slug}/main.py`.

```python
```
(Empty file -- no boilerplate. The lab is exploratory; don't impose structure.)

**notebook.ipynb** (when format is `notebook` or `both`):

For single-phase, create at `labs/{concept_area}/{slug}/notebook.ipynb`.
For multi-phase, create one per phase at `labs/{concept_area}/{slug}/phase_##_{slug}/notebook.ipynb`.

Minimal valid notebook (one empty code cell):

```json
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

---

### Step 8 -- Commit with user approval

Show the exact commands and ask permission:

```
git add labs/{concept_area}/{slug}/
git commit -m "wip: scaffold labs/{concept_area}/{slug}"
```

For multi-phase, append a brief suffix:
```
git commit -m "wip: scaffold labs/{concept_area}/{slug} -- {n} phases, {framework}"
```

Wait for explicit approval. Do not commit until the user says yes.

---

### Step 9 -- Push with user approval

Show the exact command and ask permission:

```
git push -u origin labs/{concept_area}/{slug}
```

Wait for explicit approval. Do not push until the user says yes.

---

After everything is done, confirm what was created and remind the user:
- Fill in `## Key Concepts` in README.md as they learn
- Fill in `notes.md` sections as they work through the lab
- Use `/raise-pr` when the lab is ready to merge
