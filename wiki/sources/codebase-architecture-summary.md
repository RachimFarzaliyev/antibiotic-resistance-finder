---
title: "Summary: Antibiotic Resistance Gene Finder Codebase Architecture"
type: source
tags:
  - source-summary
  - codebase
  - architecture
  - biopython
last_updated: "2026-09-04"
raw_path: "raw/codebase_architecture.md"
---

# Source Summary: Antibiotic Resistance Gene Finder Codebase Architecture

- **Source File**: `[[codebase_architecture|raw/codebase_architecture.md]]`
- **Domain**: Bioinformatics Pipeline Engineering
- **Ingested Date**: 2026-09-04

## Executive Summary
This document summarizes the technical architecture, modular design, and computational workflows of the **Antibiotic Resistance Gene Finder** Python codebase. It establishes the contracts of the CLI orchestrator ([`main.py`](file:///c:/Users/Acer/Desktop/antibiotic-resistance-finder/main.py)), the FASTA sequence loader (`src/sequence_loader.py`), the quality control module (`src/qc.py`), the local pairwise sequence alignment engine (`src/alignment.py`), the threshold-based candidate gene caller (`src/gene_finder.py`), and the multi-format reporting module (`src/reporting.py`).

## Key Extractions & Specifications

1. **System & Pipeline Entity**:
   - Encapsulated in [[amr-finder-pipeline]], driven by [[biopython]] data structures (`SeqRecord`, `PairwiseAligner`).
2. **Quality Control & Composition**:
   - Formally conceptualized in [[genomic-qc-metrics]], computing GC content percentage, individual nucleotide distributions (A, T, G, C), and ambiguous (non-ACGT) base counts.
3. **Alignment Engine Parameters**:
   - Refined in [[pairwise-alignment-screening]]: Local Smith-Waterman alignment using affine-like gap penalties (`match=2.0`, `mismatch=-1.0`, `open_gap=-2.0`, `extend_gap=-0.5`).
4. **Candidate Decision Logic**:
   - Dual-threshold gate: requires both identity $\ge \text{min\_identity}$ (default 80%) and coverage $\ge \text{min\_coverage}$ (default 70%).
5. **Architectural Data Flow**:
   - Fully synthesized in [[pipeline-dataflow-and-architecture]], tracing input FASTA loading through QC, local alignment, candidate calling, and multi-format reporting (CSV, PNG, TXT).

## Linked Entities & Concepts
- Entities: [[amr-finder-pipeline]], [[biopython]], [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]
- Concepts: [[genomic-qc-metrics]], [[pairwise-alignment-screening]]
- Syntheses: [[pipeline-dataflow-and-architecture]], [[amr-mechanisms-overview]]
