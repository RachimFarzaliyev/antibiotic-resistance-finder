---
title: "tetA Efflux Pump"
type: entity
tags:
  - gene
  - tetracycline
  - efflux
  - mfs
  - gram-negative
last_updated: "2026-09-04"
aro_id: "ARO:3000165"
aliases:
  - tetA
  - TetA(A)
---

# `tetA` (Tetracycline Efflux Transporter)

`tetA` is a classic acquired resistance determinant conferring high-level resistance to first- and second-generation tetracyclines in Gram-negative bacteria.

## Molecular Profile
- **ARO Accession**: `ARO:3000165`
- **Gene Product**: TetA antiporter protein (~400 amino acids, 12 alpha-helical transmembrane segments)
- **Target Antibiotic Class**: Tetracyclines (tetracycline, chlortetracycline, oxytetracycline, doxycycline)
- **Mechanism Category**: [[efflux-pumps]]

## Mechanism of Action
Tetracyclines inhibit bacterial protein synthesis by reversibly binding to the 30S ribosomal subunit (interfering with aminoacyl-tRNA accommodation at the A-site).
- `tetA` functions as a **proton-dependent antiporter** within the **Major Facilitator Superfamily (MFS)**.
- It couples the energized export of a divalent metal cation-tetracycline chelate complex ($[\text{Me-tetracycline}]^+$) out of the cytoplasm with the stoichiometric import of a proton ($\text{H}^+$).
- This keeps intracellular tetracycline concentrations below the threshold required to saturate ribosomes.
- Note: Classic `tetA` does not effectively efflux glycylcyclines (tigecycline) or eravacycline due to bulky steric modifications at C9.

## Regulation & Genomic Context
- Expression is strictly repressed by the adjacent repressor `tetR`.
- Upon entering the cell, tetracycline binds TetR, triggering conformational release from the operator/promoter region and driving rapid transcription of both `tetA` and `tetR`.
- Highly mobile on broad-host-range plasmids (e.g., IncP, IncF) and transposons such as **Tn1721**.

## Bioinformatic Detection
- Screened via [[pairwise-alignment-screening]].
- Coding sequence: ~1,197 bp (~399 amino acids).
- Thresholds: Identity $\ge 80\%$, Coverage $\ge 70\%$.

## Related Pages
- Mechanism: [[efflux-pumps]]
- Database Reference: [[card-database]]
- Synthesis: [[amr-mechanisms-overview]]
- Source: [[card-amr-foundations-summary]]
