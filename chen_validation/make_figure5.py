"""Figure 5. External validation on Chen et al. 2024 human antibodies.
(A) AUROC transfer; (B) AUPRC transfer; (C) coefficient conservation (full width).
Data: chen_anarci_results.json (ANARCI run, n=79,999).
"""
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

plt.rcParams.update({
    'font.family': 'Liberation Sans', 'font.size': 10, 'axes.labelsize': 10.5,
    'axes.titlesize': 11.5, 'axes.spines.top': False, 'axes.spines.right': False,
})

R = json.load(open('chen_anarci_results.json'))
C_OURS1, C_OURS, C_CHG = '#d62728', '#ff9896', '#8c6bb1'

conds = [
    ('Frozen Model 1\n(zero refit)', 'modeA', C_OURS1),
    ('Refit 13-feat\nfamily',        'modeB', C_OURS),
    ('Full 52-feat\nrefit',          'modeC', C_OURS),
    ('Full-seq charge\n(1 feat)',    'fchg',  C_CHG),
    ('Full-seq pI\n(1 feat)',        'fpi',   C_CHG),
    ('CDR-H3 charge\n(1 feat)',      'h3chg', C_CHG),
]
auroc = {'modeA': R['modeA_frozen']['auroc'], 'modeB': R['modeB_refit13']['auroc'],
         'modeC': R['modeC_refit52']['auroc'], 'fchg': R['zero']['full_charge'],
         'fpi': R['zero']['full_pi'], 'h3chg': R['zero']['h3_charge']}
auprc = {'modeA': R['modeA_frozen']['auprc'], 'modeB': R['modeB_refit13']['auprc'],
         'modeC': R['modeC_refit52']['auprc'], 'fchg': R['zero_auprc']['full_charge'],
         'fpi': R['zero_auprc']['full_pi'], 'h3chg': R['zero_auprc']['h3_charge']}

fig = plt.figure(figsize=(13.5, 10.5))
gs = GridSpec(2, 2, height_ratios=[1.0, 1.15], hspace=0.5, wspace=0.24)
axA = fig.add_subplot(gs[0, 0]); axB = fig.add_subplot(gs[0, 1]); axC = fig.add_subplot(gs[1, :])

labels = [c[0] for c in conds]; cols = [c[2] for c in conds]; xpos = range(len(conds))

def bar_panel(ax, valmap, ylabel, title, ref_line, ref_label, is_auroc):
    vals = [valmap[c[1]] for c in conds]
    ax.bar(xpos, vals, color=cols, edgecolor='black', linewidth=0.6, width=0.68)
    if is_auroc:
        ci = R['modeA_frozen']['auroc_ci']
        ax.plot([0, 0], ci, color='black', linewidth=1.2)
        ax.plot([-0.08, 0.08], [ci[0], ci[0]], color='black', linewidth=1.2)
        ax.plot([-0.08, 0.08], [ci[1], ci[1]], color='black', linewidth=1.2)
    ax.axhline(ref_line, ls='--', color='#1a3a66', linewidth=1.5)
    ax.text(len(conds)-0.5, ref_line+0.006, ref_label, color='#1a3a66', ha='right', va='bottom', fontsize=8.5, weight='bold')
    ax.axhline(0.5, ls=':', color='#555555', linewidth=1.1)
    ax.text(len(conds)-0.5, 0.508, 'chance', color='#333333', ha='right', va='bottom', fontsize=8, weight='bold')
    for xi, v in zip(xpos, vals):
        ax.text(xi, v+0.006, f'{v:.3f}', ha='center', va='bottom', fontsize=8.5)
    ax.set_xticks(list(xpos)); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel(ylabel); ax.set_ylim(0.45, 1.0)
    ax.set_title(title, loc='left', fontsize=11, weight='bold')

bar_panel(axA, auroc, 'AUROC on Chen 2024\n(n = 79,999)', '(A) Cross-species transfer \u2014 AUROC', 0.834, 'NbBench in-domain (0.834)', True)
bar_panel(axB, auprc, 'AUPRC on Chen 2024\n(n = 79,999)', '(B) Cross-species transfer \u2014 AUPRC', 0.836, 'NbBench in-domain (0.836)', False)

# Panel C
lim = 2.1
feats = list(R['refit_coef'].keys())
nb = [R['nbbench_coef'][f] for f in feats]; ch = [R['refit_coef'][f] for f in feats]
def is_charge(f): return any(k in f for k in ['charge', '_R', 'pos_frac', 'neg_frac', 'abs_charge', '_pI'])
order = sorted(range(len(feats)), key=lambda i: -abs(nb[i]))
num_of = {feats[i]: rank for rank, i in enumerate(order, start=1)}
axC.axhline(0, color='black', linewidth=0.8); axC.axvline(0, color='black', linewidth=0.8)
axC.plot([-1.0, 2.1], [-1.0, 2.1], ls='--', color='gray', linewidth=0.8, zorder=1)
axC.axhspan(0, lim, xmin=0.5, xmax=1.0, color='#f0f0f0', zorder=0)
axC.axhspan(-lim, 0, xmin=0.0, xmax=0.5, color='#f0f0f0', zorder=0)
jitter = {'H1_arom': (0.045, 0.045), 'H3_abs_charge': (-0.045, -0.045)}
for f, xnb, ych in zip(feats, nb, ch):
    same = (xnb >= 0) == (ych >= 0); charge = is_charge(f)
    if charge and same: mc, ec, mk = C_OURS1, 'black', 'o'
    elif same: mc, ec, mk = '#bbbbbb', 'black', 'o'
    else: mc, ec, mk = 'white', 'black', 's'
    jx, jy = jitter.get(f, (0.0, 0.0))
    axC.scatter(xnb+jx, ych+jy, s=170, c=mc, edgecolors=ec, linewidth=1.0, marker=mk, zorder=4)
    txtcol = 'white' if (charge and same) else 'black'
    axC.text(xnb+jx, ych+jy, str(num_of[f]), fontsize=7.3, ha='center', va='center', color=txtcol, zorder=5, weight='bold')
axC.set_xlim(-1.0, 1.0); axC.set_ylim(-lim, lim)
axC.set_xlabel('NbBench coefficient (camelid nanobody, frozen)')
axC.set_ylabel('Chen refit coefficient (human antibody)')
axC.set_title('(C) Charge coefficients conserved across species', loc='left', fontsize=11, weight='bold')
axC.text(1.03, 0.99, 'Feature key', transform=axC.transAxes, fontsize=9, weight='bold', va='top')
for j, i in enumerate(order):
    f = feats[i]; same = (nb[i] >= 0) == (ch[i] >= 0); charge = is_charge(f)
    col = C_OURS1 if (charge and same) else ('#666666' if same else 'black')
    ycoord = 0.93 - j * 0.066
    axC.text(1.03, ycoord, f'{num_of[f]}.', transform=axC.transAxes, fontsize=8, va='top', ha='left', color=col, weight='bold')
    axC.text(1.09, ycoord, f, transform=axC.transAxes, fontsize=8, va='top', ha='left')
legC = [mpatches.Patch(facecolor=C_OURS1, edgecolor='black', label='Charge feature, sign conserved'),
        mpatches.Patch(facecolor='#bbbbbb', edgecolor='black', label='Other feature, sign conserved'),
        mpatches.Patch(facecolor='white', edgecolor='black', label='Sign flipped (3 weak terms)')]
axC.legend(handles=legC, loc='lower right', fontsize=8, frameon=True)
axC.text(-0.97, lim-0.15, '10 of 13 signs conserved\n(all charge terms agree)', fontsize=8.5, style='italic', va='top')

fig.subplots_adjust(right=0.82, left=0.07, top=0.95, bottom=0.06)
fig.savefig('figure5_chen_validation.pdf', bbox_inches='tight')
fig.savefig('figure5_chen_validation.tif', dpi=350, bbox_inches='tight', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig('figure5_chen_validation.png', dpi=150, bbox_inches='tight')
print('Figure 5 (3-panel) saved')
