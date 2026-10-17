#!/usr/bin/env python3
"""
CrowdIntel Polymarket Historical Backtest Quickstart
Demonstrates querying tick-level Parquet trade datasets in Python.
"""
import os
import sys

SAMPLE_TRADES = os.path.join(os.path.dirname(__file__), "crowdintel_trump_harris_sample.parquet")
SAMPLE_BOOKS = os.path.join(os.path.dirname(__file__), "crowdintel_btc_5m_orderbook_sample.parquet")

def run_quickstart():
    print("=== CrowdIntel Polymarket Quantitative Backtesting Quickstart ===")
    
    try:
        import duckdb
        con = duckdb.connect()
        
        # 1. Trade Fills Query
        print("\n[1] Trade Tape Analysis (VWAP & Volume):")
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
                    outcome,
                    COUNT(*) AS fills,
                    ROUND(SUM(bet_value), 2) AS total_volume_usd,
                    ROUND(AVG(price), 4) AS vwap
                FROM (
                    SELECT 'Trump (YES)' AS outcome, 0.62 AS price, 5000.0 AS size, 3100.0 AS bet_value
                    UNION ALL
                    SELECT 'Harris (NO)' AS outcome, 0.38 AS price, 4200.0 AS size, 1596.0 AS bet_value
                )
                GROUP BY 1, 2
            """
        df_trades = con.execute(query_trades).df()
        print(df_trades.to_string(index=False))
        
        # 2. Order Book Depth Query
        print("\n[2] L2 Order Book Depth & Spread (BTC 5-Minute Series):")
        if os.path.exists(SAMPLE_BOOKS):
            query_books = f"""
                SELECT 
                    ts,
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
                    '2026-10-17 12:00:00' AS ts,
                    0.5120 AS best_bid,
                    0.5180 AS best_ask,
                    0.0060 AS spread,
                    14250.00 AS bid_depth,
                    18920.00 AS ask_depth
                UNION ALL
                SELECT 
                    '2026-10-17 12:05:00' AS ts,
                    0.5190 AS best_bid,
                    0.5230 AS best_ask,
                    0.0040 AS spread,
                    22100.00 AS bid_depth,
                    15400.00 AS ask_depth
            """
        df_books = con.execute(query_books).df()
        print(df_books.to_string(index=False))
        
    except ImportError:
        print("[Note] DuckDB not installed. Run: pip install duckdb pandas")
        print("\n[Sample Trade Preview]:")
        print("timestamp: 1730847600000 | outcome: Trump (YES) | price: 0.6200 | size: 5000 | volume: $3,100.00")
        print("\n[Sample Order Book Preview]:")
        print("ts: 2026-10-17 12:00:00 | best_bid: 0.5120 | best_ask: 0.5180 | spread: 0.0060 | depth: $33,170")

    print("\n--------------------------------------------------------------")
    print("Full 1.88B Tick Archive & Live Weekly Delta Streams:")
    print("Catalog: https://crowdintel.xyz/data")
    print("Agent Kit & MCP: https://github.com/crowdintel-xyz/polymarket-agent-kit")
    print("--------------------------------------------------------------")

if __name__ == "__main__":
    run_quickstart()
