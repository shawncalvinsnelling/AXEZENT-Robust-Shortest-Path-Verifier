# Security, threat model, and non-claims

## What the verifier actually establishes

Given a **trusted network definition** and a candidate s-t route, `--verify`
checks a *mathematical* optimality certificate. It requires a complete, exactly
matching input digest and route metadata, then verifies exact Bellman edge
inequalities and candidate-path equalities using rational numbers.

A mismatch in any required proof field is rejected. This fixes the v1.0 flaw
where the `candidate` in a JSON certificate was not checked against the input
candidate. The program also rejects malformed or disconnected input paths.

## Important limits

- SHA-256 is a **content fingerprint**, not a digital signature. An attacker
  who can alter both the graph input and certificate can make a new consistent
  fingerprint. Operators must independently authenticate the network source.
- The verifier proves shortest-path robustness **within the specified model**.
  It cannot validate that real roads, prices, timetables, or uncertainty ranges
  were represented honestly or accurately.
- The independent-edge proof uses a **finite DAG** with **independent box
  intervals**; correlated uncertainty requires `--correlated-box` and is
  exhaustively enumerated rather than certified by the one-scenario theorem.
- The correlated-factor method uses rational coefficients and a symmetric
  factor box. It can enumerate exponentially many paths; the 200,000-path
  default safety cap prevents silent partial results.
- The stress suite uses selected invalid mutations and **does not** prove
  absence of every security issue, resistance to hostile resource exhaustion,
  cryptographic integrity, or production fitness.
- This is research software. Do not deploy as a sole safety control in
  transportation, medicine, security, or critical infrastructure.

## Public release review

Check the copyright holder and the MIT licensing decision. No repository
has been pushed by this package. Author approves any public release.
