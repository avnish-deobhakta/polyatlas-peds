# Data sources

This repository does not redistribute raw data. Each dataset is obtained from its original licensed source, as documented below. Notebook 01 rebuilds the unified dataframe from these sources; Notebooks 02–07 load the NbBench PolyRx dataset directly from Hugging Face.

---

## 1. NbBench PolyRx (primary benchmark)

**Source:** `ZYMScott/polyreaction` on Hugging Face
**Paper:** Zhang Y, Tsuda K. *NbBench: Benchmarking Language Models for Comprehensive Nanobody Tasks.* arXiv:2505.02022, 2025.

**Published split sizes** (as released by NbBench): 141,474 rows total — train 101,854 / validation 14,613 / test 25,007.
**Sizes used in our analysis** (after excluding rows with empty gap-removed CDR-H3 annotations): 141,204 rows — train 101,673 / validation 14,576 / test 24,955. The 270 excluded rows (0.19 % of the benchmark) are addressed as a caveat in Section 2.1 and the Limitations section of the manuscript.

**Ground truth:** Harvey 2022 high/low PSR pool labels
**Split strategy:** MMseqs2 clustering at 70% sequence identity

No manual download is required. Notebooks 02–07 load this automatically:

```python
from datasets import load_dataset
ds = load_dataset("ZYMScott/polyreaction")
```

---

## 2. Harvey 2022 (nanobody FACS-PSR)

**Source:** `debbiemarkslab/nanobody-polyreactivity` on GitHub (Marks lab, Harvard)
**Paper:** Harvey EP, Shin J-E, et al. *An in silico method to assess antibody fragment polyreactivity.* Nat Commun 13, 7554 (2022).
**License:** MIT

Clone the repo and place the three CSVs where notebook 01 expects them:

```bash
git clone https://github.com/debbiemarkslab/nanobody-polyreactivity.git
# Then point notebook 01's input path at:
#   nanobody-polyreactivity/backend/app/experiments/high_polyreactivity_high_throughput.csv
#   nanobody-polyreactivity/backend/app/experiments/low_polyreactivity_high_throughput.csv
#   nanobody-polyreactivity/backend/app/experiments/low_throughput_polyspecificity_scores_w_exp.csv
```

---

## 3. Boughter 2020 (conventional Fab ELISA)

**Source:** Supplementary data of Boughter et al. 2020, plus the companion code repository
**Paper:** Boughter CT, Borowska MT, et al. *Biochemical patterns of antibody polyreactivity revealed through a bioinformatics-based analysis of CDR loops.* eLife 9, e61393 (2020).
**Files needed:** The 19 FASTA files (flu_fastaH/L, mouse_fastaH/L, plos_hiv_fastaH/L, gut_hiv_fastaH/L, nat_hiv_fastaH/L, nat_cntrl_fastaH/L, plus the corresponding non-polyreactive partner files) bundled with the paper's supplementary materials.

Save under `data/raw/boughter_2020/` with the filenames used in the original supplement. Notebook 01 will find and process them.

---

## 4. Shehata 2019 (conventional Fab PSR)

**Source:** Supplementary Table S2 of Shehata et al. 2019
**Paper:** Shehata L, Maurer DP, et al. *Affinity maturation enhances antibody specificity but compromises conformational stability.* Cell Reports 28(13), 3300–3308 (2019).
**File needed:** `mmc2.xlsx`

Save to `data/raw/shehata_2019/mmc2.xlsx`.

---

## 5. Jain 2017 (clinical-stage mAbs)

**Source:** Supplementary Dataset S1 of Jain et al. 2017
**Paper:** Jain T, Sun T, et al. *Biophysical properties of the clinical-stage antibody landscape.* PNAS 114(5), 944–949 (2017).
**File needed:** `pnas.1616408114.sd01.xlsx`

Save to `data/raw/jain_2017/`.
