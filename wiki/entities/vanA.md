---
title: "vanA Ligase"
type: entity
tags:
  - gene
  - vancomycin
  - glycopeptide
  - vre
  - enterococcus
last_updated: "2026-09-04"
aro_id: "ARO:3000589"
aliases:
  - vanA
  - VanA ligase
---

# `vanA` (Vancomycin Resistance Ligase)

`vanA` is the principal catalytic gene mediating high-level, inducible resistance to glycopeptide antibiotics (vancomycin and teicoplanin) in **Vancomycin-Resistant *Enterococcus* (VRE)** and Vancomycin-Resistant *Staphylococcus aureus* (VRSA).

## Molecular Profile
- **ARO Accession**: `ARO:3000589`
- **Gene Product**: D-alanine--D-lactate ligase (VanA, ~343 amino acids)
- **Target Antibiotic Class**: Glycopeptides (vancomycin, teicoplanin)
- **Mechanism Category**: [[target-modification]]

## Mechanism of Action
Vancomycin binds via five key hydrogen bonds to the terminal **D-Ala-D-Ala** dipeptide of lipid II peptidoglycan precursors on the outer surface of the cytoplasmic membrane, sterically inhibiting transglycosylation and transpeptidation.
- `vanA` encodes an altered ligase with strict substrate specificity for synthesizing **D-alanyl-D-lactate (D-Ala-D-Lac)** rather than D-Ala-D-Ala.
- Replacing the terminal amide linkage (-NH-) with an ester bond (-O-) eliminates a pivotal hydrogen bond and introduces electrostatic repulsion, **reducing vancomycin binding affinity by ~1,000-fold**.
- The `vanA` operon functions in concert with accessory proteins:
  - `vanH`: Dehydrogenase converting pyruvate to D-lactate.
  - `vanX`: D,D-dipeptidase hydrolyzing normal host D-Ala-D-Ala precursors to ensure only modified D-Ala-D-Lac enters nascent peptidoglycan.
  - `vanR` / `vanS`: Two-component sensory regulatory system that induces transcription in response to extracellular glycopeptides.

## Clinical Relevance & Mobility
- Disseminated globally within the mobile transposon **Tn1546** (often carried on conjugative plasmids such as pIP501).
- Poses a major healthcare-associated infection threat (*Enterococcus faecium*, *Enterococcus faecalis*) and can be transferred conjugatively to MRSA, yielding VRSA.

## Bioinformatic Detection
- Screened via [[pairwise-alignment-screening]].
- Coding sequence: ~1,032 bp (~343 amino acids).
- Thresholds: Identity $\ge 80\%$, Coverage $\ge 70\%$.

## Related Pages
- Mechanism: [[target-modification]]
- Database Reference: [[card-database]]
- Syntheses: [[amr-mechanisms-overview]], [[mecA-vs-vanA-resistance-comparison]]
- Source: [[card-amr-foundations-summary]]
