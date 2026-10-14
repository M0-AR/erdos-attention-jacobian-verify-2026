# Benchmark spec — all thresholds are computed, not chosen

## B1 Ramsey (benchmarks/test_ramsey.py)
- `test_r33_equals_6_exhaustive`: all 2^15=32,768 K6 colorings contain a mono
  triangle; exhibited K5 (C5-red) has 0. Pass iff proved==True.
- `test_k5_counter_on_empty_and_complete`: K7 empty/complete → C(7,5)=21.
- `test_r55_public_bounds`: lower==43, upper==46, sources contain
  "2409.15709" and "Exoo".
- `test_sat_size_k43_matches_literature`: vars==903, clauses>1M
  (exact C(43,5)*2=1,925,196).
- `test_exoo_style_graph_counts`: 42-node circulant builds; counter verifies.

## B2 Verifiability (benchmarks/test_verifiability.py)
- `test_resultant_sign_bug_fixed`: truth numeric −8, symbolic −a³;
  `bug_live==True` on SymPy 1.14.0; `wrapper_detected==True`. This is the
  essay's thesis reproduced as a failing-CAS/passing-wrapper pair.
- `test_resultant_swap_identity_holds_both_orders`: truth respects
  (−1)^(1·3)=−1 flip (−8 vs +8); wrapper flags `sympy_correct==False` on the
  ascending-degree order.
- `test_factor_poly_guards_21180`: factor_list rebuilds by expansion;
  contains (x+3)^2 factor.

## B3 Attention (benchmarks/test_attention.py)
- `test_bottleneck_quantifies_tsimerman_claim`: blowup==60.0; backlog>0.
- `test_parallelism_dividend`: p_any monotone in horizon; sim/analytic >0.
- `test_manufactured_attention_scales_quadratically`: 4× tokens → 16× ops.

## B4 Live market (benchmarks/test_live_market.py)
- `test_snapshot_is_real`: BTC 78539.74→81646.44; AAPL 345.925; EUR 0.86573.
- `test_market_graph_forces_order`: n==16, total==C(16,3)==560,
  mono-K3 > total/4. Observed 2026-10-14: **229/560 vs null 140 (+89)**.

## Runners
- `pytest -q`: 13 tests (gate for any claim).
- `experiments/run_all.py --out results`: 9 experiments E1–E4 + JSONL +
  SUMMARY.md + market snapshot. Exit 1 on any FAIL.
- `docker compose up research/test`: identical results in container.
