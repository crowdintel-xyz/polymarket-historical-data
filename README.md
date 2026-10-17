# Polymarket Historical Market Data (Free Sample Pack)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Data Format: Apache Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-orange.svg)](https://parquet.apache.org/)
[![Database: CrowdIntel](https://img.shields.io/badge/Catalog-crowdintel.xyz%2Fdata-green.svg)](https://crowdintel.xyz/data)
[![Ecosystem: Agent Kit](https://img.shields.io/badge/Tools-polymarket--agent--kit-blueviolet.svg)](https://github.com/crowdintel-xyz/polymarket-agent-kit)

This repository contains verified, tick-level Polymarket datasets across two primary modalities: **Trade Execution Fills** (for flow analytics, whale tracking, and PnL) and **Continuous L2 Order Book Depth** (for market makers, latency arbitrageurs, and execution slippage modeling).

---

## 1. Two Production Data Streams

Unlike disconnected synthetic rows, this repository provides two real-world market datasets:

### A. Closed-Event Trade Tape (`data/sample_fills.parquet` & `.csv`)
* **Scope:** 10,000 tick-by-tick fills across the **2024 US Presidential Election (Trump vs. Harris)** from market creation to final resolution settlement.
* **Fields:** Transaction hashes, millisecond block timestamps, execution prices, quantities transacted, maker/taker proxy wallet addresses, and final contract payoffs.
* **Use Cases:**
  * **Whale Tracking & Forensics:** Trace which wallets accumulated early contrarian positions.
  * **Volume Profiling:** Calculate volume-weighted average price (VWAP) and liquidity shocks.
  * **Strategy PnL & Backtesting:** Replay settled event outcomes against real execution prices.

### B. High-Frequency Order Book Snapshots (`data/sample_orderbooks.parquet` & `.csv`)
* **Scope:** 5,000 continuous L2 order book depth snapshots for **BTC 5-Minute / 15-Minute** prediction markets.
* **Fields:** Best bid, best ask, mid-market price, tick spread, cumulative bid/ask USD depth, and serialized level-2 price ladders (`bids_json`, `asks_json`).
* **Use Cases:**
  * **Market Making:** Simulate queue position, spread capture, and adverse selection.
  * **Slippage Modeling:** Evaluate expected fill price for larger taker order sizes.
  * **Latency Arbitrage:** Backtest reaction speeds between spot CEX moves and Polymarket order book revisions.

---

## 2. Quickstart (< 5 Lines of Code)

Query billions of rows in memory without configuring a database:

### Query Trade Tape (VWAP & Hourly Volume) with DuckDB
```python
import duckdb

con = duckdb.connect()
df = con.execute("""
    SELECT 
        time_bucket(INTERVAL '1 hour', to_timestamp(timestamp / 1000)) AS window_1h,
        outcome,
        COUNT(*) AS fills,
        ROUND(SUM(bet_value), 2) AS volume_usd,
        ROUND(SUM(price * size) / SUM(size), 4) AS vwap
    FROM 'data/sample_fills.parquet'
    GROUP BY 1, 2
    ORDER BY window_1h DESC
""").df()

print(df)
```

### Query Order Book Depth & Spreads with DuckDB
```python
import duckdb

con = duckdb.connect()
books_df = con.execute("""
    SELECT 
        to_timestamp(ts / 1000) AS time_utc,
        best_bid,
        best_ask,
        ROUND(spread, 4) AS spread,
        ROUND(bid_depth_usd, 2) AS bid_depth,
        ROUND(ask_depth_usd, 2) AS ask_depth
    FROM 'data/sample_orderbooks.parquet'
    WHERE spread > 0.005
    ORDER BY ts DESC
    LIMIT 10
""").df()

print(books_df)
```

---

## 3. Schema Specifications

### Fills Tape Schema (`polywhales.trades`)
| Column | Type | Description |
| :--- | :--- | :--- |
| `timestamp` | `INT64` | Millisecond Unix epoch from Polygon PoS block header |
| `tx_hash` | `STRING` | 0x-prefixed unique Polygon transaction hash |
| `condition_id` | `STRING` | CTF condition ID for market settlement |
| `market_slug` | `STRING` | Human-readable market slug identifier |
| `category` | `STRING` | Market category (`politics`, `crypto`, `sports`, `other`) |
| `side` | `STRING` | Execution side (`BUY` or `SELL`) |
| `price` | `FLOAT32` | Execution price in USDC ($0.0001 to $1.0000) |
| `size` | `FLOAT32` | Number of outcome shares transacted |
| `bet_value` | `FLOAT32` | Notional USD volume transacted |
| `maker_address` | `STRING` | 42-character hex address of order maker |
| `taker_address` | `STRING` | 42-character hex address of order taker |
| `outcome` | `STRING` | Resolved outcome token name |

### L2 Order Book Snapshot Schema (`bot_book_snapshots`)
| Column | Type | Description |
| :--- | :--- | :--- |
| `ts` | `INT64` | Millisecond Unix timestamp (UTC) |
| `token_id` | `STRING` | Polymarket CLOB token identifier |
| `condition_id` | `STRING` | CTF market condition identifier |
| `market_slug` | `STRING` | Market identifier |
| `best_bid` | `FLOAT32` | Highest available bid price |
| `best_ask` | `FLOAT32` | Lowest available ask price |
| `mid` | `FLOAT32` | Mid-market price `(best_bid + best_ask) / 2` |
| `spread` | `FLOAT32` | Absolute bid-ask spread `(best_ask - best_bid)` |
| `bid_depth_usd`| `FLOAT32` | Cumulative USD liquidity on the bid side |
| `ask_depth_usd`| `FLOAT32` | Cumulative USD liquidity on the ask side |
| `bids_json` | `STRING` | Serialized JSON array of price-level bids `[[price, size], ...]` |
| `asks_json` | `STRING` | Serialized JSON array of price-level asks `[[price, size], ...]` |

---

## 4. Ecosystem & Tooling

* **[Polymarket Agent Kit](https://github.com/crowdintel-xyz/polymarket-agent-kit):** Official Python/TypeScript SDK & Model Context Protocol (MCP) server for autonomous AI agents and bot runners.
* **[Commercial Data Store](https://crowdintel.xyz/data):** Full 1.88B historical database (2020–present) with automated weekly delta sync, forensic wallet intelligence graph, and raw S3/R2 presigned Parquet downloads.
  * **All-Access Terminal Pass ($99/mo):** Master database access + automated weekly delta sync via REST API.
  * **Perpetual Master Buyout ($299):** Complete 42 GB Snappy Parquet archive.
  * **Category Packs ($49–$79):** Politics, Crypto/Macro, Sports, and Whale Graph.

---

## License

Apache 2.0. Curated by the CrowdIntel Quantitative Engineering Team.
