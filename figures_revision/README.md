# Revision figures (350 dpi TIFF for PEDS production)

Regenerated figure files for the PEDS revision. Every figure is provided as a
vector PDF and a 350 dpi RGB TIFF (LZW-compressed), matching PEDS production
requirements (350 dpi for colour/halftone; vector PDF also accepted).

## Figure-generation scripts

Original figures (content unchanged from initial submission; TIFF output added):
- `make_figure1.py` -> figure1.pdf / figure1.tif  (forward-selection climb)
- `make_figure2.py` -> figure2.pdf / figure2.tif  (univariate feature importance)
- `make_figure3.py` -> figure3.pdf / figure3.tif  (model vs language-model ranking)
- `make_figure4.py` -> figure4.pdf / figure4.tif  (Model 1 coefficients)

New in revision:
- `make_figure5.py`  -> figure5_chen_validation.*  (Chen 2024 external validation)
- `make_figureS1.py` -> figureS1_feature_distributions.*  (feature distributions by label)

## Notes

- All scripts are self-contained (data is inline or loaded from
  ../chen_validation/chen_anarci_results.json for Figure 5).
- Fonts: Liberation Sans. Spines: top/right removed. Colour scheme matches the
  parent repository figure style.
- TIFFs are flattened to RGB on a white background (no alpha channel) for
  production compatibility.
