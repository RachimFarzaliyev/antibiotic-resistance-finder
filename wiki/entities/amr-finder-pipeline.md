---
title: "Antibiotic Resistance Gene Finder Pipeline"
type: entity
tags:
  - software
  - pipeline
  - cli
  - python
last_updated: "2026-09-04"
aliases:
  - AMR Finder Pipeline
  - Gene Finder Tool
  - main.py
---

# Antibiotic Resistance Gene Finder Pipeline

The **Antibiotic Resistance Gene Finder Pipeline** is a modular Python command-line application designed to screen bacterial genomic sequences against curated reference databases to detect candidate antimicrobial resistance genes.

## Architectural Components

The pipeline is organized into five functional modules orchestrated by `main.py`:

```text
Input FASTA ───► sequence_loader.py ───► qc.py (GenomeStats)
                         │
                         ▼
Reference FASTA ─► alignment.py (Bio.Align) ──► gene_finder.py ──► reporting.py
                         │                              ▲               │
Metadata CSV ────────────┴──────────────────────────────┘               ▼
                                                                Results (CSV, PNG, TXT)
```

1. **CLI Orchestrator (`main.py`)**:
   - Parses arguments via `argparse`.
   - Coordinates sequential execution: loading, QC, alignment, threshold evaluation, and reporting.
2. **FASTA Loader (`src/sequence_loader.py`)**:
   - Interfaces with [[biopython]]'s `Bio.SeqIO` to stream query genomes and multi-gene reference databases.
3. **Quality Control (`src/qc.py`)**:
   - Generates [[genomic-qc-metrics]] (GC%, length, base counts, ambiguous base detection).
4. **Alignment Engine (`src/alignment.py`)**:
   - Executes local dynamic programming alignments using [[pairwise-alignment-screening]].
5. **Candidate Calling (`src/gene_finder.py`)**:
   - Evaluates dual thresholds: `min_identity` (default 80.0%) and `min_coverage` (default 70.0%).
6. **Reporting (`src/reporting.py`)**:
   - Exports `results.csv`, text summary report (`analysis_report.txt`), and matplotlib visualizations (`base_composition.png`, `gc_content.png`, `identity_by_gene.png`).

## CLI Interface & Execution Parameters

```bash
python main.py \
  --input data/sample.fasta \
  --database data/resistance_genes.fasta \
  --metadata data/resistance_metadata.csv \
  --output results/results.csv \
  --min-identity 80 \
  --min-coverage 70
```

## Related Pages
- Core Library: [[biopython]]
- Methods: [[pairwise-alignment-screening]], [[genomic-qc-metrics]]
- Architecture Synthesis: [[pipeline-dataflow-and-architecture]]
- Reference Genes: [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]
- Source Summary: [[codebase-architecture-summary]]
