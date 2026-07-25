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
| Frozen Model 1, zero retraining (common test, n=16,000) | 0.785 [0.777, 0.791] | 0.774 |
| &nbsp;&nbsp;(frozen model scored on all 79,999 annotated antibodies) | 0.781 [0.777, 0.783] | 0.768 |
| Feature family refit within Chen (exploratory upper bound) | 0.892 | 0.896 |
| Full 52-feature catalog refit (upper bound) | 0.975 | 0.975 |
| Full-sequence net charge alone (1 feature), common test | 0.903 | 0.892 |
| Full-sequence pI alone (1 feature), common test | 0.892 | 0.886 |

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
- `chen_anarci_results.json` — the all-79,999 frozen/baseline results.
- `chen_fig5_common_test.json` / `chen_fig5_merged.json` — the common held-out test set
  results (n=16,000) that Figure 5A,B are drawn from, plus the coefficient values used
  for the coefficient-conservation panel (Figure 5C). `make_figure5.py` reads the merged file.
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
writes `chen_annotated.csv` and three JSON files on completion: `chen_anarci_results.json` (all-data frozen and baseline results), `chen_fig5_common_test.json` (common held-out test results), and `chen_fig5_merged.json` (the combined file read by make_figure5.py).

To use more of the library, raise `N_PER_CLASS` in the annotation cell (up to the
full ~246k library).

## Notes

- CDR boundaries use the IMGT numbering scheme via ANARCI (through the `abnumber`
  wrapper). All physicochemical features are computed with the identical code used
  for the NbBench analysis in the parent repository.
- Chen 2024 antibodies are conventional human paired antibodies (VH + VL); we use
  the heavy-chain variable region (VH), consistent with Chen's finding that
  polyreactivity is governed primarily by the heavy-chain CDRs.

## Reproducibility notes (v1.4.2)

- The notebooks download the fitted Model 1 coefficients pinned to the `v1.4.2`
  release tag (not the mutable `main` branch) and verify the file's SHA-256 checksum
  before use. A local copy, `model1_coefficients.csv`, is also included in this
  directory so the coefficients need not be downloaded; note that the Chen data itself
  is still downloaded from its public source (or must be supplied locally), so the
  notebook is not fully offline.
- The external-validation sample is 40,000 sequences per class (80,000 total),
  drawn with `random_state=42`. For Figure 5, this sample is split once into
  stratified 80/20 train/test partitions (`random_state=42`), and every Figure 5A,B
  condition is evaluated on the common held-out test set (n=16,000).
- `make_figure5.py` resolves its input JSON relative to its own location, so it runs
  correctly from any working directory.
