---
marp: true
theme: default
paginate: true
header: "Antibiotic Resistance & Bioinformatics Wiki"
footer: "Compounding Knowledge Base"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
---

# Antimicrobial Resistance & Bioinformatics Screening

### Genomic Screening, Resistance Mechanisms & Compounding Wiki
**Author**: Rachim Farzaliyev
**Knowledge Base**: [[index|Wiki Catalog]]

---

# 1. Four Core Resistance Mechanisms

- **[[enzymatic-inactivation]]**: Direct hydrolytic degradation or group modification (e.g., [[blaTEM]] beta-lactamase).
- **[[target-modification]]**: Altering the molecular receptor or precursor to eliminate drug affinity (e.g., [[mecA]] PBP2a, [[vanA]] dipeptide ligase).
- **[[efflux-pumps]]**: Active transmembrane extrusion of drug molecules (e.g., [[tetA]] proton antiporter).
- **[[bypass-mechanisms]]**: Expression of alternative, drug-insensitive metabolic enzymes (e.g., [[sul1]] DHPS).

---

# 2. Reference Resistance Determinants

| Gene | Target Drug Class | Mechanism Category | Mobile Element |
| :--- | :--- | :--- | :--- |
| **[[blaTEM]]** | Penicillins, early cephalosporins | [[enzymatic-inactivation]] | Tn1/Tn2/Tn3, Plasmids |
| **[[mecA]]** | Methicillin, oxacillin | [[target-modification]] | SCC*mec* Cassette |
| **[[tetA]]** | Tetracyclines | [[efflux-pumps]] | Tn1721, IncP/F Plasmids |
| **[[sul1]]** | Sulfonamides | [[bypass-mechanisms]] | Class 1 Integron (3'-CS) |
| **[[vanA]]** | Glycopeptides (vancomycin) | [[target-modification]] | Tn1546 Transposon |

---

# 3. mecA vs. vanA: Target Modification Divergence

- **[[mecA]] (MRSA)**:
  - *Target Replacement*: Acquires low-affinity transpeptidase PBP2a.
  - Cell wall precursor chemistry remains canonical.
- **[[vanA]] (VRE)**:
  - *Precursor Remodeling*: Reprograms dipeptide terminus from D-Ala-D-Ala to D-Ala-D-Lac.
  - Loss of one critical hydrogen bond $	o$ **1,000-fold affinity drop**.
- **The VRSA Convergence**:
  - Tn1546 conjugative transfer from VRE to MRSA yields multi-resistant VRSA.
  - Reference: [[mecA-vs-vanA-resistance-comparison]].

---

# 4. Computational Screening Architecture

```text
Input FASTA ──► sequence_loader.py ──► qc.py (GenomeStats)
                      │
                      ▼
Reference DB ──► alignment.py (Bio.Align) ──► gene_finder.py ──► reporting.py
                      │                              │
                      └──────────────────────────────┴──► (CSV, Figures, Reports)
```

- **Algorithm**: Local Smith-Waterman via [[biopython]]'s `Bio.Align.PairwiseAligner`.
- **Thresholds**: $	ext{Identity} \ge 80\% \land 	ext{Coverage} \ge 70\%$.
- Reference: [[pipeline-dataflow-and-architecture]].

---

# 5. The LLM Wiki Pattern

- **Layer 1: Raw Sources (`raw/`)**: Immutable truth (CARD exports, literature).
- **Layer 2: The Wiki (`wiki/`)**: Compounding markdown graph with `[[wikilinks]]`.
- **Layer 3: The Schema (`AGENTS.md`)**: Operational rulebook for Ingest, Query, and Lint.
- **Bi-directional Integration**: Pipeline CLI cross-references wiki pages upon candidate detection.
