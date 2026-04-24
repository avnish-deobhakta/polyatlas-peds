"""Figure 3. Ranked AUROC on NbBench PolyRx test set.

Our three linear hand-crafted-feature models versus all 11 language models from
NbBench Table 10. Our 13-feature CDR-only Model 1 ranks 4th of 15, with 14 trainable
parameters versus 15M-650M backbone parameters for the language models.

Data source: notebooks/06_robustness_matrix.ipynb cell 23 (final ranking table).
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

# (name, AUROC, category, size_label)
# Ordered by AUROC (descending)
rows = [
    ('ESM-2 (650M)',                                  0.842, 'lm',    '650M'),
    ('ProtBert',                                      0.837, 'lm',    '420M'),
    ('Full 16-feat forward-selected LR',              0.836, 'ours',  '17'),
    ('Model 1: 13-feat CDR-only LR',                  0.834, 'ours1', '14'),
    ('ESM-2 (150M)',                                  0.833, 'lm',    '150M'),
    ('AntiBERTa2',                                    0.833, 'lm',    '203M'),
    ('AbLang-H',                                      0.831, 'lm',    '86M'),
    ('AntiBERTa2-CSSP',                               0.830, 'lm',    '202M'),
    ('Model 2: 21-feat Boughter pre-specified',       0.829, 'ours',  '22'),
    ('IgBert',                                        0.829, 'lm',    '420M'),
    ('AntiBERTy',                                     0.828, 'lm',    '26M'),
    ('AbLang-L',                                      0.819, 'lm',    '86M'),
    ('VHHBERT',                                       0.818, 'lm',    '86M'),
    ('Model 3: 12-feat leave-NbBench-out LR',         0.817, 'ours',  '13'),
    ('NanoBERT',                                      0.815, 'lm',    '15M'),
    ('Model 4: H3-charge zero-training',              0.726, 'ours',  '0'),
]

color_map = {
    'ours1': '#d62728',   # bright red for Model 1 (headline)
    'ours':  '#ff9896',   # lighter red for our other models
    'lm':    '#7f7f7f',   # gray for language models
}

names  = [r[0] for r in rows]
aucs   = [r[1] for r in rows]
cats   = [r[2] for r in rows]
sizes  = [r[3] for r in rows]
colors = [color_map[c] for c in cats]

fig, ax = plt.subplots(figsize=(8.2, 6.2))

y_pos = list(range(len(rows)))[::-1]
bars = ax.barh(y_pos, aucs, color=colors, edgecolor='black', linewidth=0.4, height=0.78)

# Annotate AUROC + params
for i, (bar, auc, size, cat) in enumerate(zip(bars, aucs, sizes, cats)):
    weight = 'bold' if cat == 'ours1' else 'normal'
    ax.text(auc + 0.002, bar.get_y() + bar.get_height() / 2,
            f'{auc:.3f}', va='center', fontsize=8.5, fontweight=weight)
    # Size label next to AUROC
    size_text = f'  ({size} params)' if size != '0' else '  (zero-training)'
    ax.text(auc + 0.013, bar.get_y() + bar.get_height() / 2,
            size_text, va='center', fontsize=7.5, style='italic',
            color='#555555')

ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=9)

# Bold Model 1's label
for label, cat in zip(ax.get_yticklabels(), cats):
    if cat == 'ours1':
        label.set_fontweight('bold')
        label.set_color(color_map['ours1'])

ax.set_xlim(0.70, 0.88)
ax.set_xlabel('Test AUROC on NbBench PolyRx (n = 24,955); model size in italics')
ax.set_title('Ranked performance: hand-crafted features vs. 11 pretrained language models',
             fontsize=11, pad=8)
ax.grid(alpha=0.2, axis='x', linestyle='--')

# Legend
legend_patches = [
    mpatches.Patch(color=color_map['ours1'], label='Our primary model (13-feat CDR-only)'),
    mpatches.Patch(color=color_map['ours'],  label='Our other linear models'),
    mpatches.Patch(color=color_map['lm'],    label='NbBench language models'),
]
ax.legend(handles=legend_patches, loc='upper center',
          bbox_to_anchor=(0.5, -0.08), ncol=3,
          fontsize=9, frameon=True, framealpha=0.95)

plt.tight_layout()
plt.savefig('/home/claude/polyatlas-peds/figures/figure3_comparison.png',
            dpi=300, bbox_inches='tight')
plt.close()
print('Figure 3 saved.')
