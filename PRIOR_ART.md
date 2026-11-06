# Related literature and scope of the research contribution

GaugeRail is a reproducible software-and-proof package for a precise class of uncertain routing problems. It combines several established mathematical tools in an independently executable implementation. This section identifies the foundations and the boundaries of the claims; it is **not** a declaration that existing theorems have been discovered anew.

## Relevant published work

1. **O. E. Karasan, M. C. Pinar and H. Yaman (2001; revised 2003), *The Robust Shortest Path Problem with Interval Data*.** [Optimization Online](https://optimization-online.org/2001/08/361/). This research explicitly studies directed acyclic networks with interval arc costs and minimax-regret routing. It is important prior work for GaugeRail's interval-uncertainty and regret setting.
2. **MIT OpenCourseWare, *Johnson's Algorithm / Reweighting Shortest Paths*.** [Lecture materials](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/). Potential-based edge reweighting preserves comparisons among paths with common endpoints. This is established background for the gauge/potential calculations.
3. **C. Filippi, F. Maggioni and M. G. Speranza (2025), *Robust and Distributionally Robust Shortest Path Problems: A Survey*.** *Computers & Operations Research* 182, 107096. [DOI](https://doi.org/10.1016/j.cor.2025.107096). This literature survey places robust routing in the broader field and documents multiple distinct robustness criteria and uncertainty models.
4. **Computing all shortest passenger routes with a tropical Dijkstra algorithm (2025).** *EURO Journal on Transportation and Logistics* 14, 100163. [DOI](https://doi.org/10.1016/j.ejtl.2025.100163). This work studies interval-valued passenger-routing costs and parameterized path sets; its objective differs from verifying universal optimality of one fixed candidate.

## What this repository contributes as software

- A readable, self-contained derivation of six scoped results for finite DAGs, including a complete characterization of route-invisible edge transformations on the source–target-relevant subgraph.
- Exact-rational code for checking whether a proposed path is shortest for *all* independent interval realizations, not only randomly sampled values.
- Independently checkable Bellman-potential certificates, concrete negative-case witnesses, graph fingerprints and adversarial regression tests.
- A separate correlated-factor-box calculation with explicit witness factors and exact radius; **all routes are enumerated**, with an explicit cap, to avoid a false polynomial-time claim.
- A focused reproducibility workflow, input examples, citations and clear model limitations.

A package can be an original implementation and exposition even when its building blocks are established. Neither the presence of a proof nor its GitHub publication alone demonstrates first mathematical priority, novelty sufficient for journal publication, or independent peer approval.

## Boundary between proved mathematics and open research

| Mathematical subject | Status in this project | Related prior knowledge |
|---|---|---|
| Potential gradients preserve shortest-path rankings | Proved here under stated assumptions | Standard reweighting and path-independence theory |
| Route-invisible changes equal gradients on the relevant DAG | Proved here | Conservative edge fields / path-independence principles |
| Worst regret for one fixed route under independent interval costs | Proved here | Robust interval shortest-path literature |
| Exact rational potential certificates and negative witnesses | Proved and implemented | Bellman optimality inequalities |
| Symmetric independent stability radius | Proved; radius implementation enumerates paths | Sensitivity/robust optimization methods |
| Correlated symmetric factor-box radius | Proved for the stated box; enumerated implementation | Support functions and robust optimization |
| One efficiently checkable universal correlated scenario | **Not claimed** | Not established by this work |
| Peer review / historical first discovery | **Not claimed** | Requires independent review and full priority search |

The full technical proofs and assumptions appear in [`THEOREM.md`](THEOREM.md). The public priority record and recommended citation appear in [`PUBLICATION.md`](PUBLICATION.md).
