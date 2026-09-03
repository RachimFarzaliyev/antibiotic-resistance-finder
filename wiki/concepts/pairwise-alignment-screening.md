---
title: "Pairwise Alignment for AMR Gene Screening"
type: concept
tags:
  - bioinformatics
  - alignment
  - algorithms
  - biopython
last_updated: "2026-09-04"
aliases:
  - Pairwise Alignment Screening
  - Sequence Alignment
---

# Pairwise Alignment for AMR Gene Screening

**Pairwise Alignment** is the bioinformatic process of aligning a query sequence (e.g., an assembled bacterial genome or contig) against a curated reference sequence (e.g., a known resistance gene from the [[card-database|CARD database]]) to identify regions of sequence similarity.

## Computational Implementation
In the [[amr-finder-pipeline]] implementation (`src/alignment.py` leveraging [[biopython]]'s `Bio.Align.PairwiseAligner`):
- **Local Alignment (Smith-Waterman style)**: Finds the optimal local region of similarity between a long query genome (e.g., 5 Mbp) and a short reference gene (e.g., 1 kbp).
- **Affine-like Scoring Scheme**:
  - `mode = "local"`
  - `match_score = 2.0`: Reward for identical nucleotide matches.
  - `mismatch_score = -1.0`: Penalty for base substitutions.
  - `open_gap_score = -2.0`: Initial penalty to introduce an insertion/deletion.
  - `extend_gap_score = -0.5`: Penalty for each subsequent extension of an existing gap.

## Key Screening Metrics

### 1. Percent Identity
$$\text{Identity} = \frac{\text{Identical Matches}}{\text{Aligned Length}} \times 100$$
- Reflects base-by-base concordance across aligned blocks.
- High identity indicates close phylogenetic relationship or true homology.
- Lower identity (<80%) often flags divergent gene families, distant paralogs, or non-specific alignments.

### 2. Query Coverage
$$\text{Coverage} = \min\left(100.0, \frac{\text{Aligned Length}}{\text{Reference Gene Length}} \times 100\right)$$
- Evaluates what portion of the full reference resistance gene is aligned against the query genome.
- Crucial for distinguishing intact, full-length functional resistance genes from truncated fragments, pseudogenes, or partial transposon footprints.

### 3. Dual-Threshold Candidate Logic
Implemented in `src/gene_finder.py` via `ThresholdConfig`:
$$\text{Status} = \begin{cases} 
\text{"CANDIDATE DETECTED"} & \text{if } \text{Identity} \ge 80\% \land \text{Coverage} \ge 70\% \\ 
\text{"NOT DETECTED"} & \text{otherwise} 
\end{cases}$$

## Distinguishing Candidates vs. Phenotypes
Sequence homology alone does not guarantee active phenotypic resistance:
- Promoter mutations or insertions may silence transcription.
- Frameshifts or premature stop codons may render the protein non-functional.
- Phenotypic antimicrobial susceptibility testing (AST) remains the clinical gold standard.

## Related Pages
- Pipeline Tool: [[amr-finder-pipeline]]
- Toolkit: [[biopython]]
- Preceding Step: [[genomic-qc-metrics]]
- Architecture Synthesis: [[pipeline-dataflow-and-architecture]]
- Reference Genes: [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]
- Database: [[card-database]]
- Biological Synthesis: [[amr-mechanisms-overview]]
- Source Summary: [[codebase-architecture-summary]]
