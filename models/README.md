# Model 1 — 13-feature CDR-only logistic regression

This directory contains the exact fitted parameters of Model 1 so reviewers or users can apply the model without retraining.

---

## Files

- `model1_coefficients.csv` — the 13 standardized coefficients, the intercept, and the per-feature training-set means and standard deviations needed for standardization.

---

## Performance (NbBench PolyRx test set, n=24,955)

| Metric | Value | 95% CI (bootstrap, 500 resamples) |
|---|---|---|
| AUROC | 0.834 | [0.828, 0.839] |
| AUPRC | 0.836 | — |
| Precision at recall 0.80 | 0.779 | — |
| Precision at recall 0.95 | 0.643 | — |
| Top 5% precision | 0.925 | (lift 1.72×) |
| Top 10% precision | 0.917 | (lift 1.70×) |
| Top 20% precision | 0.890 | (lift 1.65×) |

Baseline positive-class rate (precision at recall 1.0): 0.539.

---

## Features and feature definitions

| Feature | Region | Description |
|---|---|---|
| H1_charge | CDR-H1 | Net charge at pH 7.4 (Arg+Lys+0.1·His − Asp−Glu) |
| H1_arom | CDR-H1 | Fraction of aromatic residues (F+W+Y) |
| H1_hphob | CDR-H1 | Mean Kyte–Doolittle hydrophobicity |
| H2_charge | CDR-H2 | Net charge at pH 7.4 |
| H2_len | CDR-H2 | Length in amino acids |
| H2_hphob_frac | CDR-H2 | Fraction of hydrophobic residues (A,V,I,L,M,F,W,Y,C) |
| H3_charge | CDR-H3 | Net charge at pH 7.4 |
| H3_abs_charge | CDR-H3 | Absolute value of net charge |
| H3_arom | CDR-H3 | Fraction of aromatic residues |
| H3_len | CDR-H3 | Length in amino acids |
| H3_neg_frac | CDR-H3 | Fraction of negatively charged residues (D+E) |
| H3_R | CDR-H3 | Fraction of arginine |
| H3_charge_dipole | CDR-H3 | Signed charge centroid × length (captures whether positive charge is at N- or C-terminus of the loop) |

CDRs are extracted using ANARCI with IMGT numbering. For exact feature-computation code, see §1 of any of notebooks 03–07 (they share one feature catalog).

---

## How to apply Model 1 to a new sequence

```python
import pandas as pd
import numpy as np

coefs = pd.read_csv("model1_coefficients.csv")
intercept = float(coefs.loc[coefs["feature"] == "_intercept", "standardized_coefficient"].iloc[0])
coefs = coefs[coefs["feature"] != "_intercept"]

def score(feature_vector):
    """feature_vector: dict mapping feature name -> raw (unstandardized) value."""
    logit = intercept
    for _, row in coefs.iterrows():
        raw = feature_vector[row["feature"]]
        z = (raw - row["train_mean"]) / row["train_std"]
        logit += row["standardized_coefficient"] * z
    return 1.0 / (1.0 + np.exp(-logit))
```

For a full turnkey inference pipeline including CDR extraction and feature computation, rerun `notebooks/07_model1_exact_metrics.ipynb` — it builds and exposes the full pipeline.

---

## Training details

- **Training set:** NbBench PolyRx train split (n = 101,854)
- **Feature selection:** Greedy forward selection on validation split (n = 14,576), CDR-only restriction, MIN_GAIN=0.0005, max 25 features (climb stopped at 13)
- **Classifier:** `sklearn.linear_model.LogisticRegression` with `class_weight='balanced'`, `random_state=42`, default L2 regularization (C=1.0)
- **Standardization:** `sklearn.preprocessing.StandardScaler` fit on training split only

Source notebook: `notebooks/05_cdr_only_climb.ipynb` (selection) and `notebooks/07_model1_exact_metrics.ipynb` (exact-coefficient dump).
