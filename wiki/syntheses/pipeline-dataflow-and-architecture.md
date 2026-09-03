---
title: "Pipeline Dataflow and Software Architecture"
type: synthesis
tags:
  - architecture
  - pipeline
  - dataflow
  - bioinformatics
last_updated: "2026-09-04"
aliases:
  - Pipeline Dataflow and Architecture
  - Software Architecture Synthesis
---

# Pipeline Dataflow and Software Architecture

This synthesis traces the end-to-end lifecycle of genomic data through the [[amr-finder-pipeline]], mapping inputs, transformation stages, algorithmic steps, and output artifacts.

---

## 1. End-to-End Execution Flow

```text
[Input Files]
├── Query Genome (data/sample.fasta)
├── Reference Database (data/resistance_genes.fasta)
└── Resistance Metadata (data/resistance_metadata.csv)
                           │
                           ▼
                  [1. Ingestion Phase]
              src/sequence_loader.py (SeqIO)
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
 [Genome Record]                        [Reference Records]
       │                                       │
       ▼                                       │
[2. Quality Control]                           │
   src/qc.py                                   │
 (GenomeStats)                                 │
  - Length, GC%                                │
  - A/T/G/C counts                             │
  - Ambiguous bases                            │
       │                                       │
       ▼                                       ▼
 ┌───────────────────────────────────────────────────┐
 │       [3. Local Pairwise Alignment Engine]        │
 │              src/alignment.py                     │
 │          Bio.Align.PairwiseAligner                │
 │  - mode = "local"                                 │
 │  - match: +2.0, mismatch: -1.0                    │
 │  - gap open: -2.0, gap extend: -0.5               │
 └─────────────────────────┬─────────────────────────┘
                           │
                           ▼
         [4. Candidate Screening & Metadata Join]
                   src/gene_finder.py
        - Identity >= 80%  AND  Coverage >= 70%
        - Joins ARO metadata (class, mechanism)
                           │
                           ▼
              [5. Multi-Format Reporting]
                   src/reporting.py
  ├── CSV Table: results/results.csv
  ├── Figures: results/figures/
  │   ├── base_composition.png
  │   ├── gc_content.png
  │   └── identity_by_gene.png
  └── Clinical Summary: results/analysis_report.txt
```

---

## 2. Transformation Stages and Data Contracts

### Stage 1: Ingestion & Sequence Parsing
- **Module**: `src/sequence_loader.py` powered by [[biopython]].
- **Function**: `load_genome()` isolates the primary contig from FASTA; `load_reference_genes()` creates an array of reference determinants.
- **Fail-safe**: Verifies non-empty FASTA files; warns if a genome contains multiple unmerged contigs.

### Stage 2: Quality Control Evaluation
- **Module**: `src/qc.py`.
- **Concept**: [[genomic-qc-metrics]].
- **Contract**: Produces a `GenomeStats` instance detailing length, nucleotide frequencies, GC percentage, and non-canonical base counts.
- **Purpose**: Establishes confidence in the query sequence prior to computationally intensive alignment.

### Stage 3: Local Sequence Alignment
- **Module**: `src/alignment.py`.
- **Concept**: [[pairwise-alignment-screening]].
- **Contract**: Returns an `AlignmentResult` containing:
  - `percent_identity`: $\frac{\text{matches}}{\text{aligned\_length}} \times 100$
  - `coverage`: $\min\left(100.0, \frac{\text{aligned\_length}}{\text{gene\_length}} \times 100\right)$
  - `alignment_score`: Optimal local score via dynamic programming.

### Stage 4: Threshold Filtering and Metadata Enrichment
- **Module**: `src/gene_finder.py`.
- **Inputs**: Reference alignments, `data/resistance_metadata.csv` (mapping [[card-database|CARD ARO]] classifications), and `ThresholdConfig`.
- **Classification**:
  - `CANDIDATE DETECTED`: Meets both identity and coverage cutoffs.
  - `NOT DETECTED`: Below threshold.
- **Output**: Pandas DataFrame sorted descending by detection status and identity.

### Stage 5: Artifact Rendering
- **Module**: `src/reporting.py`.
- **Artifacts**:
  1. `results.csv`: Tabular output for downstream automated parsers.
  2. `base_composition.png` & `gc_content.png`: Visual QC breakdown.
  3. `identity_by_gene.png`: Comparative bar chart color-coded by detection status.
  4. `analysis_report.txt`: Standard text summary including educational disclaimer.

---

## 3. Computational Complexity and Scalability
- **Pairwise Alignment**: $O(N \times M)$ where $N$ is genome length (~5 Mbp) and $M$ is reference gene length (~1 kbp).
- **Educational Scope vs. Production**: While dynamic programming via `Bio.Align.PairwiseAligner` is ideal for exact, transparent scoring in small reference sets, massive genomic databases (e.g. screening 5,000 CARD genes) typically employ indexed seed-and-extend heuristics like BLAST or DIAMOND.

---

## Related Pages
- Core Pipeline Entity: [[amr-finder-pipeline]]
- Toolkit: [[biopython]]
- Methods: [[pairwise-alignment-screening]], [[genomic-qc-metrics]]
- Biological Synthesis: [[amr-mechanisms-overview]]
- Reference Genes: [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]
- Source Summary: [[codebase-architecture-summary]]
