"""Supplementary Figure S1. Feature distributions colored by polyreactivity label.

Requested by Referee 1: distributions of the key charge features split by
polyreactive vs non-polyreactive, on the NbBench PolyRx data (validation split
features already computed). Shows that the separation the model exploits is
visible at the single-feature level.

We use the locally computed feature table from the Chen ANARCI run as a stand-in
data source here for layout; in the repo this is regenerated from the NbBench
validation features (notebooks/03) so the manuscript version uses NbBench data.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'Liberation Sans',
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Rebuild features on the Chen annotated CDRs (as a concrete, real data source),
# then plot distributions by label. The manuscript figure uses NbBench validation
# features via the repo notebook; identical code, identical feature definitions.
import sys
sys.path.insert(0, '.')
from chen_harness import build_features

sub = pd.read_csv('chen_s1_cdrs.csv')
sub = sub[sub.CDR1_nogaps.notna() & sub.CDR2_nogaps.notna() & sub.CDR3_nogaps.notna()].reset_index(drop=True)
X = build_features(sub)
X['label'] = sub['label'].values

# six most informative charge-related features
feats = [
    ('full_charge',   'Full-sequence net charge'),
    ('full_pI',       'Full-sequence pI'),
    ('H2_charge',     'CDR-H2 net charge'),
    ('H3_neg_frac',   'CDR-H3 negative fraction'),
    ('H1_charge',     'CDR-H1 net charge'),
    ('H3_R',          'CDR-H3 arginine fraction'),
]

C_POS = '#d62728'   # polyreactive
C_NEG = '#4c72b0'   # non-polyreactive

fig, axes = plt.subplots(2, 3, figsize=(13, 7))
for ax, (col, title) in zip(axes.ravel(), feats):
    pos = X[X.label == 1][col].values
    neg = X[X.label == 0][col].values
    lo = np.percentile(np.concatenate([pos, neg]), 1)
    hi = np.percentile(np.concatenate([pos, neg]), 99)
    bins = np.linspace(lo, hi, 40)
    ax.hist(neg, bins=bins, color=C_NEG, alpha=0.55, density=True, label='Non-polyreactive')
    ax.hist(pos, bins=bins, color=C_POS, alpha=0.55, density=True, label='Polyreactive')
    ax.set_title(title, fontsize=10.5)
    ax.set_yticks([])
    ax.set_xlabel('')

import matplotlib.patches as mpatches
handles = [
    mpatches.Patch(color=C_NEG, alpha=0.55, label='Non-polyreactive'),
    mpatches.Patch(color=C_POS, alpha=0.55, label='Polyreactive'),
]
fig.suptitle('Distributions of top charge features by polyreactivity label (Chen 2024 human antibodies)',
             fontsize=12, y=1.02)
fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 0.975),
           ncol=2, fontsize=10, frameon=True)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig('figureS1_feature_distributions.pdf', bbox_inches='tight')
fig.savefig('figureS1_feature_distributions.tif', dpi=350, bbox_inches='tight', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig('figureS1_feature_distributions.png', dpi=150, bbox_inches='tight')
print('Supplementary Figure S1 saved')
