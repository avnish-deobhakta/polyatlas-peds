"""Figure 1. Forward-selection climb trajectories on NbBench PolyRx.

Three candidate-pool variants evaluated: full 52-feature pool (16 features selected),
CDR-only pool (13 features selected, this is Model 1), and CDR-H3-only pool (11 features
selected). All climbs start from H3_charge alone. Y-axis: validation AUROC at each step
(used for feature selection). Final test AUROC annotated at the end of each curve.

Data source: notebooks/05_cdr_only_climb.ipynb cell 11 (climb logs) and cell 13 (final
test AUROCs).
"""
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'Liberation Sans',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Val AUROC at each step of each climb (from 05h cell 11).
full_val = [0.7261, 0.7983, 0.8081, 0.8158, 0.8244, 0.8284, 0.8304, 0.8313,
            0.8343, 0.8356, 0.8365, 0.8372, 0.8380, 0.8386, 0.8391, 0.8394]
cdr_val  = [0.7261, 0.7983, 0.8081, 0.8151, 0.8202, 0.8250, 0.8282, 0.8296,
            0.8329, 0.8340, 0.8348, 0.8356, 0.8358]
h3_val   = [0.7261, 0.7419, 0.7445, 0.7500, 0.7525, 0.7533, 0.7540, 0.7544,
            0.7546, 0.7547, 0.7548]

# Final test AUROCs (05h cell 13)
full_test  = 0.8359
cdr_test   = 0.8336
h3_test    = 0.7538

# NbBench LM reference band: 0.815 (NanoBERT, lowest) to 0.842 (ESM-2 650M, highest)
lm_low, lm_high = 0.815, 0.842

fig, ax = plt.subplots(figsize=(7.2, 4.6))

# Reference band for NbBench LM range
ax.axhspan(lm_low, lm_high, color='#bbbbbb', alpha=0.25,
           label=f'NbBench 11 LMs range ({lm_low:.3f}–{lm_high:.3f})')
ax.axhline(lm_high, color='#555555', linewidth=0.6, linestyle=':')
ax.axhline(lm_low, color='#555555', linewidth=0.6, linestyle=':')

# Three climb curves
x_full = list(range(1, len(full_val) + 1))
x_cdr  = list(range(1, len(cdr_val) + 1))
x_h3   = list(range(1, len(h3_val) + 1))

ax.plot(x_full, full_val, marker='o', markersize=5, linewidth=1.8,
        color='#2b7bba', label='Full 52-feat pool (final: 16 features)')
ax.plot(x_cdr,  cdr_val,  marker='s', markersize=5, linewidth=1.8,
        color='#d95f02', label='CDR-only pool (Model 1: 13 features)')
ax.plot(x_h3,   h3_val,   marker='^', markersize=5, linewidth=1.8,
        color='#7570b3', label='CDR-H3-only pool (final: 11 features)')

# Annotate final test AUROC at end of each curve
def annotate_final(x, y_val, y_test, color, text_offset=(8, 0)):
    ax.plot(x, y_test, marker='*', markersize=12, color=color,
            markeredgecolor='black', markeredgewidth=0.6, zorder=5)
    ax.annotate(f'test = {y_test:.3f}', xy=(x, y_test),
                xytext=text_offset, textcoords='offset points',
                fontsize=8.5, color=color, fontweight='bold', va='center')

annotate_final(len(full_val), full_val[-1], full_test, '#2b7bba', (8,  6))
annotate_final(len(cdr_val),  cdr_val[-1],  cdr_test,  '#d95f02', (8, -8))
annotate_final(len(h3_val),   h3_val[-1],   h3_test,   '#7570b3', (8,  0))

ax.set_xlabel('Number of features in model')
ax.set_ylabel('Validation AUROC (NbBench val, n=14,576)')
ax.set_xlim(0.5, 20)
ax.set_ylim(0.72, 0.855)
ax.set_xticks(range(1, 17))
ax.grid(alpha=0.2, linestyle='--')

# Starting-point annotation
ax.annotate('H3_charge alone\n(Model 4 baseline)',
            xy=(1, 0.7261), xytext=(3.2, 0.735),
            fontsize=8.5, ha='left',
            arrowprops=dict(arrowstyle='-', color='gray', lw=0.6))

ax.legend(loc='lower right', fontsize=8.5, framealpha=0.95)
ax.set_title('Forward-selection climb: full, CDR-only, CDR-H3-only pools',
             fontsize=11, pad=8)

plt.tight_layout()
out_dir = Path(__file__).resolve().parent
plt.savefig(out_dir / 'figure1_climb.png', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'figure1.pdf', bbox_inches='tight')
plt.close()
print('Figure 1 saved.')
