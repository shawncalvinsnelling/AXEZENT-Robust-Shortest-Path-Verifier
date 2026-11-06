# AXEZENT Robust Shortest Path Verifier

**Exact proofs for routing decisions under uncertain costs.**

[![Python tests](https://github.com/shawncalvinsnelling/AXEZENT-Robust-Shortest-Path-Verifier/actions/workflows/python-tests.yml/badge.svg)](https://github.com/shawncalvinsnelling/AXEZENT-Robust-Shortest-Path-Verifier/actions/workflows/python-tests.yml) · [MIT License](LICENSE) · [The mathematics](THEOREM.md) · [Publication and citation](PUBLICATION.md)

**Author:** Shawn Calvin Snelling · **Project:** AXEZENT AI Research · **Current software version:** 1.2.0

## What does it do?

A routing system proposes a path through a network, but the cost of each connection may change within specified bounds. **GaugeRail checks whether that exact proposed path is still a shortest path for every allowed combination of those costs.** It does not merely sample a few possibilities: for the supported independent-interval model, it constructs an exact worst-case scenario and checks it using rational arithmetic.

The tool delivers one of two inspectable results:

- **Verified route:** an exact shortest-path *certificate* that a second program can check independently, without trusting the original solver.
- **Rejected route:** a competing path and an admissible cost scenario showing precisely why the claimed route fails.

It can also determine the *stability radius*—how far the stated uncertainty may scale before a different route can become cheaper—and evaluate a separate, correlated-factor model by exhaustive route enumeration.

## A real example

The bundled four-node graph offers these baseline options:

| Candidate route | Baseline total | Under the candidate's worst-case independent interval scenario |
|---|---:|---:|
| `s → a → t` | 6 | **13/2 = 6.5** |
| `s → b → t` | 10 | 19/2 = 9.5 |
| `s → t` | 9 | 35/4 = 8.75 |

Each connection has an independent adjustment from `-1/4` to `+1/4`. The candidate remains cheapest even in its exact worst-case scenario, so it is guaranteed shortest for **all** combinations allowed by that interval model. The verified certificate reports `"robust": true` and `"worst_regret": "0"`.

Increase the uncertainty sufficiently and the same method finds an explicit cheaper competitor. In the correlated-factor example, the limiting route gives an exact stability radius of **4/3**. These are mathematical model results, not forecasts of real traffic.

## Run it (Python 3.10–3.13, no external dependencies)

Clone the public repository and enter its directory:

```bash
git clone https://github.com/shawncalvinsnelling/AXEZENT-Robust-Shortest-Path-Verifier.git
cd AXEZENT-Robust-Shortest-Path-Verifier
```

**1. Check whether a proposed path is robust:**

```bash
python src/gaugerail.py examples/robust_route.json
```

**2. Independently verify an existing certificate:**

```bash
python src/gaugerail.py examples/robust_route.json --verify examples/robust_certificate.json
# {"verified": true}
```

**3. See an exact counterexample to an unsafe route:**

```bash
python src/gaugerail.py examples/nonrobust_route.json
```

**4. Compute an exact correlated-factor robustness radius:**

```bash
python src/gaugerail.py examples/robust_route.json --correlated-box examples/correlated_box.json
# "sharp_radius": "4/3"
```

**5. Run the complete local test suite:**

```bash
python -m unittest discover -s tests -v
python scripts/adversarial_stress.py
```

Detailed input specifications, explanations of JSON outputs, gauge transformations, symmetric radii, and additional examples are in [USAGE.md](USAGE.md).

## Why mathematical certificates matter

A solver can claim a route is safe without giving evidence. GaugeRail instead binds a result to its **specific graph, endpoints, proposed path, and rational costs**, then verifies exact Bellman inequalities. Under the specified assumptions, those inequalities demonstrate the result; a cryptographic fingerprint merely detects mismatched input files and **is not a signature**.

This architecture is useful for evaluating candidate solutions in logistics, data networks, project scheduling DAGs, and auditable algorithmic workflows, provided the model captures the real uncertainty correctly.

## Scope and performance

| Capability | Mathematical method | Computational boundary |
|---|---|---|
| Route optimal for all independent edge intervals? | Single extremal scenario + shortest-path certificate | Linear number of graph operations on a DAG, excluding rational bit costs |
| Does a potential-gradient cost shift change rankings? | Exact path-invariance classification | DAG traversal |
| Independent symmetric stability radius | Exact route-comparison ratios | Implemented by complete path enumeration; may be exponential |
| Correlated symmetric factor-box regret and radius | Exact box support function over competing routes | Complete path enumeration with a configurable cap; may be exponential |
| Corrupted or mismatched proof JSON | Strict instance binding and Bellman checks | Detects covered errors; not cryptographic authentication |

The software uses only finite **directed acyclic graphs**, additive edge costs, and rational input. It does not claim optimality for every kind of physical network, a polynomial-time algorithm for general correlated robust routing, or a solution to an unsolved complexity problem. The full assumptions appear in [THEOREM.md](THEOREM.md), the threat model in [SECURITY.md](SECURITY.md), and the comparison with existing research in [PRIOR_ART.md](PRIOR_ART.md).

## Research and verification

The accompanying technical note gives **six self-contained statements with proofs** about path-invisible edge shifts, exact worst-case regret, potential certificates, independent uncertainty radii, faithful edge subdivision, and correlated factor-box radii. They are mathematical statements within the stated model, not evidence of a world-first discovery. The approach draws on established shortest-path potentials and interval-robust optimization, which are cited explicitly.

The project includes 20 automated unit tests, deterministic randomized cross-checks, 1,024 invalid-certificate mutation cases, and a 2,500-vertex example smoke test. These check the implementation; the universal statements depend on their written proofs. See [VALIDATION.md](VALIDATION.md) for a reproducible verification protocol and [GitHub Actions](https://github.com/shawncalvinsnelling/AXEZENT-Robust-Shortest-Path-Verifier/actions) for continuous integration.

## Publication, attribution and reuse

**Shawn Calvin Snelling** is the author of this AXEZENT research software and its accompanying technical note. The public GitHub history provides a timestamped record of the source and its revisions beginning **November 6, 2026**. The [publication record and recommended citation](PUBLICATION.md) identify those commits without claiming priority over earlier mathematics. The [CITATION.cff](CITATION.cff) also supports GitHub's *Cite this repository* feature.

The project is available under the [MIT License](LICENSE). This names a standard permissive software license; it **does not signify affiliation with the Massachusetts Institute of Technology**. Contributions and independent verification are welcome. The software is research-grade, and applications with safety consequences require their own validation.
