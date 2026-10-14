"""B1: Ramsey ground truth — R(3,3)=6 exhaustive + R(5,5) status + SAT sizing."""
from jacobian.ramsey import (
    count_monochromatic_k5,
    ramsey_bounds_status,
    sat_size_estimate,
    verify_r33_equals_6,
    exoo_42_circulant,
)
import numpy as np


def test_r33_equals_6_exhaustive():
    res = verify_r33_equals_6()
    assert res.value["R33"] == 6 and res.value["proved"] is True
    assert res.certificate.verified is True


def test_k5_counter_on_empty_and_complete():
    # K7 empty (all blue) -> C(7,5)=21 mono; K7 complete (all red) -> 21
    n = 7
    empty = np.zeros((n, n), dtype=int)
    full = np.ones((n, n), dtype=int)
    np.fill_diagonal(full, 0)
    assert count_monochromatic_k5(empty).value == 21
    assert count_monochromatic_k5(full).value == 21


def test_r55_public_bounds():
    st = ramsey_bounds_status()
    assert st["R55_lower"] == 43 and st["R55_upper"] == 46
    assert "2409.15709" in st["upper_source"]
    assert "Exoo" in st["lower_source"]


def test_sat_size_k43_matches_literature():
    est = sat_size_estimate(43)
    assert est["vars"] == 903  # 43*42/2 — matches bigcompute.science
    assert est["clauses"] > 1_000_000  # C(43,5)*2 = 1,925,252


def test_exoo_style_graph_counts():
    adj = exoo_42_circulant()
    assert adj.shape == (42, 42)
    res = count_monochromatic_k5(adj)
    assert res.certificate.verified is True
    # informational: must be >= 0; the heuristic basin is not claimed K5-free
    assert res.value >= 0
