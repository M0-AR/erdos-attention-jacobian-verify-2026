# Reproducibility

- Date anchor (UTC): 2026-10-14 (via `get_current_date`).
- Python 3.12, numpy/sympy(1.14.0)/networkx/pandas/requests/pyyaml/pytest.
- Seeds: long-horizon sim seed=0; market graph deterministic (no RNG).
- Live data: BTC 30d CoinGecko keyless ending 2026-10-14; FX ECB/Frankfurter
  same window (23 pts, weekends sparse); AAPL Yahoo v8 2026-10-14
  (345.925, +1.36%). Raw snapshot checked into
  `results/market_snapshot_2026-10-14.json` by the runner (regenerate with
  `persist_snapshot`). If offline, tests use the in-code SNAPSHOT (identical).
- Docker: `docker compose build && docker compose up research` reproduces
  `results/`; `docker compose up test` reproduces 13/13 pytest.
- No network required for verification (all tests hermetic).
- Version pins: see evidence fields (`sympy_version`, `checked_utc`,
  `window`) in every certificate.
