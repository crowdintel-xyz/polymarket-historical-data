#!/usr/bin/env python3
"""Query the CrowdIntel free Polymarket tape in under a minute.

Downloads the 2024 US Presidential Election fills from Hugging Face on first
run, then answers the questions the dataset card promises.

    pip install duckdb huggingface_hub
    python3 quickstart.py
"""
from pathlib import Path

import duckdb
from huggingface_hub import hf_hub_download

REPO = "Crowdintel/polymarket-historical-data"
FILLS = "fills_2024_us_presidential.parquet"
MARKETS = "markets.parquet"


def fetch(name: str) -> str:
    local = Path(__file__).parent / "data" / name
    if local.exists():
        return str(local)
    return hf_hub_download(REPO, name, repo_type="dataset")


def main() -> None:
    con = duckdb.connect()
    fills = fetch(FILLS)
    markets = fetch(MARKETS)

    print("=== CrowdIntel · Polymarket 2024 US Presidential Election ===")
    print(
        con.sql(
            f"""
            SELECT market_slug,
                   count(*)                            AS fills,
                   count(DISTINCT proxy_wallet)        AS wallets,
                   round(sum(bet_value), 0)            AS volume_usd,
                   min(to_timestamp(timestamp_ms / 1000)) AS first_fill,
                   max(to_timestamp(timestamp_ms / 1000)) AS last_fill
            FROM read_parquet('{fills}')
            GROUP BY 1 ORDER BY volume_usd DESC
            """
        ).df().to_string(index=False)
    )

    print("\n=== Realized outcome (resolved on-chain) ===")
    print(
        con.sql(
            f"""
            SELECT slug, resolved_outcome, resolved_at, final_price, fill_count
            FROM read_parquet('{markets}')
            ORDER BY fill_count DESC
            """
        ).df().to_string(index=False)
    )

    print("\n=== Last price before resolution ===")
    print(
        con.sql(
            f"""
            SELECT market_slug, outcome, arg_max(price, timestamp_ms) AS last_price
            FROM read_parquet('{fills}')
            GROUP BY 1, 2 ORDER BY 1, 2
            """
        ).df().to_string(index=False)
    )


if __name__ == "__main__":
    main()
