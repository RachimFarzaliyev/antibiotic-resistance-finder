---
title: "Comprehensive Antibiotic Resistance Database (CARD)"
type: entity
tags:
  - database
  - ontology
  - aro
  - bioinformatics
last_updated: "2026-09-04"
aliases:
  - CARD
  - ARO
  - CARD Database
---

# Comprehensive Antibiotic Resistance Database (CARD)

The **Comprehensive Antibiotic Resistance Database (CARD)** is an open-access biological resource developed at McMaster University that provides curated reference DNA/protein sequences and ontology classifications for antimicrobial resistance determinants.

## Core Capabilities & Ontology
- **Antibiotic Resistance Ontology (ARO)**: The central backbone of CARD. ARO is a controlled hierarchical vocabulary interconnecting:
  - Specific resistance genes (e.g., [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]).
  - Mechanisms of resistance (e.g., [[enzymatic-inactivation]], [[target-modification]], [[efflux-pumps]], [[bypass-mechanisms]]).
  - Drug classes and clinical targets.
- **Strict Curation**: High-confidence AMR determinants verified by peer-reviewed experimental literature.
- **RGI (Resistance Gene Identifier)**: Computational software providing BLAST and DIAMOND matching against CARD reference data.

## Role in Sequence Screening
When running bioinformatics screening (such as the pairwise alignment implemented in this repository via [[pairwise-alignment-screening]]), CARD serves as the authoritative gold-standard reference database for:
1. Canonical FASTA reference sequences.
2. Standardized ARO accession tags.
3. Functional mechanism classifications.

## Related Pages
- Concept: [[pairwise-alignment-screening]]
- Synthesis: [[amr-mechanisms-overview]]
- Genes: [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]
