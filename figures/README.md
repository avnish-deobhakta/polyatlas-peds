# Figures

The four manuscript figures and their generation scripts.

## Contents

| File | Purpose | Paper reference |
|---|---|---|
| `figure1_climb.png` / `figure1.pdf` + `make_figure1.py` | Forward-selection climb trajectories for the full, CDR-only, and CDR-H3-only candidate pools, plotted as validation AUROC by number of features, with final test AUROC annotated. | Figure 1; Results §3.2 |
| `figure2_univariate.png` / `figure2.pdf` + `make_figure2.py` | Ranked univariate feature importances (top 25), colored by property category (charge / hydrophobicity / length). All ten top-ranked features are charge-related. | Figure 2; Results §3.3 |
| `figure3_comparison.png` / `figure3.pdf` + `make_figure3.py` | Two-panel comparison: (A) test AUROC and (B) test AUPRC of our four hand-crafted-feature models vs. all 11 NbBench pretrained language models, with parameter counts annotated in panel A to highlight efficiency. Rows sorted by AUROC (same order in both panels). | Figure 3; Results §3.4 |
| `figure4_coefficients.png` / `figure4.pdf` + `make_figure4.py` | Model 1's 13 standardized coefficients sorted by magnitude, colored by sign (red = predicts polyreactive, blue = predicts non-polyreactive). | Figure 4; Results §3.5 |

## Regenerating the figures

Each script is self-contained — the underlying data (climb steps, comparison rows, coefficients) is hard-coded directly from the notebook outputs, so no notebook runs or data files are required.

```bash
python make_figure1.py
python make_figure2.py
python make_figure3.py
python make_figure4.py
```

Each script writes both a PNG (300 DPI) and a PDF (vector) to this directory. Outputs are written relative to the script's own location, so the scripts are portable and can be run from any working directory. Fonts use `Liberation Sans` (metric-compatible with Arial and available on most Linux distributions); change `font.family` to `Arial` or `Helvetica` if running on a system where those are installed.

## Relationship to notebooks

If you want to rerun the full analysis from scratch and regenerate the numbers that feed these figures, rerun the source notebooks in order:

- Figure 1 data ← `notebooks/05_cdr_only_climb.ipynb` (climb logs and final test AUROCs)
- Figure 2 data ← `notebooks/03_feature_climb_full.ipynb` (univariate feature importance table)
- Figure 3 data ← `notebooks/06_robustness_matrix.ipynb` (NbBench Table 10 AUROC/AUPRC + our four models ranking)
- Figure 4 data ← `notebooks/07_model1_exact_metrics.ipynb` and `models/model1_coefficients.csv`
