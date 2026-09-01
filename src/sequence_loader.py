"""
sequence_loader.py

Utilities for loading FASTA files (genome and reference gene database)
using Biopython's SeqIO.
"""

from typing import List
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def load_genome(fasta_path: str) -> SeqRecord:
    """
    Load a bacterial genome FASTA file and return the first record.

    If the file contains multiple contigs/records, only the first one
    is used and a warning is printed. For a typical undergraduate
    demo/single-contig genome this is sufficient.
    """
    with open(fasta_path) as handle:
        records = list(SeqIO.parse(handle, "fasta"))
    if not records:
        raise ValueError(f"No sequences found in genome FASTA: {fasta_path}")
    if len(records) > 1:
        print(
            f"[sequence_loader] Warning: {len(records)} records found in "
            f"{fasta_path}. Using only the first record: {records[0].id}"
        )
    return records[0]


def load_reference_genes(fasta_path: str) -> List[SeqRecord]:
    """
    Load the antibiotic resistance reference gene database FASTA file.
    Returns a list of SeqRecord objects, one per gene.
    """
    with open(fasta_path) as handle:
        records = list(SeqIO.parse(handle, "fasta"))
    if not records:
        raise ValueError(f"No sequences found in reference database: {fasta_path}")
    return records
