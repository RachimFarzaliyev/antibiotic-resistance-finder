# Codebase Architecture and Design: Antibiotic Resistance Gene Finder

**Source**: Antibiotic Resistance Gene Finder Python Implementation (`main.py`, `src/`, `tests/`)
**Date**: 2026-09-04
**Domain**: Bioinformatics Software Engineering, Sequence Screening Pipelines

---

## 1. System Overview

The **Antibiotic Resistance Gene Finder** is a modular Python command-line tool built on **Biopython** (`Bio.SeqIO`, `Bio.Align.PairwiseAligner`), **pandas**, and **matplotlib**. It screens a target bacterial genome against a reference database of antibiotic resistance genes using dynamic programming local alignment (Smith-Waterman style), filtering candidate resistance determinants using dual percent-identity and query-coverage thresholds.

---

## 2. Directory and Module Decomposition

```text
antibiotic-resistance-finder/
├── main.py                          # CLI orchestrator & argument parsing
├── src/
│   ├── sequence_loader.py           # FASTA I/O handling
│   ├── qc.py                        # Sequence composition & quality metrics
│   ├── alignment.py                 # Pairwise local sequence alignment
│   ├── gene_finder.py               # Candidate calling logic & metadata merging
│   └── reporting.py                 # Multi-format artifact generation (CSV, PNG, TXT)
├── tests/
│   └── test_basic.py                # Unit and integration test suite
└── data/
    ├── sample.fasta                 # Query bacterial genome
    ├── resistance_genes.fasta       # Reference resistance determinants
    └── resistance_metadata.csv      # Gene to antibiotic class & mechanism mapping
```

---

## 3. Module Specifications

### 3.1 `main.py` (CLI Orchestration)
- **Entry point**: `main.py:main()`
- **CLI Options**:
  - `--input` (required): Path to query bacterial genome FASTA.
  - `--database` (required): Path to reference resistance genes FASTA.
  - `--metadata` (required): Path to CSV mapping gene names to antibiotic class and mechanism.
  - `--output` (required): Path for exported results CSV.
  - `--min-identity` (optional, default `80.0`): Minimum percent identity for candidate detection.
  - `--min-coverage` (optional, default `70.0`): Minimum percent coverage for candidate detection.
  - `--figures-dir` (optional): Output directory for visual charts (default: `<output_dir>/figures`).
  - `--report` (optional): Output path for text analysis report (default: `<output_dir>/analysis_report.txt`).

### 3.2 `src/sequence_loader.py` (FASTA Parsing)
- Uses `Bio.SeqIO.parse()` to read multi-record FASTA files.
- `load_genome(fasta_path: str) -> SeqRecord`: Returns the first sequence record (emits warning if multi-contig).
- `load_reference_genes(fasta_path: str) -> List[SeqRecord]`: Loads all reference gene sequences.

### 3.3 `src/qc.py` (Genomic Quality Control)
- Evaluates nucleotide integrity and GC distribution prior to alignment.
- `GenomeStats` dataclass:
  - Sequence ID, total length (bp).
  - A, T, G, C base counts and percentages.
  - Ambiguous base count (e.g., non-ACGT characters: `N`, IUPAC degenerate codes).
  - GC content percentage ($100 \times \frac{G+C}{\text{length}}$).

### 3.4 `src/alignment.py` (Pairwise Local Alignment Engine)
- Uses `Bio.Align.PairwiseAligner` configured in local mode (`mode = "local"`).
- **Alignment Scoring Parameters**:
  - `match_score = 2.0`
  - `mismatch_score = -1.0`
  - `open_gap_score = -2.0`
  - `extend_gap_score = -0.5`
- **Output Metrics (`AlignmentResult`)**:
  - `percent_identity = (matches / aligned_length) * 100`
  - `coverage = (aligned_length / gene_length) * 100` (capped at 100%)
  - `alignment_score`: Dynamic programming optimal local alignment score.

### 3.5 `src/gene_finder.py` (Candidate Screening Logic)
- Encapsulates classification thresholds in `ThresholdConfig(min_identity, min_coverage)`.
- `screen_genome()`:
  - Iterates over reference genes, aligns each against the genome.
  - Evaluates:
    $$\text{is\_candidate} = (\text{percent\_identity} \ge \text{min\_identity}) \land (\text{coverage} \ge \text{min\_coverage})$$
  - Assigns status: `"CANDIDATE DETECTED"` or `"NOT DETECTED"`.
  - Merges metadata (`antibiotic_class`, `resistance_mechanism`).
  - Sorts results descending by detection status and percent identity.

### 3.6 `src/reporting.py` (Artifact Generation)
- `save_results_csv()`: Exports structured pandas DataFrame to CSV.
- `plot_base_composition()`: Bar chart of A, T, G, C frequencies.
- `plot_gc_content()`: Pie chart comparing GC vs AT content percentage.
- `plot_identity_coverage()`: Color-coded bar chart of candidate vs non-candidate identities.
- `generate_text_report()`: Plain-text comprehensive report with QC section, threshold details, candidate list, and clinical disclaimer.

---

## 4. Test Suite (`tests/test_basic.py`)
- Unit tests for:
  - `TestQC`: Ambiguous bases detection, GC content calculation.
  - `TestAlignment`: Exact identity matching, unrelated sequence low coverage.
  - `TestGeneFinderIntegration`: Full end-to-end integration run on demo synthetic data.
