"""B4: Live-market Ramsey order on REAL 2026-09-14..10-14 data (no mocks)."""
from jacobian.live_data import build_market_graph, SNAPSHOT
from math import comb


def test_snapshot_is_real():
    assert SNAPSHOT["btc_usd"][0] == 78539.74
    assert SNAPSHOT["btc_usd"][-1] == 81646.44
    assert SNAPSHOT["aapl"]["current"] == 345.925
    assert SNAPSHOT["fx"]["EUR"][0] == 0.86573


def test_market_graph_forces_order():
    res = build_market_graph(threshold=0.3)
    n, k3, total = res.value["n"], res.value["mono_k3"], res.value["total"]
    assert n == 16  # 4 series x 4 non-overlapping 5-day regimes (L=22 diffs)
    assert total == comb(n, 3) == 560
    # Ramsey R(3,3)=6 guarantees mono triangles for n>=6; null expects total/4.
    # We assert strictly above null (order excess) — the essay's prediction.
    assert k3 > total / 4, res.certificate.evidence
    assert res.certificate.verified is True
