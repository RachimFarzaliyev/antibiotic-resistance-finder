---
title: "Genomic Quality Control Metrics"
type: concept
tags:
  - qc
  - genomics
  - metrics
  - gc-content
last_updated: "2026-09-04"
aliases:
  - Genomic QC Metrics
  - Sequence Quality Control
  - Genome Statistics
---

# Genomic Quality Control Metrics

**Genomic Quality Control (QC)** encompasses computational analyses performed on input sequence files to evaluate nucleotide composition, sequence completeness, and base ambiguity prior to downstream alignment or annotation.

## Metrics Computed in `src/qc.py`

### 1. Sequence Length (bp)
- Measures total base pairs in the contig or genome assembly.
- Provides context on whether the input represents a complete circular chromosome, a plasmid, or an incomplete assembly contig.

### 2. Base Composition ($A, T, G, C$)
- Exact counts and percentages for adenine (A), thymine (T), guanine (G), and cytosine (C).
- Base frequencies reflect taxonomic signatures (e.g., AT-rich Firmicutes vs. GC-rich Actinobacteria).

### 3. GC Content Percentage
$$\text{GC\%} = \frac{\text{Count}(G) + \text{Count}(C)}{\text{Total Length}} \times 100$$
- Serves as a standard phylogenetic and taxonomic indicator. Deviations in GC content across specific genomic islands can also signal horizontal gene transfer (HGT) events where foreign resistance cassettes have integrated.

### 4. Ambiguous Base Count
- Calculates all non-canonical nucleotide characters:
  $$\text{Ambiguous} = \text{Length} - (\text{Count}(A) + \text{Count}(T) + \text{Count}(G) + \text{Count}(C))$$
- Identifies unresolved sequencing reads (such as `N` placeholders, or IUPAC degenerate symbols like `R`, `Y`, `S`, `W`, `K`, `M`).
- High ambiguous base counts alert researchers to poor sequence quality or assembly gaps that might disrupt gene detection.

## Visualization
The pipeline renders these metrics into visual plots in `src/reporting.py`:
- `base_composition.png`: Absolute nucleotide counts.
- `gc_content.png`: Proportional comparison of GC vs AT fractions.

## Related Pages
- Pipeline Implementation: [[amr-finder-pipeline]]
- Downstream Analysis: [[pairwise-alignment-screening]]
- Architecture Synthesis: [[pipeline-dataflow-and-architecture]]
- Source Summary: [[codebase-architecture-summary]]
