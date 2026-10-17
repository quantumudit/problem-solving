"""
Extract post content from a saved Microsoft Fabric Community HTML page.

The Fabric Community forum (Khoros/Lithium platform) uses Next.js CSS modules,
so class names look like: lia-g-message-body__LkV7_ or MessageViewStandard_lia-author-text__3ExAu
The semantic prefix (e.g. lia-g-message-body, lia-author-text) is stable across saves;
the hash suffix changes. All regex here matches on the stable semantic prefix only.

Usage:
    python extract_posts.py <html_file> [output_file]

Output is written to output_file (or stdout) as plain text with === POST N === separators.
"""

import re
import html as html_mod
import sys


def clean_inner(raw_html):
    """Minimal clean for content already inside a code block."""
    text = re.sub(r"<[^>]+>", "", raw_html)
    return html_mod.unescape(text).strip()


def clean_text(raw_html):
    """Convert an HTML fragment to readable plain text."""
    # Preserve line breaks
    text = re.sub(r"<br\s*/?>", "\n", raw_html, flags=re.IGNORECASE)

    # Preserve list items
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.IGNORECASE)

    # Preserve code blocks: wrap in ``` fences
    # Matches both <pre>...</pre> and <code>...</code>
    def fence_code(m):
        inner = clean_inner(m.group(1))
        return f"\n```\n{inner}\n```\n"

    text = re.sub(
        r"<(?:pre|code)[^>]*>(.*?)</(?:pre|code)>",
        fence_code,
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Describe images (alt text when available)
    def describe_img(m):
        full_tag = m.group(0)
        alt_match = re.search(r'alt="([^"]*)"', full_tag, re.IGNORECASE)
        alt = alt_match.group(1).strip() if alt_match else ""
        return f"[image: {alt}]" if alt else "[image]"

    text = re.sub(r"<img[^>]*>", describe_img, text, flags=re.IGNORECASE)

    # Strip all remaining HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode HTML entities
    text = html_mod.unescape(text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def is_noise(author, content):
    """Return True for footer rows, CSS blobs, or other non-post content."""
    if author == "unknown":
        return True
    if len(content) < 20:
        return True
    # CSS blocks start with selectors or property declarations
    if re.match(r"^\s*[\.#@\*]|^\s*\w[\w-]*\s*\{", content[:200]):
        return True
    # Copyright footer
    if content.startswith("(c)") or "Microsoft" in content[:50]:
        return True
    return False


def extract_posts(html_path):
    """Parse the HTML file and return a list of post dicts."""
    with open(html_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # --- Authors ---
    # Stable prefix: MessageViewStandard_lia-author-text
    # The CSS module hash (e.g. __3ExAu) varies between saves -- match with [^"]*
    raw_authors = re.findall(
        r'MessageViewStandard_lia-author-text[^"]*"[^>]*>(.*?)</span>',
        content,
        re.DOTALL,
    )
    authors = [re.sub(r"<[^>]+>", "", a).strip() for a in raw_authors]

    # --- Message bodies ---
    # Stable prefix: lia-g-message-body
    # The closing </div></div> ends the body section
    raw_bodies = re.findall(
        r'lia-g-message-body[^"]*"[^>]*>(.*?)</div>\s*</div>',
        content,
        re.DOTALL,
    )

    posts = []
    seen_fingerprints = set()

    for i, body in enumerate(raw_bodies):
        author = authors[i] if i < len(authors) else "unknown"
        cleaned = clean_text(body)

        if is_noise(author, cleaned):
            continue

        # Deduplicate: the forum renders an inline preview AND the full post
        # for each message -- both have identical content. Keep only the first.
        fingerprint = (author, cleaned[:120])
        if fingerprint in seen_fingerprints:
            continue
        seen_fingerprints.add(fingerprint)

        posts.append(
            {
                "index": i + 1,
                "author": author,
                "content": cleaned,
            }
        )

    return posts


def format_output(posts):
    """Format posts as readable text with section separators."""
    lines = []
    for p in posts:
        lines.append(f"=== POST {p['index']} | Author: {p['author']} ===")
        lines.append(p["content"])
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_posts.py <html_file> [output_file]")
        sys.exit(1)

    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    posts = extract_posts(html_file)
    output = format_output(posts)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Extracted {len(posts)} posts -> {output_file}")
    else:
        # Use utf-8 with replacement for Windows consoles (cp1252 can't handle emoji)
        sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
        sys.stdout.buffer.write(b"\n")
