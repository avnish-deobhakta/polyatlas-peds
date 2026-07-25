# Revision figures (350 dpi TIFF for PEDS production)

Regenerated figure files for the PEDS revision. Every figure is provided as a
vector PDF and a 350 dpi RGB TIFF (LZW-compressed), matching PEDS production
requirements.

## Figure-generation scripts

Original figures (content unchanged from initial submission; TIFF output added):
- `make_figure1.py` -> figure1.pdf / figure1.tif  (forward-selection climb)
- `make_figure2.py` -> figure2.pdf / figure2.tif  (univariate feature importance)
- `make_figure3.py` -> figure3.pdf / figure3.tif  (model vs language-model performance comparison)
- `make_figure4.py` -> figure4.pdf / figure4.tif  (Model 1 coefficients)

New in revision:
- `make_figure5.py`  -> figure5_chen_validation.*  (Chen 2024 external validation,
  panels A/B/C). Reads `chen_fig5_merged.json` (resolved relative to the script location;
  it also searches ../chen_validation/ automatically).
- `make_figureS1.py` -> figureS1_feature_distributions.*  (distributions of all 20
  Figure-2 features across all retained train + validation + test sequences, n=141,204,
  by label).

## Data dependencies (important)

Scripts differ in what they require:

- `make_figure1.py` .. `make_figure4.py` — self-contained; summary values are inline.
- `make_figure5.py` — reads `chen_fig5_merged.json` (the common held-out test results
  produced by the canonical Chen validation notebook), resolving the path relative to the
  script location. No internet needed once that JSON exists.
- `make_figureS1.py` — **requires internet access** to load the NbBench PolyRx dataset
  from Hugging Face (`ZYMScott/polyreaction`); it computes features inline and needs
  no local CSVs or other modules. For a turnkey run, use
  `../chen_validation/make_figureS1_notebook.ipynb` (Colab, CPU, Run all).

## Notes

- Fonts: Liberation Sans / DejaVu Sans. Spines: top/right removed.
- TIFFs are flattened to RGB on a white background (no alpha channel).
