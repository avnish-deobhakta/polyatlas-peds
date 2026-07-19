# Chen 2024 external validation

External validation of the PolyAtlas hand-crafted physicochemical polyreactivity
model on an independent human antibody dataset (Chen et al. 2024, Cell Reports;
Tessier lab). This directory reproduces the cross-species transfer analysis added
in revision (Results Section 3.8, Figure 5, Supplementary Figure S1).

## What this shows

A 13-feature CDR logistic regression trained only on camelid nanobodies
(NbBench PolyRx) transfers to ~80,000 human antibodies:

| Evaluation | AUROC | AUPRC |
|---|---|---|
| Frozen NbBench Model 1 applied with zero retraining | 0.780 [0.777, 0.783] | 0.768 |
| Same 13-feature family refit on human data | 0.892 | 0.896 |
| Full 52-feature catalog refit (upper bound) | 0.975 | 0.975 |
| Full-sequence net charge alone (1 feature) | 0.902 | — |
| Full-sequence pI alone (1 feature) | 0.890 | — |

Ten of thirteen coefficient signs are conserved across species, including every
charge-related feature.

## Files

- `chen_anarci_validation.ipynb` — self-contained Google Colab notebook that installs
  ANARCI (pip route, no conda), downloads the Chen data and the frozen Model 1
  coefficients, annotates CDRs with ANARCI (IMGT scheme), computes the feature
  catalog, and runs the three evaluation modes. Runtime -> Run all on a CPU runtime.
- `chen_harness.py` — standalone feature-computation code (identical to the main
  repo's feature definitions) plus a lightweight regex CDR extractor used for local
  validation. The notebook uses ANARCI for the canonical annotations.
- `chen_anarci_results.json` — the numeric results (n=79,999), including the refit
  coefficients and the NbBench comparison coefficients used for Figure 5B.
- `make_figure5.py` — generates Figure 5 (transfer performance + coefficient
  conservation) at 350 dpi TIFF, vector PDF, and PNG.
- `make_figureS1.py` — generates Supplementary Figure S1 (feature distributions by
  polyreactivity label).

## Data source

Chen, H.-T. et al. (2024). Prediction and reduction of antibody polyreactivity /
non-specific binding. Cell Reports. Data deposited by the Tessier lab:
- GitHub: https://github.com/Tessier-Lab-UMich/Human_Ab_Polyreactivity
- Zenodo: https://doi.org/10.5281/zenodo.14735846 (record 14735846)
- License: MIT

The notebook downloads the data automatically from the GitHub release archive.
Raw sequence libraries are not redistributed here; obtain them from the source above.

## Reproduce

Open `chen_anarci_validation.ipynb` in Google Colab (CPU runtime) and Run all.
Total time ~10-15 minutes, most of it CDR annotation with ANARCI. The notebook
writes `chen_annotated.csv` and `chen_results.json` on completion.

To use more of the library, raise `N_PER_CLASS` in the annotation cell (up to the
full ~246k library).

## Notes

- CDR boundaries use the IMGT numbering scheme via ANARCI (through the `abnumber`
  wrapper). All physicochemical features are computed with the identical code used
  for the NbBench analysis in the parent repository.
- Chen 2024 antibodies are conventional human paired antibodies (VH + VL); we use
  the heavy-chain variable region (VH), consistent with Chen's finding that
  polyreactivity is governed primarily by the heavy-chain CDRs.
