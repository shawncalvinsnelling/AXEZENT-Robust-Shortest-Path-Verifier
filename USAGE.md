# User guide — verify a route or falsify it

This guide describes the executable software. The mathematical justification is in [`THEOREM.md`](THEOREM.md).

## Requirements

Python 3.10–3.13 and the standard library; no package installation, service, cloud account or API key required. Run commands from the repository root.

## Input format

The core input is a JSON object containing:

- `vertices`: list of distinct vertex names.
- `source`, `target`: two distinct vertices, with at least one directed path between them.
- `edges`: directed arcs with **unique IDs**, `u`, `v`, `base`, `lo` and `hi`. Parallel arcs are allowed if IDs differ.
- `candidate`: list of arc IDs, forming a connected path from source to target.

`lo` and `hi` are residual adjustments relative to the `base` cost. Use exact integer or rational **strings** such as `"-1/4"`, not JSON floating-point numbers. The graph must be acyclic. The program rejects invalid paths, duplicate IDs and invalid intervals.

**Example:** [`examples/robust_route.json`](examples/robust_route.json).

## Check a route

```bash
python src/gaugerail.py examples/robust_route.json
```

A `PROVED_EXACT_CERTIFICATE` result means the candidate is shortest for all independently permitted edge residuals. Inspect the `candidate`, `graph_sha256`, `distance_certificate`, and `worst_regret` fields. The example's regret is exactly `"0"`.

A `EXACT_COUNTEREXAMPLE` result supplies `witness_path`, `adversarial_costs`, and positive `worst_regret`. These explain why the proposed route fails. See `examples/nonrobust_route.json`.

## Verify a certificate without invoking the shortest-path solver

```bash
python src/gaugerail.py examples/robust_route.json --verify examples/robust_certificate.json
```

A valid result prints `{"verified": true}`. Failure produces an error and a nonzero exit code. The checker enforces the complete claimed instance/path identity, graph fingerprint, exact costs, and Bellman inequalities. This is mathematical verification of a certificate for **trusted input**, not independent authentication of the source graph.

## Study cost changes that cannot affect route rankings

```bash
python src/gaugerail.py examples/robust_route.json --gauge-shifts examples/gauge_shifts.json
python src/gaugerail.py examples/robust_route.json --gauge-shifts examples/non_gauge_shifts.json
```

The first returns a vertex potential showing why the change is path-invisible; the second returns two valid paths witnessing unequal induced cost changes.

## Exact symmetric uncertainty radius

```bash
python src/gaugerail.py examples/robust_route.json --radius-amplitudes examples/radius_amplitudes.json
```

`amplitudes` contains a nonnegative rational magnitude for every edge. The returned radius identifies the largest nonnegative scale factor at which the candidate remains shortest for every independently bounded residual. `"+infinity"` means the allowed perturbations cannot change its optimality under that specified model. Finding the radius currently enumerates paths and may take exponential time.

## Correlated factor-box uncertainty

```bash
python src/gaugerail.py examples/robust_route.json --correlated-box examples/correlated_box.json
```

The configuration contains `coupling` (an edge-to-factor coefficient vector for every edge), `factor_amplitudes` (nonnegative rational magnitudes), and optionally `radius`. Each factor varies independently within its own symmetric interval; *edge* costs may be correlated through shared factors.

The response includes `sharp_radius`, `checked_paths`, and `limiting_path`. When `radius` is supplied it also reports whether the candidate is robust at that radius, its exact worst regret, and (if unsafe) a witness factor vector. The implementation **enumerates every source–target path** and refuses to return a purported exact result after its path cap is exceeded. It is not a general-purpose polynomial solver for correlated uncertainty.

## Testing and verification

```bash
python -m unittest discover -s tests -v
python scripts/adversarial_stress.py
python scripts/stress_test.py
```

The repository's GitHub Actions workflow also runs unit tests, mutation checks and example commands across Python 3.10–3.13. A passing test run supports implementation reliability for tested cases, not universal security or physical-world predictions.

## Interpretation, errors and deployment

- The computed guarantee depends on the specified intervals and model being accurate.
- Fraction inputs are exact; decimal floating-point JSON values are not accepted.
- Certificate hashes bind to data, but are **not** digital signatures or proof of trusted authorship.
- DAG-only restrictions prevent directed cycles from creating unhandled negative-cycle behavior.
- Use this software for research, benchmarking, audit prototypes and controlled evaluations. Do not use it alone to control safety-critical routing.

See [`SECURITY.md`](SECURITY.md) for the threat model and [`PUBLICATION.md`](PUBLICATION.md) for citation details.
