PolyAtlas PEDS — Hand-crafted physicochemical features for nanobody polyreactivity prediction

Code and data for the manuscript:

Hand-crafted physicochemical features approach language-model performance for nanobody polyreactivity prediction.
Deobhakta A, Quiroz J, Jaipalli S, Rosen RB.
Protein Engineering, Design and Selection (PEDS-26-0067), under revision.

Correspondence: adeobhakta@nyee.edu


Summary

On the NbBench PolyRx benchmark, a logistic regression with 13 hand-crafted
physicochemical features from the three CDRs (14 trainable parameters) achieves
test AUROC 0.834 and AUPRC 0.836, placing it within the reported range of eleven
pretrained protein and antibody language models on both metrics. Convergent
analyses using a pre-specified literature feature set (AUROC 0.829) and
leave-NbBench-out feature selection (0.817) indicate this reflects a benchmark-level
property rather than benchmark-specific tuning. All ten top univariate predictors
are charge-related.

The approach transfers across species: applied with zero retraining to ~80,000
human antibodies (Chen et al. 2024, Tessier lab), the frozen nanobody model reaches
AUROC 0.780, rising to 0.892 when the feature family is recalibrated. Full-sequence
charge alone reaches AUROC 0.902, and 10 of 13 coefficient signs — including every
charge feature — are conserved across species.

Repository layout

polyatlas-peds/
  data/                 dataset construction / access notes
  notebooks/            feature computation + Results 3.1-3.7 (NbBench)
  models/               model1_coefficients.csv (with train means/stds)
  figures/              make_figure1..4.py (primary manuscript figures)
  figures_revision/     all 6 figures as vector PDF + 350 dpi TIFF, all scripts
  chen_validation/      external-validation analysis (Results 3.8, Figure 5):
                          chen_anarci_validation.ipynb  (Colab, CPU, Run all)
                          chen_harness.py               (feature code + CDR utils)
                          chen_anarci_results.json      (numeric results, n=79,999)
                          make_figure5.py, make_figureS1.py
                          README.md
  REPRODUCTION_GUIDE.docx   step-by-step guide to every result and figure
  requirements.txt
  LICENSE (MIT)

Reproducing the results

Primary benchmark (Sections 3.1-3.7, Tables, Figures 1-4): run the notebooks in
notebooks/ in order on the NbBench PolyRx data (Hugging Face ZYMScott/polyreaction).
All seeds are fixed (random_state=42, 500 bootstrap resamples).

External validation (Section 3.8, Figure 5): open
chen_validation/chen_anarci_validation.ipynb in Google Colab on a CPU runtime
and Run all (~10-15 min). The notebook installs ANARCI via pip, downloads the Chen
2024 data and the frozen Model 1 coefficients, annotates CDRs (IMGT), and reproduces
the three evaluation modes.

See REPRODUCTION_GUIDE.docx for full environment details, feature definitions, and
a per-figure script map.

Data and licenses


NbBench PolyRx: Hugging Face ZYMScott/polyreaction (labels trace to the
Harvey et al. 2022 synthetic-library assay).
Chen et al. 2024 (external validation): Tessier lab,
Tessier-Lab-UMich/Human_Ab_Polyreactivity (GitHub) / Zenodo record 14735846, MIT.
This repository: MIT license. Raw source libraries are not redistributed;
obtain them from the original sources.


Citation

Please cite the manuscript (PEDS, under revision) and the Zenodo archive
(concept DOI 10.5281/zenodo.19744597).
