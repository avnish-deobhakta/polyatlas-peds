"""Figure 3. Ranked AUROC and AUPRC on NbBench PolyRx test set.

Two-panel figure: (A) Test AUROC and (B) Test AUPRC. Rows sorted by AUROC (same
order in both panels). Our three primary linear models (Models 1, 2, 3) compared
against all eleven NbBench pretrained language models.

Note: the Full 16-feature forward-selected reference variant and the Model 4
zero-training baseline are intentionally excluded from this figure. The Full
16-feature model is a methodological ceiling reference (nearly identical to
Model 1 with one extra non-CDR feature) and Model 4 sits far below the rest of
the field, compressing the visualization scale. Both are discussed in the text.

Data source: notebooks/06_robustness_matrix.ipynb (AUROC/AUPRC by model x dataset),
notebooks/07_model1_exact_metrics.ipynb (Model 1 AUPRC 0.8364).
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

# (name, AUROC, AUPRC, category)
# 3 linear models + 11 NbBench language models, ordered by AUROC (descending)
rows = [
    ('ESM-2 (650M)',                                     0.842, 0.847,  'lm'),
    ('ProtBert',                                         0.837, 0.844,  'lm'),
    ('Model 1: 13-feat CDR-only (forward-selected)',     0.834, 0.8364, 'ours1'),
    ('ESM-2 (150M)',                                     0.833, 0.840,  'lm'),
    ('AntiBERTa2',                                       0.833, 0.840,  'lm'),
    ('AbLang-H',                                         0.831, 0.839,  'lm'),
    ('AntiBERTa2-CSSP',                                  0.830, 0.838,  'lm'),
    ('IgBert',                                           0.829, 0.836,  'lm'),
    ('Model 2: 21-feat Boughter 2020 pre-specified',     0.829, 0.8301, 'ours'),
    ('AntiBERTy',                                        0.828, 0.835,  'lm'),
    ('AbLang-L',                                         0.819, 0.823,  'lm'),
    ('VHHBERT',                                          0.818, 0.823,  'lm'),
    ('Model 3: 12-feat leave-NbBench-out (CV-selected)', 0.817, 0.8170, 'ours'),
    ('NanoBERT',                                         0.815, 0.823,  'lm'),
]

color_map = {
    'ours1': '#d62728',
    'ours':  '#ff9896',
    'lm':    '#4c72b0',
}

names  = [r[0] for r in rows]
aurocs = [r[1] for r in rows]
auprcs = [r[2] for r in rows]
cats   = [r[3] for r in rows]
colors = [color_map[c] for c in cats]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14.5, 6.5), sharey=True)
y_pos = list(range(len(rows)))[::-1]

barsA = axA.barh(y_pos, aurocs, color=colors, edgecolor='black', linewidth=0.4, height=0.78)
for bar, val, cat in zip(barsA, aurocs, cats):
    weight = 'bold' if cat == 'ours1' else 'normal'
    axA.text(val + 0.0015, bar.get_y() + bar.get_height() / 2,
             f'{val:.3f}', va='center', fontsize=9, fontweight=weight)

axA.set_yticks(y_pos)
axA.set_yticklabels(names, fontsize=9)
for label, cat in zip(axA.get_yticklabels(), cats):
    if cat in ('ours1', 'ours'):
        label.set_fontweight('bold')

axA.set_xlim(0.79, 0.86)
axA.set_xlabel('Test AUROC')
axA.set_title('(A) AUROC', fontsize=11, pad=8, loc='left', fontweight='bold')
axA.grid(alpha=0.2, axis='x', linestyle='--')

barsB = axB.barh(y_pos, auprcs, color=colors, edgecolor='black', linewidth=0.4, height=0.78)
for bar, val, cat in zip(barsB, auprcs, cats):
    weight = 'bold' if cat == 'ours1' else 'normal'
    axB.text(val + 0.0015, bar.get_y() + bar.get_height() / 2,
             f'{val:.3f}', va='center', fontsize=9, fontweight=weight)

axB.set_xlim(0.79, 0.86)
axB.set_xlabel('Test AUPRC')
axB.set_title('(B) AUPRC', fontsize=11, pad=8, loc='left', fontweight='bold')
axB.grid(alpha=0.2, axis='x', linestyle='--')

legend_patches = [
    mpatches.Patch(color=color_map['ours1'], label='Our models (hand-crafted)'),
    mpatches.Patch(color=color_map['lm'],    label='NbBench language models'),
]
fig.legend(handles=legend_patches, loc='lower center',
           bbox_to_anchor=(0.5, -0.02), ncol=2,
           fontsize=10, frameon=True, framealpha=0.95)

fig.suptitle('Rows sorted by AUROC; Model 1, Model 2, Model 3 are our linear models (others are NbBench language models)',
             fontsize=10, y=0.995, style='italic')
plt.tight_layout(rect=[0, 0.04, 1, 0.96])

out_dir = Path(__file__).resolve().parent
plt.savefig(out_dir / 'figure3_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'figure3.pdf', bbox_inches='tight')
plt.close()
print(f'Figure 3 saved to {out_dir}/figure3_comparison.png and figure3.pdf')
