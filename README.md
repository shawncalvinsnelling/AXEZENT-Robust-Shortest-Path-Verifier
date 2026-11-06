# AXEZENT GaugeRail-001

**GitHub project:** [AXEZENT-Robust-Shortest-Path-Verifier](https://github.com/shawncalvinsnelling/AXEZENT-Robust-Shortest-Path-Verifier)

## Gauge-invariant robust routing with exact certificates

**Prepared for Shawn Calvin Snelling / AXEZENT AI Research, 2026-11-06.**

This repository contains six mathematically proved statements for finite directed acyclic networks: independent rational interval uncertainty with vertex-potential-gradient shifts, and a separately scoped **correlated-factor-box** extension computed by exhaustive path enumeration. It includes an exact non-probabilistic verifier and constructive counterexamples.

**Important scope of claim:** The proofs are complete for the explicitly stated hypotheses. Originality and first publication are **not established**; important elements are already known in graph theory and robust shortest-path optimization. The artifact is research-ready, not a validated major new discovery, patent, or commercially priced asset. **Public code availability does not imply peer review or mathematical novelty.**

### Read first

- [`THEOREM.md`](THEOREM.md) — six theorem statements, full proofs, and sharp limitations.
- [`PRIOR_ART.md`](PRIOR_ART.md) — what is known, what is distinctive about this combination, and what would need genuine novelty review.
- [`examples`](examples/) — exact-rational examples and certificates.
- [`src/gaugerail.py`](src/gaugerail.py) — standard-library Python solution and independent checker.
- [`tests/test_gaugerail.py`](tests/test_gaugerail.py) and [`tests/test_security_correlated.py`](tests/test_security_correlated.py) — exhaustive small-case comparisons, forged-certificate rejection, and invariance checks.

### One-command independent test

```bash
python -m unittest discover -s tests -v
```

### v1.1.0 hardened checks and correlated uncertainties

The verifier now requires strict matching of the full graph fingerprint,
claimed candidate, cost fields, certificate field set, and exact mathematical
inequalities. This prevents accidental acceptance of mismatched or corrupted
proof envelopes. The hash **does not authenticate the graph's origin**.

```bash
python scripts/adversarial_stress.py
python src/gaugerail.py examples/robust_route.json --verify examples/robust_certificate.json
python src/gaugerail.py examples/robust_route.json --correlated-box examples/correlated_box.json
```

The stress script generates 1,024 seeded mutations over 16 attack categories
and writes `ADVERSARIAL_RECEIPT.json`. The true correlated-box routine computes
worst regret and the exact robust radius using **all** source-target routes,
with a hard cap. The algorithm does **not** assert a polynomial-time solution
for correlated routing. On the included factor-box example, the sharp radius
is **4/3**; see Theorem 6 and `SECURITY.md` for precise assumptions.

Do **not** paste the proposed `mean(active)-mean(inactive)` stability heuristic
or the dimension-only malicious-cert test: neither is a proof of robust route
optimality. The v1.1 routine instead compares valid competing paths and checks
actual Bellman inequalities.

**Compatibility:** v1.0 certificates do not contain a graph fingerprint and
are deliberately rejected by the stricter v1.1 `--verify`. Regenerate them
using `python src/gaugerail.py ... > proof.json`. The v1.0 theorem and inputs
remain intact; only the certification envelope has changed.

### Analyze a proposed path

```bash
python src/gaugerail.py examples/robust_route.json > examples/robust_certificate.json
python src/gaugerail.py examples/robust_route.json --verify examples/robust_certificate.json
python src/gaugerail.py examples/nonrobust_route.json
python src/gaugerail.py examples/robust_route.json --gauge-shifts examples/gauge_shifts.json
python src/gaugerail.py examples/robust_route.json --gauge-shifts examples/non_gauge_shifts.json
python src/gaugerail.py examples/robust_route.json --radius-amplitudes examples/radius_amplitudes.json
```

The output is exact: fractions such as `13/2` are never converted to rounded floating point. Never pass floats as numerical input.

### The operational problem

Suppose an AI dispatch system proposes a route. Each road/connection may vary independently within a guaranteed range. Additionally, potentially huge day-to-day variations in node prices may occur, provided they change arc costs by the potential difference `phi(destination)-phi(source)`.

To prove the route optimal under **all** possible values (including continuous, infinitely many scenarios):

1. Maximize the perturbations on the proposed route; minimize them on every other arc.
2. Find one shortest path under those synthetic weights (exact DAG DP, no sampling).
3. If that path has the same total cost, emit a node-distance certificate. Verify it using only edge inequalities and path equalities.
4. If another path is cheaper, emit that exact competing path and the extremal scenario as a falsification witness.

**This is not a solution of general NP-hard robust optimization** and does not reduce SAT complexity. It verifies the strong optimality of a **given** route under box uncertainty, a specifically delimited problem.

### More mathematical structure

Theorem 1 identifies a maximal invisible subspace of edge perturbations: exactly the potential gradients on the source-to-target relevant graph. Its quotient has `m - n + 1` degrees of freedom. Theorem 2 collapses independent box scenarios for a fixed candidate route to a single adversarial vector. Theorems 3–5 provide concise certificates, an exact sharp uniform perturbation radius, and invariance under faithful edge subdivisions. Theorem 6 separately addresses correlated factor-box uncertainties with complete path enumeration; it is not a single-scenario shortcut for arbitrary correlations.

### Larger-graph smoke test

`python scripts/stress_test.py` independently verified a constructed DAG with 2,500 vertices and 4,996 arcs and stored its environment-specific timings in `STRESS_RECEIPT.json`. This test is not a proof and is not a commercial throughput benchmark.

### Research test totals in supplied receipt

Twenty named unit tests completed, including 250 deterministically seeded random small DAGs checked against brute-force enumeration of **all endpoint assignments**, 100 potential-reweighting cases, 200 exact gauge classification cases, exact certificate-tampering rejection, and edge subdivision tests. These are finite tests and do not alone establish the universal theorem (the proof does).

### Candidate applications

- Logistics and dispatch: explain when a chosen route is immune to bounded uncertainty.
- Computer networking: independently verify claimed optimal routes.
- Software assurance: a compact pass/fail receipt with counterexample when false.
- Scheduling DAGs: sensitivity and scenario compression when additive costs are modeled accurately.

Applicability depends on defensible input uncertainty intervals. There is **no warranted million-dollar market-value claim**.

### Provenance

The design uses AXEZENT's documented preferences for exact arithmetic, finite window validation, independently verified certificates, and negative-case witnesses. Prior quantum work motivated the search for a representation-independent invariant; it was not copied or modified. See source notes and external citations in `PRIOR_ART.md`.

### License and release

The author has authorized public distribution of this v1.1.0 research artifact under the included **MIT `LICENSE`**. It is provided as-is with the limitations explained in `THEOREM.md`, `PRIOR_ART.md`, and `SECURITY.md`.
