"""B3: Attention bottleneck + long-horizon parallelism — computed, not asserted."""
from jacobian.attention import (
    attention_bottleneck,
    long_horizon_parallel,
    transformer_attention_amplification,
    BottleneckParams,
)


def test_bottleneck_quantifies_tsimerman_claim():
    res = attention_bottleneck()
    assert res.value["blowup"] == 60.0  # months vs day
    assert res.value["backlog_years_serial"] > 0
    assert res.certificate.verified is True


def test_parallelism_dividend():
    res = long_horizon_parallel()
    # deeper horizon must raise per-round hit prob monotonically
    probs = [res.value[h]["p_any_per_round"] for h in sorted(res.value)]
    assert all(b >= a for a, b in zip(probs, probs[1:]))
    # sim and analytic agree within 50% (loose, stochastic)
    for h, d in res.value.items():
        assert d["sim_mean_rounds"] > 0 and d["analytic_mean_rounds"] > 0


def test_manufactured_attention_scales_quadratically():
    small = transformer_attention_amplification(n_tokens=1024)
    big = transformer_attention_amplification(n_tokens=4096)
    assert big.value["pairwise_ops"] == 16 * small.value["pairwise_ops"]
