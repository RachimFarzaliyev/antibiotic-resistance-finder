---
title: "sul1 (Sulfonamide Resistance Gene)"
type: entity
tags:
  - gene
  - sulfonamide
  - bypass
  - integron
  - dhps
last_updated: "2026-09-04"
aro_id: "ARO:3000420"
aliases:
  - sul1
  - DHPS-I
---

# `sul1` (Sulfonamide-Insensitive Dihydropteroate Synthase)

`sul1` confers resistance to synthetic sulfonamide antimicrobial agents and serves as a classic molecular hallmark of mobile Class 1 integrons.

## Molecular Profile
- **ARO Accession**: `ARO:3000420`
- **Gene Product**: Sulfonamide-resistant dihydropteroate synthase (type I DHPS)
- **Target Antibiotic Class**: Sulfonamides (sulfamethoxazole, sulfadiazine, sulfisoxazole)
- **Mechanism Category**: [[bypass-mechanisms]]

## Mechanism of Action
Sulfonamides are competitive structural analogs of *para*-aminobenzoic acid (PABA). They normally bind bacterial dihydropteroate synthase (FolP), competitively inhibiting the first committed step of de novo folic acid biosynthesis and arresting nucleotide synthesis.
- `sul1` encodes an **alternative, drug-insensitive DHPS enzyme**.
- This enzyme maintains sufficient catalytic affinity for natural substrate PABA and 6-hydroxymethyl-7,8-dihydropterin pyrophosphate, while exhibiting several orders of magnitude lower affinity for sulfonamide drug molecules.
- As a result, the bacterium bypasses the drug block and maintains uninterrupted folic acid and thymidine production.

## Genetic Context & Dissemination
- `sul1` is uniquely positioned within the **3'-conserved segment (3'-CS)** of **Class 1 integrons** alongside `qacEΔ1` (quaternary ammonium compound resistance).
- Because Class 1 integrons capture multi-drug cassette arrays (conferring resistance to beta-lactams, aminoglycosides, chloramphenicol), detection of `sul1` in a genome frequently serves as a surrogate marker for multi-drug resistant (MDR) horizontal gene transfer elements.

## Bioinformatic Detection
- Screened via [[pairwise-alignment-screening]].
- Sequence length: ~840 bp (~279 amino acids).
- Thresholds: Identity $\ge 80\%$, Coverage $\ge 70\%$.

## Related Pages
- Mechanism: [[bypass-mechanisms]]
- Database Reference: [[card-database]]
- Synthesis: [[amr-mechanisms-overview]]
- Source: [[card-amr-foundations-summary]]
