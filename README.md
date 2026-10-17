# Polymarket Historical Market Data (Free Research Benchmark)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Data Format: Apache Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-orange.svg)](https://parquet.apache.org/)
[![Database: CrowdIntel](https://img.shields.io/badge/Catalog-crowdintel.xyz%2Fdata-green.svg)](https://crowdintel.xyz/data)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Datasets-yellow)](https://huggingface.co/datasets/Crowdintel/polymarket-historical-data)
[![Ecosystem: Agent Kit](https://img.shields.io/badge/Tools-polymarket--agent--kit-blueviolet.svg)](https://github.com/crowdintel-xyz/polymarket-agent-kit)

> ⚠️ **You are viewing the Free Research Benchmark (10k Fills & 5k Order Book Snapshots).**  
> Looking for the complete 1.88 Billion fill tape, historical orderbook archives, or automated weekly delta sync?  
> 👉 **[Explore the Full Commercial Data Store at crowdintel.xyz/data →](https://crowdintel.xyz/data)**

---

## 1. Why This Dataset Exists

In February 2026, Polymarket deprecated its official historical order book API (`/orderbook-history`). Quant researchers, bot builders, and market makers were left without historical tick-level depth or trade execution tapes.

CrowdIntel indexes every Polygon PoS block and records continuous WebSocket order book feeds into ClickHouse. This repository provides **two verified benchmark samples** in zero-copy Apache Parquet:

1. **Trade Execution Fills (`data/sample_fills.parquet` & `.csv`)**: For whale forensics, volume profiling, and flow analytics.
2. **Continuous L2 Order Book Depth (`data/sample_orderbooks.parquet` & `.csv`)**: For market-making simulation, spread dynamics, and execution slippage modeling.

---

## 2. Free Benchmark vs. Commercial Data Store

| Capability | Free Benchmark (This Repo) | Commercial Data Store (`crowdintel.xyz/data`) |
| :--- | :--- | :--- |
| **Historical Range** | 1 Closed Market (2024 Presidential Election) | **Complete 2020–Present History (2,130,000+ Markets)** |
| **Total Trade Fills** | 10,000 executed fills | **1,880,000,000+ Fills (Complete Tick-Level Tape)** |
| **Order Book Depth** | 5,000 BTC 5-min snapshots | **Continuous L2 snapshots across all active liquid markets** |
| **Whale Intelligence** | None | **3.06M Scored Wallets (PnL, FDR q-values, Sybil cluster graphs)** |
| **Data Delivery** | Direct Git / Parquet download | **Signed Cloudflare R2 URLs + High-Speed Direct S3** |
| **Data Updates** | None (Static benchmark) | **Automated Weekly Delta Sync via REST API** |
| **AI Agent Tooling** | Manual Python scripts | **Official MCP Server for Claude Desktop & Cursor** |
| **Commercial License** | Personal / Academic Research | **Commercial Redistribution & Algorithmic Trading Allowed** |
| **Pricing** | **$0 (Free)** | **$79 Packs · $99/mo All-Access · $299 Master Buyout** |

👉 **[Browse Available Category Slices on the Commercial Data Store →](https://crowdintel.xyz/data)**

---

## 3. Data Specification & Schemas

### Dataset A: Trade Execution Tape (`data/sample_fills.parquet` & `.csv`)
* **Scope:** 10,000 executed trade fills for the **2024 US Presidential Election (Trump vs. Harris)** from market inception through final resolution settlement.
* **Format:** Apache Parquet v1 with Snappy block compression (plus CSV text fallback).
* **Parity:** 100% schema parity with ClickHouse table `polywhales.trades`.

| Column | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `timestamp` | `INT64` | `1730847600000` | Millisecond Unix epoch from Polygon block header |
| `tx_hash` | `STRING` | `0x5b3a...7f12` | 66-character unique Polygon transaction hash |
| `condition_id` | `STRING` | `0x192a...c01a` | 32-byte hex CTF condition identifier |
| `market_slug` | `STRING` | `will-donald-trump-win-2024`| Human-readable Polymarket market slug |
| `category` | `STRING` | `politics` | Market taxonomy category |
| `side` | `STRING` | `BUY` | Execution side (`BUY` or `SELL`) |
| `price` | `FLOAT32` | `0.6200` | Normalized execution price in USDC ($0.0001 to $1.0000) |
| `size` | `FLOAT32` | `5000.0` | Number of outcome share tokens transacted |
| `bet_value` | `FLOAT32` | `3100.00` | Notional USD volume transacted (`price * size`) |
| `maker_address`| `STRING` | `0x82f4...d57a` | 42-character hex on-chain maker proxy wallet |
| `taker_address`| `STRING` | `0xe780...e245` | 42-character hex on-chain taker proxy wallet |
| `outcome` | `STRING` | `Yes` | Resolved contract outcome token leg |

### Dataset B: High-Frequency Order Book Depth (`data/sample_orderbooks.parquet` & `.csv`)
* **Scope:** 5,000 continuous 1-second interval L2 order book depth snapshots for **BTC 5-Minute prediction markets**.
* **Format:** Apache Parquet v1 with Snappy block compression (plus CSV text fallback).
* **Parity:** 100% schema parity with ClickHouse table `bot_book_snapshots`.

| Column | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `ts` | `INT64` | `1730000000000` | Millisecond Unix epoch timestamp (UTC) |
| `token_id` | `STRING` | `21742633...` | Polymarket CLOB ERC-1155 token leg identifier |
| `condition_id` | `STRING` | `0x82f4...f7b8` | CTF market condition identifier |
| `market_slug` | `STRING` | `btc-up-down-5m-series` | High-frequency market series slug |
| `best_bid` | `FLOAT32` | `0.5120` | Highest available bid price in USDC |
| `best_ask` | `FLOAT32` | `0.5180` | Lowest available ask price in USDC |
| `mid` | `FLOAT32` | `0.5150` | Mid-market price `(best_bid + best_ask) / 2` |
| `spread` | `FLOAT32` | `0.0060` | Absolute bid-ask spread `(best_ask - best_bid)` |
| `bid_depth_usd`| `FLOAT32` | `18240.50` | Cumulative USD liquidity available on the bid side |
| `ask_depth_usd`| `FLOAT32` | `21980.20` | Cumulative USD liquidity available on the ask side |
| `bids_json` | `STRING` | `[[0.51, 8500], ...]` | Serialized level-2 price ladder: `[[price, size], ...]` |
| `asks_json` | `STRING` | `[[0.52, 9200], ...]` | Serialized level-2 price ladder: `[[price, size], ...]` |

---

## 4. Quickstart (< 5 Lines of Code)

Query billions of rows in memory without configuring a database:

### Query Trade Tape (VWAP & Outcome Volume) with DuckDB
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

### Query Order Book Spreads & Depth with DuckDB
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

## 5. Commercial Offerings Ladder

For teams building production bots or conducting institutional research:

| Offering | Coverage | Format | Price | Delivery |
| :--- | :--- | :--- | :--- | :--- |
| **US Politics & Policy** | 2020–2026 Presidential, Senate & Policy markets | Parquet (~7.5 GB) | **$79** one-time | Signed R2 link |
| **Crypto & High-Freq** | 5m/15m BTC/ETH markets + TWAP settlement series | Parquet (~11 GB) | **$79** one-time | Signed R2 link |
| **Sports & Culture** | Full resolved soccer, NBA, NFL, and esports markets | Parquet (~14 GB) | **$79** one-time | Signed R2 link |
| **Whale & Bot Intelligence** | 3.06M scored wallets: PnL, FDR q-values, sybils | Parquet (~3 GB) | **$149** one-time | Signed R2 link |
| **⭐ All-Access Terminal** | **1.88B master archive + weekly delta sync + API** | API / Parquet | **$99 / month** | REST / Curl token |
| **Master Archive Buyout** | Complete 1.88B historical database (2020–present) | Parquet (~42 GB) | **$299** one-time | Direct S3 dump |

👉 **[Purchase Datasets or Subscriptions at crowdintel.xyz/data →](https://crowdintel.xyz/data)**

---

## 6. Bespoke Market Cuts & Inquiries

Need a custom slice (e.g. French Presidential Election, Fed Interest Rate cuts, or specific DeFi markets)? Don't waste weeks scraping.

* **Email:** `hi@crowdintel.xyz` (Custom Parquet extracts delivered within 2 hours)
* **Telegram:** [@CrowdIntel](https://t.me/crowdintel)
* **Official AI Agent Kit:** [`crowdintel-xyz/polymarket-agent-kit`](https://github.com/crowdintel-xyz/polymarket-agent-kit) (Model Context Protocol server for Claude & Cursor)

---

## License

Apache 2.0. Curated by the CrowdIntel Quantitative Engineering Team.
