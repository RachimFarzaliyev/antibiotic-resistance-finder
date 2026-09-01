"""
qc.py

Basic quality-control / composition statistics for a genome sequence.
"""

from dataclasses import dataclass
from Bio.SeqRecord import SeqRecord

VALID_BASES = ("A", "T", "G", "C")


@dataclass
class GenomeStats:
    record_id: str
    length: int
    count_a: int
    count_t: int
    count_g: int
    count_c: int
    ambiguous_bases: int
    gc_content: float

    def as_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "length_bp": self.length,
            "A_count": self.count_a,
            "T_count": self.count_t,
            "G_count": self.count_g,
            "C_count": self.count_c,
            "A_pct": round(100 * self.count_a / self.length, 3) if self.length else 0,
            "T_pct": round(100 * self.count_t / self.length, 3) if self.length else 0,
            "G_pct": round(100 * self.count_g / self.length, 3) if self.length else 0,
            "C_pct": round(100 * self.count_c / self.length, 3) if self.length else 0,
            "GC_content_pct": round(self.gc_content, 3),
            "ambiguous_bases": self.ambiguous_bases,
        }


def compute_genome_stats(record: SeqRecord) -> GenomeStats:
    """
    Compute genome length, base composition, GC content, and count of
    ambiguous (non-ACGT) bases (e.g. N and IUPAC ambiguity codes).
    """
    seq = str(record.seq).upper()
    length = len(seq)

    count_a = seq.count("A")
    count_t = seq.count("T")
    count_g = seq.count("G")
    count_c = seq.count("C")

    known = count_a + count_t + count_g + count_c
    ambiguous_bases = length - known

    gc_content = 100 * (count_g + count_c) / length if length else 0.0

    return GenomeStats(
        record_id=record.id,
        length=length,
        count_a=count_a,
        count_t=count_t,
        count_g=count_g,
        count_c=count_c,
        ambiguous_bases=ambiguous_bases,
        gc_content=gc_content,
    )
