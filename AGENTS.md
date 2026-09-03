# LLM Wiki Schema: Antibiotic Resistance & Bioinformatics

This file governs how LLM agents (e.g., Antigravity, Claude Code, OpenAI Codex) interact with, maintain, and expand this knowledge base. It establishes the rules, conventions, and operational workflows for a compounding, persistent personal wiki.

---

## 1. Core Architecture & Philosophy

The wiki sits between raw source documents and the user. It is not a static cache or a transient RAG index—it is an **actively maintained, persistent knowledge base** that compounds in value over time.

### The Three Layers
1. **Raw Sources (`raw/`)**:
   - **Immutable source of truth.** The agent reads from this directory but NEVER alters, overwrites, or deletes files here.
   - Contains downloaded papers, web clippings, CARD ontology exports, clinical guidelines, and sequence metadata.
2. **The Wiki (`wiki/`)**:
   - **Maintained entirely by the LLM.** The agent creates, edits, interlinks, and reorganizes pages here.
   - Uses standard Markdown with Obsidian-compatible `[[wikilinks]]` for graph connectivity.
   - Organized into:
     - `entities/`: Concrete nouns (genes, proteins, antibiotics, pathogens, databases).
     - `concepts/`: Abstract biological/computational principles (mechanisms, algorithms, metrics).
     - `syntheses/`: Comparative analyses, evolving syntheses, deep dives.
     - `sources/`: Per-source summaries and extracted evidence linking back to `raw/`.
     - `index.md`: Dynamic content catalog categorized by section with 1-line summaries.
     - `log.md`: Append-only chronological audit log.
3. **The Schema (`AGENTS.md`)**:
   - This document. Defines the contract, conventions, and procedures the agent must strictly follow.

---

## 2. Division of Responsibilities

- **Human**:
  - Curates and deposits source material into `raw/`.
  - Asks questions, requests syntheses, and explores associative trails.
  - Reviews updates in Obsidian or any markdown viewer.
- **LLM Agent**:
  - Performs all summarization, cross-referencing, linking, and bookkeeping.
  - Updates `wiki/index.md` on every change.
  - Records every action in `wiki/log.md`.
  - Flags contradictions between old notes and incoming evidence.

---

## 3. Workflows

### 3.1. Ingest Workflow
Triggered when the user says: *"Ingest `raw/<filename>`"* or drops a new source into `raw/`.

1. **Read & Analyze**:
   - Carefully read the raw source document in `raw/`.
2. **Create Source Summary**:
   - Create `wiki/sources/<source_stem>-summary.md`.
   - Include key claims, methodology, target genes/mechanisms studied, and references.
3. **Update / Create Entity Pages (`wiki/entities/`)**:
   - Identify every gene (e.g., `blaTEM`, `mecA`), antibiotic class (e.g., penicillins, glycopeptides), or database referenced.
   - If the entity page exists, integrate new findings, update evidence, and note contradictions.
   - If the entity page does not exist, create it following the Entity Template.
4. **Update / Create Concept Pages (`wiki/concepts/`)**:
   - Link biological mechanisms (e.g., `enzymatic-inactivation`, `efflux-pumps`) or computational methods (e.g., `pairwise-alignment-screening`).
5. **Cross-Link**:
   - Ensure bidirectional references using `[[PageName]]` links.
6. **Update Catalog (`wiki/index.md`)**:
   - Add entries for any new pages with a crisp 1-line summary under their respective category.
7. **Record in Log (`wiki/log.md`)**:
   - Append:
     ```markdown
     ## [YYYY-MM-DD] ingest | <Source Title>
     - **Source**: `raw/<filename>`
     - **Created**: `[[wiki/sources/...]]`, ...
     - **Updated**: `[[wiki/entities/...]]`, ...
     - **Summary**: <2-3 sentence executive takeaway>
     ```

---

### 3.2. Query Workflow
Triggered when the user asks a domain question (e.g., *"How does vanA compare to mecA in terms of resistance transfer?"*).

1. **Consult Index**:
   - Read `wiki/index.md` first to identify existing entity and concept pages relevant to the query.
2. **Retrieve & Synthesize**:
   - Read the relevant wiki pages (and underlying source summaries if deep citations are required).
   - Synthesize a comprehensive, rigorous answer with explicit links/citations to wiki pages.
3. **Compound Knowledge (Writeback)**:
   - If the query produces a novel comparison, taxonomy, or analytical synthesis, **file it back into `wiki/syntheses/<topic>.md`**.
   - Update `wiki/index.md` and append an entry to `wiki/log.md`:
     ```markdown
     ## [YYYY-MM-DD] query | <Question/Topic>
     - **Filed to**: `[[wiki/syntheses/<topic>]]`
     - **Synthesized from**: `[[...]]`, `[[...]]`
     ```

---

### 3.3. Lint Workflow
Triggered periodically or when requested via *"Lint the wiki"* or running `python tools/wiki_tool.py lint`.

Check for:
1. **Broken Links**: internal wikilinks that target non-existent files.
2. **Orphan Pages**: Pages with 0 inbound references from other pages or `index.md`.
3. **Unindexed Pages**: Markdown files present in `wiki/` but missing from `wiki/index.md`.
4. **Stale/Contradictory Claims**: Conflicting statements between older summaries and newer sources.
5. **Entity Stubs**: Frequently referenced entities that do not yet have dedicated pages.
6. **Log Format Integrity**: Ensure all entries in `wiki/log.md` match `## [YYYY-MM-DD] <operation> | <title>`.

Log the lint pass in `wiki/log.md`:
```markdown
## [YYYY-MM-DD] lint | Health check
- **Findings**: <Summary of broken links, orphans, or gaps resolved>
```

---

## 4. Frontmatter Standards

Every file in `wiki/` (except `index.md` and `log.md`) must start with YAML frontmatter:

```yaml
---
title: "blaTEM-1 Beta-Lactamase"
type: entity          # entity | concept | synthesis | source
tags:
  - gene
  - beta-lactam
  - enzymatic-inactivation
last_updated: "2026-09-04"
aro_id: "ARO:3000186" # Optional, domain-specific
aliases:
  - blaTEM
  - TEM-1
---
```

---

## 5. Tooling

- Use `python tools/wiki_tool.py lint` to validate link integrity and index consistency.
- Use `python tools/wiki_tool.py search "<keyword>"` for instant multi-page text matching.
- Use `python tools/wiki_tool.py stats` to inspect wiki metrics and growth.
