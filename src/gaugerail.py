"""AXEZENT GaugeRail-001: exact rational, independent proof verifier.
All computations use Python's standard-library Fraction, never floating point.
An input is a finite directed acyclic multigraph and a directed s-t path.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from collections import deque
import hashlib
from typing import Iterable, Mapping
import json


def F(x) -> Fraction:
    if isinstance(x, float):
        raise TypeError('Float input forbidden: use a rational string or integer')
    return Fraction(x)


def fmt(x: Fraction | None) -> str | None:
    return None if x is None else str(x)


@dataclass(frozen=True)
class Edge:
    id: str
    u: str
    v: str
    base: Fraction
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        object.__setattr__(self, 'base', F(self.base))
        object.__setattr__(self, 'lo', F(self.lo))
        object.__setattr__(self, 'hi', F(self.hi))
        if self.lo > self.hi:
            raise ValueError(f'Invalid interval on {self.id}')


def _topo(nodes: Iterable[str], edges: list[Edge]) -> list[str]:
    nodes = sorted(set(nodes))
    indeg = {x: 0 for x in nodes}
    outgoing = {x: [] for x in nodes}
    for e in edges:
        if e.u not in indeg or e.v not in indeg:
            raise ValueError('An edge has an unknown vertex')
        indeg[e.v] += 1
        outgoing[e.u].append(e)
    q = deque(sorted(x for x in nodes if indeg[x] == 0))
    result = []
    while q:
        u = q.popleft()
        result.append(u)
        for e in outgoing[u]:
            indeg[e.v] -= 1
            if indeg[e.v] == 0:
                q.append(e.v)
    if len(result) != len(nodes):
        raise ValueError('Input graph must be acyclic')
    return result


class Graph:
    def __init__(self, nodes: Iterable[str], edges: Iterable[Edge], s: str, t: str):
        self.nodes = sorted(set(nodes))
        self.edges = list(edges)
        self.s, self.t = s, t
        if s == t or s not in self.nodes or t not in self.nodes:
            raise ValueError('s and t must be different known vertices')
        ids = [e.id for e in self.edges]
        if len(ids) != len(set(ids)):
            raise ValueError('Edge IDs must be unique, including parallel edges')
        self.order = _topo(self.nodes, self.edges)
        self.by_id = {e.id: e for e in self.edges}
        self.out = {u: [] for u in self.nodes}
        self.inc = {u: [] for u in self.nodes}
        for e in self.edges:
            self.out[e.u].append(e)
            self.inc[e.v].append(e)
        self.coreachable = set()
        q = [t]
        while q:
            u = q.pop()
            if u in self.coreachable:
                continue
            self.coreachable.add(u)
            q.extend(e.u for e in self.inc[u])
        if s not in self.coreachable:
            raise ValueError('No s-t route')

    def graph_sha256(self) -> str:
        """Canonical mathematical-input fingerprint; NOT a signature or authentication."""
        obj = {
            'vertices': self.nodes, 'source': self.s, 'target': self.t,
            'edges': [
                {'id': e.id, 'u': e.u, 'v': e.v, 'base': str(e.base),
                 'lo': str(e.lo), 'hi': str(e.hi)}
                for e in sorted(self.edges, key=lambda e: e.id)
            ],
        }
        canonical = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    def path_edges(self, path: Iterable[str]) -> list[Edge]:
        path = list(path)
        if not path:
            raise ValueError('Path must not be empty')
        pos = self.s
        used = []
        for id in path:
            if id not in self.by_id:
                raise ValueError(f'Unknown path edge: {id}')
            e = self.by_id[id]
            if e.u != pos:
                raise ValueError('Broken path')
            pos = e.v
            used.append(e)
        if pos != self.t:
            raise ValueError('Path does not reach target')
        return used

    def scenario(self, path: Iterable[str]) -> dict[str, Fraction]:
        chosen = {e.id for e in self.path_edges(path)}
        return {e.id: e.base + (e.hi if e.id in chosen else e.lo) for e in self.edges}

    def cost(self, path: Iterable[str], weights: Mapping[str, Fraction]) -> Fraction:
        return sum((F(weights[e.id]) for e in self.path_edges(path)), Fraction(0))

    def dist_to_t(self, weights: Mapping[str, Fraction]) -> tuple[dict[str, Fraction], list[str]]:
        # Constructs the certificate; verification below is independent.
        d = {self.t: Fraction(0)}
        pick = {}
        for u in reversed(self.order):
            if u == self.t:
                continue
            choices = [(F(weights[e.id]) + d[e.v], e.id) for e in self.out[u] if e.v in d]
            if choices:
                best, edge_id = min(choices)
                d[u] = best
                pick[u] = edge_id
        path = []
        here = self.s
        while here != self.t:
            e = self.by_id[pick[here]]
            path.append(e.id)
            here = e.v
        return d, path

    def verify_certificate(self, path: Iterable[str], distance: Mapping[str, Fraction | str]) -> bool:
        """An O(|V|+|E|) checker without any shortest-path algorithm."""
        p = self.path_edges(path)
        if set(distance) != self.coreachable:
            raise AssertionError('Certificate must cover exactly t-reachable vertices')
        d = {x: F(distance[x]) for x in self.coreachable}
        if d[self.t] != 0:
            raise AssertionError('d(t) must be 0')
        weights = self.scenario([e.id for e in p])
        for e in self.edges:
            if e.v in self.coreachable:
                if d[e.u] > weights[e.id] + d[e.v]:
                    raise AssertionError(f'Violated edge inequality: {e.id}')
        for e in p:
            if d[e.u] != weights[e.id] + d[e.v]:
                raise AssertionError(f'Non-tight claimed path edge: {e.id}')
        return True

    def verify_claim(self, path: Iterable[str], cert: Mapping) -> bool:
        """Verify a whole claimed robust certificate, including instance and path binding.

        The actual mathematical proof remains the Bellman inequalities + path
        tightness, not the hash. A hash is not an issuer's digital signature.
        """
        path = list(path)
        self.path_edges(path)
        if not isinstance(cert, Mapping):
            raise AssertionError('Certificate must be an object')
        expected = {'status', 'graph_sha256', 'robust', 'candidate',
                    'candidate_extremal_cost', 'shortest_extremal_cost',
                    'worst_regret', 'distance_certificate', 'witness_path',
                    'adversarial_costs'}
        if set(cert) != expected:
            raise AssertionError('Unexpected, missing, or unauthorized claim fields')
        if cert.get('graph_sha256') != self.graph_sha256():
            raise AssertionError('Graph fingerprint mismatch or missing fingerprint')
        if cert.get('candidate') != path:
            raise AssertionError('Claimed route does not match the input route')
        if cert.get('status') != 'PROVED_EXACT_CERTIFICATE' or cert.get('robust') is not True:
            raise AssertionError('Certificate is not a robust-optimality proof')
        if cert.get('worst_regret') != '0':
            raise AssertionError('Certificate claims nonzero or malformed regret')
        if cert.get('witness_path') is not None or cert.get('adversarial_costs') is not None:
            raise AssertionError('A proof certificate cannot contain a counterexample witness')
        d = cert.get('distance_certificate')
        if not isinstance(d, Mapping):
            raise AssertionError('Missing node-potential proof certificate')
        # Edge inequalities and path equalities are the proof; DO NOT run the solver.
        self.verify_certificate(path, d)
        extremal_cost = self.cost(path, self.scenario(path))
        if cert.get('candidate_extremal_cost') != fmt(extremal_cost):
            raise AssertionError('Candidate cost metadata mismatch')
        if cert.get('shortest_extremal_cost') != fmt(extremal_cost):
            raise AssertionError('Optimal cost metadata mismatch')
        if F(d[self.s]) != extremal_cost:
            raise AssertionError('Claimed node potential is inconsistent with route cost')
        return True

    def analyze(self, path: Iterable[str]) -> dict:
        path = list(path)
        self.path_edges(path)
        c = self.scenario(path)
        d, witness = self.dist_to_t(c)
        regret = self.cost(path, c) - d[self.s]
        assert regret >= 0
        if regret == 0:
            self.verify_certificate(path, d)
        else:
            assert self.cost(witness, c) < self.cost(path, c)
        return {
            'status': 'PROVED_EXACT_CERTIFICATE' if regret == 0 else 'EXACT_COUNTEREXAMPLE',
            'graph_sha256': self.graph_sha256(),
            'robust': regret == 0,
            'candidate': path,
            'candidate_extremal_cost': fmt(self.cost(path, c)),
            'shortest_extremal_cost': fmt(d[self.s]),
            'worst_regret': fmt(regret),
            'distance_certificate': {u: fmt(d[u]) for u in sorted(d)} if regret == 0 else None,
            'witness_path': witness if regret > 0 else None,
            'adversarial_costs': {k: fmt(v) for k, v in sorted(c.items())} if regret > 0 else None,
        }

    def enumerate_paths(self, max_paths=200000) -> list[list[str]]:
        """Enumerate valid DAG routes with an explicit stack, abort at path cap.

        This enumeration is potentially exponential and must never silently
        return a truncated set when a caller asks for an exact result.
        """
        if not isinstance(max_paths, int) or isinstance(max_paths, bool) or max_paths < 1:
            raise ValueError('max_paths must be a positive integer')
        routes = []
        path = []
        stack = [(self.s, iter(self.out[self.s]))]
        while stack:
            v, iterator = stack[-1]
            if v == self.t:
                routes.append(path[:])
                if len(routes) > max_paths:
                    raise ValueError('Path enumeration cap exceeded')
                stack.pop()
                if stack:
                    path.pop()
                continue
            try:
                e = next(iterator)
            except StopIteration:
                stack.pop()
                if stack:
                    path.pop()
                continue
            path.append(e.id)
            stack.append((e.v, iter(self.out[e.v])))
        return routes

    def gauge_audit(self, shifts: Mapping[str, Fraction | str]) -> dict:
        """Check path-invisibility of an edge-cost change in linear time.

        Only edges on some s-t path are relevant. For non-gauge changes,
        return two explicit s-t paths with different shifts.
        """
        h = {e.id: F(shifts[e.id]) for e in self.edges}
        reachable = {self.s}
        for u in self.order:
            if u in reachable:
                reachable.update(e.v for e in self.out[u])
        core = reachable.intersection(self.coreachable)
        core_edges = [e for e in self.edges if e.u in core and e.v in core]
        by_out = {v: [] for v in core}
        for e in core_edges:
            by_out[e.u].append(e)
        phi = {self.s: Fraction(0)}
        prev = {self.s: None}
        def prefix(v):
            result = []
            while v != self.s:
                u, edge_id = prev[v]
                result.append(edge_id)
                v = u
            return list(reversed(result))
        for u in self.order:
            if u not in core:
                continue
            for e in by_out[u]:
                val = phi[u] + h[e.id]
                if e.v not in phi:
                    phi[e.v] = val
                    prev[e.v] = (u, e.id)
                elif phi[e.v] != val:
                    # Construct a deterministic route from v to t in core.
                    tail = []
                    here = e.v
                    while here != self.t:
                        next_edge = by_out[here][0]
                        tail.append(next_edge.id)
                        here = next_edge.v
                    p1 = prefix(e.v) + tail
                    p2 = prefix(u) + [e.id] + tail
                    h1 = self.cost(p1, h)
                    h2 = self.cost(p2, h)
                    assert h1 != h2
                    return {'is_gauge': False, 'first_path': p1, 'second_path': p2,
                            'first_shift': fmt(h1), 'second_shift': fmt(h2),
                            'core_vertices': len(core), 'core_edges': len(core_edges)}
        assert set(phi) == core
        return {'is_gauge': True, 'potential': {v: fmt(phi[v]) for v in sorted(phi)},
                'core_vertices': len(core), 'core_edges': len(core_edges),
                'observable_dimensions': len(core_edges)-len(core)+1}

    def exact_radius(self, path: Iterable[str], amplitude: Mapping[str, Fraction | str], max_paths=200000) -> Fraction | None:
        """Sharp symmetric independent uncertainty radius; finite path enumeration.
        None means infinity. Complexity may be exponential (not claimed fast).
        """
        path = list(path)
        self.path_edges(path)
        aa = {e.id: F(amplitude[e.id]) for e in self.edges}
        if any(v < 0 for v in aa.values()):
            raise ValueError('Negative uncertainty magnitude')
        ids = set(path)
        base = {e.id: e.base for e in self.edges}
        cP = self.cost(path, base)
        vals = []
        for other in self.enumerate_paths(max_paths):
            co = self.cost(other, base)
            if co < cP:
                raise ValueError('Candidate not optimal at radius zero')
            diff = ids.symmetric_difference(set(other))
            sensitivity = sum((aa[k] for k in diff), Fraction(0))
            if sensitivity > 0:
                vals.append((co - cP) / sensitivity)
        return min(vals) if vals else None



    def correlated_box(self, path: Iterable[str],
                       coupling: Mapping[str, Iterable[Fraction | str]],
                       factor_amplitudes: Iterable[Fraction | str],
                       radius: Fraction | str | None = None,
                       max_paths: int = 200000) -> dict:
        """Exact correlated-factor box robustness and sharp radius by path enumeration.

        Model c_e = base_e + sum_j Lambda[e,j] * xi_j, with
        |xi_j| <= rho * factor_amplitudes[j]. A graph-gradient term may be
        added to every edge and cancels from all s-t path comparisons.

        For fixed P,Q, the worst difference at radius rho is
        b(P)-b(Q) + rho * sum_j alpha_j * abs(sum_P Lambda_ej-sum_Q Lambda_ej).
        No universal single adversarial scenario is asserted. Enumeration can
        require exponentially many paths. No floating point or LP tolerance.
        """
        path = list(path)
        self.path_edges(path)
        amps = tuple(F(x) for x in factor_amplitudes)
        if not amps or any(x < 0 for x in amps):
            raise ValueError('Must supply positive number of nonnegative factor amplitudes')
        if set(coupling) != set(self.by_id):
            raise ValueError('Coupling must specify exactly every graph edge ID')
        lam = {eid: tuple(F(x) for x in vals) for eid, vals in coupling.items()}
        k = len(amps)
        if any(len(row) != k for row in lam.values()):
            raise ValueError('Each coupling row must match the factor dimension')
        rho = None if radius is None else F(radius)
        if rho is not None and rho < 0:
            raise ValueError('Radius must be nonnegative')
        base = {e.id: e.base for e in self.edges}
        p_cost = self.cost(path, base)
        paths = self.enumerate_paths(max_paths)
        minimum = None
        limiting = None
        worst = Fraction(0)
        worst_competitor = None
        witness_delta = None
        for q in paths:
            q_cost = self.cost(q, base)
            gap = q_cost - p_cost
            if gap < 0:
                raise ValueError('Candidate is not nominally shortest at radius zero')
            p_ids, q_ids = set(path), set(q)
            diff = tuple(
                sum((lam[eid][j] for eid in p_ids - q_ids), Fraction(0)) -
                sum((lam[eid][j] for eid in q_ids - p_ids), Fraction(0))
                for j in range(k)
            )
            sensitivity = sum((amps[j] * abs(diff[j]) for j in range(k)), Fraction(0))
            if sensitivity:
                threshold = gap / sensitivity
                if minimum is None or threshold < minimum:
                    minimum = threshold
                    limiting = q[:]
            if rho is not None:
                regret_vs_q = -gap + rho * sensitivity
                if regret_vs_q > worst:
                    worst = regret_vs_q
                    worst_competitor = q[:]
                    witness_delta = diff
        result = {
            'status': 'EXACT_ENUMERATED_CORRELATED_BOX',
            'graph_sha256': self.graph_sha256(),
            'candidate': path,
            'correlation_factors': k,
            'checked_paths': len(paths),
            'sharp_radius': fmt(minimum) if minimum is not None else '+infinity',
            'limiting_path': limiting,
            'scope': 'finite DAG; exact rational low-dimensional factor box; exhaustive path enumeration',
        }
        if rho is not None:
            result['tested_radius'] = fmt(rho)
            result['robust_at_radius'] = worst == 0
            result['worst_regret'] = fmt(worst)
            result['witness_path'] = worst_competitor
            if worst_competitor is not None:
                # One explicit factor vector that realizes the proven worst regret.
                factors = tuple(
                    rho * amps[j] * (1 if witness_delta[j] > 0 else -1 if witness_delta[j] < 0 else 0)
                    for j in range(k)
                )
                result['witness_factors'] = [fmt(x) for x in factors]
                weights = {eid: base[eid] + sum(
                    (lam[eid][j] * factors[j] for j in range(k)), Fraction(0))
                    for eid in self.by_id}
                # The witness is checked against all competitors; never trust a bare flag.
                actual_regret = self.cost(path, weights) - min(self.cost(q, weights) for q in paths)
                assert actual_regret == worst
            else:
                result['witness_factors'] = None
        return result


def parse(data: dict) -> tuple[Graph, list[str]]:
    edges = [Edge(id=str(x['id']), u=str(x['u']), v=str(x['v']),
                  base=F(x['base']), lo=F(x['lo']), hi=F(x['hi'])) for x in data['edges']]
    g = Graph([str(x) for x in data['vertices']], edges, str(data['source']), str(data['target']))
    path = [str(x) for x in data['candidate']]
    g.path_edges(path)
    return g, path


def main():
    import argparse
    p = argparse.ArgumentParser(description='Exact gauge-invariant robust route certificate')
    p.add_argument('data', help='Input graph JSON')
    options = p.add_mutually_exclusive_group()
    options.add_argument('--verify', help='Optional certificate JSON to check without solving shortest paths')
    options.add_argument('--gauge-shifts', help='JSON with shifts mapping for exact gauge classification')
    options.add_argument('--radius-amplitudes', help='JSON with amplitude mapping for exact symmetric radius')
    options.add_argument('--correlated-box', help='JSON of factor couplings, amplitudes, and optional radius')
    args = p.parse_args()
    with open(args.data, encoding='utf8') as f:
        data = json.load(f)
    g, path = parse(data)
    if args.verify:
        with open(args.verify, encoding='utf8') as f:
            cert = json.load(f)
        if not cert.get('robust') or not cert.get('distance_certificate'):
            raise ValueError('Only proof certificates can be verified; counterexamples are analyzed separately')
        print(json.dumps({'verified': g.verify_claim(path, cert)}))
    elif args.gauge_shifts:
        with open(args.gauge_shifts, encoding='utf8') as f:
            shifts=json.load(f)['shifts']
        print(json.dumps(g.gauge_audit(shifts), indent=2))
    elif args.correlated_box:
        with open(args.correlated_box, encoding='utf8') as f:
            conf = json.load(f)
        print(json.dumps(g.correlated_box(path, conf['coupling'], conf['factor_amplitudes'], conf.get('radius')), indent=2))
    elif args.radius_amplitudes:
        with open(args.radius_amplitudes, encoding='utf8') as f:
            amps=json.load(f)['amplitudes']
        radius=g.exact_radius(path, amps)
        print(json.dumps({'sharp_radius':fmt(radius) if radius is not None else '+infinity'}, indent=2))
    else:
        print(json.dumps(g.analyze(path), indent=2))


if __name__ == '__main__':
    main()
