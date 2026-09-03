---
title: "mecA (PBP2a)"
type: entity
tags:
  - gene
  - mrsa
  - staphylococcus
  - beta-lactam
  - pbp2a
last_updated: "2026-09-04"
aro_id: "ARO:3000617"
aliases:
  - mecA
  - PBP2a
  - PBP2'
---

# `mecA` (Penicillin-Binding Protein 2a)

`mecA` is the defining biomarker for **Methicillin-Resistant *Staphylococcus aureus* (MRSA)** and methicillin resistance in coagulase-negative staphylococci (CoNS).

## Molecular Profile
- **ARO Accession**: `ARO:3000617`
- **Gene Product**: Penicillin-Binding Protein 2a (PBP2a / PBP2'), a 78 kDa transpeptidase
- **Target Antibiotic Class**: Beta-lactams (anti-staphylococcal penicillins: methicillin, oxacillin, nafcillin, as well as cephalosporins and carbapenems)
- **Mechanism Category**: [[target-modification]]

## Mechanism of Action
Native staphylococcal PBPs (PBP1, PBP2, PBP3, PBP4) are responsible for cross-linking peptidoglycan during bacterial cell wall synthesis and are readily acylated and inactivated by beta-lactam antibiotics.
- `mecA` encodes **PBP2a**, an acquired, structurally divergent transpeptidase whose active site is closed by an allosteric gate.
- Beta-lactams bind to the active site of PBP2a with extremely low affinity, allowing transpeptidation and cell wall biosynthesis to proceed unimpeded even at high clinical drug concentrations.
- Only specialized fifth-generation cephalosporins (e.g., ceftaroline, ceftobiprole) can induce allosteric opening and inhibit PBP2a.

## Genomic Context & Mobility
- Carried on a mobile genetic element called the **Staphylococcal Cassette Chromosome *mec* (SCC*mec*)**.
- Regulated by sensor-transducer `mecR1` and repressor `mecI`, or cross-regulated by `blaR1`-`blaI`.
- Horizontal transfer across *Staphylococcus epidermidis* and *S. aureus* represents a primary driver of hospital-acquired (HA-MRSA) and community-acquired (CA-MRSA) infections.

## Bioinformatic Detection
- Screened via [[pairwise-alignment-screening]].
- Gene length: ~2,007 bp (~668 amino acids).
- Candidate screening requires high coverage ($\ge 70\%$) to differentiate intact SCC*mec*-borne `mecA` from non-functional cassette fragments.

## Related Pages
- Mechanism: [[target-modification]]
- Database Reference: [[card-database]]
- Synthesis: [[amr-mechanisms-overview]]
- Source: [[card-amr-foundations-summary]]
