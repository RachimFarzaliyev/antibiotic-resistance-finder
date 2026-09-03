---
title: "blaTEM Beta-Lactamase"
type: entity
tags:
  - gene
  - beta-lactam
  - beta-lactamase
  - enterobacteriaceae
last_updated: "2026-09-04"
aro_id: "ARO:3000186"
aliases:
  - blaTEM
  - blaTEM-1
  - TEM-1
---

# `blaTEM` (Beta-Lactamase TEM)

`blaTEM` is one of the most widely distributed plasmid-mediated beta-lactamase genes in Gram-negative bacteria, responsible for high-level resistance to penicillins and narrow-spectrum cephalosporins.

## Molecular Profile
- **ARO Accession**: `ARO:3000186` (TEM-1 beta-lactamase)
- **Molecular Class**: Ambler Class A serine beta-lactamase
- **Target Antibiotic Class**: Beta-lactams (Penicillins such as ampicillin, amoxicillin; first-generation cephalosporins)
- **Mechanism Category**: [[enzymatic-inactivation]]

## Mechanism of Action
`blaTEM` encodes a periplasmic enzyme that catalyzes the hydrolysis of the cyclic amide bond in the four-membered beta-lactam ring.
1. The catalytic serine residue (Ser70 in standard Ambler numbering) mounts a nucleophilic attack on the carbonyl carbon of the beta-lactam ring.
2. A covalent acyl-enzyme intermediate is formed.
3. Rapid deacylation via a conserved water molecule releases an open, biologically inert penicilloic acid derivative, preventing the drug from binding to bacterial Penicillin-Binding Proteins (PBPs).

## Clinical & Epidemiological Context
- First identified in *Escherichia coli* isolated from a patient named Temoniera in Greece (1965).
- Frequently harbored on mobile transposons such as **Tn1**, **Tn2**, and **Tn3**, and transmissible plasmids.
- Over 200 derivative variants (`blaTEM-2` to `blaTEM-200+`) exist, some evolving into Extended-Spectrum Beta-Lactamases (ESBLs) capable of hydrolyzing 3rd-generation cephalosporins (e.g., ceftriaxone, cefotaxime) or inhibitor-resistant TEMs (IRTs).

## Bioinformatic Detection
- Screened via [[pairwise-alignment-screening]].
- Typical reference length: ~861 bp (~286 amino acids).
- Candidate threshold: Identity $\ge 80\%$, Coverage $\ge 70\%$.

## Related Pages
- Mechanism: [[enzymatic-inactivation]]
- Database Reference: [[card-database]]
- Synthesis: [[amr-mechanisms-overview]]
- Source: [[card-amr-foundations-summary]]
