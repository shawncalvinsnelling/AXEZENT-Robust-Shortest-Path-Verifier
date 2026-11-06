"""Deterministic larger-DAG smoke test; record local timings without promising portability."""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gaugerail import Edge, Graph

n=2500
nodes=[f'v{i}' for i in range(n)]
edges=[Edge(f'path{i}', nodes[i],nodes[i+1],1,0,0) for i in range(n-1)]
for i in range(n-3):
    edges.append(Edge(f'bypass{i}',nodes[i],nodes[i+3],6,-1,1))
path=[f'path{i}' for i in range(n-1)]
t0=time.perf_counter()
g=Graph(nodes,edges,nodes[0],nodes[-1])
a=g.analyze(path)
t1=time.perf_counter()
assert a['robust']
assert g.verify_certificate(path,a['distance_certificate'])
t2=time.perf_counter()
data={'vertices':n,'arcs':len(edges),'robust':a['robust'],'worst_regret':a['worst_regret'],
      'certificate_entries':len(a['distance_certificate']),'analyze_seconds_observed':round(t1-t0,4),
      'verify_seconds_observed':round(t2-t1,4),
      'disclaimer':'Observed times are this runner only; no universal performance claim.'}
(ROOT/'STRESS_RECEIPT.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
