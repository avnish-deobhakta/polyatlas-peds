"""
Supplementary Figure S1. Distributions of the top-ranked univariate features
(from Figure 2) across the NbBench PolyRx dataset, colored by polyreactivity label.

Responds to Referee 1: "In addition to Fig. 2, it would be helpful to see
distributions of each of these features in the entire dataset, preferably colored
by polyreactive and non-polyreactive labels."

This figure uses the SAME NbBench PolyRx data that generated Figure 2 (not the Chen
external dataset). It is fully self-contained: it loads NbBench from Hugging Face and
computes the feature catalog inline, with no external module imports or local CSVs.

Run: python make_figureS1.py   (requires internet access to Hugging Face)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datasets import load_dataset

# ----------------------------------------------------------------------
# Feature code (identical definitions to the main analysis; inline so this
# script is self-contained and does not import chen_harness).
# ----------------------------------------------------------------------
KYTE_DOOLITTLE = {"A":1.8,"C":2.5,"D":-3.5,"E":-3.5,"F":2.8,"G":-0.4,"H":-3.2,"I":4.5,"K":-3.9,"L":3.8,"M":1.9,"N":-3.5,"P":-1.6,"Q":-3.5,"R":-4.5,"S":-0.8,"T":-0.7,"V":4.2,"W":-0.9,"Y":-1.3}
CHARGE_AT_PH74 = {"D":-1,"E":-1,"K":1,"R":1,"H":0.1}
AROMATIC=set("FWY"); POSITIVE=set("KR"); NEGATIVE=set("DE")
PKA={"C_term":3.55,"D":4.05,"E":4.45,"H":5.98,"K":10.0,"R":12.0,"Y":10.0,"C":9.0,"N_term":8.0}

def net_charge(s):
    if not isinstance(s,str) or not s: return np.nan
    return sum(CHARGE_AT_PH74.get(a,0) for a in s.upper())
def frac(s,sub):
    if not isinstance(s,str) or not s: return np.nan
    s=s.upper(); return sum(1 for a in s if a in sub)/len(s)
def frac_res(s,r):
    if not isinstance(s,str) or not s: return np.nan
    return s.upper().count(r)/len(s)
def estimate_pI(s):
    if not isinstance(s,str) or not s: return np.nan
    s=s.upper()
    def c_at(ph):
        c=1/(1+10**(ph-PKA["N_term"]))-1/(1+10**(PKA["C_term"]-ph))
        for a in s:
            if a in ("K","R"): c+=1/(1+10**(ph-PKA[a]))
            elif a in ("D","E"): c-=1/(1+10**(PKA[a]-ph))
            elif a=="H": c+=1/(1+10**(ph-PKA["H"]))
            elif a=="Y": c-=1/(1+10**(PKA["Y"]-ph))
            elif a=="C": c-=1/(1+10**(PKA["C"]-ph))
        return c
    lo,hi=0.0,14.0
    for _ in range(50):
        m=(lo+hi)/2
        if c_at(m)>0: lo=m
        else: hi=m
    return (lo+hi)/2

def compute_top_features(df):
    """Compute the features that appear among the top univariate ranks in Figure 2."""
    f = pd.DataFrame(index=df.index)
    full = df["seq"].fillna("").astype(str)
    h2   = df["CDR2_nogaps"].fillna("").astype(str)
    h3   = df["CDR3_nogaps"].fillna("").astype(str)
    f["full_pI"]        = full.apply(estimate_pI)
    f["full_charge"]    = full.apply(net_charge)
    f["full_abs_charge"]= f["full_charge"].abs()
    f["full_R"]         = full.apply(lambda x: frac_res(x,"R"))
    f["full_pos_frac"]  = full.apply(lambda x: frac(x, POSITIVE))
    f["full_neg_frac"]  = full.apply(lambda x: frac(x, NEGATIVE))
    f["H3_charge"]      = h3.apply(net_charge)
    f["H3_pI"]          = h3.apply(estimate_pI)
    f["H2_charge"]      = h2.apply(net_charge)
    f["H3_neg_frac"]    = h3.apply(lambda x: frac(x, NEGATIVE))
    return f

# ----------------------------------------------------------------------
# Load NbBench PolyRx (same source as Figure 2) and compute features.
# We use the validation split (the split on which Figure 2's univariate
# AUROCs were evaluated); n reported in the caption/title.
# ----------------------------------------------------------------------
ds = load_dataset("ZYMScott/polyreaction")
val = ds["validation"].to_pandas()
val = val[val["CDR3_nogaps"].fillna("").astype(str).str.len() > 0].reset_index(drop=True)
X = compute_top_features(val)
X["label"] = val["label"].values
N = len(X)
n_pos = int((X["label"] == 1).sum()); n_neg = int((X["label"] == 0).sum())

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 10, "axes.labelsize": 10,
    "axes.titlesize": 11, "axes.spines.top": False, "axes.spines.right": False,
})

# The ten top-ranked univariate features from Figure 2, all charge-related.
feats = [
    ("full_pI",         "Full-sequence pI  (AUROC 0.779)"),
    ("full_charge",     "Full-sequence net charge  (0.779)"),
    ("full_abs_charge", "Full-sequence |charge|  (0.764)"),
    ("full_R",          "Full-sequence Arg fraction  (0.737)"),
    ("full_pos_frac",   "Full-sequence positive fraction  (0.734)"),
    ("full_neg_frac",   "Full-sequence negative fraction  (0.732)"),
    ("H3_charge",       "CDR-H3 net charge  (0.726)"),
    ("H3_pI",           "CDR-H3 pI  (0.722)"),
    ("H2_charge",       "CDR-H2 net charge  (0.719)"),
    ("H3_neg_frac",     "CDR-H3 negative fraction  (0.695)"),
]

C_POS = "#d62728"   # polyreactive
C_NEG = "#4c72b0"   # non-polyreactive

fig, axes = plt.subplots(2, 5, figsize=(16, 6.4))
for ax, (col, title) in zip(axes.ravel(), feats):
    pos = X[X.label == 1][col].dropna().values
    neg = X[X.label == 0][col].dropna().values
    allv = np.concatenate([pos, neg])
    lo, hi = np.percentile(allv, 1), np.percentile(allv, 99)
    bins = np.linspace(lo, hi, 40)
    ax.hist(neg, bins=bins, color=C_NEG, alpha=0.55, density=True, label="Non-polyreactive")
    ax.hist(pos, bins=bins, color=C_POS, alpha=0.55, density=True, label="Polyreactive")
    ax.set_title(title, fontsize=9.5)
    ax.set_yticks([])

import matplotlib.patches as mpatches
handles = [mpatches.Patch(color=C_NEG, alpha=0.55, label="Non-polyreactive"),
           mpatches.Patch(color=C_POS, alpha=0.55, label="Polyreactive")]
fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.985),
           ncol=2, fontsize=10, frameon=True)
fig.suptitle(f"Distributions of the top-ranked univariate features (Figure 2) on the "
             f"NbBench PolyRx validation set\n(n = {N:,}: {n_pos:,} polyreactive, "
             f"{n_neg:,} non-polyreactive), colored by label",
             fontsize=12, y=1.06)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("figureS1_feature_distributions.pdf", bbox_inches="tight")
fig.savefig("figureS1_feature_distributions.tif", dpi=350, bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
fig.savefig("figureS1_feature_distributions.png", dpi=150, bbox_inches="tight")
print(f"Supplementary Figure S1 saved (NbBench validation, n={N})")
