# Security scope and responsible use

## What is verified

Given a **trusted** graph definition and candidate route, the `--verify` command checks an exact robustness certificate: graph fingerprint, candidate identity, reported costs, Bellman edge inequalities and candidate-path tightness. This check does not depend on the shortest-path solver's own result.

The program rejects altered or mismatched proof objects tested by the bundled adversarial suite, invalid route sequences and malformed input fields. It rejects the older v1.0 certificate envelope, which lacks instance binding.

## Trust and resource boundaries

- **Authenticity:** SHA-256 is a deterministic content fingerprint, not a digital signature or evidence that a graph came from a trusted publisher. If a party can modify the graph and certificate together, they may create a new internally consistent pair. Authenticate input files separately.
- **Model:** A mathematical statement about an assumed cost model cannot validate whether real traffic, equipment, payments or deadlines match that model.
- **Independent vs correlated changes:** The linear-size proof certificate addresses independent edge intervals; correlated symmetric-factor analysis enumerates routes and can be exponential in graph size.
- **Availability:** Exhaustive path enumeration has a safety cap but is not a comprehensive denial-of-service defense against hostile oversized inputs or resource starvation.
- **Stress coverage:** 1,024 predetermined invalid mutations test particular failure modes; this is not a claim of universal security, formal implementation verification or cryptographic attestation.
- **Deployment:** Use research/benchmark settings or add domain-specific validation, monitoring and independent controls before critical operational use.

## Reporting

Report reproducible bugs through the repository's GitHub Issues, without posting credentials or sensitive real-world routing data. For a potentially exploitable vulnerability, prefer a private security advisory if that feature is available; otherwise avoid public disclosure of exploit details until a safe reporting channel is established.

The software and documentation are publicly released under the MIT License; no affiliation with MIT as an institution is implied.
