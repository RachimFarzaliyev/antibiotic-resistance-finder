---
title: "Target Modification and Protection"
type: concept
tags:
  - mechanism
  - target-modification
  - cell-wall
  - pbp2a
  - peptidoglycan
last_updated: "2026-09-04"
aliases:
  - Target Modification
  - Target Protection
  - Target Replacement
---

# Target Modification and Protection

**Target Modification** is an AMR strategy wherein the structural receptor or enzyme targeted by an antimicrobial agent is altered, mutated, or structurally replaced, drastically diminishing drug binding affinity while preserving essential cellular functions.

## Major Molecular Strategies

### 1. Acquisition of Drug-Insensitive Functional Orthologs (Target Replacement)
Instead of mutating the native essential enzyme (which might compromise fitness), the bacterium acquires a mobile exogenous gene encoding an enzyme that performs the same biochemical step but fails to bind the drug:
- **PBP2a in MRSA**: Encoded by [[mecA]], PBP2a provides functional transpeptidase activity in bacterial cell wall assembly even when all native penicillin-binding proteins are blocked by beta-lactam antibiotics.

### 2. Precursor / Substrate Remodeling
Rather than altering an enzyme, the bacterium biochemically reprograms the chemical building blocks targeted by the antibiotic:
- **Peptidoglycan Precursor Alteration**: In glycopeptide resistance, the [[vanA]] operon synthesizes cell wall precursors terminating in **D-Ala-D-Lac** instead of canonical **D-Ala-D-Ala**. Because vancomycin specifically forms five hydrogen bonds with D-Ala-D-Ala, the D-Ala-D-Lac substitution reduces binding affinity ~1,000-fold due to the loss of a hydrogen bond donor and electrostatic repulsion.

### 3. Enzymatic Target Methylation & Mutations
- **Ribosomal Methylation**: `erm` (erythromycin ribosome methylation) enzymes methylate specific adenine residues (e.g., A2058) on 23S rRNA, blocking macrolide, lincosamide, and streptogramin B (MLSb) binding.
- **Chromosomal Point Mutations**: Substitutions in topoisomerase genes (`gyrA`, `parC`) abolishing fluoroquinolone binding.

## Representative Genes in Knowledge Base
- [[mecA]]: Alternative penicillin-binding protein 2a.
- [[vanA]]: D-Ala-D-Lac ligase replacing peptidoglycan terminal dipeptide.

## Related Pages
- Entities: [[mecA]], [[vanA]]
- Other Mechanisms: [[enzymatic-inactivation]], [[efflux-pumps]], [[bypass-mechanisms]]
- Synthesis: [[amr-mechanisms-overview]]
