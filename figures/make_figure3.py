"""Figure 3. Ranked AUROC and AUPRC on NbBench PolyRx test set.

Two-panel figure: (A) Test AUROC and (B) Test AUPRC. Rows sorted by AUROC (same
order in both panels). Our four linear hand-crafted-feature models versus all 11
language models from NbBench Table 10.

Data source: notebooks/06_robustness_matrix.ipynb (AUROC/AUPRC by model and dataset),
notebooks/04_feature_climb_extended.ipynb (Full 16-feat AUPRC 0.8387),
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

# (name, AUROC, AUPRC, category, size_label)
# Ordered by AUROC (descending) — same row order in both panels per legend
rows = [
    ('ESM-2 (650M)',                                  0.842, 0.847, 'lm',    '650M'),
    ('ProtBert',                                      0.837, 0.844, 'lm',    '420M'),
    ('Full 16-feat forward-selected LR',              0.836, 0.8387, 'ours',  '17'),
    ('Model 1: 13-feat CDR-only LR',                  0.834, 0.8364, 'ours1', '14'),
    ('ESM-2 (150M)',                                  0.833, 0.840, 'lm',    '150M'),
    ('AntiBERTa2',                                    0.833, 0.840, 'lm',    '203M'),
    ('AbLang-H',                                      0.831, 0.839, 'lm',    '86M'),
    ('AntiBERTa2-CSSP',                               0.830, 0.838, 'lm',    '202M'),
    ('Model 2: 21-feat literature-specified',         0.829, 0.8301, 'ours',  '22'),
    ('IgBert',                                        0.829, 0.836, 'lm',    '420M'),
    ('AntiBERTy',                                     0.828, 0.835, 'lm',    '26M'),
    ('AbLang-L',                                      0.819, 0.823, 'lm',    '86M'),
    ('VHHBERT',                                       0.818, 0.823, 'lm',    '86M'),
    ('Model 3: 12-feat leave-NbBench-out LR',         0.817, 0.8170, 'ours',  '13'),
    ('NanoBERT',                                      0.815, 0.823, 'lm',    '15M'),
    ('Model 4: H3-charge zero-training',              0.726, 0.7206, 'ours',  '0'),
]

color_map = {
    'ours1': '#d62728',   # bright red for Model 1 (headline)
    'ours':  '#ff9896',   # lighter red for our other models
    'lm':    '#7f7f7f',   # gray for language models
}

names  = [r[0] for r in rows]
aurocs = [r[1] for r in rows]
auprcs = [r[2] for r in rows]
cats   = [r[3] for r in rows]
sizes  = [r[4] for r in rows]
colors = [color_map[c] for c in cats]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14.5, 6.5), sharey=True)

y_pos = list(range(len(rows)))[::-1]

# ===== Panel A: AUROC =====
barsA = axA.barh(y_pos, aurocs, color=colors, edgecolor='black', linewidth=0.4, height=0.78)

for bar, val, size, cat in zip(barsA, aurocs, sizes, cats):
    weight = 'bold' if cat == 'ours1' else 'normal'
    axA.text(val + 0.0015, bar.get_y() + bar.get_height() / 2,
             f'{val:.3f}', va='center', fontsize=8.5, fontweight=weight)
    size_text = f'  ({size} p)' if size != '0' else '  (zero-train)'
    axA.text(val + 0.010, bar.get_y() + bar.get_height() / 2,
             size_text, va='center', fontsize=7.2, style='italic', color='#555555')

axA.set_yticks(y_pos)
axA.set_yticklabels(names, fontsize=9)
for label, cat in zip(axA.get_yticklabels(), cats):
    if cat == 'ours1':
        label.set_fontweight('bold')
        label.set_color(color_map['ours1'])

axA.set_xlim(0.70, 0.88)
axA.set_xlabel('Test AUROC on NbBench PolyRx (n = 24,955)')
axA.set_title('(A) AUROC', fontsize=11, pad=8, loc='left', fontweight='bold')
axA.grid(alpha=0.2, axis='x', linestyle='--')

# ===== Panel B: AUPRC =====
barsB = axB.barh(y_pos, auprcs, color=colors, edgecolor='black', linewidth=0.4, height=0.78)

for bar, val, cat in zip(barsB, auprcs, cats):
    weight = 'bold' if cat == 'ours1' else 'normal'
    axB.text(val + 0.0015, bar.get_y() + bar.get_height() / 2,
             f'{val:.3f}', va='center', fontsize=8.5, fontweight=weight)

axB.set_xlim(0.70, 0.88)
axB.set_xlabel('Test AUPRC on NbBench PolyRx (n = 24,955)')
axB.set_title('(B) AUPRC', fontsize=11, pad=8, loc='left', fontweight='bold')
axB.grid(alpha=0.2, axis='x', linestyle='--')

# Shared legend at the bottom
legend_patches = [
    mpatches.Patch(color=color_map['ours1'], label='Our primary model (13-feat CDR-only)'),
    mpatches.Patch(color=color_map['ours'],  label='Our other linear models'),
    mpatches.Patch(color=color_map['lm'],    label='NbBench language models'),
]
fig.legend(handles=legend_patches, loc='lower center',
           bbox_to_anchor=(0.5, -0.02), ncol=3,
           fontsize=9, frameon=True, framealpha=0.95)

fig.suptitle('Ranked performance: hand-crafted features vs. 11 pretrained language models',
             fontsize=12, y=0.995)
plt.tight_layout(rect=[0, 0.04, 1, 0.97])

# Save relative to the script's own directory (portable)
out_dir = Path(__file__).resolve().parent
plt.savefig(out_dir / 'figure3_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'figure3.pdf', bbox_inches='tight')
plt.close()
print(f'Figure 3 saved to {out_dir}/figure3_comparison.png and figure3.pdf')
