---
title: "Biopython Library"
type: entity
tags:
  - software
  - library
  - python
  - biopython
last_updated: "2026-09-04"
aliases:
  - Biopython
  - Bio.SeqIO
  - Bio.Align
---

# Biopython Library

**Biopython** is an open-source collection of Python computational molecular biology tools and data structures. In this repository, Biopython serves as the core computational engine driving sequence parsing and pairwise local alignment.

## Core Modules Utilized in this Codebase

### 1. `Bio.SeqIO`
- **Purpose**: High-throughput reading and writing of biological file formats (FASTA, GenBank, FASTQ).
- **Implementation**: Used in `src/sequence_loader.py` to parse bacterial genome assemblies and multi-sequence reference FASTA files into `SeqRecord` objects containing sequence strings and accession identifiers.

### 2. `Bio.Align.PairwiseAligner`
- **Purpose**: Modern dynamic programming engine for global (Needleman-Wunsch) and local (Smith-Waterman) sequence alignments, replacing deprecated legacy modules (`Bio.pairwise2`).
- **Implementation**: Used in `src/alignment.py` configured with `mode = "local"` to identify optimal high-scoring segment pairs between reference resistance genes and target contigs.
- **Scoring Configuration**:
  - `match_score = 2.0`
  - `mismatch_score = -1.0`
  - `open_gap_score = -2.0`
  - `extend_gap_score = -0.5`

## Related Pages
- Tool Integration: [[amr-finder-pipeline]]
- Method: [[pairwise-alignment-screening]]
- Synthesis: [[pipeline-dataflow-and-architecture]]
- Source Summary: [[codebase-architecture-summary]]
