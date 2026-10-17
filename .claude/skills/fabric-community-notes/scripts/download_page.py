"""
Download a Microsoft Fabric Community forum page and save as HTML.

The forum blocks unauthenticated programmatic requests. To authenticate, copy the
Cookie header value from your browser's DevTools and pass it via --cookies.

How to get the cookie string:
  1. Open the forum in your browser (logged in).
  2. Open DevTools (F12) -> Network tab.
  3. Refresh the page, click any request to community.fabric.microsoft.com.
  4. Under Request Headers, copy the value of the "Cookie" line.
  5. Pass it to this script with --cookies "...".

Usage:
    python download_page.py <url> [--cookies "cookie_header_value"] [--out output_dir]

output_dir defaults to scratchpad/fabric-forum-refs/ relative to the repo root.
The saved filename is derived from the page <title> tag.
"""

import html as html_mod
import re
import sys
import urllib.request
from pathlib import Path


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

DEFAULT_OUTPUT_DIR = Path("scratchpad/fabric-forum-refs")


def parse_args(argv: list[str]) -> tuple[str, str | None, Path]:
    if len(argv) < 2:
        print("Usage: python download_page.py <url> [--cookies \"...\"] [--out output_dir]")
        sys.exit(1)

    url = argv[1]
    cookies: str | None = None
    output_dir = DEFAULT_OUTPUT_DIR

    i = 2
    while i < len(argv):
        if argv[i] == "--cookies" and i + 1 < len(argv):
            cookies = argv[i + 1]
            i += 2
        elif argv[i] == "--out" and i + 1 < len(argv):
            output_dir = Path(argv[i + 1])
            i += 2
        else:
            i += 1

    return url, cookies, output_dir


def fetch_page(url: str, cookies: str | None) -> bytes:
    headers = {"User-Agent": USER_AGENT}
    if cookies:
        headers["Cookie"] = cookies
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def extract_title(html_bytes: bytes) -> str:
    text = html_bytes.decode("utf-8", errors="replace")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if not m:
        return "page"
    title = html_mod.unescape(m.group(1))
    return re.sub(r"\s+", " ", title).strip()


def safe_filename(title: str) -> str:
    # Drop characters illegal in Windows filenames; keep spaces and hyphens
    cleaned = re.sub(r'[\\/:*?"<>|]', "", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > 180:
        cleaned = cleaned[:180].rstrip()
    return cleaned + ".html"


def main() -> None:
    url, cookies, output_dir = parse_args(sys.argv)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching: {url}")
    try:
        content = fetch_page(url, cookies)
    except urllib.error.HTTPError as exc:
        print(f"HTTP error {exc.code}: {exc.reason}")
        if exc.code == 403:
            print("")
            print("The forum requires authentication. To fix this:")
            print("  1. Open the forum in your browser (logged in).")
            print("  2. DevTools (F12) -> Network tab -> refresh -> click any request.")
            print("  3. Copy the Cookie header value.")
            print('  4. Re-run: python download_page.py <url> --cookies "<paste here>"')
        sys.exit(1)

    title = extract_title(content)
    filename = safe_filename(title)
    out_path = output_dir / filename

    out_path.write_bytes(content)
    print(f"Saved : {out_path}")
    print(f"Title : {title}")
    print(f"Size  : {len(content):,} bytes")


if __name__ == "__main__":
    main()
