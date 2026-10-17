#!/usr/bin/env python3
"""
CrowdIntel Polymarket Quantitative Data Quickstart
Demonstrates querying tick-level Parquet trade tape & L2 orderbook snapshots in Python.
"""
import os
import sys

SAMPLE_TRADES = os.path.join(os.path.dirname(__file__), "data", "sample_fills.parquet")
SAMPLE_BOOKS = os.path.join(os.path.dirname(__file__), "data", "sample_orderbooks.parquet")

def print_banner():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                CROWDINTEL COMMERCIAL DATA STORE & ARCHIVES                 ║
╠════════════════════════════════════════════════════════════════════════════╣
║  • Complete Archive: 1.88B Trade Fills across 2.13M Markets (2020-Present) ║
║  • Order Book Depth: Continuous L2 snapshots with bids, asks, & spreads    ║
║  • Whale Intelligence: 3.06M Scored Wallets with PnL & Cluster Graphs      ║
║  • Format: Snappy Parquet (DuckDB, Polars, & Arrow zero-copy compatible)   ║
║                                                                            ║
║  🛒 Explore Catalog & Category Packs: https://crowdintel.xyz/data          ║
║  🤖 Connect Claude / Cursor via MCP:  github.com/crowdintel-xyz            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def run_quickstart():
    print("=== CrowdIntel Polymarket Market Data Quickstart ===")
    
    try:
        import duckdb
        con = duckdb.connect()
        
        # 1. Trade Fills Query
        print("\n[1] Trade Tape Analysis (VWAP & Volume by Outcome):")
        if os.path.exists(SAMPLE_TRADES):
            query_trades = f"""
                SELECT 
                    time_bucket(INTERVAL '1 hour', to_timestamp(timestamp / 1000)) AS window_1h,
                    outcome,
                    COUNT(*) AS fills,
                    ROUND(SUM(bet_value), 2) AS total_volume_usd,
                    ROUND(SUM(price * size) / SUM(size), 4) AS vwap
                FROM read_parquet('{SAMPLE_TRADES}')
                GROUP BY 1, 2
                ORDER BY window_1h DESC
                LIMIT 5
            """
        else:
            query_trades = """
                SELECT 
                    '2024-11-05 23:00:00' AS window_1h,
                    'Trump (Yes)' AS outcome,
                    5000 AS fills,
                    3100000.00 AS total_volume_usd,
                    0.6200 AS vwap
            """
        df_trades = con.execute(query_trades).df()
        print(df_trades.to_string(index=False))
        
        # 2. Order Book Depth Query
        print("\n[2] L2 Order Book Depth & Spread (BTC 5-Minute Series):")
        if os.path.exists(SAMPLE_BOOKS):
            query_books = f"""
                SELECT 
                    to_timestamp(ts / 1000) AS time_utc,
                    best_bid,
                    best_ask,
                    ROUND(spread, 4) AS spread,
                    ROUND(bid_depth_usd, 2) AS bid_depth,
                    ROUND(ask_depth_usd, 2) AS ask_depth
                FROM read_parquet('{SAMPLE_BOOKS}')
                ORDER BY ts DESC
                LIMIT 5
            """
        else:
            query_books = """
                SELECT 
                    '2026-10-17 12:00:00' AS time_utc,
                    0.5120 AS best_bid,
                    0.5180 AS best_ask,
                    0.0060 AS spread,
                    14250.00 AS bid_depth,
                    18920.00 AS ask_depth
            """
        df_books = con.execute(query_books).df()
        print(df_books.to_string(index=False))
        
    except ImportError:
        print("[Note] DuckDB not installed. Run: pip install duckdb pandas")
        print("\n[Sample Trade Preview]:")
        print("timestamp: 1730847600000 | outcome: Trump (Yes) | price: 0.6200 | size: 5000 | volume: $3,100.00")
        print("\n[Sample Order Book Preview]:")
        print("time_utc: 2026-10-17 12:00:00 | best_bid: 0.5120 | best_ask: 0.5180 | spread: 0.0060 | depth: $33,170")

    print_banner()

if __name__ == "__main__":
    run_quickstart()
