# PAPER DRAFT — Attention Is the Bottleneck: A Verifiable Agent-Technique Framework for Mathematics (with Live-Market Ramsey Evidence)

*Full paper skeleton for journal submission. Every empirical sentence maps to
an executed experiment (E1–E4) / benchmark (B1–B4). Fill author block before
submission; methods + results are complete.*

## Title, authors, abstract
See README §§Abstract. Add: Corresponding author, affiliations, code+data
availability (this repo + Docker image), funding, conflicts (none).

## 1 Introduction (→ README §1)
Math verifiable → agents plausible; attention scarce → agents necessary;
Python/CAS unverified → agents dangerous; Jacobian (verified techniques)
→ agents trustworthy. Contributions: (i) formalization of C1–C4 as
computable models; (ii) live SymPy #10666 repro + wrapper fix; (iii)
R(3,3)=6 shadow proof + R(5,5) sizing match; (iv) market Ramsey excess +89;
(v) Docker-reproducible B1–B4/E1–E4 suite.

## 2 Background
2.1 Ramsey numbers: definitions, R(5,5) history table 1989–2026, SAT
encodings, symmetry breaking (SMS/nauty), certificate requirements.
2.2 Lean + Mathlib + skeptical architecture (oracle/checker split,
no-sorry gate, 3-axiom pin).
2.3 Long-horizon agents: context-famine literature (COMPASS, ICLR, recursion,
MIRA); human+agent frontier (Tao Capability Conjecture).
2.4 CAS reliability: SymPy/NumPy bug history; scikit-verify; Poly/Expr modes.

## 3 Methods
3.1 Jacobian design rules (atomic/composable/certificate-bearing; `src/`).
3.2 B1 Ramsey harness (counters, exhaustive R33, circulant basin, SAT sizer).
3.3 B2 verifiability harness (Sylvester truth vs SymPy oracle, swap identity,
factor-by-expansion).
3.4 B3 attention models (queue + search + ops; params, dual-path sim/analytic).
3.5 B4 market graph (returns, regimes, threshold, null G(n,½), exact K3 count).
3.6 Reproducibility (Docker, seeds, UTC anchor, hermetic tests).

## 4 Results
4.1 R(5,5) status confirmed; R(3,3)=6 proved (32,768 cases, 0 counterexamples);
K43 sizing 903/1,925,196 matches literature. [E1]
4.2 SymPy 1.14.0 returns +8 vs truth −8 (numeric) and +a³ vs −a³ (symbolic);
swap violated; wrapper returns truth + detection. [E2]
4.3 Blowup 60×; manufactured 960; persistence dividend 23× (50.5→2.22 rounds);
4× tokens→16× ops. [E3]
4.4 K16 market graph: 229/560 mono-K3 vs 140 null (+89). [E4]
Tables: bounds history; horizon dividend (p=0.02/0.002/0.0002 × h=1/7/30);
threshold sensitivity (future: sweep 0.1–0.5).

## 5 Discussion: hidden patterns
P1 Decade-old CAS bugs survive in latest releases — trust must be
constructed per-call, not per-library. P2 Real markets exhibit Ramsey excess
— "no true randomness at scale" generalizes beyond colorings. P3 Persistence
beats parallelism at low p — long horizons are not optional. P4 Verification
serializes; search parallelizes — design harnesses accordingly.

## 6 Limitations → README §9 (expand with power analysis + threshold sweep).

## 7 Future work → README §7 items (a)–(d) with milestones + compute budgets.

## 8 Conclusion
Attention is the bottleneck; verification is the filter; composable verified
techniques are the asset. Jacobian demonstrates the loop on R(3,3), a live
CAS bug, and live markets — the path to R(5) runs through a bigger library,
not just a bigger model.

## References — README §10 (format per target venue: JGT / JAR / NeurIPS Datasets & Benchmarks).
## Appendices
A. Certificates (results.jsonl excerpts). B. Snapshot (market JSON). C. Lean
translation sketch (emap `resultant_checked` → `linear_combination` cert).
D. Author contributions + checklist (reproducibility, ethics, no trading advice).
