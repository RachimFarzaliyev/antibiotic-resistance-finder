#!/usr/bin/env python3
"""
wiki_tool.py - Management and linting CLI for the LLM Wiki.

Usage:
    python tools/wiki_tool.py lint
    python tools/wiki_tool.py stats
    python tools/wiki_tool.py search <query>
"""

import sys
import os
import re
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Resolve base directories
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
WIKI_DIR = REPO_ROOT / "wiki"
RAW_DIR = REPO_ROOT / "raw"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"


def get_all_wiki_files():
    """Returns a dict of filename_stem -> Path for all markdown files in wiki/ and known root docs."""
    files = {}
    if not WIKI_DIR.exists():
        return files
    for path in WIKI_DIR.rglob("*.md"):
        files[path.stem] = path
    # Also acknowledge special files
    files["AGENTS"] = REPO_ROOT / "AGENTS.md"
    if (REPO_ROOT / "README.md").exists():
        files["README"] = REPO_ROOT / "README.md"
    return files


def extract_wikilinks(text):
    """Extracts target names from [[target]] or [[target|label]] syntax, ignoring code blocks."""
    # Strip multiline code blocks
    text_clean = re.sub(r"```[\s\S]*?```", "", text)
    # Strip inline code
    text_clean = re.sub(r"`[^`\n]*?`", "", text_clean)

    # Matches [[target]] or [[target|label]]
    raw_matches = re.findall(r"\[\[(.*?)\]\]", text_clean)
    links = []
    for match in raw_matches:
        target = match.split("|")[0].strip()
        # strip any path prefixes if present, e.g. raw/file.md -> file or target
        if "/" in target:
            target = target.split("/")[-1]
        if target.endswith(".md"):
            target = target[:-3]
        if target:
            links.append(target)
    return links


def lint_wiki():
    """Audits the wiki for broken links, orphan pages, index completeness, and log formatting."""
    print("==========================================")
    print("[LINT] LLM Wiki Health Check & Linter")
    print("==========================================\n")

    wiki_files = get_all_wiki_files()
    raw_files = {p.stem: p for p in RAW_DIR.rglob("*.md")} if RAW_DIR.exists() else {}

    errors = []
    warnings = []

    # 1. Check index.md exists
    if not INDEX_FILE.exists():
        errors.append(f"Missing catalog index file: {INDEX_FILE}")
        index_content = ""
    else:
        index_content = INDEX_FILE.read_text(encoding="utf-8")

    # 2. Check log.md exists & format
    if not LOG_FILE.exists():
        errors.append(f"Missing log file: {LOG_FILE}")
    else:
        log_content = LOG_FILE.read_text(encoding="utf-8")
        log_entries = re.findall(r"^##\s+\[\d{4}-\d{2}-\d{2}\]\s+(\w+)\s+\|\s+(.+)$", log_content, re.MULTILINE)
        if not log_entries:
            warnings.append("No valid log entries matching '## [YYYY-MM-DD] <action> | <title>' in log.md")
        else:
            print(f"[OK] Log format: {len(log_entries)} valid chronological log entries found.")

    # Inbound link tracker: stem -> list of sources referencing it
    inbound_links = {stem: [] for stem in wiki_files}

    # 3. Check internal links across all wiki markdown files
    total_links = 0
    for stem, path in wiki_files.items():
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        links = extract_wikilinks(content)
        total_links += len(links)

        for target in links:
            # Check if target exists in wiki, raw, or root
            if target in wiki_files:
                inbound_links[target].append(stem)
            elif target in raw_files:
                pass  # valid reference to raw
            elif target == "AGENTS" or target == "README":
                pass
            else:
                errors.append(f"Broken link in '{path.relative_to(REPO_ROOT)}': [[{target}]] does not resolve.")

    # 4. Check index completeness
    # All files in entities/, concepts/, syntheses/, sources/ should be referenced in index.md
    subdirs_to_index = ["entities", "concepts", "syntheses", "sources"]
    unindexed_count = 0
    for subdir in subdirs_to_index:
        dir_path = WIKI_DIR / subdir
        if dir_path.exists():
            for p in dir_path.glob("*.md"):
                if f"[[{p.stem}" not in index_content:
                    warnings.append(f"Unindexed page: '{p.relative_to(REPO_ROOT)}' is not cataloged in wiki/index.md")
                    unindexed_count += 1

    if unindexed_count == 0:
        print("[OK] Index completeness: All entity, concept, synthesis, and source pages are listed in wiki/index.md.")

    # 5. Check for orphan pages (excluding index.md and log.md)
    orphan_pages = []
    for stem, path in wiki_files.items():
        if stem in ["index", "log", "AGENTS", "README"]:
            continue
        # An orphan is a page that has 0 inbound links from any page
        if len(inbound_links.get(stem, [])) == 0:
            orphan_pages.append(path.relative_to(REPO_ROOT))

    if orphan_pages:
        for op in orphan_pages:
            warnings.append(f"Orphan page (0 inbound links): {op}")
    else:
        print("[OK] Graph connectivity: 0 orphan pages detected. All pages are connected.")

    # Print summary
    print(f"\nAudit complete: Verified {len(wiki_files)} files and {total_links} links.")
    if warnings:
        print(f"\n[WARNING] Found {len(warnings)} issue(s):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\n[ERROR] Found {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("\n[SUCCESS] All checks passed! Wiki is clean, consistent, and well-linked.")
        return True


def show_stats():
    """Prints summary statistics about the wiki."""
    wiki_files = get_all_wiki_files()
    raw_files = list(RAW_DIR.rglob("*.md")) if RAW_DIR.exists() else []

    entities = list((WIKI_DIR / "entities").glob("*.md")) if (WIKI_DIR / "entities").exists() else []
    concepts = list((WIKI_DIR / "concepts").glob("*.md")) if (WIKI_DIR / "concepts").exists() else []
    syntheses = list((WIKI_DIR / "syntheses").glob("*.md")) if (WIKI_DIR / "syntheses").exists() else []
    sources = list((WIKI_DIR / "sources").glob("*.md")) if (WIKI_DIR / "sources").exists() else []

    total_links = 0
    for path in wiki_files.values():
        if path.exists():
            links = extract_wikilinks(path.read_text(encoding="utf-8"))
            total_links += len(links)

    log_count = 0
    if LOG_FILE.exists():
        log_count = len(re.findall(r"^##\s+\[\d{4}-\d{2}-\d{2}\]", LOG_FILE.read_text(encoding="utf-8"), re.MULTILINE))

    print("==========================================")
    print("[STATS] LLM Wiki Statistics")
    print("==========================================")
    print(f"  Immutable Raw Sources : {len(raw_files)}")
    print(f"  Entity Pages          : {len(entities)}")
    print(f"  Concept Pages         : {len(concepts)}")
    print(f"  Synthesis Pages       : {len(syntheses)}")
    print(f"  Source Summaries      : {len(sources)}")
    print(f"  Total Wiki Documents  : {len(wiki_files)}")
    print(f"  Total Inter-Page Links: {total_links}")
    print(f"  Chronological Log Rows: {log_count}")
    print("==========================================")


def search_wiki(query):
    """Performs instant keyword search across all markdown files in wiki/ and raw/."""
    if not query:
        print("Please specify a search query.")
        return

    print(f"[SEARCH] Searching wiki for '{query}'...\n")
    query_lower = query.lower()
    matches_found = 0

    search_dirs = [WIKI_DIR, RAW_DIR]
    for d in search_dirs:
        if not d.exists():
            continue
        for p in sorted(d.rglob("*.md")):
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue

            file_matches = []
            for i, line in enumerate(lines, 1):
                if query_lower in line.lower():
                    file_matches.append((i, line.strip()))

            if file_matches:
                matches_found += len(file_matches)
                rel_path = p.relative_to(REPO_ROOT)
                print(f"[FILE] {rel_path} ({len(file_matches)} matches):")
                for line_no, content in file_matches[:5]:
                    print(f"   L{line_no:03d}: {content}")
                if len(file_matches) > 5:
                    print(f"   ... and {len(file_matches) - 5} more matches in this file.")
                print()

    print(f"Done. Found {matches_found} total matches.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "lint":
        success = lint_wiki()
        sys.exit(0 if success else 1)
    elif cmd == "stats":
        show_stats()
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Error: Specify a query term: python tools/wiki_tool.py search <term>")
            sys.exit(1)
        search_wiki(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command: '{cmd}'")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
