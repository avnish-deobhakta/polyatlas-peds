"""Figure 2. Univariate feature importance on NbBench validation.

Single-feature logistic regression (trained on NbBench train, evaluated on NbBench val)
AUROC for the top 20 features. Features are colored by property category to reveal
electrostatic dominance: the top 10 features are all charge-related.

Data source: notebooks/03_feature_climb_full.ipynb cell 7 (univariate table).
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams.update({
    'font.family': 'Liberation Sans',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Top 20 univariate features by val AUROC, from 03 cell 7.
# Categorization: charge (net charge, pI, absolute charge, +/- fractions, R, K);
# hydrophobicity; aromatic (F+W+Y); length; other.
feats = [
    ('full_pI',        0.7795, 'charge'),
    ('full_charge',    0.7793, 'charge'),
    ('full_abs_charge',0.7642, 'charge'),
    ('full_R',         0.7371, 'charge'),
    ('full_pos_frac',  0.7339, 'charge'),
    ('full_neg_frac',  0.7324, 'charge'),
    ('H3_charge',      0.7261, 'charge'),
    ('H3_pI',          0.7220, 'charge'),
    ('H2_charge',      0.7186, 'charge'),
    ('H3_neg_frac',    0.6945, 'charge'),
    ('H3_R',           0.6865, 'charge'),
    ('H3_pos_frac',    0.6844, 'charge'),
    ('H2_pos_frac',    0.6711, 'charge'),
    ('H2_R',           0.6655, 'charge'),
    ('H2_neg_frac',    0.6112, 'charge'),
    ('H1_charge',      0.6069, 'charge'),
    ('H2_abs_charge',  0.6050, 'charge'),
    ('H2_hphob',       0.5887, 'hydrophob'),
    ('H2_len',         0.5851, 'length'),
    ('H2_hphob_frac',  0.5832, 'hydrophob'),
]

# Color map
color_map = {
    'charge':     '#d62728',   # red
    'hydrophob':  '#2ca02c',   # green (matches manuscript embedded figure)
    'aromatic':   '#9467bd',   # purple
    'length':     '#8c564b',   # brown (matches manuscript embedded figure)
    'other':      '#7f7f7f',   # gray
}

names  = [f[0] for f in feats]
aucs   = [f[1] for f in feats]
cats   = [f[2] for f in feats]
colors = [color_map[c] for c in cats]

fig, ax = plt.subplots(figsize=(7.2, 7.0))

y_pos = list(range(len(feats)))[::-1]  # Top feature at top of chart
bars = ax.barh(y_pos, aucs, color=colors, edgecolor='black', linewidth=0.3, height=0.78)

# Annotate AUROC values at bar end
for bar, auc in zip(bars, aucs):
    ax.text(auc + 0.003, bar.get_y() + bar.get_height() / 2,
            f'{auc:.3f}', va='center', fontsize=8.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=9)
ax.set_xlim(0.5, 0.82)
ax.set_xlabel('Validation AUROC (single-feature logistic regression)')
ax.set_title('Top 20 univariate feature rankings on NbBench PolyRx',
             fontsize=11, pad=8)
ax.grid(alpha=0.2, axis='x', linestyle='--')
ax.axvline(0.5, color='black', linewidth=0.6, linestyle='-', alpha=0.5)

# Top-10 divider and annotation
# Top 10 features = indices 0-9 from the top (y_pos values 24..15)
divider_y = y_pos[10] + 0.5  # between the 10th and 11th feature from top
ax.axhline(divider_y, color='black', linestyle=':', linewidth=0.9, alpha=0.6)
ax.text(0.805, divider_y + 4, 'top 10\nall charge-\nrelated',
        fontsize=9, va='center', ha='right', style='italic',
        color=color_map['charge'], fontweight='bold')

# Legend
legend_patches = [mpatches.Patch(color=color_map[k], label=k.replace('hphob', 'hydrophob.').replace('charge', 'charge'))
                  for k in ['charge', 'hydrophob', 'length']]
ax.legend(handles=legend_patches, loc='lower right', fontsize=9,
          frameon=True, framealpha=0.95, title='Property category', title_fontsize=9)

plt.tight_layout()
out_dir = Path(__file__).resolve().parent
plt.savefig(out_dir / 'figure2_univariate.png', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'figure2.pdf', bbox_inches='tight')
plt.close()
print('Figure 2 saved.')
