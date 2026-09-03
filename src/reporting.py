"""
reporting.py

Generates output artifacts: results CSV, matplotlib figures, and a
plain-text analysis report summarizing genome QC and candidate
resistance gene detections.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for CLI/servers
import matplotlib.pyplot as plt

from src.qc import GenomeStats


def save_results_csv(results_df: pd.DataFrame, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    results_df.to_csv(output_path, index=False)


def plot_base_composition(stats: GenomeStats, figures_dir: str) -> str:
    os.makedirs(figures_dir, exist_ok=True)
    labels = ["A", "T", "G", "C"]
    counts = [stats.count_a, stats.count_t, stats.count_g, stats.count_c]

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(labels, counts, color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"])
    ax.set_title("Genome Base Composition")
    ax.set_ylabel("Base count")
    for i, c in enumerate(counts):
        ax.text(i, c, str(c), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()

    path = os.path.join(figures_dir, "base_composition.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_gc_content(stats: GenomeStats, figures_dir: str) -> str:
    os.makedirs(figures_dir, exist_ok=True)
    gc = stats.gc_content
    at = 100 - gc

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [gc, at],
        labels=["GC", "AT"],
        autopct="%1.1f%%",
        colors=["#55A868", "#4C72B0"],
        startangle=90,
    )
    ax.set_title("GC vs AT Content")
    fig.tight_layout()

    path = os.path.join(figures_dir, "gc_content.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_identity_coverage(results_df: pd.DataFrame, figures_dir: str) -> str:
    os.makedirs(figures_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [
        "#2ca02c" if s == "CANDIDATE DETECTED" else "#d62728"
        for s in results_df["detection_status"]
    ]
    ax.bar(results_df["gene_name"], results_df["percent_identity"], color=colors)
    ax.set_ylabel("Percent identity (%)")
    ax.set_title("Candidate Resistance Gene Identity by Gene")
    ax.set_ylim(0, 100)
    for i, (val, cov) in enumerate(
        zip(results_df["percent_identity"], results_df["coverage_pct"])
    ):
        ax.text(i, val + 1, f"{val:.1f}%", ha="center", fontsize=8)
    fig.tight_layout()

    path = os.path.join(figures_dir, "identity_by_gene.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def generate_text_report(
    stats: GenomeStats,
    results_df: pd.DataFrame,
    thresholds,
    report_path: str,
    include_wiki_links: bool = False,
) -> None:
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)

    detected = results_df[results_df["detection_status"] == "CANDIDATE DETECTED"]
    not_detected = results_df[results_df["detection_status"] == "NOT DETECTED"]

    lines = []
    lines.append("=" * 70)
    lines.append("ANTIBIOTIC RESISTANCE GENE FINDER - ANALYSIS REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append(
        "DISCLAIMER: This report identifies CANDIDATE antibiotic resistance "
        "genes based on sequence similarity to a reference database. It is "
        "an educational tool and does NOT constitute proof of clinical "
        "antibiotic resistance. Confirmatory laboratory / phenotypic "
        "susceptibility testing is required for any clinical conclusion."
    )
    lines.append("")
    lines.append("-" * 70)
    lines.append("1. GENOME QUALITY CONTROL SUMMARY")
    lines.append("-" * 70)
    lines.append(f"Sequence ID          : {stats.record_id}")
    lines.append(f"Genome length (bp)    : {stats.length}")
    lines.append(f"A count / percent     : {stats.count_a} ({100*stats.count_a/stats.length:.2f}%)")
    lines.append(f"T count / percent     : {stats.count_t} ({100*stats.count_t/stats.length:.2f}%)")
    lines.append(f"G count / percent     : {stats.count_g} ({100*stats.count_g/stats.length:.2f}%)")
    lines.append(f"C count / percent     : {stats.count_c} ({100*stats.count_c/stats.length:.2f}%)")
    lines.append(f"GC content            : {stats.gc_content:.2f}%")
    lines.append(f"Ambiguous bases (N..) : {stats.ambiguous_bases}")
    lines.append("")
    lines.append("-" * 70)
    lines.append("2. DETECTION THRESHOLDS USED")
    lines.append("-" * 70)
    lines.append(f"Minimum percent identity : {thresholds.min_identity}%")
    lines.append(f"Minimum coverage         : {thresholds.min_coverage}%")
    lines.append("")
    lines.append("-" * 70)
    lines.append("3. CANDIDATE RESISTANCE GENE SUMMARY")
    lines.append("-" * 70)
    lines.append(f"Genes screened        : {len(results_df)}")
    lines.append(f"Candidate genes found : {len(detected)}")
    lines.append(f"Genes not detected    : {len(not_detected)}")
    lines.append("")

    if len(detected) > 0:
        lines.append("Candidate genes detected:")
        for _, row in detected.iterrows():
            gene_label = f"{row['gene_name']} (Wiki: [[{row['gene_name']}]])" if include_wiki_links else row['gene_name']
            lines.append(
                f"  - {gene_label} | class: {row['antibiotic_class']} | "
                f"mechanism: {row['resistance_mechanism']} | "
                f"identity: {row['percent_identity']}% | "
                f"coverage: {row['coverage_pct']}% | "
                f"score: {row['alignment_score']}"
            )
    else:
        lines.append("No candidate resistance genes met the configured thresholds.")

    lines.append("")
    lines.append("-" * 70)
    lines.append("4. FULL RESULTS TABLE")
    lines.append("-" * 70)
    lines.append(results_df.to_string(index=False))
    lines.append("")

    if include_wiki_links and len(detected) > 0:
        lines.append("-" * 70)
        lines.append("5. WIKI KNOWLEDGE BASE CROSS-REFERENCES")
        lines.append("-" * 70)
        for _, row in detected.iterrows():
            g = row["gene_name"]
            lines.append(f"  - [[{g}]]: Detailed biological profile, genetic vehicles, and clinical context.")
        lines.append("  - [[amr-mechanisms-overview]]: Cross-cutting comparative resistance mechanisms.")
        lines.append("  - [[pairwise-alignment-screening]]: Algorithmic scoring and threshold methodology.")
        lines.append("  - Catalog: [[index|wiki/index.md]]")
        lines.append("")

    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
