"""
gene_finder.py

Core logic for screening a bacterial genome against a reference database
of antibiotic resistance genes using pairwise alignment, and classifying
each gene as a "candidate" hit or "not detected" based on configurable
identity/coverage thresholds.

IMPORTANT: Results represent *candidate* resistance genes based on
sequence similarity only. They are NOT proof of clinical antibiotic
resistance, which depends on gene expression, regulation, host context,
and phenotypic testing.
"""

from dataclasses import dataclass
from typing import List
import pandas as pd

from Bio.SeqRecord import SeqRecord

from src.alignment import align_gene_to_genome


@dataclass
class ThresholdConfig:
    min_identity: float = 80.0   # percent identity threshold
    min_coverage: float = 70.0   # percent coverage threshold


def load_metadata(metadata_csv: str) -> pd.DataFrame:
    """Load gene metadata (antibiotic class, mechanism, etc.) from CSV."""
    df = pd.read_csv(metadata_csv)
    required_cols = {"gene_name", "antibiotic_class", "resistance_mechanism"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Metadata CSV missing required columns: {missing}")
    return df.set_index("gene_name")


def screen_genome(
    genome_record: SeqRecord,
    reference_genes: List[SeqRecord],
    metadata_df: pd.DataFrame,
    thresholds: ThresholdConfig,
) -> pd.DataFrame:
    """
    Align each reference resistance gene against the genome and build a
    results table with identity, coverage, alignment score, and a
    candidate detection status based on the given thresholds.
    """
    genome_seq = str(genome_record.seq)
    rows = []

    for gene_record in reference_genes:
        gene_name = gene_record.id
        result = align_gene_to_genome(str(gene_record.seq), genome_seq)

        is_candidate = (
            result.percent_identity >= thresholds.min_identity
            and result.coverage >= thresholds.min_coverage
        )
        status = "CANDIDATE DETECTED" if is_candidate else "NOT DETECTED"

        if gene_name in metadata_df.index:
            meta = metadata_df.loc[gene_name]
            antibiotic_class = meta["antibiotic_class"]
            mechanism = meta["resistance_mechanism"]
        else:
            antibiotic_class = "Unknown (no metadata entry)"
            mechanism = "Unknown (no metadata entry)"

        rows.append(
            {
                "gene_name": gene_name,
                "antibiotic_class": antibiotic_class,
                "resistance_mechanism": mechanism,
                "percent_identity": result.percent_identity,
                "coverage_pct": result.coverage,
                "alignment_score": result.alignment_score,
                "aligned_length_bp": result.aligned_length,
                "detection_status": status,
            }
        )

    results_df = pd.DataFrame(rows).sort_values(
        by=["detection_status", "percent_identity"], ascending=[True, False]
    ).reset_index(drop=True)
    return results_df
