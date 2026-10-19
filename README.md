# Polymarket Historical Data — Free Closed-Event Tape

The complete on-chain fill tape for the two Polymarket markets that resolved the 2024 US
Presidential Election. Every executed fill from market creation to settlement, as Parquet, with the
transaction hash, outcome token, wallet, price, and size.

Built by [CrowdIntel](https://crowdintel.xyz/data) from Polymarket's CTF `OrderFilled` events on
Polygon. Also on Hugging Face:
[Crowdintel/polymarket-historical-data](https://huggingface.co/datasets/Crowdintel/polymarket-historical-data).

## What is in this repository

| File | Rows | Where |
| :--- | ---: | :--- |
| `fills_2024_us_presidential.parquet` | 7,655,166 | [Hugging Face](https://huggingface.co/datasets/Crowdintel/polymarket-historical-data) + [Releases](../../releases) — not committed (size) |
| `data/markets.parquet` | 2 | This repository |
| `quickstart.py` | — | This repository (downloads the fills parquet on first run) |

Markets included:

| Market | Condition ID | Fills | Resolved |
| :--- | :--- | ---: | :--- |
| Will Donald Trump win the 2024 US Presidential Election? | `0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917` | 4,963,530 | **Yes** |
| Will Kamala Harris win the 2024 US Presidential Election? | `0xc6485bb7ea46d7bb89beb9c91e7572ecfc72a6273789496f78bc5e989e4d1638` | 2,691,636 | **No** |

| | |
| :--- | :--- |
| Fills | 7,655,166 |
| Distinct wallets | 218,699 |
| Volume | $2,388,138,669.46 |
| Coverage | 2024-01-04 20:36:24 UTC → 2024-11-06 12:07:20 UTC |
| Format | Parquet, zstd, 1M-row groups (~238 MB) |

## Schema

### `fills_2024_us_presidential.parquet`

| Column | Type | Description |
| :--- | :--- | :--- |
| `timestamp_ms` | int64 | Fill time, Unix epoch milliseconds (UTC) |
| `tx_hash` | string | Polygon transaction hash, with the fill index as `-<n>` suffix |
| `condition_id` | string | CTF condition id (market key) |
| `market_slug` | string | Polymarket market slug |
| `token_id` | string | ERC-1155 outcome token id (uint256, decimal string) |
| `side` | string | `BUY` or `SELL` |
| `outcome` | string | Outcome leg the token represents (`Yes` / `No`) |
| `price` | double | Execution price, 0–1 |
| `size` | double | Shares traded |
| `bet_value` | double | USD notional (`price × size`) |
| `proxy_wallet` | string | Lowercase 0x-address whose position changed |

### `data/markets.parquet`

`condition_id`, `slug`, `title`, `category`, `end_date_ms`, `resolved_outcome`, `resolved_at_ms`,
`final_price`, `fill_count`, `volume_usd`, `first_fill_ms`, `last_fill_ms`.

## Quickstart

```bash
pip install duckdb huggingface_hub
python3 quickstart.py
```

The fills file (~300 MB) is not committed; `quickstart.py` downloads it from Hugging Face
once and caches it. `data/markets.parquet` is already in the repo.

Or query the file directly:

```python
import duckdb

con = duckdb.connect()
FILLS = "hf://datasets/Crowdintel/polymarket-historical-data/fills_2024_us_presidential.parquet"

con.sql(f"""
    SELECT market_slug,
           count(*)                 AS fills,
           count(DISTINCT proxy_wallet) AS wallets,
           round(sum(bet_value), 0) AS volume_usd
    FROM read_parquet('{FILLS}')
    GROUP BY 1 ORDER BY volume_usd DESC
""").show()
```

First and last price per outcome before resolution:

```python
con.sql(f"""
    SELECT market_slug, outcome, arg_max(price, timestamp_ms) AS last_price
    FROM read_parquet('{FILLS}')
    GROUP BY 1, 2 ORDER BY 1, 2
""").show()
```

## Provenance

- Source: Polymarket CTF `OrderFilled` events on Polygon, indexed by CrowdIntel and joined to Gamma
  market metadata and on-chain resolution.
- `tx_hash` is unique across the file (one row per fill); the file is sorted by `timestamp_ms`.
- Row counts, wallet counts, volume, and the coverage window are computed from the published file.
- Resolution rows come from on-chain condition resolution, not from an off-chain leaderboard.

## Known limitations

- Two markets, not the whole exchange. This is a closed-event extract for end-to-end backtesting.
- No maker/taker split: `proxy_wallet` is the wallet whose position changed.
- No order book history in this release.
- Prices are floats derived from the CLOB's fixed-point prices.

## License

Apache-2.0. Attribution to CrowdIntel required for redistribution.

## Full archive

The complete tape (1.9B+ fills, 2.2M+ resolved markets), reconciled wallet PnL, shrinkage-adjusted
win rates, and funding-cluster ids are available at
[crowdintel.xyz/data](https://crowdintel.xyz/data).

## Changelog

- **2026-10-19** — Replaced the synthetic 10k-row sample with the real closed-event tape
  (7.65M fills) in Parquet, added `markets.parquet`, removed the synthetic order-book subset,
  rewrote `quickstart.py` so it never fabricates rows.
