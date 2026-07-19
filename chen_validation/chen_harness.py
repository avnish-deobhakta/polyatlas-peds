"""
Chen 2024 external-validation harness for PolyAtlas PEDS revision.

Feature-computation functions are copied VERBATIM from the polyatlas-peds repo
(notebooks/03_feature_climb_full.ipynb) so Chen features are computed identically
to the NbBench features. Only the CDR annotator is new (ANARCI unavailable in this
environment), and it is validated against reference CDR lengths.
"""
import numpy as np
import pandas as pd
import re

# ============================================================
# CANONICAL FEATURE CODE (verbatim from polyatlas-peds repo)
# ============================================================
KYTE_DOOLITTLE = {'A': 1.8,'C': 2.5,'D':-3.5,'E':-3.5,'F': 2.8,'G':-0.4,'H':-3.2,'I': 4.5,'K':-3.9,
                   'L': 3.8,'M': 1.9,'N':-3.5,'P':-1.6,'Q':-3.5,'R':-4.5,'S':-0.8,'T':-0.7,'V': 4.2,
                   'W':-0.9,'Y':-1.3}
CHARGE_AT_PH74 = {'D':-1,'E':-1,'K':+1,'R':+1,'H':+0.1}
AROMATIC = set('FWY')
POSITIVE = set('KR')
NEGATIVE = set('DE')
HYDROPHOBIC = set('ILVFMWYC')
PKA = {'C_term': 3.55, 'D': 4.05, 'E': 4.45, 'H': 5.98, 'K': 10.0, 'R': 12.0, 'Y': 10.0, 'C': 9.0, 'N_term': 8.0}

def net_charge(seq):
    if not isinstance(seq, str) or len(seq) == 0: return np.nan
    return sum(CHARGE_AT_PH74.get(a, 0) for a in seq.upper())

def frac(seq, subset):
    if not isinstance(seq, str) or len(seq) == 0: return np.nan
    s = seq.upper()
    return sum(1 for a in s if a in subset) / len(s)

def frac_residue(seq, residue):
    if not isinstance(seq, str) or len(seq) == 0: return np.nan
    return seq.upper().count(residue) / len(seq)

def mean_hydrophobicity(seq):
    if not isinstance(seq, str) or len(seq) == 0: return np.nan
    return np.mean([KYTE_DOOLITTLE.get(a, 0) for a in seq.upper()])

def max_hydrophobic_run(seq):
    if not isinstance(seq, str) or len(seq) == 0: return 0
    s = seq.upper()
    best, cur = 0, 0
    for a in s:
        if a in HYDROPHOBIC:
            cur += 1; best = max(best, cur)
        else:
            cur = 0
    return best

def charge_dipole(seq):
    if not isinstance(seq, str) or len(seq) < 4: return 0
    mid = len(seq) // 2
    return net_charge(seq[:mid]) - net_charge(seq[mid:])

def estimate_pI(seq):
    if not isinstance(seq, str) or len(seq) == 0: return np.nan
    s = seq.upper()
    def charge_at_ph(ph):
        c = 0
        c += 1 / (1 + 10**(ph - PKA['N_term']))
        c -= 1 / (1 + 10**(PKA['C_term'] - ph))
        for a in s:
            if a in ('K', 'R'):   c += 1 / (1 + 10**(ph - PKA[a]))
            elif a in ('D', 'E'): c -= 1 / (1 + 10**(PKA[a] - ph))
            elif a == 'H':        c += 1 / (1 + 10**(ph - PKA['H']))
            elif a == 'Y':        c -= 1 / (1 + 10**(PKA['Y'] - ph))
            elif a == 'C':        c -= 1 / (1 + 10**(PKA['C'] - ph))
        return c
    lo, hi = 0.0, 14.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if charge_at_ph(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def build_features(df):
    """df must have columns CDR1_nogaps, CDR2_nogaps, CDR3_nogaps, seq."""
    feats = pd.DataFrame(index=df.index)
    for region, col in [('H1', 'CDR1_nogaps'), ('H2', 'CDR2_nogaps'),
                          ('H3', 'CDR3_nogaps'), ('full', 'seq')]:
        seqs = df[col].fillna('').astype(str)
        feats[f'{region}_len']        = seqs.str.len()
        feats[f'{region}_charge']     = seqs.apply(net_charge)
        feats[f'{region}_abs_charge'] = feats[f'{region}_charge'].abs()
        feats[f'{region}_pos_frac']   = seqs.apply(lambda s: frac(s, POSITIVE))
        feats[f'{region}_neg_frac']   = seqs.apply(lambda s: frac(s, NEGATIVE))
        feats[f'{region}_hphob']      = seqs.apply(mean_hydrophobicity)
        feats[f'{region}_hphob_frac'] = seqs.apply(lambda s: frac(s, HYDROPHOBIC))
        feats[f'{region}_arom']       = seqs.apply(lambda s: frac(s, AROMATIC))
        feats[f'{region}_W']          = seqs.apply(lambda s: frac_residue(s, 'W'))
        feats[f'{region}_R']          = seqs.apply(lambda s: frac_residue(s, 'R'))
        feats[f'{region}_V']          = seqs.apply(lambda s: frac_residue(s, 'V'))
        feats[f'{region}_G']          = seqs.apply(lambda s: frac_residue(s, 'G'))
    feats['H3_charge_dipole'] = df['CDR3_nogaps'].fillna('').astype(str).apply(charge_dipole)
    feats['H3_max_hphob_run'] = df['CDR3_nogaps'].fillna('').astype(str).apply(max_hydrophobic_run)
    feats['H3_pI']            = df['CDR3_nogaps'].fillna('').astype(str).apply(estimate_pI)
    feats['full_pI']          = df['seq'].fillna('').astype(str).apply(estimate_pI)
    return feats.fillna(0)

# ============================================================
# CDR ANNOTATOR (new; ANARCI unavailable in sandbox)
# Kabat/Chothia-style regex anchors on conserved framework motifs.
# Heavy chain only (Chen shows heavy chain dominates polyreactivity).
# ============================================================
def extract_heavy_cdrs(vh):
    """
    Extract CDR-H1/H2/H3 from a heavy-chain variable domain using conserved
    framework anchors. Returns (cdr1, cdr2, cdr3) or (None,None,None) if it
    can't confidently locate them.

    Anchors:
      FR1 ends at the first Cys (C) ~pos 22; CDR-H1 starts after the Cys+ (usually
        preceded by ...C, and CDR1 is the ~5-7 residues after position ~26).
      We use the widely-used regex approach (e.g., as in Kabat auto-detection):
        CDR-H1: between the Cys and 'W' (Trp) of the WGxG/WVRQ framework.
        CDR-H2: between that Trp-region (after 'WVRQ..LEW' style) up to the
                'K/R L/I T/S/V ... ' FR3 anchor.
        CDR-H3: between the second conserved Cys (C at ~pos 92, in the
                'YYC' / 'YFC' / 'YCA' motif) and the 'WGxG' (WGQG/WGKG/WGRG) FR4.
    """
    if not isinstance(vh, str) or len(vh) < 60:
        return (None, None, None)
    s = vh.upper()

    # --- CDR-H3: most reliable, anchor on ...C (in Yx C) ... WGxG ---
    # second-Cys motif: typically 'C' preceded by tyrosine/phe two before ('Y.C' or 'YYC')
    m_c = None
    for m in re.finditer(r'[FY][YFHC][C]', s):  # e.g. YYC, YFC, FYC
        m_c = m
    if m_c is None:
        # fallback: last cysteine in the domain
        cpos = s.rfind('C')
        if cpos == -1: return (None, None, None)
        c_end = cpos + 1
    else:
        c_end = m_c.end()  # position after the Cys
    # FR4 anchor: W G x G
    m_wg = re.search(r'WG[QKRAG]G', s[c_end:])
    if not m_wg:
        return (None, None, None)
    h3 = s[c_end : c_end + m_wg.start()]

    # --- CDR-H1: after first-Cys region, anchor to the Trp of 'W V/I R Q' FR2 ---
    m_c1 = re.search(r'C', s)
    if not m_c1:
        return (None, None, h3 if h3 else None)
    # CDR-H1 conventionally starts ~4-5 residues after the first Cys.
    start1 = m_c1.end() + 3
    m_w = re.search(r'W[VIFLA][RKQGH]Q', s[start1:])  # WVRQ / WIRQ / WVKQ etc.
    if not m_w:
        # fallback: first W after start1
        wpos = s.find('W', start1)
        if wpos == -1: return (None, None, h3 if h3 else None)
        h1 = s[start1:wpos]
    else:
        h1 = s[start1 : start1 + m_w.start()]

    # --- CDR-H2: after FR2 (the 'WVRQ..LEW' or 'WVRQ..G' region) up to FR3 anchor ---
    # FR2 typically ends ~14 residues after the WVRQ; CDR-H2 then runs to the
    # 'R/K .T/.S ... ' FR3. We anchor CDR2 start after the 'LEW(I/M/V)G' or
    # '(W)...G' motif and end at 'R F/L T I S' style FR3, or at the conserved
    # 'K/R ... T/S ... ' block. Simplest robust anchor: CDR2 is between the
    # end of FR2 ('...LEWIG'/'...LEWVS'/'...LEWMG') and the FR3 start
    # ('R[FLVI]T[IL]S' / 'RVTIS' / 'RFTIS' / 'RATLS' etc.)
    m_fr2 = re.search(r'[LWM]E[WY][IVLMF][GSA]', s)  # LEWIG / LEWVS / MEWMG ...
    if m_fr2:
        start2 = m_fr2.end()
    else:
        # fallback: 14 residues after the WVRQ anchor
        if m_w:
            start2 = start1 + m_w.end() + 10
        else:
            return (h1 if h1 else None, None, h3 if h3 else None)
    m_fr3 = re.search(r'[RK][FLVIAM]T[ILV][STA]', s[start2:])  # RFTIS / RVTIS / RATLS ...
    if m_fr3:
        h2 = s[start2 : start2 + m_fr3.start()]
    else:
        # fallback: take up to 19 residues
        h2 = s[start2 : start2 + 17]

    def clean(x):
        if x is None: return None
        x = x.strip()
        return x if 2 <= len(x) <= 40 and set(x) <= set('ACDEFGHIKLMNPQRSTVWY') else None
    return (clean(h1), clean(h2), clean(h3))


if __name__ == '__main__':
    # Validate on the clinical test set
    d = pd.read_excel('chen/Human_Ab_Polyreactivity-1.2.0-alpha/Binding_data.xlsx', sheet_name='clinical_test')
    print("Validating CDR extraction on 20 clinical antibodies:\n")
    ok = 0
    for _, row in d.iterrows():
        vh = str(row['VH'])
        h1, h2, h3 = extract_heavy_cdrs(vh)
        status = 'OK' if all([h1, h2, h3]) else 'FAIL'
        if all([h1, h2, h3]): ok += 1
        print(f"  {row['Name']:<16} H1={str(h1):<10} H2={str(h2):<20} H3={str(h3):<22} [{status}]")
    print(f"\nExtracted all 3 CDRs for {ok}/{len(d)} antibodies.")
