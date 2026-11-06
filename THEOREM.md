# AXEZENT GaugeRail-001: Gauge Quotients and Exact Robust Route Certificates

**Author:** Shawn Calvin Snelling (AXEZENT AI Research)  
**Public source publication:** November 6, 2026 · [publication record](PUBLICATION.md)  
**Version:** 1.2.0 · **License:** MIT  
**Reproducibility:** Python 3.10+, exact rational arithmetic, executable certificate and adversarial tests.

## Abstract

We give a self-contained characterization of edge perturbations that are invisible to all source-to-target path comparisons in a finite directed acyclic graph, and an exact single-scenario reduction for the worst regret of a fixed path under independent rational intervals. The structural invariant is the edge-cost vector modulo vertex-potential gradients. We also establish an independently checkable potential certificate, stability-radius formula, invariance under faithful series subdivision, and a separately scoped correlated-factor-box radius identity computed by exhaustive path enumeration. The results are presented with exact assumptions, proofs and corresponding executable tests. Their connections to earlier shortest-path reweighting, path independence and interval-robust optimization research are documented in the related-work section.

## Definitions and assumptions

Let \(G=(V,E)\) be a **finite directed acyclic multigraph**; parallel arcs are identified by distinct labels. Let \(s\ne t\) and assume there is at least one directed \(s\)-to-\(t\) path. A path is identified with its arc sequence and edge-incidence set, since acyclicity prevents repeated arcs.

For any arc vector \(x\in\mathbb R^E\) and path \(Q\), set \(x(Q)=\sum_{e\in Q}x_e\). Let \(G_*\) be the subgraph containing exactly the arcs and vertices that occur on at least one \(s\)-to-\(t\) path. It is connected when regarded as an undirected graph.

An **edge-gradient** is the arc field \((\nabla\phi)_{(u,v)}=\phi(v)-\phi(u)\), for a vertex function \(\phi:V_*\to\mathbb R\). A perturbation \(h\) is **route-invisible** if \(h(Q)\) is the same number for every \(s\)-to-\(t\) path \(Q\). No positivity assumptions on weights are needed because the graph is acyclic.

For the uncertainty result, fix base costs \(b_e\in\mathbb R\) and independent intervals \(\eta_e\in[\ell_e,u_e]\). A possibly unbounded correlated background field is allowed if it is an edge-gradient for each parameter choice \(\theta\):

\[
 c_e(\theta,\eta)=b_e+\phi_\theta(v)-\phi_\theta(u)+\eta_e.
\]

The function \(\phi_\theta\) may be arbitrary; **all arcs must use the same vertex-potential field within a scenario**. The \(\eta_e\) variables must be independently selectable throughout their respective intervals. These two assumptions are essential.

## Theorem 1: Exact characterization of invisible changes (gauge quotient)

The following are equivalent for an arc field \(h\) restricted to \(G_*\):

1. Every \(s\)-to-\(t\) path has the same added cost \(h(Q)\).
2. There is a vertex function \(\phi:V_*\to\mathbb R\) such that \(h_{(u,v)}=\phi(v)-\phi(u)\) for every arc of \(G_*\).

Consequently, the space of observable path-cost distinctions is the quotient
\(\mathbb R^{E_*}/\operatorname{im}(\nabla)\), whose dimension is
\(|E_*|-|V_*|+1\).

### Proof

**(2 \(\Rightarrow\) 1).** Summing along \(Q=(s=v_0,v_1,\dots,v_k=t)\), we obtain

\[
 h(Q)=\sum_{j=0}^{k-1}[\phi(v_{j+1})-\phi(v_j)]=\phi(t)-\phi(s).
\]

This does not depend on the path.

**(1 \(\Rightarrow\) 2).** Fix a vertex \(v\in V_*\). Pick an arbitrary directed path \(R_{sv}\) from \(s\) to \(v\), and define \(\phi(v)=h(R_{sv})\). This is well-defined: if \(R'_{sv}\) is another such path, choose a directed path \(T_{vt}\) from \(v\) to \(t\), which exists since \(v\in V_*\). By acyclicity, concatenations \(R_{sv}T_{vt}\) and \(R'_{sv}T_{vt}\) are directed \(s\)-to-\(t\) paths. Their added costs are equal by (1), so \(h(R_{sv})=h(R'_{sv})\). For any arc \(e=(u,v)\in E_*\), concatenate a path from \(s\) to \(u\) with \(e\). Hence \(\phi(v)=\phi(u)+h_e\), or \(h_e=\phi(v)-\phi(u)\).

The underlying undirected graph of \(G_*\) is connected because every one of its edges lies on a common-endpoint \(s\)-to-\(t\) path. The linear map \(\nabla:\mathbb R^{V_*}\to\mathbb R^{E_*}\) therefore has a one-dimensional kernel (constant vertex functions). By rank-nullity, its image has dimension \(|V_*|-1\), and the quotient has dimension \(|E_*|-|V_*|+1\). **QED.**

### Interpretation

What is invariant is *not* the absolute cost of an individual path. It is the family of differences \(h(P)-h(Q)\), which depends only on the class of \(h\) modulo gradients. This is a graph-theoretic gauge freedom, analogous in mathematical form—but not physical meaning—to changing coordinates while preserving observables.

## Theorem 2: One-scenario identity for exact worst-case regret

Fix any \(s\)-to-\(t\) path \(P\). Form the single adversarial weight vector

\[
 w^P_e=b_e+\begin{cases}u_e,&e\in P,\\\ell_e,&e\notin P.\end{cases}
\]

Define the robust regret of \(P\) by

\[
 \mathcal R(P)=\max_{\eta\in\prod_e[\ell_e,u_e]}
  \left[c(P;\theta,\eta)-\min_{Q:s\leadsto t}c(Q;\theta,\eta)\right].
\]

**Claim.** For every parameter \(\theta\), with no bound on the vertex potentials,

\[
 \boxed{\mathcal R(P)= w^P(P)-\min_{Q:s\leadsto t}w^P(Q).}
\]

In particular, \(P\) remains a shortest path for **every** allowed uncertainty scenario if and only if \(\mathcal R(P)=0\), equivalently if and only if \(P\) is a shortest path for the single vector \(w^P\).

### Proof

For any two paths \(P,Q\), the gradient terms cancel by telescoping:

\[
 c(P;\theta,\eta)-c(Q;\theta,\eta)
  =b(P)-b(Q)+\sum_{e\in P\setminus Q}\eta_e
                    -\sum_{e\in Q\setminus P}\eta_e.
\]

Terms on shared arcs cancel. All coefficients of variables in \(P\setminus Q\) are positive; all coefficients on \(Q\setminus P\) are negative. The expression is therefore maximized by setting \(\eta_e=u_e\) for \(e\in P\) and \(\eta_e=\ell_e\) for \(e\notin P\). Crucially, **this same scenario maximizes the difference for every competing \(Q\) simultaneously**, because terms on common edges cancel. Thus, for all admissible \(\eta\),

\[
 c(P;\theta,\eta)-c(Q;\theta,\eta)
 \le w^P(P)-w^P(Q).
\]

Now use the finite path family and the identity
\(a(P)-\min_Q a(Q)=\max_Q[a(P)-a(Q)]\):

\[
\begin{aligned}
\mathcal R(P)
&=\max_{\eta}\max_Q [c(P;\theta,\eta)-c(Q;\theta,\eta)]\\
&\le \max_Q[w^P(P)-w^P(Q)]\\
&=w^P(P)-\min_Q w^P(Q).
\end{aligned}
\]

At the explicitly allowed scenario \(\eta_e=u_e\) on \(P\) and \(\eta_e=\ell_e\) off \(P\), every difference realizes the corresponding right-hand expression, so equality holds. A path is shortest in every scenario precisely when its regret is zero. **QED.**

### Constructive falsification witness

If \(\mathcal R(P)>0\), a shortest route \(Q\) under \(w^P\) and the single scenario \(\eta^P\) give an exact counterexample: \(c(P;\theta,\eta^P)>c(Q;\theta,\eta^P)\). No appeal to random testing is required.

## Theorem 3: Short, independently verifiable proof certificate

For a fixed \(P\), let \(w^P\) be the vector above. Write \(V_t\) for all vertices that can reach \(t\). An exact rational vector \(d:V_t\to\mathbb Q\) is a **robustness certificate** if:

- \(d(t)=0\);
- for every arc \(e=(u,v)\) with \(v\in V_t\), \(d(u)\le w^P_e+d(v)\);
- for every arc \(e=(u,v)\in P\), \(d(u)=w^P_e+d(v)\).

Then \(P\) is shortest under \(w^P\), hence robust under every admissible scenario. Conversely, for a DAG with rational input, if \(P\) is robust, the exact shortest distances from each \(v\in V_t\) to \(t\) constitute such a certificate.

### Proof

For any \(s\)-to-\(t\) path \(Q=(e_1,\dots,e_k)\), sum the first inequalities along \(Q\):
\(d(s)\le \sum_{e\in Q}w^P_e+d(t)=w^P(Q)\). Summing the equalities on the candidate \(P\) yields \(d(s)=w^P(P)\). Therefore \(w^P(P)\le w^P(Q)\) for every \(Q\). Theorem 2 gives robustness. For the converse, take \(d(v)\) as the actual shortest distance from \(v\) to \(t\), finite on \(V_t\). Bellman's inequalities hold; the arcs on a shortest \(s\)-to-\(t\) path must all be tight, or replacing a non-shortest suffix would improve the path. **QED.**

**Verification complexity:** after parsing and graph reachability, \(O(|V|+|E|)\) exact rational comparisons. Generating the certificate uses DAG shortest-path dynamic programming in \(O(|V|+|E|)\) arithmetic operations after a topological order is obtained. Fraction arithmetic bit complexity depends on numerator and denominator lengths. No cryptographic hash is a substitute for these inequalities.

## Theorem 4: Sharp symmetric perturbation radius

Assume base-cost optimality: \(b(P)\le b(Q)\) for every route \(Q\). Let nonnegative strengths \(a_e\ge0\) be fixed, and allow \(|\eta_e|\le \rho a_e\), independently, for \(\rho\ge0\). Set
\(D(P,Q)=\sum_{e\in P\triangle Q}a_e\), using the symmetric difference of arc sets.

Then \(P\) is shortest for every admissible scenario precisely for

\[
 0\le\rho\le\rho_*:=\min_{Q:D(P,Q)>0}
 \frac{b(Q)-b(P)}{D(P,Q)},
\]

where the minimum over the empty set is \(+\infty\). This bound is sharp, including ties at equality.

### Proof

Theorem 2 with \(u_e=\rho a_e\), \(\ell_e=-\rho a_e\) gives
\[
\mathcal R_\rho(P)
 =\max_Q\{b(P)-b(Q)+\rho D(P,Q)\}.
\]

Because \(b(P)\le b(Q)\), each term with \(D(P,Q)=0\) is nonpositive, and for every term with positive \(D(P,Q)\), nonpositivity holds exactly when
\(\rho\le[b(Q)-b(P)]/D(P,Q)\). Since \(Q=P\) contributes zero, the maximum is zero precisely when all terms are nonpositive. If \(\rho>\rho_*\) and the family is nonempty, a minimizing competing path yields a strictly positive regret. **QED.**

**Scope:** The formula is exact, but naive enumeration of every path to compute \(\rho_*\) may be exponential. The software intentionally caps exhaustive radius enumeration and **does not claim polynomial-time radius optimization**. For a fixed proposed \(\rho\), the certificate from Theorem 3 still gives a linear-size check.

## Theorem 5: Faithful edge subdivision does not change any conclusion

Suppose a single arc \(e=(u,v)\) is replaced by \(e_1=(u,z)\), \(e_2=(z,v)\), where \(z\) is a fresh vertex with no other incident arcs. Suppose
\(b_{e_1}+b_{e_2}=b_e\), \(\ell_{e_1}+\ell_{e_2}=\ell_e\), and \(u_{e_1}+u_{e_2}=u_e\), and that the two new interval residuals vary independently. Then the family of path-cost vectors induced on the old routes is exactly unchanged, as are all robust regret values and robust/fragile classifications. A vertex potential assigned arbitrarily to \(z\) also cancels along the two new arcs.

### Proof

Every old \(s\)-to-\(t\) path has precisely one new counterpart, replacing occurrence of \(e\) by the consecutive pair \(e_1e_2\). Conversely every new route traversing \(z\) must use both new arcs because \(z\) has no other incidences. The Minkowski sum of independent intervals \([\ell_{e_1},u_{e_1}] + [\ell_{e_2},u_{e_2}]\) is exactly \([\ell_e,u_e]\). Thus every old edge residual is realized by a pair of new residuals and vice versa, and all route-cost choices correspond, after summing the two edge costs. The gradient offset telescopes: \(\phi(z)-\phi(u)+\phi(v)-\phi(z)=\phi(v)-\phi(u)\). Therefore all route cost comparisons and the maximum regret are identical. **QED.**

## Theorem 6: Exact robustness radius for a correlated-factor box

This is an **additional, narrowly scoped theorem**; it is **not** a general
single-scenario compression theorem for arbitrary correlations.

Assume the same finite acyclic multigraph and fixed candidate route \(P\) as
above. Let the uncertain arc costs be

\[
 c_e(\theta,\xi)=b_e+\phi_\theta(v)-\phi_\theta(u)
                +\sum_{j=1}^{k}\Lambda_{ej}\xi_j,
 \qquad |\xi_j|\le\rho a_j,
\]

where \(\Lambda\) is an arbitrary *fixed rational* edge-by-factor matrix,
\(a_j\ge0\) are fixed rational amplitudes, and the factor coordinates
\(\xi_j\) vary **independently in a symmetric box**. The factors may correlate
arbitrarily many arc costs because one factor appears on many edges. Assume
\(P\) is shortest at \(\rho=0\), and define for any competing route \(Q\)

\[
 g(P,Q)=b(Q)-b(P)\ge0,
 \quad
 S(P,Q)=\sum_{j=1}^{k} a_j\left|
        \sum_{e\in P}\Lambda_{ej}-\sum_{e\in Q}\Lambda_{ej}
        \right|.
\]

**Claim (sharp radius and regret):** At any \(\rho\ge0\), the exact maximum
regret of the candidate is

\[
 \boxed{\mathcal R_\rho(P)=\max_{Q:s\leadsto t}
       \{\rho S(P,Q)-g(P,Q)\}.}
\]

Thus the route is shortest for every admissible correlated uncertainty
configuration if and only if \(\rho\le\rho_*\), with

\[
 \boxed{\rho_* = \min_{Q:S(P,Q)>0}\frac{g(P,Q)}{S(P,Q)},}
\]

where the minimum over an empty set is \(+\infty\). Equality permits ties.
When the computed regret is positive, a maximizing competitor \(Q_*\) and
factor vector \(\xi_j=\rho a_j\operatorname{sgn}(\Delta_j(P,Q_*))\),
where \(\Delta_j(P,Q)=\sum_{e\in P}\Lambda_{ej}-\sum_{e\in Q}\Lambda_{ej}\),
give an explicit falsification witness. Set the factor to zero when its
coefficient is zero.

### Proof

For a fixed pair \(P,Q\), telescope all edge-gradient terms. Then

\[
 c(P;\theta,\xi)-c(Q;\theta,\xi)
   =-g(P,Q)+\sum_{j=1}^k\Delta_j(P,Q)\xi_j.
\]

The maximum over the independent box \(|\xi_j|\le\rho a_j\) is the support
function of the box:
\[
 \max_{\xi}\sum_j\Delta_j\xi_j
     =\rho\sum_j a_j|\Delta_j|=\rho S(P,Q).
\]

The family of routes is finite since the graph is a DAG. Therefore the
order of maximizing over \(Q\) and \(\xi\) can be interchanged:

\[
 \max_{\xi}\bigl[c(P;\xi)-\min_Q c(Q;\xi)\bigr]
   =\max_Q\max_{\xi}[c(P;\xi)-c(Q;\xi)]
   =\max_Q[\rho S(P,Q)-g(P,Q)].
\]

Since \(Q=P\) contributes zero, the regret vanishes if and only if every
term is nonpositive. The nominal-optimality assumption makes
\(g(P,Q)\ge0\); for \(S>0\), the condition is precisely
\(\rho\le g(P,Q)/S(P,Q)\). Competitors with \(S=0\) impose no additional
constraint. Taking the minimum yields the sharp threshold. Choosing the
factor signs as above simultaneously realizes the support value for the
worst competitor, supplying the concrete witness. **QED.**

### Complexity and essential limitation

The bundled verifier exhaustively enumerates directed s-to-t routes to
compute \(\rho_*\), and aborts on exceeding a configurable path cap. Hence
its time can be **exponential in the number of vertices**, even though
factor dimension \(k\) is small. It uses **exact rational arithmetic**.

Unlike independent edge intervals, a *single constructed factor vector*
need not maximize the differences against **all** competitors at once:
one route comparison can favor \(\xi_1=+\rho a_1\), while another favors
\(\xi_1=-\rho a_1\). Consequently, the earlier single-scenario certificate
is **not** extended to arbitrary affine correlations. A candidate statement
saying arbitrary correlated routing has a universally valid single
adversarial scenario or quadratic-time proof is **not justified** by this
result.

### Worked correlated example

For `examples/robust_route.json` and `examples/correlated_box.json`, the
candidate has two edges, both with coefficient \(1\) on the first factor.
The rival `s-b-t` has two edges each with coefficient \(-1\) on the second
factor, whose amplitude is \(1/2\). The path-cost gap is 4 and the
sensitivity is \(2+2(1/2)=3\), hence this rival gives \(4/3\). The direct
`s-t` arc gives gap 3 and sensitivity 2, hence \(3/2\). Therefore the
**exact correlated radius is \(4/3\)**, with ties at equality.

## Example: three-route logistics network

The `examples/robust_route.json` graph has candidate \(P=s\to a\to t\) with baseline cost 6, competitors \(s\to b\to t\) at 10 and \(s\to t\) at 9. Every edge residual lies in \([-1/4,1/4]\).

Under the single adversarial scenario, the candidate costs \(13/2\); the other routes cost \(19/2\) and \(35/4\). Thus \(P\) remains shortest, with exact regret zero. The potential certificate is \(d(t)=0\), \(d(a)=13/4\), \(d(b)=19/4\), \(d(s)=13/2\).

If instead the uncertainty grows to \([-2,2]\) on the two-path example, the candidate costs 10 while the alternative costs 4, giving an exact worst-regret witness of 6.

The sharp uniform radius for the first graph with \(a_e=1\) is \(\rho_*=1\). In particular the rival \(s\to b\to t\) has nominal cost gap 4 and four edges in its symmetric difference with \(P\), which makes \(4/4=1\).

## Assumptions, related work and implementation limits

1. The **one-scenario reduction** holds for **independently** varying edge residuals. Grouped or correlated errors beyond the gradient field can invalidate it. Theorem 6 covers only a specified correlated **factor box**, by potentially exponential path enumeration.
2. The characterization of gradient invisibility is on the **s-to-t relevant subgraph**. Perturbations on arcs in no s-to-t route are unobservable for trivial reasons and are not required to be gradients.
3. Acyclicity permits negative costs without negative-cycle complications. General directed graphs require additional conventions for negative cycles and feasible walks.
4. Gauge invariance, shortest-path potentials, and adversarial scenarios in interval robust optimization are **known mathematical themes**. The linked references document relevant foundations. This note offers its own complete exposition and software implementation, without claiming priority over those earlier results or suggesting external peer review.
5. The input fingerprint is a **consistency check, not source authentication**; the certificate verifier assumes trusted network data. See `SECURITY.md`. The Python tests are finite evidence of implementation correctness. They do **not** replace the general algebraic proofs above and do not constitute Lean/Coq formal verification.
6. The examples demonstrate behavior within the specified mathematical models; commercial impact requires independent field evaluation.

## References and context

- MIT 6.006, *Johnson's Algorithm: Reweighting Shortest Paths* (2020): https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/6027e2a155c948937fdfb93981f7070c_MIT6_006S20_r14.pdf
- *The Robust Shortest Path Problem with Interval Data* (2001): https://optimization-online.org/2001/08/361/
- *Robust and Distributionally Robust Shortest Path Problems: A Survey* (2025): https://doi.org/10.1016/j.cor.2025.107096
- *Computing all shortest passenger routes with a tropical Dijkstra algorithm* (2025): https://doi.org/10.1016/j.ejtl.2025.100163
- Motivating physics analogy: Barrios Hita et al., *Quantum Mechanics Based on Real Numbers: A Consistent Description*, PRL 136, 240202 (2026), https://doi.org/10.1103/4k13-sdjh . **The present graph theorem is not a result about quantum physics.**

For executable usage, validation instructions and publication-history anchors, see [USAGE.md](USAGE.md), [VALIDATION.md](VALIDATION.md) and [PUBLICATION.md](PUBLICATION.md).
