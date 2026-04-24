# PolyAtlas PEDS — Hand-crafted physicochemical features for nanobody polyreactivity prediction

Code and data for the manuscript:

**Hand-crafted physicochemical features approach pretrained language model performance for nanobody polyreactivity prediction on the NbBench benchmark.**
Deobhakta A, Quiroz J, Jaipalli S, Rosen RB. *Protein Engineering, Design and Selection*, submitted 2026.

Correspondence: `adeobhakta@nyee.edu`

---

## Summary

We show that a logistic regression with 13 hand-crafted physicochemical features of the three complementarity-determining regions (CDRs) achieves test AUROC 0.834 and test AUPRC 0.836 on the NbBench PolyRx benchmark, numerically exceeding 9 of 11 pretrained language models on AUROC and tying IgBert on AUPRC, with 14 trainable parameters versus 15M–650M backbone parameters for the language models.

The result holds under three convergent ablations: a pre-specified 21-feature model derived from Boughter et al. 2020 literature (AUROC 0.829), a leave-NbBench-out feature selection on three independent conventional antibody polyreactivity datasets (AUROC 0.817), and a zero-training CDR-H3 charge baseline (AUROC 0.726). All top-10 univariate predictors are charge-related.

---

## Repository layout

```
polyatlas-peds/
├── notebooks/      Seven notebooks that reproduce every paper number
├── figures/        PNGs and generation scripts for Figures 1–4
├── models/         Model 1 exact coefficients (13-feature CDR-only model)
└── data/           Instructions for obtaining NbBench PolyRx and the unified dataset
```

---

## Notebooks

Each notebook corresponds to specific sections of the paper. Run in order for a fresh reproduction.

| Notebook | Paper mapping |
|---|---|
| `01_harvey_ingestion.ipynb` | Methods §2.2. Ingests Harvey 2022 nanobody sequences; builds the unified dataframe combining Boughter 2020, Shehata 2019, Jain 2017, and Harvey 2022. |
| `02_charge_baseline.ipynb` | Results §3.1. Zero-training CDR-H3 net charge baseline on NbBench PolyRx: test AUROC 0.726 [0.720, 0.732], AUPRC 0.721. Also computes a trained 1-feature LR on the same feature (essentially identical, confirming no parameter advantage). |
| `03_feature_climb_full.ipynb` | Results §3.2; Figure 1. Forward selection climb on the full 52-feature catalog (MIN_GAIN=0.002) — stops at 7 features, test AUROC 0.826. Also produces the univariate feature-importance ranking used to generate Figure 2. |
| `04_feature_climb_extended.ipynb` | Results §3.3. Extended forward selection (MIN_GAIN=0.0005, up to 25 features) — reaches 16 features at test AUROC 0.836. Establishes the full-feature plateau used as a ceiling reference for Model 1. |
| `05_cdr_only_climb.ipynb` | Results §3.4. CDR-only variant of the forward selection, restricting to H1+H2+H3 features. Produces **Model 1** (13-feature CDR-only LR, test AUROC **0.834** [0.828, 0.839], AUPRC 0.836). Also runs the CDR-H3-only extreme (11 features, AUROC 0.754) and the full-feature replicate (16 features, AUROC 0.836). |
| `06_robustness_matrix.ipynb` | Results §3.5, §3.6; Table 2; Figure 3. Four-model × four-dataset robustness matrix with bootstrap 95% confidence intervals. Models 1–4 evaluated on NbBench test, Boughter 2020, Shehata 2019, Jain 2017. Produces Model 1 AUROC 0.834 [0.828, 0.839], Model 2 (Boughter pre-specified 21-feature) AUROC 0.829 [0.824, 0.834], Model 3 (leave-NbBench-out 12-feature) AUROC 0.817 [0.812, 0.823], Model 4 (H3-charge zero-training) AUROC 0.726 [0.720, 0.733]. |
| `07_model1_exact_metrics.ipynb` | Results §3.7; Figure 4. Model 1 exact standardized coefficients (saved to `models/model1_coefficients.csv`) and precision-recall metrics: precision at recall 0.80 = 0.779, precision at recall 0.95 = 0.643, top-5% lift 1.72×. |

---

## Reproducing the paper

### Prerequisites

- Python ≥ 3.10
- Google Colab with GPU (A100 or T4) recommended for notebook 01 (AbLang embedding) and notebook 02 (NbBench dataset loading). Notebooks 03–07 run on CPU in a few minutes each.
- A Google Drive mount at `/content/drive/MyDrive/PolyAtlas/` for intermediate outputs (or adjust `DRIVE_ROOT` in each notebook to a local path).

### Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Download the NbBench PolyRx dataset

See `data/README.md`. The NbBench PolyRx dataset is publicly hosted at Hugging Face (`ZYMScott/polyreaction`) and is loaded automatically by notebooks 02–07 via the `datasets` library.

### Step 3 — Obtain the four source datasets

Notebook 01 rebuilds the unified dataframe that combines Boughter 2020, Shehata 2019, Jain 2017, and Harvey 2022. See `data/README.md` for acquisition instructions for each source.

### Step 4 — Run notebooks in order

Each notebook saves its outputs to a versioned subdirectory under `/content/drive/MyDrive/PolyAtlas/` so downstream notebooks can load them. Runtime estimates are listed in the Purpose cell of each notebook.

---

## Using Model 1 on new sequences (no retraining)

If you just want to score a new VHH sequence with Model 1 without rerunning anything, `models/model1_coefficients.csv` contains the 13 standardized coefficients, per-feature training-set means and standard deviations, and the intercept. To score a sequence:

1. Extract CDR-H1, CDR-H2, CDR-H3 using ANARCI with IMGT numbering.
2. Compute the 13 features listed in the coefficient file from those CDRs (feature definitions: see the feature-building section shared by notebooks 03–07).
3. Standardize each feature: `(feature_value − train_mean) / train_std`.
4. Apply: `logit = intercept + Σ (coef × standardized_feature)`; `prob_polyreactive = 1 / (1 + exp(−logit))`.

For a turnkey inference pipeline, run `07_model1_exact_metrics.ipynb` — it fits the model fresh and exposes the full preprocessing pipeline as a reusable object.

---

## License

MIT (see `LICENSE`).

---

## Citation

If you use this code or Model 1 in your work, please cite:

```
Deobhakta A, Quiroz J, Jaipalli S, Rosen RB. Hand-crafted physicochemical features approach
pretrained language model performance for nanobody polyreactivity prediction on the
NbBench benchmark. Protein Engineering, Design and Selection, 2026.
```
