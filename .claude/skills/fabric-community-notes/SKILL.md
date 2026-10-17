---
name: fabric-community-notes
description: >
  Use this skill whenever the user provides a saved HTML file from the Microsoft Fabric
  Community forum and wants to fill in a community notes.md for that contribution.
  Triggers on: HTML file path from community.fabric.microsoft.com, "fill in the notes",
  "populate notes.md", or any request to extract problem/solution from a saved forum thread.
  Always use this skill before attempting to read or parse community HTML files manually.
---

# Fabric Community Notes Filler

Extracts the thread content from a saved Fabric Community HTML export and fills in the
`notes.md` stub for that contribution.

---

## Background: how the forum HTML is structured

The Fabric Community runs on the Khoros/Lithium platform rendered with Next.js CSS modules.
Class names look like `lia-g-message-body__LkV7_` -- the semantic prefix is stable across
saves; the hash suffix varies. The HTML is typically minified (very long single lines).

Two CSS class prefixes matter:
- `lia-g-message-body` -- the div containing each post's text
- `MessageViewStandard_lia-author-text` -- the span containing the poster's username

The bundled script `scripts/extract_posts.py` handles all of this. Use it, do not try to
parse the HTML manually.

---

## Step 1 -- Run the extraction script

```powershell
python -I ".claude/skills/fabric-community-notes/scripts/extract_posts.py" `
    "<html_file_path>" `
    "<scratchpad_output_path>.txt"
```

The script outputs `=== POST N | Author: username ===` blocks -- one per real post.
It automatically skips footer rows, CSS blobs, and other noise.

Read the output file to get all posts.

---

## Step 2 -- Map posts to notes.md sections

| Post | Who | Maps to |
|---|---|---|
| Post 1 | OP (original poster) | `## Problem` |
| Posts by `quantumudit` | Your answer(s) | `## My Solution` |
| OP follow-up posts | OP responding | Use as context -- may clarify problem or confirm solution worked |
| Posts by others | Community members | `## Alternate Solutions` (only if substantive) |

**Identifying the accepted answer:**
- `accepted: true` when: "Marked as Solution" appears in the post text, OR OP thanks
  `quantumudit` and confirms it worked, OR the tracker row already has `accepted: yes`
- `accepted: false` otherwise

**Multiple `quantumudit` posts:**
Combine them into one coherent solution. The first is usually the main answer; follow-ups
are clarifications. Merge into one narrative rather than listing them sequentially.

---

## Step 3 -- Fill in the notes.md

### `## Problem`
Write 2-4 sentences of clean prose -- do not copy-paste verbatim from the thread.
Capture:
- What the user is trying to achieve
- What they tried and why it failed (if mentioned)
- Any relevant data model details (table names, column names, structure)

### `## My Solution`
Present the DAX/PQ code from your post in a properly fenced code block (` ```dax ` or
` ```powerquery `). Clean up any HTML artefacts in the extracted code.

Add a brief note if the solution uses generic placeholder names (e.g., `'Table'[Column1]`)
so the reader knows what to substitute.

### `## Why It Works`
2-5 sentences explaining the key mechanism. Focus on:
- Why the naive approach fails (if the OP tried something wrong)
- What the core DAX/PQ function actually does in this context
- Any non-obvious invariant the solution relies on

Omit this section only if the solution is completely self-explanatory.

### `## Alternate Solutions`
Include only if other community members posted substantively different, valid solutions.
Write "None in the thread." otherwise.

### Frontmatter to update after reading the thread

| Field | What to set |
|---|---|
| `date_answered` | Date of your first reply in the thread (if different from publish date) |
| `topics` | Replace placeholder tags with actual DAX functions/concepts used |
| `accepted` | `true` / `false` based on thread outcome |

---

## Edge cases -- use judgment, do not skip these

**Images in posts:**
The script replaces `<img>` tags with `[image]` or `[image: alt text]`. If an image is
clearly important (a screenshot of the data model, the expected output, a visual of the
problem), note it explicitly:
> `[OP attached a screenshot of the data -- not available in the HTML export]`

**Quoted / nested messages:**
The forum sometimes embeds quoted prior posts inside a reply. These show up as duplicated
text in the extraction. Ignore the quoted portion; only use the new content above or below it.

**Long back-and-forth threads:**
Focus on: the original question, your solution post(s), the final outcome. Skip intermediate
debugging exchanges unless they reveal something important about why the solution works.

**Garbled or incomplete code:**
HTML renderers sometimes split code blocks awkwardly. If the extracted code looks wrong,
note it with a comment at the bottom of the solution:
> `<!-- code extracted from HTML export -- verify against thread URL if anything looks off -->`

**Non-code answers:**
Some answers are explanations with no code (e.g., "use a bidirectional relationship instead").
Write these as prose in `## My Solution` without a code block.

**Thread never resolved:**
OP did not respond or the thread went cold. Set `accepted: false` and write a note in
`## Alternate Solutions` if your solution is provisional.

**Unexpected content:**
If the extraction produces something you did not expect -- extra posts, odd formatting,
content that does not fit the sections above -- read it with judgment and incorporate what
is useful. The goal is an accurate, readable notes.md, not mechanical slot-filling.
