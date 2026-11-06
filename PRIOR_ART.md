# Prior-Art Review and Claims Ledger (2026-11-06)

## Distinguish three kinds of results

| Assertion | Mathematical status | Novelty status |
|---|---|---|
| Edge potential gradients preserve shortest paths | PROVED-EXACT (Theorem 1) | KNOWN: Johnson reweighting / path independence |
| On the s-t relevant DAG, all route-invisible changes are gradients | PROVED-EXACT (Theorem 1) | KNOWN in graph cohomology / conservative edge fields, specific presentation not exhaustively checked |
| Strong optimality under independent intervals reduces to fixed path's adversarial scenario | PROVED-EXACT (Theorem 2) | PRIOR-ART OVERLAP: interval-data robust path literature |
| Independently checkable robust certificate using tight potentials | PROVED-EXACT (Theorem 3) | KNOWN: shortest path dual potentials, combined here |
| Sharp uniform independent symmetric interval radius formula | PROVED-EXACT (Theorem 4) | Sensitivity analysis has precedent; priority unverified |
| Faithful subdivision preserves robust regret under endpoint-sum interval matching | PROVED-EXACT (Theorem 5) | Elementary equivalence; priority unverified |
| Single reproducible package combining these properties | VERIFIED-BOUNDED (tests); general math proved separately | Originality of code packaging not independently checked |
| Correlated factor-box sharp radius via full route enumeration | PROVED-EXACT (Theorem 6); tests finite | Support-function methods and robust parametric routing are known; originality not established |
| Major breakthrough, $1M valuation, journal acceptance | NOT ESTABLISHED | Do not claim |

## Correlated factor-box extension, v1.1.0

Theorem 6 derives the exact worst-regret identity under *symmetric rational
factor-box uncertainty* via the support function of a box and finite
interchange of maxima. It gives a sharp radius using path enumeration, but
**does not give a common adversarial factor vector for all routes**, and does
**not** establish a polynomial-time algorithm for correlated robust shortest
path problems. Box support functions, robust optimization duality, and
parametric path sensitivity are well-developed; novelty is NOT ESTABLISHED.

The previously proposed formula based on differences of **average active and
inactive edge costs divided by a matrix norm** is a **HEURISTIC, NOT A
STABILITY-RADIUS THEOREM**, because it need not correspond to *any* valid
competing route, let alone the limiting one. Likewise an alleged
"malicious-certificate test" that only validates array shapes cannot prove
routing feasibility or shortest-path inequalities.

## Source checks

1. MIT OpenCourseWare lecture notes, *Johnson's Algorithm* (2020), establish that adding potential differences to edge costs telescopes on paths, preserving shortest paths. https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/6027e2a155c948937fdfb93981f7070c_MIT6_006S20_r14.pdf
2. Karasan et al., *The Robust Shortest Path Problem with Interval Data* (2001), reviews interval uncertainty and robust routing, https://optimization-online.org/2001/08/361/ .
3. *Robust and Distributionally Robust Shortest Path Problems: A Survey* (2025), https://doi.org/10.1016/j.cor.2025.107096 — comprehensive review of prior interval, relative, and absolute robust optimization.
4. *Computing all shortest passenger routes with a tropical Dijkstra algorithm* (2025), https://doi.org/10.1016/j.ejtl.2025.100163 — interval path scenario formalism, highlighting prior knowledge in this area.
5. Physics analogy only: Barrios Hita et al., *Quantum Mechanics Based on Real Numbers: A Consistent Description* (2026), DOI 10.1103/4k13-sdjh. Their work concerns changing representations while retaining predictions; this repository concerns route comparisons in finite graphs, not quantum mechanics.

## What can be responsibly posted

> We present AXEZENT GaugeRail-001, a reproducible, exact-rational verification note for gauge-invariant robust route classification on directed acyclic networks. It supplies six self-contained proofs, independently checkable optimality certificates, falsification witnesses, and exhaustive small-case regression tests. We recognize the underlying connections to Johnson potentials and interval robust shortest paths and do not assert a novel mathematical theorem pending a broader literature review.

## If the goal is peer-recognized novelty

The next research problem is **correlated, non-gradient uncertainty with low-rank coupling**. The single adversarial scenario generally fails there; find nontrivial conditions that admit an efficiently checkable alternative exact certificate. This is marked **OPEN / RESEARCH DIRECTION**, not a proved result. The theorem here gives a precise baseline against which more general proposed claims can be falsified.
