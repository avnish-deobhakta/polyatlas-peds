"""
Supplementary Figure S1 — all 20 Figure-2 features across the entire retained
NbBench PolyRx dataset (train + validation + test; n = 141,204), colored by label.

Self-contained: loads NbBench from Hugging Face and computes features inline.
Requires internet access to Hugging Face. Run: python make_figureS1.py
"""
import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Cell 2 — feature code (inline; identical definitions to the main analysis)
KYTE_DOOLITTLE = {"A":1.8,"C":2.5,"D":-3.5,"E":-3.5,"F":2.8,"G":-0.4,"H":-3.2,"I":4.5,"K":-3.9,"L":3.8,"M":1.9,"N":-3.5,"P":-1.6,"Q":-3.5,"R":-4.5,"S":-0.8,"T":-0.7,"V":4.2,"W":-0.9,"Y":-1.3}
CHARGE_AT_PH74 = {"D":-1,"E":-1,"K":1,"R":1,"H":0.1}
AROMATIC=set("FWY"); POSITIVE=set("KR"); NEGATIVE=set("DE"); HYDROPHOBIC=set("ILVFMWYC")
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
def mean_hphob(s):
    if not isinstance(s,str) or not s: return np.nan
    return np.mean([KYTE_DOOLITTLE.get(a,0) for a in s.upper()])
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
print("feature code ready")

# Cell 1 — load all three NbBench splits and print shapes
import pandas as pd, numpy as np
from datasets import load_dataset

ds = load_dataset("ZYMScott/polyreaction")
print("raw splits:", {k: ds[k].num_rows for k in ds})

frames = []
for split in ["train", "validation", "test"]:
    df = ds[split].to_pandas()
    df = df[df["CDR3_nogaps"].fillna("").astype(str).str.len() > 0].copy()
    df["_split"] = split
    frames.append(df)
    print(f"  {split}: retained {len(df)}")
full = pd.concat(frames, ignore_index=True)
print("TOTAL retained:", len(full))
print("cols:", list(full.columns))

# Cell 3 — compute the 20 Figure-2 features on all 141,204 sequences (with progress)
import sys, time

full_seq = full["seq"].fillna("").astype(str)
h1 = full["CDR1_nogaps"].fillna("").astype(str)
h2 = full["CDR2_nogaps"].fillna("").astype(str)
h3 = full["CDR3_nogaps"].fillna("").astype(str)

X = pd.DataFrame(index=full.index)
# --- the 20 Figure-2 features, in Figure-2 order ---
t0=time.time()
print("computing pI over full sequences (slowest step)...", flush=True)
X["full_pI"]        = full_seq.apply(estimate_pI)
print(f"  full_pI done ({time.time()-t0:.0f}s)", flush=True)
X["full_charge"]    = full_seq.apply(net_charge)
X["full_abs_charge"]= X["full_charge"].abs()
X["full_R"]         = full_seq.apply(lambda x: frac_res(x,"R"))
X["full_pos_frac"]  = full_seq.apply(lambda x: frac(x, POSITIVE))
X["full_neg_frac"]  = full_seq.apply(lambda x: frac(x, NEGATIVE))
X["H3_charge"]      = h3.apply(net_charge)
print("computing H3 pI...", flush=True)
X["H3_pI"]          = h3.apply(estimate_pI)
X["H2_charge"]      = h2.apply(net_charge)
X["H3_neg_frac"]    = h3.apply(lambda x: frac(x, NEGATIVE))
X["H3_R"]           = h3.apply(lambda x: frac_res(x,"R"))
X["H3_pos_frac"]    = h3.apply(lambda x: frac(x, POSITIVE))
X["H2_pos_frac"]    = h2.apply(lambda x: frac(x, POSITIVE))
X["H2_R"]           = h2.apply(lambda x: frac_res(x,"R"))
X["H2_neg_frac"]    = h2.apply(lambda x: frac(x, NEGATIVE))
X["H1_charge"]      = h1.apply(net_charge)
X["H2_abs_charge"]  = h2.apply(net_charge).abs()
X["H2_hphob"]       = h2.apply(mean_hphob)
X["H2_len"]         = h2.str.len()
X["H2_hphob_frac"]  = h2.apply(lambda x: frac(x, HYDROPHOBIC))
X["label"]          = full["label"].astype(int).values
N=len(X); n_pos=int((X.label==1).sum()); n_neg=int((X.label==0).sum())
print(f"done in {time.time()-t0:.0f}s. n={N} ({n_pos} polyreactive, {n_neg} non-polyreactive)")

# Cell 4 — 4x5 grid of all 20 features, colored by label, saved at 350 dpi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.titlesize":9.5,
                     "axes.spines.top":False,"axes.spines.right":False})

# (feature, display title, category) in Figure-2 order; AUROCs from Figure 2
feats = [
    ("full_pI","Full-seq pI  (0.779)","charge"),
    ("full_charge","Full-seq net charge  (0.779)","charge"),
    ("full_abs_charge","Full-seq |charge|  (0.764)","charge"),
    ("full_R","Full-seq Arg fraction  (0.737)","charge"),
    ("full_pos_frac","Full-seq positive frac  (0.734)","charge"),
    ("full_neg_frac","Full-seq negative frac  (0.732)","charge"),
    ("H3_charge","CDR-H3 net charge  (0.726)","charge"),
    ("H3_pI","CDR-H3 pI  (0.722)","charge"),
    ("H2_charge","CDR-H2 net charge  (0.719)","charge"),
    ("H3_neg_frac","CDR-H3 negative frac  (0.695)","charge"),
    ("H3_R","CDR-H3 Arg fraction  (0.687)","charge"),
    ("H3_pos_frac","CDR-H3 positive frac  (0.684)","charge"),
    ("H2_pos_frac","CDR-H2 positive frac  (0.671)","charge"),
    ("H2_R","CDR-H2 Arg fraction  (0.665)","charge"),
    ("H2_neg_frac","CDR-H2 negative frac  (0.611)","charge"),
    ("H1_charge","CDR-H1 net charge  (0.607)","charge"),
    ("H2_abs_charge","CDR-H2 |charge|  (0.605)","charge"),
    ("H2_hphob","CDR-H2 hydrophobicity  (0.589)","hydrophob"),
    ("H2_len","CDR-H2 length  (0.585)","length"),
    ("H2_hphob_frac","CDR-H2 hydrophobic frac  (0.583)","hydrophob"),
]
# label colors (consistent with earlier S1): red=polyreactive, blue=non
C_POS, C_NEG = "#d62728", "#4c72b0"

fig, axes = plt.subplots(4, 5, figsize=(17, 11))
for ax,(col,title,cat) in zip(axes.ravel(), feats):
    pos = X[X.label==1][col].dropna().values
    neg = X[X.label==0][col].dropna().values
    allv = np.concatenate([pos,neg])
    lo,hi = np.percentile(allv,1), np.percentile(allv,99)
    if lo==hi: hi=lo+1
    bins=np.linspace(lo,hi,45)
    ax.hist(neg,bins=bins,color=C_NEG,alpha=0.55,density=True)
    ax.hist(pos,bins=bins,color=C_POS,alpha=0.55,density=True)
    ax.set_title(title,fontsize=9.3); ax.set_yticks([])
handles=[mpatches.Patch(color=C_NEG,alpha=0.55,label="Non-polyreactive"),
         mpatches.Patch(color=C_POS,alpha=0.55,label="Polyreactive")]
fig.legend(handles=handles,loc="upper center",bbox_to_anchor=(0.5,0.995),ncol=2,fontsize=11,frameon=True)
fig.suptitle(f"Distributions of all twenty Figure-2 features across the entire retained NbBench PolyRx dataset\n"
             f"(train + validation + test; n = {N:,}: {n_pos:,} polyreactive, {n_neg:,} non-polyreactive), colored by label",
             fontsize=13, y=1.035)
fig.tight_layout(rect=[0,0,1,0.965])
fig.savefig("figureS1_feature_distributions.pdf", bbox_inches="tight")
fig.savefig("figureS1_feature_distributions.tif", dpi=350, bbox_inches="tight", pil_kwargs={"compression":"tiff_lzw"})
fig.savefig("figureS1_feature_distributions.png", dpi=140, bbox_inches="tight")
print(f"saved S1 (20 features, n={N}) as tif/pdf/png")
plt.show()
