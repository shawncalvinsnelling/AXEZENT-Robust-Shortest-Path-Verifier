import itertools
import json
import random
import unittest
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from gaugerail import Graph, Edge, parse, F

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return parse(json.loads((ROOT / 'examples' / name).read_text()))


def brute_regret(g, p):
    paths = g.enumerate_paths()
    extreme = None
    for bits in itertools.product([0, 1], repeat=len(g.edges)):
        weights = {e.id: e.base + (e.hi if bit else e.lo) for e, bit in zip(g.edges, bits)}
        best = min(g.cost(q, weights) for q in paths)
        regret = g.cost(p, weights) - best
        if extreme is None or regret > extreme:
            extreme = regret
    return extreme


class TestGaugeRail(unittest.TestCase):
    def test_examples(self):
        g, p = load('robust_route.json')
        a = g.analyze(p)
        self.assertTrue(a['robust'])
        self.assertEqual(a['worst_regret'], '0')
        self.assertTrue(g.verify_certificate(p, a['distance_certificate']))
        h, p2 = load('nonrobust_route.json')
        b = h.analyze(p2)
        self.assertFalse(b['robust'])
        self.assertEqual(F(b['worst_regret']), brute_regret(h,p2))
        self.assertTrue(b['witness_path'])

    def test_adversarial_random_exhaustive_250(self):
        rng = random.Random(20261106)
        for _ in range(250):
            n = rng.randint(3, 6)
            nodes = [f'v{k}' for k in range(n)]
            edges = []
            # Chain provides a route; additional DAG edges provide competition.
            for i in range(n-1):
                edges.append(Edge(f'e{i}_{i+1}',nodes[i],nodes[i+1],rng.randint(-3,9),-rng.randint(0,2),rng.randint(0,3)))
            for i in range(n):
                for j in range(i+2,n):
                    if rng.random() < .3 and len(edges)<11:
                        edges.append(Edge(f'e{i}_{j}',nodes[i],nodes[j],rng.randint(-3,10),-rng.randint(0,2),rng.randint(0,3)))
            g = Graph(nodes,edges,nodes[0],nodes[-1]); p = [f'e{i}_{i+1}' for i in range(n-1)]
            a = g.analyze(p)
            self.assertEqual(F(a['worst_regret']), brute_regret(g,p))
            if a['robust']:
                self.assertTrue(g.verify_certificate(p, a['distance_certificate']))
            else:
                w = {k:F(v) for k,v in a['adversarial_costs'].items()}
                self.assertEqual(g.cost(p,w)-g.cost(a['witness_path'],w),F(a['worst_regret']))

    def test_potential_gauge_100(self):
        rng = random.Random(9281)
        g,p = load('nonrobust_route.json')
        for _ in range(100):
            pot = {v:Q(rng.randint(-1000,1000),rng.randint(1,20)) for v in g.nodes}
            weights=g.scenario(p)
            transformed={e.id:weights[e.id]+pot[e.v]-pot[e.u] for e in g.edges}
            expected=pot[g.t]-pot[g.s]
            for path in g.enumerate_paths():
                self.assertEqual(g.cost(path,transformed)-g.cost(path,weights),expected)

    def test_tamper_cert(self):
        g,p=load('robust_route.json')
        d=g.analyze(p)['distance_certificate']
        for v in list(d):
            altered=dict(d); altered[v]=str(F(altered[v])+Q(1,7))
            with self.assertRaises(AssertionError):
                g.verify_certificate(p,altered)

    def test_subdivision(self):
        g,p=load('nonrobust_route.json')
        for edge in g.edges:
            mid='sub_'+edge.id
            e1=Edge(edge.id+'_1',edge.u,mid,edge.base/2,edge.lo/3,edge.hi/3)
            e2=Edge(edge.id+'_2',mid,edge.v,edge.base/2,edge.lo*2/3,edge.hi*2/3)
            h=Graph(g.nodes+[mid],[e for e in g.edges if e.id!=edge.id]+[e1,e2],g.s,g.t)
            pp=[]
            for id in p:
                pp.extend([e1.id,e2.id] if id==edge.id else [id])
            self.assertEqual(h.analyze(pp)['worst_regret'],g.analyze(p)['worst_regret'])

    def test_radius(self):
        g,p=load('robust_route.json')
        amp={e.id:Q(1) for e in g.edges}
        r=g.exact_radius(p,amp)
        self.assertEqual(r,Q(1)) # path s-b-t: cost gap 4 / 4 differing edges
        for factor,should_hold in [(Q(1,2),True),(Q(1),True),(Q(3,2),False)]:
            e2=[Edge(e.id,e.u,e.v,e.base,-factor,factor) for e in g.edges]
            g2=Graph(g.nodes,e2,g.s,g.t)
            self.assertEqual(g2.analyze(p)['robust'],should_hold)

    def test_rational_validation(self):
        with self.assertRaises(TypeError):
            F(0.1)
        with self.assertRaises(ValueError):
            Edge('bad','a','b',0,2,1)
        with self.assertRaises(ValueError):
            Graph(['a','b'],[Edge('x','a','b',0,0,0),Edge('y','b','a',0,0,0)],'a','b')

if __name__ == '__main__':
    unittest.main()

class TestGaugeCharacterization(unittest.TestCase):
    def test_gauge_detected_and_witnessed(self):
        g,p = load('robust_route.json')
        pot={'s':Q(-4),'a':Q(3,2),'b':Q(9),'t':Q(7)}
        shifts={e.id:pot[e.v]-pot[e.u] for e in g.edges}
        x=g.gauge_audit(shifts)
        self.assertTrue(x['is_gauge'])
        self.assertEqual(x['observable_dimensions'], len(g.edges)-len(g.nodes)+1)
        shifts['at']+=Q(1,4)
        y=g.gauge_audit(shifts)
        self.assertFalse(y['is_gauge'])
        self.assertNotEqual(y['first_shift'],y['second_shift'])
        self.assertEqual(g.cost(y['first_path'],shifts),F(y['first_shift']))

    def test_random_nongauge_witnesses(self):
        rng=random.Random(76)
        g,p=load('robust_route.json')
        for _ in range(200):
            shifts={e.id:Q(rng.randint(-10,10),rng.randint(1,8)) for e in g.edges}
            result=g.gauge_audit(shifts)
            costs={g.cost(q,shifts) for q in g.enumerate_paths()}
            self.assertEqual(result['is_gauge'],len(costs)==1)
            if not result['is_gauge']:
                self.assertNotEqual(F(result['first_shift']),F(result['second_shift']))
