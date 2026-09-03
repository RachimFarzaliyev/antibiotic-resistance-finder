---
title: "Obsidian & LLM Wiki: Concept and Practical Guide"
type: concept
tags:
  - obsidian
  - workflow
  - llm-wiki
  - second-brain
last_updated: "2026-09-04"
aliases:
  - Obsidian LLM Wiki Guide
  - Obsidian Workflow
  - Obsidian Integration
---

# Obsidian & LLM Wiki: Concept and Practical Guide

The **LLM Wiki** is designed around a symbiotic relationship between a human researcher, an LLM coding agent, and **[Obsidian](https://obsidian.md/)**. In this workflow:
- **Obsidian** is your interactive IDE, knowledge viewer, and visual graph explorer.
- **The LLM Agent** is your tireless maintainer, researcher, compiler, and bookkeeper.
- **The Wiki (`wiki/`)** is the compounding, interlinked codebase of knowledge.

---

## 1. The Core Operating Model

Traditional RAG (Retrieval-Augmented Generation) systems treat documents as passive chunks to be searched at query time. The LLM must rediscover relationships from scratch on every prompt.

In contrast, the **LLM Wiki compiles knowledge ahead of time into a persistent, interlinked graph**:

```text
┌────────────────┐                     ┌───────────────────────────┐
│  Raw Sources   │                     │      Human Explorer       │
│    (raw/)      │                     │   (Browsing Obsidian)     │
└───────┬────────┘                     └─────────────▲─────────────┘
        │                                            │
        ▼ (Agent Ingests)                            ▼ (Questions & Exploration)
┌──────────────────────────────────────────────────────────────────┐
│                   Compounding LLM Wiki (wiki/)                   │
│  - Entities: Concrete genes, software, and databases             │
│  - Concepts: Biological mechanisms & computational algorithms     │
│  - Syntheses: Comparative matrices & evolving hypotheses         │
│  - Catalog & Log: index.md and log.md                            │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
                       ▲          ▼          ▲
                       │   LLM Coding Agent  │
                       └── (Agent Maintains) ┘
```

---

## 2. How Obsidian Supercharges the LLM Wiki

When you open this repository folder in Obsidian as a vault:

### 2.1 The Interactive Graph View
- Press **Ctrl + G** in Obsidian to open the **Graph View**.
- Every markdown note in `wiki/` becomes a node.
- Every `[[wikilink]]` becomes an edge connecting genes to mechanisms, software modules to algorithms, and syntheses to evidence.
- Hub nodes (like [[amr-mechanisms-overview]] or [[card-database]]) immediately stand out as central clustering points.
- Orphan pages (disconnected nodes) are visually apparent.

### 2.2 Bidirectional Linking and Backlinks
- In any page (e.g. [[blaTEM]]), open the **Backlinks** pane in Obsidian.
- Obsidian automatically shows every synthesis, source summary, and pipeline report that references `blaTEM`, even if the source note didn't explicitly track back.

### 2.3 Page Previews (Hover Cards)
- Hovering your cursor over any `[[wikilink]]` while holding **Ctrl** renders an instant, live popup preview of that entire note without navigating away from your current text.

---

## 3. Recommended Obsidian Plugins & Setups

### 3.1 Dataview (Dynamic Frontmatter Queries)
Because every page in this wiki includes structured YAML frontmatter (`type`, `tags`, `aro_id`, `last_updated`), you can write dynamic queries inside Obsidian notes:

```dataview
TABLE aro_id as "ARO ID", tags as "Tags", last_updated as "Updated"
FROM "wiki/entities"
WHERE type = "entity"
SORT file.name ASC
```

### 3.2 Obsidian Web Clipper (Instant Raw Ingestion)
- Install the official **Obsidian Web Clipper** browser extension.
- When reading a journal paper (PubMed, Nature, BioRxiv) or clinical guideline, click the clipper icon to download the article directly as a clean markdown file into `raw/`.
- Then prompt the agent: *"Ingest raw/<clipped_paper>.md"*.

### 3.3 Marp Plugin (In-Editor Presentation Decks)
- Install the **Marp** community plugin in Obsidian.
- Open [[amr-slide-deck|wiki/syntheses/amr-slide-deck.md]].
- Obsidian will render the markdown directly as interactive, slide-show presentation slides.

---

## 4. Daily Workflow: The Side-by-Side Setup

In practice, the most productive way to work:

1. **Left Half of Screen**: Obsidian open to this repository root.
2. **Right Half of Screen**: LLM agent chat interface.
3. **Action Cycle**:
   - **Ingest**: You drop a paper into `raw/` $\to$ tell agent to ingest $\to$ watch new entity and concept notes appear in Obsidian's file explorer.
   - **Explore**: You click through notes in Obsidian, follow links, check graph clusters, and notice gaps or contradictions.
   - **Query**: You ask the agent a subtle synthesis question $\to$ the agent retrieves evidence and compiles a new synthesis into `wiki/syntheses/` $\to$ Obsidian updates instantly.
   - **Audit**: You run `python tools/wiki_tool.py lint` to verify link health.

---

## Related Pages
- File Guide: [[complete-repository-file-guide]]
- Operating Contract: [[AGENTS.md]]
- Slide Deck: [[amr-slide-deck]]
- Catalog: [[index|wiki/index.md]]
