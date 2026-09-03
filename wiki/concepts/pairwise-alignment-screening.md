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
In Python-based bioinformatics pipelines (such as `src/alignment.py` using `Bio.Align.PairwiseAligner`):
- **Local Alignment (Smith-Waterman style)**: Finds the optimal local region of similarity between a long query genome (e.g., 5 Mbp) and a short reference gene (e.g., 1 kbp).
- **Scoring Matrix**: Assigns positive rewards for matches and negative penalties for mismatches, open gaps, and gap extensions.

## Key Screening Metrics

### 1. Percent Identity
$$\text{Identity} = \frac{\text{Identical Matches}}{\text{Alignment Length}} \times 100$$
- Reflects the exact nucleotide concordance between query and reference.
- High identity indicates close phylogenetic relationship or true homology.
- Lower identity (<80%) often flags divergent gene families, distant paralogs, or false positives.

### 2. Query Coverage
$$\text{Coverage} = \frac{\text{Aligned Reference Length}}{\text{Total Reference Length}} \times 100$$
- Evaluates what portion of the reference gene is actually present in the query genome.
- Essential for distinguishing intact, full-length functional resistance genes from truncated fragments, pseudogenes, or partial transposon footprints.

### 3. Dual-Threshold Candidate Logic
A gene is classified as a **candidate resistance determinant** only when both thresholds are met:
- **Identity** $\ge \text{Threshold}$ (default: $80\%$)
- **Coverage** $\ge \text{Threshold}$ (default: $70\%$)

## Distinguishing Candidates vs. Phenotypes
Sequence homology alone does not guarantee active phenotypic resistance:
- Promoter mutations or insertions may silence transcription.
- Frameshifts or premature stop codons may render the protein non-functional.
- Phenotypic antimicrobial susceptibility testing (AST) remains the clinical gold standard.

## Related Pages
- Reference Genes: [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]
- Database: [[card-database]]
- Synthesis: [[amr-mechanisms-overview]]
