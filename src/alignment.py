"""
alignment.py

Sequence alignment / similarity search between a reference gene and a
target genome sequence, using Biopython's pairwise local alignment
(Smith-Waterman style local alignment via Bio.Align.PairwiseAligner).

This is a simple, educational implementation: it locally aligns each
reference gene against the whole genome sequence. For very large real
genomes, a proper tool such as BLAST would be used instead; here we
keep dependencies minimal as required by the assignment.
"""

from dataclasses import dataclass
from Bio import Align


@dataclass
class AlignmentResult:
    gene_name: str
    percent_identity: float
    coverage: float
    alignment_score: float
    aligned_length: int


def _build_aligner() -> Align.PairwiseAligner:
    """
    Configure a local pairwise aligner with simple, reasonable scoring
    for nucleotide sequences (match/mismatch + linear gap penalties).
    """
    aligner = Align.PairwiseAligner()
    aligner.mode = "local"
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5
    return aligner


def align_gene_to_genome(gene_seq: str, genome_seq: str) -> AlignmentResult:
    """
    Perform a local pairwise alignment of a reference gene against the
    genome sequence and compute percent identity, coverage, and score.

    percent_identity = matches / aligned_length * 100
    coverage         = aligned_length / gene_length * 100
    """
    aligner = _build_aligner()
    gene_seq = str(gene_seq).upper()
    genome_seq = str(genome_seq).upper()

    alignments = aligner.align(gene_seq, genome_seq)
    best = alignments[0]  # highest-scoring local alignment
    score = best.score

    # Walk aligned blocks to count matches and aligned length.
    aligned_gene_str, aligned_genome_str = _aligned_strings(best)

    matches = 0
    aligned_length = 0
    for a, b in zip(aligned_gene_str, aligned_genome_str):
        if a == "-" or b == "-":
            aligned_length += 1
            continue
        aligned_length += 1
        if a == b:
            matches += 1

    percent_identity = (matches / aligned_length * 100) if aligned_length else 0.0
    coverage = (aligned_length / len(gene_seq) * 100) if len(gene_seq) else 0.0
    # Coverage can't exceed 100% conceptually (aligned_length counts gaps too)
    coverage = min(coverage, 100.0)

    return AlignmentResult(
        gene_name="",  # filled in by caller
        percent_identity=round(percent_identity, 2),
        coverage=round(coverage, 2),
        alignment_score=round(float(score), 2),
        aligned_length=aligned_length,
    )


def _aligned_strings(alignment):
    """
    Extract the aligned (gapped) representations of the two sequences
    from a Biopython Alignment object as plain strings.
    """
    aligned = alignment.aligned  # tuple of (target_blocks, query_blocks)
    seqA = alignment.target
    seqB = alignment.query

    a_blocks, b_blocks = aligned
    a_str_parts = []
    b_str_parts = []

    prev_a_end = a_blocks[0][0] if len(a_blocks) else 0
    prev_b_end = b_blocks[0][0] if len(b_blocks) else 0

    for (a_start, a_end), (b_start, b_end) in zip(a_blocks, b_blocks):
        # gap handling: insert '-' for any unaligned region between blocks
        gap_a = a_start - prev_a_end
        gap_b = b_start - prev_b_end
        gap_len = max(gap_a, gap_b)
        if gap_len > 0:
            a_str_parts.append(str(seqA[prev_a_end:a_start]).ljust(gap_len, "-"))
            b_str_parts.append(str(seqB[prev_b_end:b_start]).ljust(gap_len, "-"))

        a_str_parts.append(str(seqA[a_start:a_end]))
        b_str_parts.append(str(seqB[b_start:b_end]))

        prev_a_end = a_end
        prev_b_end = b_end

    return "".join(a_str_parts), "".join(b_str_parts)
