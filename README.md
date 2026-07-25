<h1 align="center">PolyAtlas — PEDS</h1>

<p align="center">
  <b>Hand-crafted physicochemical features approach language-model performance<br>for nanobody polyreactivity prediction</b>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://doi.org/10.5281/zenodo.19744597"><img src="https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.19744597-1682D4.svg" alt="Zenodo DOI"></a>
  <a href="https://huggingface.co/datasets/ZYMScott/polyreaction"><img src="https://img.shields.io/badge/data-NbBench%20PolyRx-yellow.svg" alt="Dataset"></a>
  <img src="https://img.shields.io/badge/status-under%20revision-orange.svg" alt="Status">
</p>

<p align="center">
  Deobhakta A, Quiroz J, Jaipalli S, Rosen RB &nbsp;·&nbsp;
  <i>Protein Engineering, Design and Selection</i> (PEDS-26-0067) &nbsp;·&nbsp;
  <a href="mailto:adeobhakta@nyee.edu">adeobhakta@nyee.edu</a>
</p>

---

## Overview

On the [**NbBench PolyRx**](https://huggingface.co/datasets/ZYMScott/polyreaction) benchmark, a logistic regression with **13 hand-crafted physicochemical features** from the three CDRs (14 trainable parameters) achieves test **AUROC 0.834** and **AUPRC 0.836** — within the reported range of eleven pretrained protein and antibody language models on both metrics. Convergent analyses using a pre-specified literature feature set (AUROC 0.829) and leave-NbBench-out selection (0.817) indicate a benchmark-level property rather than benchmark-specific tuning. All ten top univariate predictors are **charge-related**.

The frozen-model results **provide evidence of transfer across species and antibody formats**: applied with *zero retraining* to ~80,000 human antibodies ([Chen et al. 2024](https://doi.org/10.5281/zenodo.14735846), Tessier lab), the frozen nanobody model reaches AUROC 0.785 on a common held-out test set (0.781 when scored on all 79,999 annotated antibodies), rising to 0.892 when the feature family is recalibrated within Chen. Full-sequence charge alone reaches AUROC 0.903, and 10 of 13 coefficient signs — including *every* charge feature — are conserved across species.

## Key results

| Evaluation | AUROC | AUPRC |
| :--- | :---: | :---: |
| Model 1 — 13-feature CDR model (NbBench test) | **0.834** | **0.836** |
| Model 2 — literature features, no NbBench selection | 0.829 | 0.830 |
| Model 3 — leave-NbBench-out selection | 0.817 | 0.817 |
| **Cross-species transfer (external validation)** — frozen model, common test n=16,000 | 0.785 | 0.774 |
| &nbsp;&nbsp;&nbsp;&nbsp;(frozen model scored on all 79,999 annotated antibodies) | 0.781 | 0.768 |
| Within-Chen recalibration — feature family refit (exploratory upper bound) | 0.892 | 0.896 |
| Full-sequence charge alone (1 feature), common test | 0.903 | 0.892 |

## Repository layout

> **Note:** `figures_revision/` contains the final, current R1 figure set (Figures 1-5 and S1). The older `figures/` directory holds only the original Figures 1-4 and is retained for history.


| Path | Contents |
| :--- | :--- |
| [`notebooks/`](notebooks) | Feature computation + Results §3.1–3.7 (NbBench) |
| [`models/`](models) | `model1_coefficients.csv` (with training means / stds) |
| [`figures_revision/`](figures_revision) | **Final R1 figure set** — all 6 figures (1-5 + S1) as vector PDF and 350 dpi TIFF, plus every generation script. Use this directory. |
| [`figures/`](figures) | Original submission figures 1-4 (superseded by `figures_revision/`; retained for history) |
| [`chen_validation/`](chen_validation) | External-validation analysis (§3.8, Figure 5) |
| [`REPRODUCTION_GUIDE.docx`](REPRODUCTION_GUIDE.docx) | Step-by-step guide to every result and figure |

Inside [`chen_validation/`](chen_validation): a self-contained [Colab notebook](chen_validation/chen_anarci_validation.ipynb), the feature harness (`chen_harness.py`), numeric results (`chen_anarci_results.json`, `chen_fig5_common_test.json`, and `chen_fig5_merged.json`), and the Figure 5 / S1 scripts.

## Reproducing the results

**Primary benchmark** (§3.1–3.7, Tables, Figures 1–4) — run the notebooks in [`notebooks/`](notebooks) in order on the NbBench PolyRx data. All seeds are fixed (`random_state=42`, 500 bootstrap resamples).

**External validation** (§3.8, Figure 5) — open [`chen_validation/chen_anarci_validation.ipynb`](chen_validation/chen_anarci_validation.ipynb) in **Google Colab** on a **CPU** runtime and *Run all* (~15 min). This is the canonical notebook: it installs ANARCI via pip, downloads the Chen 2024 data and the checksum-verified Model 1 coefficients (pinned to the release tag), annotates CDRs (IMGT), and reproduces both the parenthetical all-79,999 frozen score and the common held-out test set (n=16,000) on which every Figure 5A,B bar is evaluated.

See [`REPRODUCTION_GUIDE.docx`](REPRODUCTION_GUIDE.docx) for the full environment, feature definitions, and per-figure script map.

## Data & licenses

- **NbBench PolyRx** — [Hugging Face `ZYMScott/polyreaction`](https://huggingface.co/datasets/ZYMScott/polyreaction) (labels trace to the [Harvey et al. 2022](https://doi.org/10.1038/s41467-022-35276-4) synthetic-library assay).
- **Chen et al. 2024** (external validation) — [`Tessier-Lab-UMich/Human_Ab_Polyreactivity`](https://github.com/Tessier-Lab-UMich/Human_Ab_Polyreactivity) · [Zenodo 14735846](https://doi.org/10.5281/zenodo.14735846) · MIT.
- **This repository** — [MIT License](LICENSE). Raw source libraries are not redistributed; obtain them from the original sources.

## Citation

If you use this code or data, please cite the manuscript (PEDS, under revision) and the Zenodo archive:

```bibtex
@software{polyatlas_peds,
  author  = {Deobhakta, Avnish and Quiroz, José and Jaipalli, Sujai and Rosen, Richard B.},
  title   = {PolyAtlas: Hand-crafted physicochemical features for nanobody polyreactivity prediction},
  year    = {2026},
  publisher = {Zenodo},
  doi     = {10.5281/zenodo.19744597},
  url     = {https://doi.org/10.5281/zenodo.19744597}
}
```
