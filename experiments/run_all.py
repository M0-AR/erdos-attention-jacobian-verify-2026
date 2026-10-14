"""Reproducible experiment runner: executes every benchmark as an experiment,
writes JSONL + markdown evidence, exits non-zero on any failure.

Usage: python experiments/run_all.py [--out results/]
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from jacobian import attention as A
from jacobian import live_data as L
from jacobian import ramsey as R
from jacobian import verification as V


def run(name, fn):
    t0 = time.time()
    try:
        res = fn()
        val = res.value if hasattr(res, "value") else res
        cert = res.certificate.__dict__ if hasattr(res, "certificate") else {}
        # json-safe
        def safe(o):
            try:
                json.dumps(o)
                return o
            except Exception:
                return str(o)

        return {"experiment": name, "status": "pass", "seconds": round(time.time() - t0, 3), "value": safe(val if not isinstance(val, dict) or "adj" not in val else {k: v for k, v in val.items() if k != "adj"}), "certificate": safe(cert)}
    except Exception as e:
        return {"experiment": name, "status": "FAIL", "error": str(e), "trace": traceback.format_exc()[-2000:]}


def main():
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "results"
    os.makedirs(outdir, exist_ok=True)
    import sympy as sp

    x, a = sp.symbols("x a")
    experiments = [
        ("E1-r33-exhaustive", R.verify_r33_equals_6),
        ("E1-r55-status", lambda: type("O", (), {"value": R.ramsey_bounds_status(), "certificate": type("C", (), {"__dict__": {}})()})()),
        ("E1-sat43", lambda: type("O", (), {"value": R.sat_size_estimate(43), "certificate": type("C", (), {"__dict__": {}})()})()),
        ("E2-resultant-bug", V.classic_bug_demo),
        ("E2-factor-guard", lambda: V.factor_poly_checked(sp.Poly(x**4 + 6*x**3 + 4*x**2 - 30*x - 45, x))),
        ("E3-bottleneck", A.attention_bottleneck),
        ("E3-long-horizon", A.long_horizon_parallel),
        ("E3-attention-ops", A.transformer_attention_amplification),
        ("E4-market-order", L.build_market_graph),
    ]
    rows = [run(n, f) for n, f in experiments]
    # persist snapshot too
    snap_path = L.persist_snapshot(os.path.join(outdir, "market_snapshot_2026-10-14.json"))
    with open(os.path.join(outdir, "results.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    fails = [r for r in rows if r["status"] != "pass"]
    md = ["# Experiment results (2026-10-14 UTC)", ""]
    for r in rows:
        md.append(f"- {r['experiment']}: **{r['status']}** ({r.get('seconds', '?')}s)")
    md += ["", f"snapshot: {snap_path}", f"failures: {len(fails)}"]
    with open(os.path.join(outdir, "SUMMARY.md"), "w") as f:
        f.write("\n".join(md))
    print("\n".join(md))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
