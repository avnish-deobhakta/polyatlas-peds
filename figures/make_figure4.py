"""Figure 4. Model 1 standardized coefficients.

The 13 fitted standardized coefficients of the CDR-only logistic regression
(trained on NbBench PolyRx train, n=101,854), sorted by absolute magnitude.
Positive coefficients (red) indicate features whose increase raises predicted
polyreactivity; negative coefficients (blue) indicate features whose increase
lowers it. Intercept = -0.0523 (not shown).

Data source: notebooks/07_model1_exact_metrics.ipynb cell 7 / models/model1_coefficients.csv.
"""
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

# (feature, standardized_coef, human_readable_description)
coefs = [
    ('H2_charge',        +0.7971, 'net charge, CDR-H2'),
    ('H3_neg_frac',      -0.6095, 'negative-charge fraction, CDR-H3'),
    ('H2_len',           +0.4089, 'length, CDR-H2'),
    ('H3_R',             +0.3791, 'arginine fraction, CDR-H3'),
    ('H1_charge',        +0.3508, 'net charge, CDR-H1'),
    ('H3_len',           -0.3275, 'length, CDR-H3'),
    ('H1_arom',          +0.2564, 'aromatic fraction, CDR-H1'),
    ('H3_abs_charge',    +0.2432, '|net charge|, CDR-H3'),
    ('H3_arom',          +0.1887, 'aromatic fraction, CDR-H3'),
    ('H2_hphob_frac',    -0.1261, 'hydrophobic fraction, CDR-H2'),
    ('H3_charge_dipole', +0.1129, 'charge dipole, CDR-H3'),
    ('H3_charge',        +0.1049, 'net charge, CDR-H3'),
    ('H1_hphob',         +0.0253, 'mean hydrophobicity, CDR-H1'),
]

# Already sorted by |coef| descending above.
names  = [f'{c[0]}  ({c[2]})' for c in coefs]
values = [c[1] for c in coefs]

# Colors: red for positive (predicts polyreactive), blue for negative (predicts non-polyreactive)
pos_color = '#d62728'  # red
neg_color = '#1f77b4'  # blue
colors = [pos_color if v > 0 else neg_color for v in values]

fig, ax = plt.subplots(figsize=(8.2, 5.2))

y_pos = list(range(len(coefs)))[::-1]
bars = ax.barh(y_pos, values, color=colors, edgecolor='black', linewidth=0.4, height=0.78)

# Annotate each bar with its coefficient value
for bar, v in zip(bars, values):
    x_text = v + 0.015 if v > 0 else v - 0.015
    ha = 'left' if v > 0 else 'right'
    ax.text(x_text, bar.get_y() + bar.get_height() / 2,
            f'{v:+.3f}', va='center', ha=ha, fontsize=8.5, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=9)
ax.axvline(0, color='black', linewidth=0.8)

ax.set_xlim(-0.8, 1.0)
ax.set_xlabel('Standardized logistic-regression coefficient')
ax.set_title('Model 1 (13-feature CDR-only) fitted coefficients',
             fontsize=11, pad=8)
ax.grid(alpha=0.2, axis='x', linestyle='--')

# Legend
legend_patches = [
    mpatches.Patch(color=pos_color, label='Higher value → predicts polyreactive'),
    mpatches.Patch(color=neg_color, label='Higher value → predicts non-polyreactive'),
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=9,
          frameon=True, framealpha=0.95)

# Intercept annotation
ax.text(0.98, -0.12, 'Intercept = −0.0523', transform=ax.transAxes,
        fontsize=8.5, style='italic', ha='right', color='#555555')

plt.tight_layout()
plt.savefig('/home/claude/polyatlas-peds/figures/figure4_coefficients.png',
            dpi=300, bbox_inches='tight')
plt.close()
print('Figure 4 saved.')
