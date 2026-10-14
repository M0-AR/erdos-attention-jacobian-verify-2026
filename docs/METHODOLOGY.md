# Methodology — zero-to-hero verification (2026-10-14)

This repo verifies the essay "AI Math, Paul Erdős & Attention" end-to-end
against public data and live market data. Nothing is asserted by hand:
every number below is computed by `experiments/run_all.py` and checked by
`benchmarks/test_*.py`.

## 0. Research protocol (sequential, rate-limit-safe)

One search at a time (never parallel websearch — avoids 429), with
backoff + DuckDuckGo-lite fallback, as requested:

1. `websearch` — Erdős Problem #77 / R(5,5) status 2026.
2. `duckduckgo_search` — Tsimerman Fields Medal / Last Generation interview.
3. `openresearch.web_search` — Tao AI views / ingenuity-persistence.
4. `paper-search.search_papers` — Lean / AlphaProof / formal agents.
5. `agent-reach_search(web)` — SymPy resultant sign bug + Lean-vs-Python.
6. `kaggle.search_everything` + `discussions_search` + `datasets_list`.
7. `wiki.search` + `get_summary` — Ramsey's theorem.
8. `gitmcp.search_generic_documentation` — Lean4 verified stdlib.
9. `gsd_websearch` + `superpowers.semantic_search_skills` — benchmark practice.
10. `openresearch.search_openalex` — long-horizon reasoning (COMPASS/ICLR/recursion).
11. `paper-search.search_arxiv/semantic/openalex/crossref` — Ramsey + verification.
12. `openresearch.search_news/hacker_news/stackoverflow` — Oct-2026 proof drops.
13. `openresearch.get_current_date/get_crypto_price/get_fx_rate` +
    `agent-reach.stock_quote` — live-market anchors (BTC/FX/AAPL 2026-10-14).
14. `webfetch(lite.duckduckgo.com)` — Exa-bypass fallback confirmation.

Different keywords per tool (voting across sources, not echo-chamber).

## 1. Claim → evidence mapping

| Essay claim | Public source (checked 2026-10-14) | Repo verification |
|---|---|---|
| R(5,5) unknown; Erdős evil-spirit quote; "no true randomness at scale" | 43≤R(5,5)≤46: Exoo 1989 lower; Angeltveit–McKay arXiv:2409.15709, JGT 2026 upper; 903 vars/1.9M clauses direct-K43; 656/656 UNSAT extension (bigcompute.science, not proof) | B1: R(3,3)=6 exhaustive (32,768 colorings) + K5-counter + SAT sizing + bounds table |
| Tsimerman: sparse specialists; in-field 1 day vs out-of-field months; math bottlenecked by attention; joined OpenAI safety after 2026 Fields Medal (André–Oort) | Quanta 2026-07-23; New Scientist; Theories of Everything YT; "Last Generation" podcast 10 days post-medal | B3: bottleneck queue model, 60× blowup computed; manufactured-attention ops |
| Tao/Perelman: ingenuity+persistence (7 yrs); agent finds 1 of ~100 approaches; needs long-horizon + parallelism (human+agent) | Tao tao-web AI views; ICM 2026 "Mathematics in the Age of AI"; Simons 2026-08-13; arXiv:2608.16753 | B3: 100-approach search model, analytic+sim dual path, horizon dividend table |
| Agents = attention blocks + tools; transformers manufacture attention | Vaswani 2017; COMPASS ACL 2026; ICLR-compression arXiv:2609.29875; recursive models arXiv:2603.02112 | B3: pairwise-ops counter, quadratic scaling test |
| Python dynamically typed, less verifiable; agents reinvent wheel; NumPy/SymPy decade-old bugs; math infra lacking (Tao) | SymPy #10666 (2016) sign bug + PR #30329; #21180 Poly/Expr; GroebnerTactic 2604.13514; NSPI 2605.15445; Veriphy; Bourbaki | B2: live repro on SymPy 1.14.0 (returns +8, truth −8); wrapper returns Sylvester truth + flags bug |
| Jacobian: growing library of atomic composable techniques | Lean Mathlib (>100k lemmas); AXLE 500M reqs, 12/12 Putnam 2025; Science 2026 formal-proof-search (9/353 Erdős, 44/492 OEIS); OpenAI 722 proofs Oct-2026; Gemini 5 proofs | This repo: `src/jacobian/` — 4 modules, typed, certificate-bearing |

## 2. Best practice adopted (2026 consensus)

Tao (2026): "combin[e] with traditional verification to filter hallucinations."
Concretely: **skeptical/certificate architecture** — CAS/LLM = untrusted oracle;
minimal independent checker (Sylvester det, brute-force enumeration,
kernel-style `no-sorry` gate) = verifier. SAT results require certificates
(Glucose) + independent replication (Angeltveit–McKay did it twice).
Benchmarks pin versions, seeds, UTC dates, raw snapshots.
