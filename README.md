# Antibiotic Resistance Gene Finder

An educational, GitHub-ready Python/Biopython project that screens a bacterial
genome (FASTA) against a small reference database of antibiotic resistance
genes using **pairwise sequence alignment** (not exact string matching), and
reports **candidate** resistance genes with identity, coverage, and alignment
score.

> **This is not a clinical diagnostic tool.** It reports sequence-similarity
> *candidates* only. Confirmed antibiotic resistance requires phenotypic
> laboratory testing.

## ⚠️ About the demo data

The files in `data/` are **synthetic, educational placeholder sequences**,
generated for this repo — they are **not** real bacterial genomes or real
`blaTEM`/`mecA`/`tetA`/`sul1`/`vanA` gene sequences. This keeps the repo
self-contained and license-free while still demonstrating a realistic
detection/non-detection outcome.

To run this on **real biological data**:
- Download real resistance gene sequences from the [CARD database](https://card.mcmaster.ca/)
  (Comprehensive Antibiotic Resistance Database) or [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/),
  e.g. search NCBI Nucleotide for accessions such as `blaTEM-1` beta-lactamase genes,
  `mecA` from *Staphylococcus aureus*, `tetA`, `sul1`, `vanA` from *Enterococcus*.
- Replace `data/resistance_genes.fasta` with real FASTA records (keep the
  `gene_name` in the FASTA header consistent with `resistance_metadata.csv`).
- Replace `data/sample.fasta` with a real assembled bacterial genome/contig FASTA.

## Project structure

```text
antibiotic-resistance-finder/
├── data/
│   ├── sample.fasta                 # demo genome (synthetic)
│   ├── resistance_genes.fasta       # demo reference genes (synthetic)
│   └── resistance_metadata.csv      # gene -> antibiotic class / mechanism
├── src/
│   ├── sequence_loader.py           # FASTA I/O (Biopython SeqIO)
│   ├── qc.py                        # genome length/composition/GC/ambiguous bases
│   ├── alignment.py                 # pairwise local alignment (Bio.Align)
│   ├── gene_finder.py               # screening logic + thresholds
│   └── reporting.py                 # CSV, matplotlib figures, text report
├── results/
│   └── figures/
├── tests/
│   └── test_basic.py
├── main.py                          # CLI entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py \
  --input data/sample.fasta \
  --database data/resistance_genes.fasta \
  --metadata data/resistance_metadata.csv \
  --output results/results.csv \
  --min-identity 80 \
  --min-coverage 70
```

Optional flags: `--figures-dir`, `--report` to customize output locations.
Run `python main.py --help` for all options.

## Running tests

```bash
python -m unittest discover tests -v
```

## What the program does

1. Loads the genome FASTA with Biopython and computes length, A/T/G/C
   composition, GC content, and count of ambiguous (non-ACGT) bases.
2. Loads a reference database of 5 resistance genes (`blaTEM`, `mecA`,
   `tetA`, `sul1`, `vanA`) plus metadata (antibiotic class, mechanism).
3. Locally aligns each reference gene against the genome using Biopython's
   `Bio.Align.PairwiseAligner` (Smith-Waterman-style local alignment).
4. Computes **percent identity**, **coverage**, and **alignment score** per gene.
5. Flags a gene as a **candidate** if it meets configurable
   `--min-identity` / `--min-coverage` thresholds; otherwise "NOT DETECTED".
6. Writes `results.csv`, three matplotlib figures, and a text analysis report.

## Output files

- `results/results.csv` — one row per reference gene with identity, coverage,
  alignment score, and detection status.
- `results/figures/base_composition.png` — bar chart of A/T/G/C counts.
- `results/figures/gc_content.png` — GC vs AT pie chart.
- `results/figures/identity_by_gene.png` — percent identity per gene, colored
  by detection status (green = candidate, red = not detected).
- `results/analysis_report.txt` — human-readable summary with the disclaimer,
  QC stats, thresholds used, and full results table.

## Interpreting the output

- **"CANDIDATE DETECTED"** means the reference gene sequence aligned to the
  genome above your chosen identity/coverage thresholds. This is a
  **hypothesis worth follow-up**, not a confirmed resistance phenotype.
- **"NOT DETECTED"** means no sufficiently similar region was found — it does
  not rule out resistance from unrelated genes or mechanisms not in this
  small demo database.
- Always cross-check hits against a full reference database (e.g. CARD) and
  ideally confirm functionally important genes with additional bioinformatics
  or wet-lab methods before drawing conclusions.
