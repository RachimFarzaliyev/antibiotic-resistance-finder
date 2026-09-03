---
title: "Summary: Foundations of Antimicrobial Resistance Genes and Mechanisms"
type: source
tags:
  - raw-source
  - amr-foundations
  - card
last_updated: "2026-09-04"
raw_path: "raw/card_amr_foundations.md"
---

# Source Summary: Foundations of Antimicrobial Resistance Genes and Mechanisms

- **Source File**: `[[raw/card_amr_foundations.md]]`
- **Domain**: Antimicrobial Resistance (AMR) Genomics & Bioinformatics
- **Ingested Date**: 2026-09-04

## Executive Summary
This foundational document compiles authoritative data from the [[card-database|Comprehensive Antibiotic Resistance Database (CARD)]] and clinical microbiology literature. It defines the hierarchical [[card-database|ARO ontology]], classifies resistance into four primary biological mechanisms, provides reference profiles for five key resistance genes ([[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]]), and outlines bioinformatic principles for candidate screening via [[pairwise-alignment-screening|pairwise sequence alignment]].

## Key Claims & Conceptual Extractions

1. **CARD & ARO Architecture**:
   - The Antibiotic Resistance Ontology provides machine-readable identifiers linking sequences directly to phenotypes and mechanisms.
   - Mentioned: [[card-database]].

2. **Mechanism Taxonomy**:
   - **Enzymatic Inactivation**: [[enzymatic-inactivation]] (e.g., [[blaTEM]] hydrolyzing the beta-lactam core).
   - **Target Modification**: [[target-modification]] (e.g., [[mecA]] expressing low-affinity PBP2a; [[vanA]] reprogramming cell wall peptidoglycan from D-Ala-D-Ala to D-Ala-D-Lac).
   - **Efflux Pumps**: [[efflux-pumps]] (e.g., [[tetA]] proton-dependent MFS antiporter).
   - **Target Bypass**: [[bypass-mechanisms]] (e.g., [[sul1]] insensitive dihydropteroate synthase).

3. **Genomic Screening Heuristics**:
   - Sequence-based detection using [[pairwise-alignment-screening]] requires balancing **identity** (reflecting point mutations/divergence) and **coverage** (distinguishing complete functional genes from truncated pseudo-genes).

## Linked Entities & Concepts
- Entities: [[blaTEM]], [[mecA]], [[tetA]], [[sul1]], [[vanA]], [[card-database]]
- Concepts: [[enzymatic-inactivation]], [[target-modification]], [[efflux-pumps]], [[bypass-mechanisms]], [[pairwise-alignment-screening]]
- Syntheses: [[amr-mechanisms-overview]]
