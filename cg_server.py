from typing import Any, Dict, List, Optional, Union, Literal
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import httpx
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("cg")

# Configuration
API_KEY = os.getenv("CG_API_KEY")
BASE_URL = "https://pro-api.coingecko.com/api/v3/"

# HTTP client
client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={
        "accept": "application/json",
        "x-cg-pro-api-key": API_KEY
    },
    timeout=30.0
)

@mcp.tool()
async def get_current_time() -> str:
    """Get the current time in both human-readable format and UNIX timestamp.
    
    Returns:
        A string containing both the current time in ISO format and UNIX timestamp.
    """
    now = datetime.now()
    return f"Current time: {now.isoformat()}\nUNIX timestamp: {int(now.timestamp())}"

@mcp.tool()
async def date_to_timestamp(date_str: str) -> str:
    """Convert a human-readable date to UNIX timestamp.
    
    Parameters:
        date_str: Date string in ISO format (YYYY-MM-DD) or with time (YYYY-MM-DD HH:MM:SS)
    
    Returns:
        A string containing both the parsed date and its UNIX timestamp.
    """
    try:
        # Try parsing with time first
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If that fails, try parsing just the date
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        
        return f"Date: {dt.isoformat()}\nUNIX timestamp: {int(dt.timestamp())}"
    except ValueError as e:
        return f"Error: {str(e)}\nPlease provide date in format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"

@mcp.tool()
async def timestamp_to_date(timestamp: int) -> str:
    """Convert a UNIX timestamp to human-readable date.
    
    Parameters:
        timestamp: UNIX timestamp (seconds since epoch)
    
    Returns:
        A string containing the date in ISO format.
    """
    try:
        dt = datetime.fromtimestamp(timestamp)
        return f"Date: {dt.isoformat()}\nUNIX timestamp: {timestamp}"
    except (ValueError, OSError) as e:
        return f"Error: {str(e)}\nPlease provide a valid UNIX timestamp"

async def make_request(method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Make a request to the CoinGecko API."""
    try:
        response = await client.request(method, endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_top_gainers_losers(
    vs_currency: str,
    duration: str = "24h",
    top_coins: str = "1000"
) -> str:
    """GET /coins/top_gainers_losers

    This endpoint allows you to query the top 30 coins with largest price gain and loss by a specific time duration.
    The endpoint response only includes coins with a 24-hour trading volume of at least $50,000.
    Cache/Update Frequency: Every 5 minutes.
    Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).

    Parameters:
        vs_currency: Target currency of coins (e.g., 'usd', 'eur', 'btc')
        duration: Filter result by time range (default: '24h')
        top_coins: Filter result by market cap ranking (top 300 to 1000) or 'all' coins
                  (including coins that do not have market cap) (default: '1000')

    Returns:
        List of top 30 gainers and losers with the following fields:
        - id: coin ID
        - symbol: coin symbol
        - name: coin name
        - image: coin image url
        - market_cap_rank: coin rank by market cap
        - usd: coin price in USD
        - usd_24h_vol: coin 24hr volume in USD
        - usd_1y_change: coin 1 year change in USD
    """
    params = {
        'vs_currency': vs_currency,
        'duration': duration,
        'top_coins': top_coins
    }
    result = await make_request('GET', 'coins/top_gainers_losers', params)
    return str(result)

@mcp.tool()
async def get_coin_markets(
    vs_currency: str,
    ids: str = None,
    names: str = None,
    symbols: str = None,
    include_tokens: str = None,
    category: str = None,
    order: str = "market_cap_desc",
    per_page: int = 100,
    page: int = 1,
    sparkline: bool = False,
    price_change_percentage: str = None,
    locale: str = "en",
    precision: str = None
) -> str:
    """GET /coins/markets

    This endpoint allows you to query all the supported coins with price, market cap, volume and market related data.

    Parameters:
        vs_currency: Target currency of coins and market data (required)
        ids: Coins' IDs, comma-separated if querying more than 1 coin
        names: Coins' names, comma-separated if querying more than 1 coin
        symbols: Coins' symbols, comma-separated if querying more than 1 coin
        include_tokens: For symbols lookups, specify 'all' to include all matching tokens
        category: Filter based on coins' category
        order: Sort result by field (default: market_cap_desc)
        per_page: Total results per page (default: 100, max: 250)
        page: Page through results (default: 1)
        sparkline: Include sparkline 7 days data (default: false)
        price_change_percentage: Include price change percentage timeframe (e.g., "1h,24h,7d")
        locale: Language background (default: en)
        precision: Decimal place for currency price value
    """
    params = {
        "vs_currency": vs_currency,
        "order": order,
        "per_page": per_page,
        "page": page,
        "sparkline": str(sparkline).lower(),
        "locale": locale
    }
    
    if ids is not None:
        params["ids"] = ids
    if names is not None:
        params["names"] = names
    if symbols is not None:
        params["symbols"] = symbols
    if include_tokens is not None:
        params["include_tokens"] = include_tokens
    if category is not None:
        params["category"] = category
    if price_change_percentage is not None:
        params["price_change_percentage"] = price_change_percentage
    if precision is not None:
        params["precision"] = precision

    result = await make_request('GET', 'coins/markets', params)
    return str(result)

@mcp.tool()
async def get_coin_by_id(
    id: str,
    localization: bool = True,
    tickers: bool = True,
    market_data: bool = True,
    community_data: bool = True,
    developer_data: bool = True,
    sparkline: bool = False
) -> str:
    """GET /coins/{id}

    This endpoint allows you to query all the metadata and market data of a coin from the CoinGecko coin page.

    Parameters:
        id: Coin ID (required)
        localization: Include all localized languages in response (default: true)
        tickers: Include tickers data (default: true)
        market_data: Include market data (default: true)
        community_data: Include community data (default: true)
        developer_data: Include developer data (default: true)
        sparkline: Include sparkline 7 days data (default: false)
    """
    params = {
        "localization": str(localization).lower(),
        "tickers": str(tickers).lower(),
        "market_data": str(market_data).lower(),
        "community_data": str(community_data).lower(),
        "developer_data": str(developer_data).lower(),
        "sparkline": str(sparkline).lower()
    }

    result = await make_request('GET', f'coins/{id}', params)
    return str(result)

@mcp.tool()
async def get_coin_ohlc_range(
    id: str,
    vs_currency: str,
    from_timestamp: int,
    to_timestamp: int,
    interval: Literal["daily", "hourly"]
) -> str:
    """GET /coins/{id}/ohlc/range

    This endpoint allows you to get the OHLC chart (Open, High, Low, Close) of a coin within a range of timestamp.

    Parameters:
        id: Coin ID (required)
        vs_currency: Target currency of price data (required)
        from_timestamp: Starting date in UNIX timestamp (required)
        to_timestamp: Ending date in UNIX timestamp (required)
        interval: Data interval (required) - "daily" or "hourly"
            - Daily: up to 180 days per request
            - Hourly: up to 31 days per request

    Notes:
        - Available from 9 February 2018 onwards (1518147224 epoch time)
        - Cache/Update Frequency: Every 15 minutes
        - Exclusive for Paid Plan Subscribers
    """
    params = {
        "vs_currency": vs_currency,
        "from": from_timestamp,
        "to": to_timestamp,
        "interval": interval
    }

    result = await make_request('GET', f'coins/{id}/ohlc/range', params)
    return str(result)

@mcp.tool()
async def get_coin_by_contract(
    id: str,
    contract_address: str
) -> str:
    """GET /coins/{id}/contract/{contract_address}

    This endpoint allows you to query all the metadata and market data of a coin based on an asset platform
    and a particular token contract address.

    Parameters:
        id: Asset platform ID (required)
        contract_address: The contract address of token (required)

    Notes:
        - Cache/Update Frequency: Every 60 seconds
        - Coin descriptions may include newline characters represented as \r\n
    """
    result = await make_request('GET', f'coins/{id}/contract/{contract_address}')
    return str(result)

@mcp.tool()
async def search(query: str) -> str:
    """GET /search

    This endpoint allows you to search for coins, categories and markets listed on CoinGecko.

    Parameters:
        query: Search query (required)

    Notes:
        - Responses are sorted in descending order by market cap
        - Cache/Update Frequency: Every 15 minutes
    """
    params = {
        "query": query
    }

    result = await make_request('GET', 'search', params)
    return str(result)

@mcp.tool()
async def get_trending_searches(show_max: str = None) -> str:
    """GET /search/trending

    This endpoint allows you to query trending search coins, NFTs and categories on CoinGecko in the last 24 hours.

    Parameters:
        show_max: Show max number of results available for the given type
            - Available values: coins, nfts, categories
            - Example: "coins" or "coins,nfts,categories"
            - Default: None (returns standard limits: 15 coins, 7 NFTs, 6 categories)

    Notes:
        - Standard limits:
            - Top 15 trending coins
            - Top 7 trending NFTs
            - Top 6 trending categories
        - With show_max parameter (Analyst plan & above):
            - Up to 30 coins
            - Up to 10 NFTs
            - Up to 10 categories
        - Cache/Update Frequency: Every 10 minutes
    """
    params = {}
    if show_max is not None:
        params["show_max"] = show_max

    result = await make_request('GET', 'search/trending', params)
    return str(result)

@mcp.tool()
async def get_token_price_by_address(
    network: str,
    addresses: str,
    include_market_cap: bool = False,
    mcap_fdv_fallback: bool = False,
    include_24hr_vol: bool = False,
    include_24hr_price_change: bool = False,
    include_total_reserve_in_usd: bool = False
) -> str:
    """GET /onchain/simple/networks/{network}/token_price/{addresses}

    This endpoint allows you to get token price based on the provided token contract address on a network.

    Parameters:
        network: Network ID (required)
        addresses: Token contract address, comma-separated if more than one (required)
        include_market_cap: Include market capitalization (default: false)
        mcap_fdv_fallback: Return FDV if market cap is not available (default: false)
        include_24hr_vol: Include 24hr volume (default: false)
        include_24hr_price_change: Include 24hr price change (default: false)
        include_total_reserve_in_usd: Include total reserve in USD (default: false)

    Notes:
        - Cache/Update Frequency: Every 30 seconds
        - Up to 100 contract addresses per request (Analyst plan & above)
        - Price currency is in USD
        - Addresses not found in GeckoTerminal will be ignored
    """
    params = {
        "include_market_cap": str(include_market_cap).lower(),
        "mcap_fdv_fallback": str(mcap_fdv_fallback).lower(),
        "include_24hr_vol": str(include_24hr_vol).lower(),
        "include_24hr_price_change": str(include_24hr_price_change).lower(),
        "include_total_reserve_in_usd": str(include_total_reserve_in_usd).lower()
    }

    result = await make_request('GET', f'onchain/simple/networks/{network}/token_price/{addresses}', params)
    return str(result)

@mcp.tool()
async def get_trending_pools(
    include: str = None,
    page: int = 1,
    duration: str = "24h"
) -> str:
    """GET /onchain/networks/trending_pools

    This endpoint allows you to query all the trending pools across all networks on GeckoTerminal.

    Parameters:
        include: Attributes to include, comma-separated (e.g., "base_token,dex")
            Available values: base_token, quote_token, dex, network
        page: Page through results (default: 1)
        duration: Duration to sort trending list by (default: 24h)

    Notes:
        - Returns up to 20 pools per page
        - Pagination beyond 10 pages requires Analyst plan or above
        - Cache/Update frequency: Every 30 seconds
    """
    params = {
        "page": page,
        "duration": duration
    }
    if include is not None:
        params["include"] = include

    result = await make_request('GET', 'onchain/networks/trending_pools', params)
    return str(result)

@mcp.tool()
async def get_network_trending_pools(
    network: str,
    include: str = None,
    page: int = 1,
    duration: str = "24h"
) -> str:
    """GET /onchain/networks/{network}/trending_pools

    This endpoint allows you to query the trending pools based on the provided network.

    Parameters:
        network: Network ID (required)
        include: Attributes to include, comma-separated (e.g., "base_token,dex")
            Available values: base_token, quote_token, dex
        page: Page through results (default: 1)
        duration: Duration to sort trending list by (default: 24h)

    Notes:
        - Returns up to 20 pools per page
        - Pagination beyond 10 pages requires Analyst plan or above
        - Cache/Update frequency: Every 30 seconds
    """
    params = {
        "page": page,
        "duration": duration
    }
    if include is not None:
        params["include"] = include

    result = await make_request('GET', f'onchain/networks/{network}/trending_pools', params)
    return str(result)

@mcp.tool()
async def get_pool_data(
    network: str,
    address: str,
    include: str = None
) -> str:
    """GET /onchain/networks/{network}/pools/{address}

    This endpoint allows you to query the specific pool based on the provided network and pool address.

    Parameters:
        network: Network ID (required)
        address: Pool address (required)
        include: Attributes to include, comma-separated (e.g., "base_token,dex")
            Available values: base_token, quote_token, dex

    Notes:
        - Cache/Update Frequency: Every 30 seconds
        - Address not found in GeckoTerminal will be ignored
        - Market Cap can be verified by and sourced from CoinGecko
        - Locked liquidity percentage updated daily
    """
    params = {}
    if include is not None:
        params["include"] = include

    result = await make_request('GET', f'onchain/networks/{network}/pools/{address}', params)
    return str(result)

@mcp.tool()
async def get_pools_megafilter(
    networks: str = None,
    dexes: str = None,
    include: str = None,
    page: int = 1,
    sort: str = "h6_trending",
    fdv_usd_min: float = None,
    fdv_usd_max: float = None,
    reserve_in_usd_min: float = None,
    reserve_in_usd_max: float = None,
    h24_volume_usd_min: float = None,
    h24_volume_usd_max: float = None,
    pool_created_hour_min: float = None,
    pool_created_hour_max: float = None,
    tx_count_min: int = None,
    tx_count_max: int = None,
    tx_count_duration: str = "24h",
    buys_min: int = None,
    buys_max: int = None,
    buys_duration: str = "24h",
    sells_min: int = None,
    sells_max: int = None,
    sells_duration: str = "24h",
    checks: str = None,
    buy_tax_percentage_min: float = None,
    buy_tax_percentage_max: float = None,
    sell_tax_percentage_min: float = None,
    sell_tax_percentage_max: float = None
) -> str:
    """GET /onchain/pools/megafilter

    This endpoint allows you to query pools based on various filters across all networks on GeckoTerminal.

    Parameters:
        networks: Filter pools by networks, comma-separated
        dexes: Filter pools by DEXes, comma-separated (only when 1 network is specified)
        include: Attributes to include, comma-separated (e.g., "base_token,dex")
            Available values: base_token, quote_token, dex, network
        page: Page through results (default: 1)
        sort: Sort the pools by field (default: h6_trending)
        fdv_usd_min/max: Filter by fully diluted value in USD
        reserve_in_usd_min/max: Filter by reserve in USD
        h24_volume_usd_min/max: Filter by 24hr volume in USD
        pool_created_hour_min/max: Filter by pool age in hours
        tx_count_min/max: Filter by transaction count
        tx_count_duration: Duration for transaction count metric (default: 24h)
        buys_min/max: Filter by number of buy transactions
        buys_duration: Duration for buy transactions metric (default: 24h)
        sells_min/max: Filter by number of sell transactions
        sells_duration: Duration for sell transactions metric (default: 24h)
        checks: Filter options for various checks, comma-separated
            Available values: no_honeypot, good_gt_score, on_coingecko, has_social
        buy_tax_percentage_min/max: Filter by buy tax percentage
        sell_tax_percentage_min/max: Filter by sell tax percentage

    Notes:
        - Returns up to 20 pools per page
        - Cache/Update frequency: Every 30 seconds
        - Exclusive for Paid Plan subscribers (Analyst plan or above)
        - dexes param can only be used when only 1 network is specified
    """
    params = {
        "page": page,
        "sort": sort,
        "tx_count_duration": tx_count_duration,
        "buys_duration": buys_duration,
        "sells_duration": sells_duration
    }

    # Add optional parameters if they are provided
    if networks is not None:
        params["networks"] = networks
    if dexes is not None:
        params["dexes"] = dexes
    if include is not None:
        params["include"] = include
    if fdv_usd_min is not None:
        params["fdv_usd_min"] = fdv_usd_min
    if fdv_usd_max is not None:
        params["fdv_usd_max"] = fdv_usd_max
    if reserve_in_usd_min is not None:
        params["reserve_in_usd_min"] = reserve_in_usd_min
    if reserve_in_usd_max is not None:
        params["reserve_in_usd_max"] = reserve_in_usd_max
    if h24_volume_usd_min is not None:
        params["h24_volume_usd_min"] = h24_volume_usd_min
    if h24_volume_usd_max is not None:
        params["h24_volume_usd_max"] = h24_volume_usd_max
    if pool_created_hour_min is not None:
        params["pool_created_hour_min"] = pool_created_hour_min
    if pool_created_hour_max is not None:
        params["pool_created_hour_max"] = pool_created_hour_max
    if tx_count_min is not None:
        params["tx_count_min"] = tx_count_min
    if tx_count_max is not None:
        params["tx_count_max"] = tx_count_max
    if buys_min is not None:
        params["buys_min"] = buys_min
    if buys_max is not None:
        params["buys_max"] = buys_max
    if sells_min is not None:
        params["sells_min"] = sells_min
    if sells_max is not None:
        params["sells_max"] = sells_max
    if checks is not None:
        params["checks"] = checks
    if buy_tax_percentage_min is not None:
        params["buy_tax_percentage_min"] = buy_tax_percentage_min
    if buy_tax_percentage_max is not None:
        params["buy_tax_percentage_max"] = buy_tax_percentage_max
    if sell_tax_percentage_min is not None:
        params["sell_tax_percentage_min"] = sell_tax_percentage_min
    if sell_tax_percentage_max is not None:
        params["sell_tax_percentage_max"] = sell_tax_percentage_max

    result = await make_request('GET', 'onchain/pools/megafilter', params)
    return str(result)

@mcp.tool()
async def get_trending_search_pools(
    include: str = None,
    pools: int = 4
) -> str:
    """GET /onchain/pools/trending_search

    This endpoint allows you to query all the trending search pools across all networks on GeckoTerminal.

    Parameters:
        include: Attributes to include, comma-separated (e.g., "base_token,dex")
            Available values: base_token, quote_token, dex, network
        pools: Number of pools to return, maximum 10 (default: 4)

    Notes:
        - Cache/Update frequency: Every 60 seconds
        - Exclusive for Paid Plan subscribers (Analyst plan or above)
    """
    params = {
        "pools": pools
    }
    if include is not None:
        params["include"] = include

    result = await make_request('GET', 'onchain/pools/trending_search', params)
    return str(result)

if __name__ == "__main__":
    mcp.run(transport='stdio')