# -*- coding: utf-8 -*-
"""Batch 4 sample info query"""
import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

samples = ['SSBR-010', 'SSBR-027', 'SSBR-006', 'SSBR-080', 'SSBR-033', 
           'SSBR-075', 'SSBR-012', 'SSBR-082', 'SSBR-009', 'SSBR-072', 'SSBR-073']

df = pd.read_excel('dataset/数据.xlsx')

cols = {
    'id': 0, 'lit_id': 1, 'source': 2, 'styrene': 3, 'vinyl': 4,
    'mol_type': 6, 'func_type': 7, 'func_reagent': 8, 'func_degree': 9,
    'scenario': 17, 'research': 18, 'tem': 19, 'mech_fig': 20, 'doi': 22,
}

print("=" * 100)
print("Batch 4 Sample Info")
print("=" * 100)

for sample_id in samples:
    row = df[df.iloc[:, 0] == sample_id]
    if row.empty:
        print(f"\n[X] {sample_id}: NOT FOUND")
        continue
    
    r = row.iloc[0]
    print(f"\n{'='*50}")
    print(f"[{sample_id}]")
    print(f"{'='*50}")
    print(f"  Lit ID: {r.iloc[cols['lit_id']]}")
    print(f"  DOI: {r.iloc[cols['doi']]}")
    print(f"  Polymer Type: {r.iloc[cols['mol_type']]}")
    print(f"  Func Type: {r.iloc[cols['func_type']]}")
    print(f"  Func Reagent: {r.iloc[cols['func_reagent']]}")
    print(f"  Styrene: {r.iloc[cols['styrene']]}")
    print(f"  Vinyl: {r.iloc[cols['vinyl']]}")
    print(f"  Scenario: {r.iloc[cols['scenario']]}")
    print(f"  Research: {r.iloc[cols['research']]}")
    print(f"  TEM: {r.iloc[cols['tem']]}")
    print(f"  Mech Fig: {r.iloc[cols['mech_fig']]}")
