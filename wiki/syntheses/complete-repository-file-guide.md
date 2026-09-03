---
title: "Complete Repository File & Architecture Guide"
type: synthesis
tags:
  - documentation
  - codebase
  - file-reference
  - architecture
last_updated: "2026-09-04"
aliases:
  - Complete Repository File Guide
  - File Reference
---

# Complete Repository File & Architecture Guide

This comprehensive reference documents every file, script, data table, and configuration asset across the **Antibiotic Resistance Gene Finder & LLM Wiki** repository.

---

## 1. Directory Tree Overview

```text
antibiotic-resistance-finder/
├── AGENTS.md                                # LLM Wiki schema and agent operational contract
├── README.md                                # Project overview, quickstart, and disclaimer
├── requirements.txt                         # Python dependencies
├── .gitignore                               # Git ignore patterns (including Obsidian & results)
├── main.py                                  # CLI orchestrator & entry point
├── src/                                     # Core application source code
│   ├── sequence_loader.py                   # FASTA sequence loading via Biopython
│   ├── qc.py                                # Sequence quality control & base statistics
│   ├── alignment.py                         # Local pairwise sequence alignment engine
│   ├── gene_finder.py                       # Threshold filtering & candidate gene calling
│   └── reporting.py                         # CSV, Matplotlib figure, and report generation
├── tests/
│   └── test_basic.py                        # Automated unit and integration test suite
├── data/                                    # Input genomic and reference datasets
│   ├── sample.fasta                         # Synthetic demo query bacterial genome
│   ├── resistance_genes.fasta               # Synthetic demo reference resistance genes
│   └── resistance_metadata.csv              # Gene to antibiotic class & CARD ARO metadata
├── results/                                 # Generated pipeline outputs
│   ├── results.csv                          # Tabular alignment & detection output
│   ├── analysis_report.txt                  # Full text report with wiki cross-references
│   └── figures/                             # Visual analysis plots
│       ├── base_composition.png             # A/T/G/C base count bar chart
│       ├── gc_content.png                   # GC vs AT content percentage pie chart
│       └── identity_by_gene.png             # Candidate identity bar chart
├── tools/
│   └── wiki_tool.py                         # LLM Wiki maintenance CLI (lint, stats, search, marp)
├── raw/                                     # Layer 1: Immutable raw source documents
│   ├── README.md                            # Ingestion guidelines and immutability rules
│   ├── card_amr_foundations.md              # Curated CARD ontology & biological reference
│   └── codebase_architecture.md             # Codebase technical architecture specification
└── wiki/                                    # Layer 2: LLM-maintained persistent wiki
    ├── index.md                             # Content catalog with category links & 1-line summaries
    ├── log.md                               # Append-only chronological audit log
    ├── entities/                            # Entity definitions (genes, databases, software)
    │   ├── blaTEM.md                        # Class A beta-lactamase (ARO:3000186)
    │   ├── mecA.md                          # PBP2a transpeptidase in MRSA (ARO:3000617)
    │   ├── tetA.md                          # MFS tetracycline efflux pump (ARO:3000165)
    │   ├── sul1.md                          # Insensitive DHPS in integrons (ARO:3000420)
    │   ├── vanA.md                          # D-Ala-D-Lac dipeptide ligase in VRE (ARO:3000589)
    │   ├── card-database.md                 # CARD knowledgebase & ARO ontology
    │   ├── amr-finder-pipeline.md           # CLI screening tool system entity
    │   └── biopython.md                     # Biopython library data structures & modules
    ├── concepts/                            # Scientific & algorithmic principles
    │   ├── enzymatic-inactivation.md        # Beta-lactamase hydrolysis, transferases
    │   ├── target-modification.md           # PBP2a, peptidoglycan remodeling, methylation
    │   ├── efflux-pumps.md                  # MFS, RND, proton-dependent transport
    │   ├── bypass-mechanisms.md             # Antimetabolite bypass in folate pathway
    │   ├── pairwise-alignment-screening.md  # Local alignment scoring & dual-threshold logic
    │   ├── genomic-qc-metrics.md            # Nucleotide counts, GC%, ambiguous base metrics
    │   └── obsidian-llm-wiki-guide.md       # Obsidian workflow, graph navigation & LLM pair programming
    ├── syntheses/                           # Cross-cutting comparative analyses
    │   ├── amr-mechanisms-overview.md       # Matrix comparing 4 primary AMR mechanisms
    │   ├── mecA-vs-vanA-resistance-comparison.md # Deep dive on MRSA vs VRE target modification
    │   ├── pipeline-dataflow-and-architecture.md # End-to-end dataflow and module contracts
    │   ├── complete-repository-file-guide.md     # This comprehensive file guide
    │   └── amr-slide-deck.md                # Presentation-ready Marp slide deck
    └── sources/                             # Per-source summaries linking to raw/
        ├── card-amr-foundations-summary.md  # Summary of raw/card_amr_foundations.md
        └── codebase-architecture-summary.md # Summary of raw/codebase_architecture.md
```

---

## 2. Detailed File Specifications

### 2.1 Project Roots & Configuration

#### `README.md`
- **Purpose**: Primary documentation for GitHub and repository visitors.
- **Contents**: Project summary, educational disclaimer, demo synthetic sequence notice, installation instructions, usage examples, and pipeline explanation.

#### `requirements.txt`
- **Purpose**: Declares Python package dependencies with pinned versions.
- **Packages**:
  - `biopython==1.83`: Core sequence I/O and local pairwise alignment.
  - `pandas==2.2.0`: DataFrames for tabular alignment results and metadata merging.
  - `matplotlib==3.8.2`: Rendering QC and candidate identity charts.

#### `.gitignore`
- **Purpose**: Excludes transient, environment-specific, and generated files from git tracking.
- **Rules**: Python bytecode (`__pycache__`), virtual environments (`.venv/`), test caches, output figures/CSVs (`results/*.csv`), and Obsidian vault state directories (`.obsidian/`, `*.trash/`).

#### `AGENTS.md`
- **Purpose**: The foundational **Schema & Operating Contract** governing how LLM agents interact with the repository.
- **Rules**: Defines the 3 layers (Raw, Wiki, Schema), immutability of `raw/`, and step-by-step procedures for the three core workflows: **Ingest**, **Query**, and **Lint**.

---

### 2.2 Application Pipeline (`main.py` & `src/`)

#### `main.py`
- **Role**: Command-line interface and workflow coordinator.
- **Key Function**: `main()`
- **CLI Options**:
  - `--input`: Path to target bacterial genome FASTA.
  - `--database`: Path to reference resistance genes FASTA.
  - `--metadata`: Path to metadata CSV mapping genes to class and mechanism.
  - `--output`: Path for results CSV.
  - `--min-identity`: Identity threshold percentage (default: `80.0`).
  - `--min-coverage`: Coverage threshold percentage (default: `70.0`).
  - `--figures-dir`: Directory for generated PNG charts.
  - `--report`: Path for plain-text analysis report.
  - `--wiki-links`: Toggles Obsidian `[[wikilink]]` cross-references in output reports (auto-enabled if `wiki/` exists).

#### `src/sequence_loader.py`
- **Role**: FASTA file parsing using [[biopython]]'s `Bio.SeqIO`.
- **Functions**:
  - `load_genome(fasta_path)`: Reads query genome, extracts the primary contig, and emits warnings for multi-record files.
  - `load_reference_genes(fasta_path)`: Parses and returns a list of `SeqRecord` objects for all reference genes.

#### `src/qc.py`
- **Role**: Genomic quality control and composition profiling.
- **Data Structure**: `GenomeStats(record_id, length, count_a, count_t, count_g, count_c, ambiguous_bases, gc_content)`
- **Key Function**: `compute_genome_stats(record)`: Evaluates length, exact base frequencies, GC percentage, and non-canonical/ambiguous nucleotides.

#### `src/alignment.py`
- **Role**: Pairwise sequence alignment engine.
- **Data Structure**: `AlignmentResult(gene_name, percent_identity, coverage, alignment_score, aligned_length)`
- **Key Functions**:
  - `_build_aligner()`: Initializes `Bio.Align.PairwiseAligner` in local mode (`match=2.0`, `mismatch=-1.0`, `gap_open=-2.0`, `gap_extend=-0.5`).
  - `align_gene_to_genome(gene_seq, genome_seq)`: Executes local alignment, walks aligned blocks, and computes percent identity and query coverage.
  - `_aligned_strings(alignment)`: Extracts gapped string representations from alignment blocks.

#### `src/gene_finder.py`
- **Role**: Candidate screening logic and metadata joining.
- **Data Structure**: `ThresholdConfig(min_identity, min_coverage)`
- **Key Functions**:
  - `load_metadata(metadata_csv)`: Reads CSV and indexes by `gene_name`.
  - `screen_genome(...)`: Aligns each reference gene, applies dual threshold filters, tags hits with `"CANDIDATE DETECTED"` or `"NOT DETECTED"`, merges metadata, and sorts descending.

#### `src/reporting.py`
- **Role**: Multi-format artifact generation.
- **Key Functions**:
  - `save_results_csv(results_df, output_path)`: Exports tabular CSV.
  - `plot_base_composition(stats, figures_dir)`: Generates bar chart of nucleotide counts.
  - `plot_gc_content(stats, figures_dir)`: Generates pie chart of GC vs AT content.
  - `plot_identity_coverage(results_df, figures_dir)`: Generates color-coded candidate bar chart.
  - `generate_text_report(...)`: Compiles comprehensive plain-text summary report with QC statistics, candidate lists, full results table, and dynamic wiki cross-references.

---

### 2.3 Automated Testing (`tests/`)

#### `tests/test_basic.py`
- **Role**: Automated test suite executing via `unittest` or `pytest`.
- **Test Classes**:
  - `TestQC`: Validates composition arithmetic, GC percentage, and ambiguous character detection (`ATGCNNRY` $\to 4$ ambiguous bases).
  - `TestAlignment`: Asserts 100% identity on identical sequences and verifies that low-complexity decoy sequences fail the coverage threshold.
  - `TestGeneFinderIntegration`: End-to-end integration test verifying that demo data produces valid tabular results with all expected schema columns.

---

### 2.4 Data Files (`data/`)

#### `data/sample.fasta`
- **Role**: Synthetic demo query genome fragment.
- **Profile**: 2,840 bp nucleotide sequence representing an assembled bacterial fragment containing synthetic regions homologous to `mecA` and `blaTEM`.

#### `data/resistance_genes.fasta`
- **Role**: Multi-record FASTA database containing 5 reference resistance determinants:
  - `blaTEM`: 240 bp synthetic reference.
  - `mecA`: 300 bp synthetic reference.
  - `tetA`: 210 bp synthetic reference.
  - `sul1`: 271 bp synthetic reference.
  - `vanA`: 260 bp synthetic reference.

#### `data/resistance_metadata.csv`
- **Role**: Curated reference table providing biological metadata for each gene:
  - `gene_name`: Target identifier matching FASTA headers.
  - `antibiotic_class`: Target drug family.
  - `resistance_mechanism`: Biological mode of action.
  - `reference_source`: Direct citations to CARD ARO accessions (`ARO:3000186`, `ARO:3000617`, etc.).

---

### 2.5 Wiki Tooling (`tools/`)

#### `tools/wiki_tool.py`
- **Role**: Cross-platform maintenance and utility CLI for the LLM Wiki.
- **Commands**:
  - `python tools/wiki_tool.py lint`: Audits wiki health (finds broken `[[wikilinks]]`, orphan pages with 0 inbound links, unindexed pages, and validates `log.md`).
  - `python tools/wiki_tool.py stats`: Reports summary metrics (counts of entities, concepts, syntheses, links, and log rows).
  - `python tools/wiki_tool.py search <query>`: Instant multi-file keyword search with line numbers and preview snippets.
  - `python tools/wiki_tool.py marp`: Generates a presentation-ready Marp markdown slide deck in `wiki/syntheses/amr-slide-deck.md`.

---

## Related Pages
- Architecture Synthesis: [[pipeline-dataflow-and-architecture]]
- Wiki Catalog: [[index|wiki/index.md]]
- Obsidian Integration: [[obsidian-llm-wiki-guide]]
- Operational Rules: [[AGENTS.md]]
