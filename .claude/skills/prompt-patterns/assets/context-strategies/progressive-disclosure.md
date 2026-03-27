---
name: Progressive Disclosure
category: context-strategies
applies_when:
  - generating-execution-agent
  - generating-research-agent
  - generating-coding-team
  - context-constrained
tags: [just-in-time, lazy-loading, metadata, exploration]
source: raw/context-engineering-blog.md
---

# Progressive Disclosure

## Core Principle

Rather than pre-loading all relevant data, agents maintain lightweight identifiers (file paths, stored queries, URLs) and dynamically load data into context at runtime using tools. This mirrors human cognition — people do not memorize entire corpuses but use external organization systems to retrieve information on demand.

## Pattern

**Lightweight identifiers over full content:**
- File paths instead of file contents
- Saved queries instead of query results
- URLs and bookmarks instead of full documents
- Database schema instead of row data

**Metadata as guidance signals:**
- File names hint at purpose (`test_utils.py` in `tests/` vs `src/core_logic/`)
- Folder hierarchies signal organization and ownership
- File sizes suggest complexity (large file = investigate deeper)
- Timestamps proxy relevance (recent = likely active)
- Naming conventions reveal intent without reading contents

**Incremental discovery:** Each interaction yields context informing the next decision. Agents assemble understanding layer by layer, maintaining only necessary working memory. Claude Code uses `head` and `tail` to analyze data without loading full objects. Glob and grep enable targeted retrieval without indexing.

## A-Team Application

When generating execution agents: equip them with exploration tools (Read, Grep, Glob, Bash) and instruct them to inspect metadata before loading full content. When generating coding teams: include rules that agents must use targeted file reads, never bulk-load directories. When generating research agents: instruct them to scan folder structures and file names first, then selectively deep-dive. Generated CLAUDE.md files must reference key documents via `@path/to/file` imports for pre-loaded norms, while leaving code-level context to just-in-time retrieval.
