# Revision figures (350 dpi TIFF for PEDS production)

Regenerated figure files for the PEDS revision. Every figure is provided as a
vector PDF and a 350 dpi RGB TIFF (LZW-compressed), matching PEDS production
requirements.

## Figure-generation scripts

Original figures (content unchanged from initial submission; TIFF output added):
- `make_figure1.py` -> figure1.pdf / figure1.tif  (forward-selection climb)
- `make_figure2.py` -> figure2.pdf / figure2.tif  (univariate feature importance)
- `make_figure3.py` -> figure3.pdf / figure3.tif  (model vs language-model ranking)
- `make_figure4.py` -> figure4.pdf / figure4.tif  (Model 1 coefficients)

New in revision:
- `make_figure5.py`  -> figure5_chen_validation.*  (Chen 2024 external validation,
  panels A/B/C). Reads `../chen_validation/chen_anarci_results.json`.
- `make_figureS1.py` -> figureS1_feature_distributions.*  (feature distributions by
  label on the NbBench validation set).

## Data dependencies (important)

Scripts differ in what they require:

- `make_figure1.py` .. `make_figure4.py` — self-contained; summary values are inline.
- `make_figure5.py` — reads `../chen_validation/chen_anarci_results.json` (produced
  by the Chen validation notebook). No internet needed once that JSON exists.
- `make_figureS1.py` — **requires internet access** to load the NbBench PolyRx dataset
  from Hugging Face (`ZYMScott/polyreaction`); it computes features inline and needs
  no local CSVs or other modules. For a turnkey run, use
  `../chen_validation/PolyAtlas_FigureS1_NbBench_colab.ipynb` (Colab, CPU, Run all).

## Notes

- Fonts: Liberation Sans / DejaVu Sans. Spines: top/right removed.
- TIFFs are flattened to RGB on a white background (no alpha channel).
