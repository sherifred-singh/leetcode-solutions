#!/usr/bin/env python3
"""
LeetCode Local Sync Script
==========================
Synchronizes your accepted LeetCode submissions directly to your local repository.
Reads credentials from environment variables or a local .env file:
  - LEETCODE_SESSION
  - LEETCODE_CSRF_TOKEN
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "my-submissions"

EXTENSION_MAP = {
    "c": "c",
    "cpp": "cpp",
    "python": "py",
    "python3": "py",
    "java": "java",
    "javascript": "js",
    "typescript": "ts",
    "golang": "go",
    "rust": "rs",
}

def load_env():
    """Loads simple KEY=VALUE pairs from .env if present."""
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

def get_submissions(session: str, csrf: str, offset: int = 0, limit: int = 20):
    """Fetches submission list from LeetCode API."""
    url = f"https://leetcode.com/api/submissions/?offset={offset}&limit={limit}"
    headers = {
        "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf};",
        "X-CSRFToken": csrf,
        "Referer": "https://leetcode.com/submissions/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        print(f"[!] Error fetching submissions: HTTP {resp.status_code}")
        return []
    return resp.json().get("submissions_dump", [])

def main():
    load_env()
    session = os.getenv("LEETCODE_SESSION")
    csrf = os.getenv("LEETCODE_CSRF_TOKEN")

    if not session or not csrf:
        print("[X] Missing credentials!")
        print("    Please set LEETCODE_SESSION and LEETCODE_CSRF_TOKEN in your environment or in a .env file.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[*] Starting LeetCode sync to: {OUTPUT_DIR}")

    offset = 0
    limit = 20
    total_saved = 0

    while True:
        print(f"[*] Fetching submissions (offset={offset})...")
        submissions = get_submissions(session, csrf, offset=offset, limit=limit)
        if not submissions:
            break

        for sub in submissions:
            if sub.get("status_display") != "Accepted":
                continue

            title_slug = sub.get("title_slug") or sub.get("title", "unknown").lower().replace(" ", "-")
            lang = sub.get("lang", "txt")
            ext = EXTENSION_MAP.get(lang, lang)
            code = sub.get("code")

            prob_dir = OUTPUT_DIR / title_slug
            prob_dir.mkdir(parents=True, exist_ok=True)

            code_file = prob_dir / f"solution.{ext}"
            if not code_file.exists():
                with open(code_file, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"  [+] Saved {title_slug} ({lang})")
                total_saved += 1

        if len(submissions) < limit:
            break

        offset += limit
        time.sleep(1)

    print(f"[✓] Sync complete! Saved {total_saved} new accepted submissions.")

if __name__ == "__main__":
    main()
