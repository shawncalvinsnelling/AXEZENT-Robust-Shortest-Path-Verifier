"""Adversarial, property, and exact correlated-factor regression tests."""
import copy
import itertools
import json
import random
import sys
import unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gaugerail import Graph, Edge, parse, F


def load(name):
    return parse(json.loads((ROOT / 'examples' / name).read_text()))


class MaliciousCertificateTests(unittest.TestCase):
    def setUp(self):
        self.g, self.p = load('robust_route.json')
        self.cert = self.g.analyze(self.p)
        self.assertTrue(self.g.verify_claim(self.p, self.cert))

    def rejection(self, change):
        cert = copy.deepcopy(self.cert)
        change(cert)
        with self.assertRaises((AssertionError, ValueError, KeyError, TypeError)):
            self.g.verify_claim(self.p, cert)

    def test_good_certificate_and_modified_fields(self):
        def cases():
            yield lambda c: c.update(graph_sha256='0' * 64)
            yield lambda c: c.pop('graph_sha256')
            yield lambda c: c.update(candidate=['sb', 'bt'])
            yield lambda c: c.update(status='EXACT_COUNTEREXAMPLE')
            yield lambda c: c.update(robust='True')
            yield lambda c: c.update(worst_regret='1')
            yield lambda c: c.update(peer_reviewed=True)
            yield lambda c: c.update(candidate_extremal_cost='0')
            yield lambda c: c.update(shortest_extremal_cost='0')
            yield lambda c: c.update(witness_path=['sb','bt'])
            yield lambda c: c.update(adversarial_costs={'sa':'0'})
            yield lambda c: c.update(distance_certificate=None)
            yield lambda c: c['distance_certificate'].pop('a')
            yield lambda c: c['distance_certificate'].update(ghost='123')
            yield lambda c: c['distance_certificate'].update(t='1')
            yield lambda c: c['distance_certificate'].update(s='777')
            yield lambda c: c['distance_certificate'].update(a='777')
        for fn in cases():
            with self.subTest(case=fn.__code__.co_firstlineno):
                self.rejection(fn)

    def test_bad_candidate_path_is_not_accepted(self):
        for bad in [['sa'], ['sa','bt'], ['missing'], [], ['sb','bt']]:
            with self.subTest(bad=bad):
                with self.assertRaises((AssertionError, ValueError)):
                    self.g.verify_claim(bad, self.cert)

    def test_nonrobust_path_cannot_forge_proof(self):
        g, p = load('nonrobust_route.json')
        bad = g.analyze(p)
        bad['status'] = 'PROVED_EXACT_CERTIFICATE'
        bad['robust'] = True
        bad['worst_regret'] = '0'
        bad['distance_certificate'] = self.cert['distance_certificate']
        with self.assertRaises((AssertionError, ValueError)):
            g.verify_claim(p, bad)

    def test_changed_network_cannot_reuse_certificate(self):
        edges = [Edge(e.id, e.u, e.v, e.base + (1 if e.id == 'sa' else 0), e.lo, e.hi) for e in self.g.edges]
        other = Graph(self.g.nodes, edges, self.g.s, self.g.t)
        with self.assertRaises(AssertionError):
            other.verify_claim(self.p, self.cert)

    def test_forged_claim_ignoring_candidate_metadata_rejected(self):
        bad = copy.deepcopy(self.cert)
        bad['candidate'] = ['sb', 'bt']
        # The previous CLI verified only distance inequalities for the *input*
        # candidate, ignoring the embedded certificate candidate. Now rejects.
        self.rejection(lambda c: c.update(candidate=bad['candidate']))


class CorrelatedFactorTests(unittest.TestCase):
    def test_symmetric_box_exact_radius(self):
        g, p = load('robust_route.json')
        # P has 2 unit loads, rivals 0 loads: gap 4 / sensitivity 2 = 2;
        # direct edge rival is gap 3/2 = 1.5, so radius is 3/2.
        lam = {e.id: ['1' if e.id in p else '0'] for e in g.edges}
        out = g.correlated_box(p, lam, ['1'], '3/2')
        self.assertEqual(out['sharp_radius'], '3/2')
        self.assertTrue(out['robust_at_radius'])
        self.assertEqual(out['worst_regret'], '0')
        bad = g.correlated_box(p, lam, ['1'], '2')
        self.assertFalse(bad['robust_at_radius'])
        self.assertEqual(bad['worst_regret'], '1')
        self.assertEqual(bad['witness_factors'], ['2'])

    def test_coupling_cancels_and_radius_infinite(self):
        g, p = load('robust_route.json')
        lam = {e.id: ['1' if e.id == 'sa' else '-1' if e.id == 'at' else '0'] for e in g.edges}
        a = g.correlated_box(p, lam, ['3'], '10000')
        self.assertEqual(a['sharp_radius'], '+infinity')
        self.assertTrue(a['robust_at_radius'])
        self.assertIsNone(a['limiting_path'])

    def test_anticorrelated_paths_no_single_favored_scenario(self):
        g = Graph(['s','a','b','t'],
                  [Edge('sa','s','a',0,0,0),Edge('at','a','t',0,0,0),
                   Edge('sb','s','b',0,0,0),Edge('bt','b','t',0,0,0)],'s','t')
        p = ['sa','at']
        lam = {'sa':[1], 'at':[0], 'sb':[-1], 'bt':[0]}
        out = g.correlated_box(p,lam,[1],Q(1,2))
        self.assertEqual(out['sharp_radius'], '0')
        self.assertEqual(out['worst_regret'],'1')
        self.assertEqual(out['witness_path'],['sb','bt'])

    def test_random_small_graphs_vs_exhaustive_factor_corners(self):
        rng = random.Random(20261106)
        for trial in range(180):
            n = rng.randint(3,6)
            vertices = [f'v{i}' for i in range(n)]
            edges = [Edge(f'e{i}_{i+1}',vertices[i],vertices[i+1],rng.randint(0,9),0,0)
                     for i in range(n-1)]
            for i in range(n):
                for j in range(i+2,n):
                    if rng.random()<0.5:
                        edges.append(Edge(f'e{i}_{j}',vertices[i],vertices[j],rng.randint(0,9),0,0))
            g = Graph(vertices,edges,vertices[0],vertices[-1])
            base = {e.id:e.base for e in edges}
            _, p = g.dist_to_t(base)
            k = rng.randint(1,3)
            lam = {e.id:[Q(rng.randint(-3,3)) for _ in range(k)] for e in edges}
            amps = [Q(rng.randint(0,3)) for _ in range(k)]
            rho = Q(rng.randint(0,4),rng.randint(1,4))
            a = g.correlated_box(p,lam,amps,rho)
            all_paths=g.enumerate_paths()
            worst=Q(0)
            for sides in itertools.product([-1,1],repeat=k):
                factors=[rho*amps[j]*sides[j] for j in range(k)]
                weights={e.id:e.base+sum((lam[e.id][j]*factors[j] for j in range(k)),Q(0)) for e in edges}
                worst=max(worst,g.cost(p,weights)-min(g.cost(q,weights) for q in all_paths))
            with self.subTest(trial=trial):
                self.assertEqual(F(a['worst_regret']),worst)
                self.assertEqual(a['robust_at_radius'],worst == 0)
                if a['sharp_radius'] != '+infinity':
                    boundary=F(a['sharp_radius'])
                    self.assertTrue(g.correlated_box(p,lam,amps,boundary)['robust_at_radius'])
                    self.assertFalse(g.correlated_box(p,lam,amps,boundary+Q(1,7))['robust_at_radius'])

    def test_long_chain_iterative_enumeration(self):
        n = 1100  # Larger than typical Python recursion depth.
        nodes = [str(i) for i in range(n)]
        edges = [Edge(f'e{i}', str(i), str(i+1), 1, 0, 0) for i in range(n-1)]
        g = Graph(nodes, edges, nodes[0], nodes[-1])
        p = [e.id for e in edges]
        self.assertEqual(g.enumerate_paths(max_paths=1), [p])
        coeff = {e.id:['1'] for e in edges}
        a = g.correlated_box(p, coeff, [1], '100')
        self.assertEqual(a['sharp_radius'], '+infinity')
        self.assertTrue(a['robust_at_radius'])

    def test_invalid_factors_and_path_cap(self):
        g,p=load('robust_route.json')
        lam={e.id:[1,0] for e in g.edges}
        for bad_lam,bad_amp,radius in [
            ({'sa':[1,0]},[1,1],1),
            (lam,[1],1),
            (lam,[-1,2],1),
            (lam,[1,1],-1),
            (lam,[1.5,1],1),
        ]:
            with self.subTest(radius=radius,amps=bad_amp):
                with self.assertRaises((ValueError,TypeError)):
                    g.correlated_box(p,bad_lam,bad_amp,radius)
        with self.assertRaises(ValueError):
            g.correlated_box(p,lam,[1,1],1,max_paths=1)


if __name__=='__main__':
    unittest.main()
