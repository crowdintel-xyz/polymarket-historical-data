# Polymarket Historical Backtesting Dataset (Free Sample Pack)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Data Format: Apache Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-orange.svg)](https://parquet.apache.org/)
[![Database: CrowdIntel](https://img.shields.io/badge/Catalog-crowdintel.xyz%2Fdata-green.svg)](https://crowdintel.xyz/data)

This repository contains an end-to-end verified historical sample of Polymarket tick-level trade executions. Designed for quantitative researchers, algorithmic market makers, and statistical arbitrage bot developers.

---

## 1. What is Inside This Free Sample Pack

Unlike random synthetic rows, this repository provides two distinct institutional-grade datasets:

### A. Closed-Event Trade Tape (`crowdintel_trump_harris_sample.parquet`)
* **Scope:** Every executed trade fill and resolution from market creation to final settlement for the **2024 US Presidential Election (Trump vs. Harris)**.
* **Granularity:** Tick-by-tick millisecond Polygon PoS block header timestamps.
* **Attribution:** On-chain maker and taker proxy wallet addresses, transaction hashes, execution prices, and share quantities.
* **Integrity:** Zero dropped transactions; 100% verified against Polygon on-chain logs.

### B. High-Frequency Order Book Snapshots (`crowdintel_btc_5m_orderbook_sample.parquet`)
* **Scope:** Continuous L2/L3 order book depth snapshots for **BTC 5-minute / 15-minute** prediction markets.
* **Metrics:** Best bid, best ask, mid-market price, tick spread, USD bid/ask depth, and full raw level-2 bid/ask arrays (`bids_json`, `asks_json`).
* **Use Case:** Market-making simulation, latency arbitrage backtesting, and limit-order fill probability / slippage modeling.

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
    FROM 'crowdintel_trump_harris_sample.parquet'
    GROUP BY 1, 2
    ORDER BY window_1h DESC
""").df()

print(df)
```

### Query Order Book Depth & Spread with DuckDB
```python
import duckdb

con = duckdb.connect()
books_df = con.execute("""
    SELECT 
        ts,
        best_bid,
        best_ask,
        spread,
        bid_depth_usd,
        ask_depth_usd
    FROM 'crowdintel_btc_5m_orderbook_sample.parquet'
    WHERE spread > 0.01
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
| `timestamp` | `INT64` | Millisecond Unix timestamp from Polygon block header |
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
| `ts` | `DATETIME` | Snapshot timestamp (UTC) |
| `token_id` | `STRING` | Polymarket CLOB token identifier |
| `condition_id` | `STRING` | CTF market condition identifier |
| `best_bid` | `FLOAT64` | Highest available bid price |
| `best_ask` | `FLOAT64` | Lowest available ask price |
| `mid` | `FLOAT64` | Mid-market price `(best_bid + best_ask) / 2` |
| `spread` | `FLOAT64` | Absolute bid-ask spread `(best_ask - best_bid)` |
| `bids_json` | `STRING` | Serialized JSON array of price-level bids `[[price, size], ...]` |
| `asks_json` | `STRING` | Serialized JSON array of price-level asks `[[price, size], ...]` |
| `bid_depth_usd`| `FLOAT64` | Cumulative USD liquidity on the bid side |
| `ask_depth_usd`| `FLOAT64` | Cumulative USD liquidity on the ask side |

---

## 4. Ecosystem & Tooling

* **[Polymarket Agent Kit](https://github.com/crowdintel-xyz/polymarket-agent-kit):** Official Python/TypeScript SDK & Model Context Protocol (MCP) server for autonomous AI agents and bot runners.
* **[Commercial Data Store](https://crowdintel.xyz/data):** Full 1.88B historical database (2020–present) with automated weekly delta sync, forensic wallet intelligence graph, and raw S3/R2 presigned Parquet downloads.
  * **All-Access Terminal Pass ($99/mo):** Master database access + automated weekly delta sync via REST API.
  * **Perpetual Master Buyout ($299):** Complete 42 GB Snappy Parquet archive.
  * **Category Packs ($49–$79):** Politics, Crypto/Macro, Sports, and Whale Graph.
