# Changelog

## v1.1.0 — 2026-11-06 — Proof-envelope hardening and correlated factor box

- Added *strict* full-certificate checks binding a claim to the graph, source,
  target, path, claimed costs, and exact shortest-path inequalities.
- Added canonical SHA-256 input fingerprint (not authentication/signing).
- Added independently reproducible attacks on malformed, mismatched,
  misleading, and mutated proof objects.
- Added exact correlated-factor box radius and regret by exhaustive path
  enumeration; explicit uncertainty-factor witnesses for failed claims.
- Added tests of correlated algebra against all factor-box corners.
- Added security scope, MIT licensing text, metadata, receipts, examples,
  and explicit prior-art/novelty limitations.
- Intentionally **not** adopted: mean-active-vs-mean-inactive "radius"
  heuristic or a dimension-only "forgery" check. Neither is a valid proof.
- Intentionally **not** asserted: one common worst-case cost scenario under
  arbitrary correlated uncertainties or a polynomial-time solution to
  general robust routing.

## v1.0.0 — 2026-11-06 — Baseline

- Five self-contained DAG routing and gauge invariance theorem statements.
- Exact independent interval box robust verification and route witnesses.
- Exact independent symmetric perturbation radius and finite tests.

### First public GitHub publication (2026-11-06)

- Standardized the module filename spelling from `gagerail.py` to `gaugerail.py`; updated imports and commands.
- Aligned README, CITATION, release checklist, and scope ledger with the authorized GitHub repository.
- Added GitHub Actions Python regression test workflow.
- Rebuilt all reproducibility hashes after final source and metadata edits.
