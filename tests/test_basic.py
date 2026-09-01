"""
Basic unit tests for the Antibiotic Resistance Gene Finder.
Run with: python -m pytest tests/ -v   (or: python -m unittest discover tests)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

from src.qc import compute_genome_stats
from src.alignment import align_gene_to_genome
from src.gene_finder import screen_genome, load_metadata, ThresholdConfig
from src.sequence_loader import load_genome, load_reference_genes

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


class TestQC(unittest.TestCase):
    def test_composition_and_gc(self):
        record = SeqRecord(Seq("ATGCATGC"), id="test")
        stats = compute_genome_stats(record)
        self.assertEqual(stats.length, 8)
        self.assertEqual(stats.count_a, 2)
        self.assertEqual(stats.count_t, 2)
        self.assertEqual(stats.count_g, 2)
        self.assertEqual(stats.count_c, 2)
        self.assertAlmostEqual(stats.gc_content, 50.0)
        self.assertEqual(stats.ambiguous_bases, 0)

    def test_ambiguous_bases(self):
        record = SeqRecord(Seq("ATGCNNRY"), id="test2")
        stats = compute_genome_stats(record)
        self.assertEqual(stats.ambiguous_bases, 4)


class TestAlignment(unittest.TestCase):
    def test_identical_sequence_full_identity(self):
        seq = "ATGCATGCATGCATGCATGC"
        result = align_gene_to_genome(seq, seq)
        self.assertGreaterEqual(result.percent_identity, 99.0)
        self.assertGreaterEqual(result.coverage, 99.0)

    def test_unrelated_sequence_low_coverage(self):
        # A short, low-complexity genome can still find a tiny local match
        # with high identity but very low coverage of the full gene length;
        # coverage (not identity alone) is what correctly flags this as
        # an unreliable/spurious hit.
        gene = "ATGCATGCATGCATGCATGCGGGCCCAAATTTGGGCCCAAATTT"
        genome = "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
        result = align_gene_to_genome(gene, genome)
        self.assertLess(result.coverage, 60.0)


class TestGeneFinderIntegration(unittest.TestCase):
    def test_full_pipeline_runs_on_demo_data(self):
        genome_record = load_genome(os.path.join(DATA_DIR, "sample.fasta"))
        reference_genes = load_reference_genes(
            os.path.join(DATA_DIR, "resistance_genes.fasta")
        )
        metadata_df = load_metadata(os.path.join(DATA_DIR, "resistance_metadata.csv"))
        thresholds = ThresholdConfig(min_identity=80.0, min_coverage=70.0)

        results_df = screen_genome(genome_record, reference_genes, metadata_df, thresholds)

        self.assertEqual(len(results_df), len(reference_genes))
        for col in [
            "gene_name",
            "antibiotic_class",
            "resistance_mechanism",
            "percent_identity",
            "coverage_pct",
            "alignment_score",
            "detection_status",
        ]:
            self.assertIn(col, results_df.columns)


if __name__ == "__main__":
    unittest.main()
