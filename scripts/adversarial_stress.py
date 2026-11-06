"""Repeatable malicious-certificate rejection smoke test; no external services.

This is not a cryptographic penetration test or proof that all attacks are blocked.
Every generated mutation is preselected to invalidate a required check.
"""
from __future__ import annotations
import copy
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from gaugerail import Edge, Graph, F, parse

raw=json.loads((ROOT/'examples/robust_route.json').read_text())
g,p=parse(raw)
original=g.analyze(p)
assert g.verify_claim(p, original)
rng=random.Random(20261106)
MODES = [
 'alter_candidate', 'alter_fingerprint', 'remove_fingerprint',
 'fake_status', 'fake_robust_flag', 'fake_regret',
 'fake_cost', 'fake_optimum', 'fake_distance',
 'missing_distance', 'extra_distance', 'fake_witness',
 'fake_authority_field', 'bad_target_distance', 'bad_path',
 'changed_network',
]

def attempt(mode, i):
    c=copy.deepcopy(original)
    graph=g; route=p
    if mode=='alter_candidate': c['candidate']=['sb','bt']
    elif mode=='alter_fingerprint': c['graph_sha256']='0'*64
    elif mode=='remove_fingerprint': c.pop('graph_sha256')
    elif mode=='fake_status': c['status']='EXACT_COUNTEREXAMPLE'
    elif mode=='fake_robust_flag': c['robust']='true'
    elif mode=='fake_regret': c['worst_regret']='1'
    elif mode=='fake_cost': c['candidate_extremal_cost']='1/2'
    elif mode=='fake_optimum': c['shortest_extremal_cost']='10000'
    elif mode=='fake_distance':
        v=rng.choice(list(c['distance_certificate']))
        c['distance_certificate'][v]=str(F(c['distance_certificate'][v])+Fraction(i+1,1000000))
    elif mode=='missing_distance': c['distance_certificate'].pop('a')
    elif mode=='extra_distance': c['distance_certificate']['fake_node']='0'
    elif mode=='fake_witness': c['witness_path']=['sb','bt']
    elif mode=='fake_authority_field': c['peer_reviewed']=True
    elif mode=='bad_target_distance': c['distance_certificate']['t']='1'
    elif mode=='bad_path': route=['sa','bt']
    elif mode=='changed_network':
        graph=Graph(g.nodes,[Edge(e.id,e.u,e.v,e.base+(i+1 if e.id=='at' else 0),e.lo,e.hi) for e in g.edges],g.s,g.t)
    else: raise RuntimeError(mode)
    try:
        graph.verify_claim(route,c)
    except (AssertionError, ValueError, KeyError, TypeError):
        return True
    return False

counts={m:0 for m in MODES}
failures=[]
for i in range(1024):
    mode=MODES[i%len(MODES)]
    counts[mode]+=1
    if not attempt(mode,i): failures.append({'attempt':i,'mutation':mode})
receipt={
 'name':'AXEZENT GaugeRail-001 v1.2.0 adversarial stress',
 'seed':20261106,
 'valid_certificate_accepted':True,
 'attacks_submitted':sum(counts.values()),
 'invalid_certificates_rejected':sum(counts.values())-len(failures),
 'false_acceptances':len(failures),
 'attack_categories':counts,
 'unexpected_acceptances':failures,
 'limits':'Chosen attack mutations only; not a claim of unforgeability, authenticity, or enterprise security certification',
}
(ROOT/'ADVERSARIAL_RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print(json.dumps(receipt,sort_keys=True,indent=2))
if failures: sys.exit(1)
