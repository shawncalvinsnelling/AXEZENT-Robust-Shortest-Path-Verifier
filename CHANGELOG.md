# Changelog

## v1.2.0 — 2026-11-06 — Public documentation and reproducibility edition

- Reworked the README for external engineers, students and mathematical researchers, leading with the practical routing problem, a worked example and executable commands.
- Added `USAGE.md`, `VALIDATION.md` and `PUBLICATION.md` with precise file formats, verification instructions, a citation and immutable public commit references.
- Corrected stale prepublication language in the README, citation file and security notes; public authorship is attributed to Shawn Calvin Snelling, AXEZENT AI Research.
- Strengthened the prior-art review with full citations and clear distinctions between mathematical foundations and this implementation.
- Clarified the MIT License's meaning, exact model boundaries, and the scope of CI/adversarial test evidence.
- No mathematical theorem or solver behavior was changed in this documentation-focused revision.

## v1.1.0 — 2026-11-06 — Proof-envelope hardening and correlated-factor box

- Added strict certificate checks binding graph, source, target, route and costs to exact shortest-path inequalities.
- Added an SHA-256 content fingerprint (not a signature) and 1,024 seeded corruption tests.
- Added correlated-factor-box regret and radius by exhaustive path enumeration, with explicit negative witnesses and independent small-case tests.
- Published the complete source, tests, examples, documentation and Python CI workflow to GitHub on November 6, 2026.

## v1.0.0 — 2026-11-06 — Initial proof and verifier package

- Five self-contained results for finite DAG routing and gauge transformations.
- Exact independent-interval robustness checks, short certificates, counterexamples and stability radii.
