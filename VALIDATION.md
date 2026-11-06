# Verification and reproducibility

## How to reproduce the results

From the repository root, with Python 3.10–3.13:

```bash
python -m unittest discover -s tests -v
python scripts/adversarial_stress.py
python src/gaugerail.py examples/robust_route.json --verify examples/robust_certificate.json
python src/gaugerail.py examples/robust_route.json --correlated-box examples/correlated_box.json
python scripts/stress_test.py
```

The first command runs the 20 named regression tests. The second constructs 1,024 seeded, deliberately invalid certificate mutations; expected behavior is rejection of those specified attacks. The direct verifier checks an exact proof envelope; the correlated example outputs the exact factor-box radius `4/3`. The stress script evaluates a constructed 2,500-vertex and 4,996-arc DAG. Machine-specific elapsed times are not performance guarantees.

## What is tested

- Exact paths, rational arithmetic, candidate feasibility and rejection of malformed inputs.
- Independent-edge interval worst-scenario reduction against exhaustive small-case endpoint enumeration.
- Gauge equivalence and concrete witnesses for non-gradient perturbations.
- Exact edge-potential certificates and invalid-claim rejection.
- Independent and correlated symmetric robustness radii.
- Correlated-box results against all factor-box corners on 180 seeded small examples.
- An iterative path enumerator on a long, acyclic chain.

The methods are specified in [`THEOREM.md`](THEOREM.md), and the test source is in [`tests/`](tests/). Automated GitHub Actions currently exercises Python 3.10, 3.11, 3.12 and 3.13.

## Interpreting the receipt files

`REPRODUCIBILITY_RECEIPT.json`, `ADVERSARIAL_RECEIPT.json` and `STRESS_RECEIPT.json` are records of specific execution runs. They contain **observations**, not a cryptographic attestation or an independent proof of mathematical novelty. `SHA256SUMS.txt` lists project file checksums for integrity comparison. Running scripts that rewrite receipts may change those files; the published checksums reflect the committed snapshot only.

## Trust boundary

Successful testing does not prove absence of every implementation defect, resistance to arbitrary untrusted input, or suitability for safety-critical control. In particular, certificates are checked against **the input network supplied to the verifier**; the input must be authenticated externally when provenance matters. Additional failure modes and accepted threat assumptions are documented in [`SECURITY.md`](SECURITY.md).
