"""Figure 5. External validation on Chen et al. 2024 human antibodies.

Option-3 layout: every A/B bar evaluated on ONE common stratified held-out test set
(n=16,000), grouped into (i) External validation (frozen zero-shot + charge baselines)
and (ii) Within-Chen recalibration (refit models, exploratory upper bound).
(A) AUROC, (B) AUPRC, (C) coefficient conservation.

Data: chen_fig5_merged.json.
"""
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from pathlib import Path

HERE = Path(__file__).resolve().parent
# resolve the results JSON whether run from figures_revision/ or chen_validation/
def _find(name):
    for cand in [HERE/name, HERE.parent/'chen_validation'/name, HERE/'..'/'chen_validation'/name]:
        if Path(cand).exists(): return str(cand)
    return name

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.labelsize': 10.5,
    'axes.titlesize': 11.5, 'axes.spines.top': False, 'axes.spines.right': False,
})

M = json.load(open(_find('chen_fig5_merged.json')))
CT = M['common_test']
N_TEST = M['n_test']

C_FROZEN = '#d62728'   # frozen zero-shot (headline)
C_CHG    = '#8c6bb1'   # charge baselines
C_REFIT  = '#ff9896'   # refit (recalibration)

# order: external-validation group first (frozen + charge baselines), then recalibration group
groups = [
    ('External validation (zero-shot)', [
        ('Frozen\nModel 1',        'frozen',      C_FROZEN),
        ('Full-seq\ncharge',       'full_charge', C_CHG),
        ('Full-seq\npI',           'full_pi',     C_CHG),
        ('CDR-H3\ncharge',         'h3_charge',   C_CHG),
    ]),
    ('Within-Chen recalibration', [
        ('Refit\n13-feat',         'refit13',     C_REFIT),
        ('Refit\n52-feat',         'refit52',     C_REFIT),
    ]),
]

def val(key, metric):
    d = CT[key]
    return d[metric] if isinstance(d, dict) else d

fig = plt.figure(figsize=(13.5, 10.8))
gs = GridSpec(2, 2, height_ratios=[1.0, 1.15], hspace=0.5, wspace=0.24)
axA = fig.add_subplot(gs[0, 0]); axB = fig.add_subplot(gs[0, 1]); axC = fig.add_subplot(gs[1, :])

def bar_panel(ax, metric, ylabel, title, ref, ref_label):
    xpos = []; x = 0.0; labels = []; heights = []; colors = []; groupspans = []
    for gname, conds in groups:
        start_idx = len(labels)
        for lab, key, col in conds:
            xpos.append(x); labels.append(lab); heights.append(val(key, metric)); colors.append(col); x += 1
        groupspans.append((gname, start_idx, len(labels)-1)); x += 0.8  # gap between groups
    bars = ax.bar(xpos, heights, color=colors, edgecolor='black', linewidth=0.6, width=0.72)
    # CI whisker on frozen (AUROC only)
    if metric == 'auroc':
        ci = CT['frozen']['auroc_ci']
        ax.plot([xpos[0], xpos[0]], ci, color='black', lw=1.2)
        ax.plot([xpos[0]-0.09, xpos[0]+0.09], [ci[0], ci[0]], color='black', lw=1.2)
        ax.plot([xpos[0]-0.09, xpos[0]+0.09], [ci[1], ci[1]], color='black', lw=1.2)
    ax.axhline(ref, ls='--', color='#1a3a66', lw=1.5)
    ax.text(xpos[-1], ref+0.006, ref_label, color='#1a3a66', ha='right', va='bottom', fontsize=8, weight='bold')
    ax.axhline(0.5, ls=':', color='#555', lw=1.0)
    ax.text(xpos[-1], 0.508, 'chance', color='#333', ha='right', va='bottom', fontsize=7.5, weight='bold')
    for xi, h in zip(xpos, heights):
        ax.text(xi, h+0.006, f'{h:.3f}', ha='center', va='bottom', fontsize=8.5)
    # group header brackets
    for gname, s, e in groupspans:
        xs, xe = xpos[s], xpos[e]
        ax.text((xs+xe)/2, 1.005, gname, transform=ax.get_xaxis_transform(),
                ha='center', va='bottom', fontsize=8.5, style='italic', color='#333')
        ax.plot([xs-0.35, xe+0.35], [1.0, 1.0], transform=ax.get_xaxis_transform(),
                color='#999', lw=0.8, clip_on=False)
    ax.set_xticks(xpos); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel(ylabel); ax.set_ylim(0.45, 1.02)
    ax.set_title(title, loc='left', fontsize=11, weight='bold')

bar_panel(axA, 'auroc', f'AUROC (common test, n={N_TEST:,})', '(A) Cross-species transfer \u2014 AUROC',
          0.834, 'NbBench in-domain (0.834)')
bar_panel(axB, 'auprc', f'AUPRC (common test, n={N_TEST:,})', '(B) Cross-species transfer \u2014 AUPRC',
          0.836, 'NbBench in-domain (0.836)')

# ---------- Panel C: coefficient conservation ----------
lim = 2.1
feats = list(CT['refit_coef'].keys())
nb = [CT['nbbench_coef'][f] for f in feats]
ch = [CT['refit_coef'][f] for f in feats]
def is_charge(f): return any(k in f for k in ['charge','_R','pos_frac','neg_frac','abs_charge','_pI'])
order = sorted(range(len(feats)), key=lambda i:-abs(nb[i]))
num_of = {feats[i]:r for r,i in enumerate(order,1)}
axC.axhline(0, color='black', lw=0.8); axC.axvline(0, color='black', lw=0.8)
axC.plot([-1.0,2.1],[-1.0,2.1], ls='--', color='gray', lw=0.8, zorder=1)
axC.axhspan(0,lim,xmin=0.5,xmax=1.0,color='#f0f0f0',zorder=0)
axC.axhspan(-lim,0,xmin=0.0,xmax=0.5,color='#f0f0f0',zorder=0)
jitter={'H1_arom':(0.045,0.045),'H3_abs_charge':(-0.045,-0.045)}
for f,xnb,ych in zip(feats,nb,ch):
    same=(xnb>=0)==(ych>=0); charge=is_charge(f)
    if charge and same: mc,ec,mk=C_FROZEN,'black','o'
    elif same: mc,ec,mk='#bbbbbb','black','o'
    else: mc,ec,mk='white','black','s'
    jx,jy=jitter.get(f,(0,0))
    axC.scatter(xnb+jx,ych+jy,s=170,c=mc,edgecolors=ec,linewidth=1.0,marker=mk,zorder=4)
    axC.text(xnb+jx,ych+jy,str(num_of[f]),fontsize=7.3,ha='center',va='center',
             color='white' if (charge and same) else 'black',zorder=5,weight='bold')
axC.set_xlim(-1.0,1.0); axC.set_ylim(-lim,lim)
axC.set_xlabel('NbBench coefficient (camelid nanobody, frozen)')
axC.set_ylabel('Chen refit coefficient (human antibody)')
axC.set_title('(C) Charge coefficients conserved across species', loc='left', fontsize=11, weight='bold')
axC.text(1.03,0.99,'Feature key',transform=axC.transAxes,fontsize=9,weight='bold',va='top')
for j,i in enumerate(order):
    f=feats[i]; same=(nb[i]>=0)==(ch[i]>=0); charge=is_charge(f)
    col=C_FROZEN if (charge and same) else ('#666' if same else 'black')
    yc=0.93-j*0.066
    axC.text(1.03,yc,f'{num_of[f]}.',transform=axC.transAxes,fontsize=8,va='top',ha='left',color=col,weight='bold')
    axC.text(1.09,yc,f,transform=axC.transAxes,fontsize=8,va='top',ha='left')
legC=[mpatches.Patch(facecolor=C_FROZEN,edgecolor='black',label='Charge feature, sign conserved'),
      mpatches.Patch(facecolor='#bbbbbb',edgecolor='black',label='Other feature, sign conserved'),
      mpatches.Patch(facecolor='white',edgecolor='black',label='Sign flipped (3 weak terms)')]
axC.legend(handles=legC,loc='lower right',fontsize=8,frameon=True)
axC.text(-0.97,lim-0.15,'10 of 13 signs conserved\n(all charge terms agree)',fontsize=8.5,style='italic',va='top')

fig.subplots_adjust(right=0.82,left=0.07,top=0.93,bottom=0.06)
fig.savefig('figure5_chen_validation.pdf', bbox_inches='tight')
fig.savefig('figure5_chen_validation.tif', dpi=350, bbox_inches='tight', pil_kwargs={'compression':'tiff_lzw'})
fig.savefig('figure5_chen_validation.png', dpi=150, bbox_inches='tight')
print('Figure 5 (option-3, common test) saved')
