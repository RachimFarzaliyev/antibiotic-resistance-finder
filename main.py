#!/usr/bin/env python3
"""
main.py

Command-line entry point for the Antibiotic Resistance Gene Finder.

Example:
    python main.py \\
        --input data/sample.fasta \\
        --database data/resistance_genes.fasta \\
        --metadata data/resistance_metadata.csv \\
        --output results/results.csv \\
        --min-identity 80 \\
        --min-coverage 70
"""

import argparse
import os
import sys

from src.sequence_loader import load_genome, load_reference_genes
from src.qc import compute_genome_stats
from src.gene_finder import load_metadata, screen_genome, ThresholdConfig
from src.reporting import (
    save_results_csv,
    plot_base_composition,
    plot_gc_content,
    plot_identity_coverage,
    generate_text_report,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Antibiotic Resistance Gene Finder: screens a bacterial genome "
            "against a reference database of resistance genes using "
            "sequence alignment. Educational tool; results are CANDIDATE "
            "genes, not confirmed clinical resistance."
        )
    )
    parser.add_argument(
        "--input", required=True, help="Path to bacterial genome FASTA file."
    )
    parser.add_argument(
        "--database",
        required=True,
        help="Path to reference resistance gene FASTA database.",
    )
    parser.add_argument(
        "--metadata",
        required=True,
        help="Path to CSV metadata for reference genes "
        "(gene_name, antibiotic_class, resistance_mechanism).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to write results CSV (e.g. results/results.csv).",
    )
    parser.add_argument(
        "--min-identity",
        type=float,
        default=80.0,
        help="Minimum percent identity to call a candidate gene (default: 80.0).",
    )
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=70.0,
        help="Minimum percent coverage to call a candidate gene (default: 70.0).",
    )
    parser.add_argument(
        "--figures-dir",
        default=None,
        help="Directory for output figures (default: <output_dir>/figures).",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Path for text analysis report (default: <output_dir>/analysis_report.txt).",
    )
    parser.add_argument(
        "--wiki-links",
        action=getattr(argparse, "BooleanOptionalAction", "store_true"),
        default=os.path.isdir("wiki"),
        help="Include Obsidian [[wikilinks]] cross-referencing wiki pages in reports and logs (default: auto if wiki/ exists).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    output_dir = os.path.dirname(args.output) or "."
    figures_dir = args.figures_dir or os.path.join(output_dir, "figures")
    report_path = args.report or os.path.join(output_dir, "analysis_report.txt")

    print(f"[main] Loading genome from: {args.input}")
    genome_record = load_genome(args.input)

    print(f"[main] Loading reference gene database from: {args.database}")
    reference_genes = load_reference_genes(args.database)

    print(f"[main] Loading gene metadata from: {args.metadata}")
    metadata_df = load_metadata(args.metadata)

    print("[main] Computing genome QC statistics...")
    stats = compute_genome_stats(genome_record)
    print(f"        Length: {stats.length} bp | GC content: {stats.gc_content:.2f}% "
          f"| Ambiguous bases: {stats.ambiguous_bases}")

    thresholds = ThresholdConfig(
        min_identity=args.min_identity, min_coverage=args.min_coverage
    )

    print(
        f"[main] Screening genome against {len(reference_genes)} reference genes "
        f"(min identity={thresholds.min_identity}%, min coverage={thresholds.min_coverage}%)..."
    )
    results_df = screen_genome(genome_record, reference_genes, metadata_df, thresholds)

    print(f"[main] Writing results CSV to: {args.output}")
    save_results_csv(results_df, args.output)

    print(f"[main] Generating figures in: {figures_dir}")
    plot_base_composition(stats, figures_dir)
    plot_gc_content(stats, figures_dir)
    plot_identity_coverage(results_df, figures_dir)

    print(f"[main] Writing analysis report to: {report_path}")
    generate_text_report(stats, results_df, thresholds, report_path, include_wiki_links=args.wiki_links)

    n_candidates = (results_df["detection_status"] == "CANDIDATE DETECTED").sum()
    print("\n[main] DONE.")
    print(
        f"[main] {n_candidates} candidate resistance gene(s) detected "
        f"out of {len(results_df)} screened."
    )
    if n_candidates > 0:
        for _, row in results_df[results_df["detection_status"] == "CANDIDATE DETECTED"].iterrows():
            ref = f" -> Wiki: [[{row['gene_name']}]]" if args.wiki_links else ""
            print(f"        * {row['gene_name']} ({row['percent_identity']}% id, {row['coverage_pct']}% cov){ref}")
    print(
        "[main] NOTE: Results are candidate genes based on sequence "
        "similarity only, not confirmed clinical resistance."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
