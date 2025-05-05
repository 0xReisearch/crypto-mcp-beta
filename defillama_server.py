from typing import Any, Dict, List, Optional, Union, Literal
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import httpx
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("defillama")

# Configuration
API_KEY = os.getenv("DEFILLAMA_API_KEY")
if not API_KEY:
    raise ValueError("DEFILLAMA_API_KEY environment variable is required")

BASE_URL = f"https://pro-api.llama.fi/{API_KEY}"

# HTTP client
client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={
        "accept": "application/json"
    },
    timeout=30.0
)

async def make_request(method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Make a request to the DefiLlama API."""
    try:
        response = await client.request(method, endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_token_protocols(symbol: str) -> str:
    """GET /api/tokenProtocols/{symbol}
    
    Lists the amount of a certain token within all protocols.
    
    Parameters:
        symbol: token slug (e.g., 'usdt')
    """
    result = await make_request('GET', f'/api/tokenProtocols/{symbol}')
    return str(result)

@mcp.tool()
async def get_protocol_inflows(protocol: str, timestamp: int) -> str:
    """GET /api/inflows/{protocol}/{timestamp}
    
    Lists the amount of inflows and outflows for a protocol at a given date.
    
    Parameters:
        protocol: protocol slug (e.g., 'compound-v3')
        timestamp: unix timestamp (e.g., 1700006400)
    """
    result = await make_request('GET', f'/api/inflows/{protocol}/{timestamp}')
    return str(result)

@mcp.tool()
async def get_chain_assets() -> str:
    """GET /api/chainAssets
    
    Get assets of all chains.
    """
    result = await make_request('GET', '/api/chainAssets')
    return str(result)

@mcp.tool()
async def get_protocols() -> str:
    """GET /api/protocols
    
    List all protocols on defillama along with their tvl.
    """
    result = await make_request('GET', '/api/protocols')
    return str(result)

@mcp.tool()
async def get_protocol_details(protocol: str) -> str:
    """GET /api/protocol/{protocol}
    
    Get historical TVL of a protocol and breakdowns by token and chain.
    
    Parameters:
        protocol: protocol slug (e.g., 'aave')
    """
    result = await make_request('GET', f'/api/protocol/{protocol}')
    return str(result)

@mcp.tool()
async def get_historical_chain_tvl() -> str:
    """GET /api/v2/historicalChainTvl
    
    Get historical TVL (excludes liquid staking and double counted tvl) of DeFi on all chains.
    """
    result = await make_request('GET', '/api/v2/historicalChainTvl')
    return str(result)

@mcp.tool()
async def get_historical_chain_tvl_by_chain(chain: str) -> str:
    """GET /api/v2/historicalChainTvl/{chain}
    
    Get historical TVL (excludes liquid staking and double counted tvl) of a chain.
    
    Parameters:
        chain: chain slug (e.g., 'Ethereum')
    """
    result = await make_request('GET', f'/api/v2/historicalChainTvl/{chain}')
    return str(result)

@mcp.tool()
async def get_protocol_tvl(protocol: str) -> str:
    """GET /api/tvl/{protocol}
    
    Simplified endpoint to get current TVL of a protocol.
    
    Parameters:
        protocol: protocol slug (e.g., 'uniswap')
    """
    result = await make_request('GET', f'/api/tvl/{protocol}')
    return str(result)

@mcp.tool()
async def get_chains() -> str:
    """GET /api/v2/chains
    
    Get current TVL of all chains.
    """
    result = await make_request('GET', '/api/v2/chains')
    return str(result)

@mcp.tool()
async def get_stablecoin_dominance(chain: str, stablecoin: Optional[int] = None) -> str:
    """GET /stablecoins/stablecoindominance/{chain}
    
    Get stablecoin dominance per chain along with the info about the largest coin in a chain.
    
    Parameters:
        chain: chain slug (e.g., 'Ethereum')
        stablecoin: stablecoin ID (optional)
    """
    params = {}
    if stablecoin is not None:
        params['stablecoin'] = stablecoin
    result = await make_request('GET', f'/stablecoins/stablecoindominance/{chain}', params)
    return str(result)

@mcp.tool()
async def get_stablecoins(include_prices: bool = True) -> str:
    """GET /stablecoins/stablecoins
    
    List all stablecoins along with their circulating amounts.
    
    Parameters:
        include_prices: whether to include current stablecoin prices (default: True)
    """
    params = {'includePrices': str(include_prices).lower()}
    result = await make_request('GET', '/stablecoins/stablecoins', params)
    return str(result)

@mcp.tool()
async def get_stablecoin_charts_all(stablecoin: Optional[int] = None) -> str:
    """GET /stablecoins/stablecoincharts/all
    
    Get historical mcap sum of all stablecoins.
    
    Parameters:
        stablecoin: stablecoin ID (optional)
    """
    params = {}
    if stablecoin is not None:
        params['stablecoin'] = stablecoin
    result = await make_request('GET', '/stablecoins/stablecoincharts/all', params)
    return str(result)

@mcp.tool()
async def get_stablecoin_charts_by_chain(chain: str, stablecoin: Optional[int] = None) -> str:
    """GET /stablecoins/stablecoincharts/{chain}
    
    Get historical mcap sum of all stablecoins in a chain.
    
    Parameters:
        chain: chain slug (e.g., 'Ethereum')
        stablecoin: stablecoin ID (optional)
    """
    params = {}
    if stablecoin is not None:
        params['stablecoin'] = stablecoin
    result = await make_request('GET', f'/stablecoins/stablecoincharts/{chain}', params)
    return str(result)

@mcp.tool()
async def get_stablecoin_history(asset: int) -> str:
    """GET /stablecoins/stablecoin/{asset}
    
    Get historical mcap and historical chain distribution of a stablecoin.
    
    Parameters:
        asset: stablecoin ID
    """
    result = await make_request('GET', f'/stablecoins/stablecoin/{asset}')
    return str(result)

@mcp.tool()
async def get_stablecoin_chains() -> str:
    """GET /stablecoins/stablecoinchains
    
    Get current mcap sum of all stablecoins on each chain.
    """
    result = await make_request('GET', '/stablecoins/stablecoinchains')
    return str(result)

@mcp.tool()
async def get_stablecoin_prices() -> str:
    """GET /stablecoins/stablecoinprices
    
    Get historical prices of all stablecoins.
    """
    result = await make_request('GET', '/stablecoins/stablecoinprices')
    return str(result)

@mcp.tool()
async def get_active_users() -> str:
    """GET /api/activeUsers
    
    Get active users on our chains and protocols pages.
    """
    result = await make_request('GET', '/api/activeUsers')
    return str(result)

@mcp.tool()
async def get_user_data(type: str, protocol_id: int) -> str:
    """GET /api/userData/{type}/{protocolId}
    
    Get user data by type and protocol.
    
    Parameters:
        type: data type (e.g., 'activeUsers')
        protocol_id: protocol ID
    """
    result = await make_request('GET', f'/api/userData/{type}/{protocol_id}')
    return str(result)

@mcp.tool()
async def get_emissions() -> str:
    """GET /api/emissions
    
    List of all tokens along with basic info for each.
    """
    result = await make_request('GET', '/api/emissions')
    return str(result)

@mcp.tool()
async def get_emission_data(protocol: str) -> str:
    """GET /api/emission/{protocol}
    
    Unlocks data for a given token/protocol.
    
    Parameters:
        protocol: protocol slug (e.g., 'aave')
    """
    result = await make_request('GET', f'/api/emission/{protocol}')
    return str(result)

@mcp.tool()
async def get_categories() -> str:
    """GET /api/categories
    
    Overview of all categories across all protocols.
    """
    result = await make_request('GET', '/api/categories')
    return str(result)

@mcp.tool()
async def get_forks() -> str:
    """GET /api/forks
    
    Overview of all forks across all protocols.
    """
    result = await make_request('GET', '/api/forks')
    return str(result)

@mcp.tool()
async def get_oracles() -> str:
    """GET /api/oracles
    
    Overview of all oracles across all protocols.
    """
    result = await make_request('GET', '/api/oracles')
    return str(result)

@mcp.tool()
async def get_hacks() -> str:
    """GET /api/hacks
    
    Overview of all hacks on our Hacks dashboard.
    """
    result = await make_request('GET', '/api/hacks')
    return str(result)

@mcp.tool()
async def get_raises() -> str:
    """GET /api/raises
    
    Overview of all raises on our Raises dashboard.
    """
    result = await make_request('GET', '/api/raises')
    return str(result)

@mcp.tool()
async def get_treasuries() -> str:
    """GET /api/treasuries
    
    List all protocols on our Treasuries dashboard.
    """
    result = await make_request('GET', '/api/treasuries')
    return str(result)

@mcp.tool()
async def get_entities() -> str:
    """GET /api/entities
    
    List all entities.
    """
    result = await make_request('GET', '/api/entities')
    return str(result)

@mcp.tool()
async def get_historical_liquidity(token: str) -> str:
    """GET /api/historicalLiquidity/{token}
    
    Provides the available liquidity for swapping from one token to another on a specific chain.
    
    Parameters:
        token: token slug (e.g., 'usdt')
    """
    result = await make_request('GET', f'/api/historicalLiquidity/{token}')
    return str(result)

@mcp.tool()
async def get_yield_pools_old() -> str:
    """GET /yields/poolsOld
    
    Same as /pools but it also includes a new parameter `pool_old` which usually contains pool address.
    """
    result = await make_request('GET', '/yields/poolsOld')
    return str(result)

@mcp.tool()
async def get_yield_pools_borrow() -> str:
    """GET /yields/poolsBorrow
    
    Borrow costs APY of assets from lending markets.
    """
    result = await make_request('GET', '/yields/poolsBorrow')
    return str(result)

@mcp.tool()
async def get_yield_chart_lend_borrow(pool: str) -> str:
    """GET /yields/chartLendBorrow/{pool}
    
    Historical borrow cost APY from a pool on a lending market.
    
    Parameters:
        pool: pool id (can be retrieved from /poolsBorrow)
    """
    result = await make_request('GET', f'/yields/chartLendBorrow/{pool}')
    return str(result)

@mcp.tool()
async def get_yield_perps() -> str:
    """GET /yields/perps
    
    Funding rates and Open Interest of perps across exchanges, including both Decentralized and Centralized.
    """
    result = await make_request('GET', '/yields/perps')
    return str(result)

@mcp.tool()
async def get_yield_lsd_rates() -> str:
    """GET /yields/lsdRates
    
    APY rates of multiple LSDs.
    """
    result = await make_request('GET', '/yields/lsdRates')
    return str(result)

@mcp.tool()
async def get_etf_overview() -> str:
    """GET /etfs/overview
    
    Get BTC ETFs and their metrics (aum, price, fees...).
    """
    result = await make_request('GET', '/etfs/overview')
    return str(result)

@mcp.tool()
async def get_etf_overview_eth() -> str:
    """GET /etfs/overviewEth
    
    Get ETH ETFs.
    """
    result = await make_request('GET', '/etfs/overviewEth')
    return str(result)

@mcp.tool()
async def get_etf_history() -> str:
    """GET /etfs/history
    
    Historical AUM of all BTC ETFs.
    """
    result = await make_request('GET', '/etfs/history')
    return str(result)

@mcp.tool()
async def get_etf_history_eth() -> str:
    """GET /etfs/historyEth
    
    Historical AUM of all ETH ETFs.
    """
    result = await make_request('GET', '/etfs/historyEth')
    return str(result)

@mcp.tool()
async def get_fdv_performance(period: Literal['7', '30', 'ytd', '365']) -> str:
    """GET /fdv/performance/{period}
    
    Get chart of narratives based on category performance (with individual coins weighted by mcap).
    
    Parameters:
        period: One of ['7', '30', 'ytd', '365']
    """
    if period not in ['7', '30', 'ytd', '365']:
        raise ValueError("Period must be one of: '7', '30', 'ytd', '365'")
    result = await make_request('GET', f'/fdv/performance/{period}')
    return str(result)

@mcp.tool()
async def get_yield_pools() -> str:
    """GET /yields/pools
    
    Retrieve the latest data for all pools, including enriched information such as predictions.
    """
    result = await make_request('GET', '/yields/pools')
    return str(result)

@mcp.tool()
async def get_yield_chart(pool: str) -> str:
    """GET /yields/chart/{pool}
    
    Get historical APY and TVL of a pool.
    
    Parameters:
        pool: pool id (can be retrieved from /pools)
    """
    result = await make_request('GET', f'/yields/chart/{pool}')
    return str(result)

@mcp.tool()
async def get_derivatives_overview(
    exclude_total_data_chart: bool = False,
    exclude_total_data_chart_breakdown: bool = False
) -> str:
    """GET /api/overview/derivatives
    
    Lists all derivatives along summaries of their volumes filtering by chain.
    
    Parameters:
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower()
    }
    result = await make_request('GET', '/api/overview/derivatives', params)
    return str(result)

@mcp.tool()
async def get_derivatives_summary(
    protocol: str,
    exclude_total_data_chart: bool = False,
    exclude_total_data_chart_breakdown: bool = False
) -> str:
    """GET /api/summary/derivatives/{protocol}
    
    Volume Details about a specific perp protocol.
    
    Parameters:
        protocol: protocol slug (e.g., 'hyperliquid')
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower()
    }
    result = await make_request('GET', f'/api/summary/derivatives/{protocol}', params)
    return str(result)

@mcp.tool()
async def get_bridges(include_chains: bool = True) -> str:
    """GET /bridges
    
    List all bridges along with summaries of recent bridge volumes.
    
    Parameters:
        include_chains: set whether to include current previous day volume breakdown by chain
    """
    params = {'includeChains': str(include_chains).lower()}
    result = await make_request('GET', '/bridges', params)
    return str(result)

@mcp.tool()
async def get_bridge_details(id: int) -> str:
    """GET /bridge/{id}
    
    Get summary of bridge volume and volume breakdown by chain.
    
    Parameters:
        id: bridge ID (can be retrieved from /bridges)
    """
    result = await make_request('GET', f'/bridge/{id}')
    return str(result)

@mcp.tool()
async def get_bridge_volume(
    chain: str,
    id: Optional[int] = None
) -> str:
    """GET /bridgevolume/{chain}
    
    Get historical volumes for a bridge, chain, or bridge on a particular chain.
    
    Parameters:
        chain: chain slug (e.g., 'Ethereum') or 'all' for volume on all chains
        id: bridge ID (optional, can be retrieved from /bridges)
    """
    params = {}
    if id is not None:
        params['id'] = id
    result = await make_request('GET', f'/bridgevolume/{chain}', params)
    return str(result)

@mcp.tool()
async def get_bridge_day_stats(
    timestamp: int,
    chain: str,
    id: Optional[int] = None
) -> str:
    """GET /bridgedaystats/{timestamp}/{chain}
    
    Get a 24hr token and address volume breakdown for a bridge.
    
    Parameters:
        timestamp: Unix timestamp for the 24hr period starting at 00:00 UTC
        chain: chain slug (e.g., 'Ethereum')
        id: bridge ID (optional, can be retrieved from /bridges)
    """
    params = {}
    if id is not None:
        params['id'] = id
    result = await make_request('GET', f'/bridgedaystats/{timestamp}/{chain}', params)
    return str(result)

@mcp.tool()
async def get_bridge_transactions(
    id: int,
    start_timestamp: Optional[int] = None,
    end_timestamp: Optional[int] = None,
    source_chain: Optional[str] = None,
    address: Optional[str] = None,
    limit: Optional[int] = None
) -> str:
    """GET /transactions/{id}
    
    Get all transactions for a bridge within a date range.
    
    Parameters:
        id: bridge ID (can be retrieved from /bridges)
        start_timestamp: start timestamp (Unix Timestamp) for date range
        end_timestamp: end timestamp (Unix Timestamp) for date range
        source_chain: filter by source chain (e.g., 'Polygon')
        address: filter by address in format {chain}:{address}
        limit: limit number of transactions returned (max 6000)
    """
    params = {}
    if start_timestamp is not None:
        params['starttimestamp'] = start_timestamp
    if end_timestamp is not None:
        params['endtimestamp'] = end_timestamp
    if source_chain is not None:
        params['sourcechain'] = source_chain
    if address is not None:
        params['address'] = address
    if limit is not None:
        params['limit'] = limit
    result = await make_request('GET', f'/transactions/{id}', params)
    return str(result)

@mcp.tool()
async def get_current_prices(
    coins: str,
    search_width: str = "6h"
) -> str:
    """GET /coins/prices/current/{coins}
    
    Get current prices of tokens by contract address.
    
    Parameters:
        coins: comma-separated tokens in format {chain}:{address} (e.g., 'ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1,coingecko:ethereum')
        search_width: time range on either side to find price data (default: '6h')
    """
    params = {'searchWidth': search_width}
    result = await make_request('GET', f'/coins/prices/current/{coins}', params)
    return str(result)

@mcp.tool()
async def get_historical_prices(
    timestamp: int,
    coins: str,
    search_width: str = "6h"
) -> str:
    """GET /coins/prices/historical/{timestamp}/{coins}
    
    Get historical prices of tokens by contract address.
    
    Parameters:
        timestamp: UNIX timestamp for historical prices
        coins: comma-separated tokens in format {chain}:{address}
        search_width: time range on either side to find price data (default: '6h')
    """
    params = {'searchWidth': search_width}
    result = await make_request('GET', f'/coins/prices/historical/{timestamp}/{coins}', params)
    return str(result)

@mcp.tool()
async def get_batch_historical_prices(
    coins: Dict[str, List[int]],
    search_width: str = "6h"
) -> str:
    """GET /coins/batchHistorical
    
    Get historical prices for multiple tokens at multiple different timestamps.
    
    Parameters:
        coins: dict where keys are coins in format {chain}:{address} and values are arrays of timestamps
        search_width: time range on either side to find price data (default: '6h')
    """
    params = {
        'coins': str(coins),
        'searchWidth': search_width
    }
    result = await make_request('GET', '/coins/batchHistorical', params)
    return str(result)

@mcp.tool()
async def get_price_chart(
    coins: str,
    start: Optional[int] = None,
    end: Optional[int] = None,
    span: Optional[int] = None,
    period: str = "24h",
    search_width: str = "600"
) -> str:
    """GET /coins/chart/{coins}
    
    Get token prices at regular time intervals.
    
    Parameters:
        coins: comma-separated tokens in format {chain}:{address}
        start: unix timestamp of earliest data point
        end: unix timestamp of latest data point
        span: number of data points returned
        period: duration between data points (default: '24h')
        search_width: time range on either side to find price data (default: '600')
    """
    params = {
        'period': period,
        'searchWidth': search_width
    }
    if start is not None:
        params['start'] = start
    if end is not None:
        params['end'] = end
    if span is not None:
        params['span'] = span
    result = await make_request('GET', f'/coins/chart/{coins}', params)
    return str(result)

@mcp.tool()
async def get_price_percentage(
    coins: str,
    timestamp: Optional[int] = None,
    look_forward: bool = False,
    period: str = "24h"
) -> str:
    """GET /coins/percentage/{coins}
    
    Get percentage change in price over time.
    
    Parameters:
        coins: comma-separated tokens in format {chain}:{address}
        timestamp: timestamp of data point (defaults to now)
        look_forward: whether to look forward from timestamp (default: False)
        period: duration between data points (default: '24h')
    """
    params = {
        'lookForward': str(look_forward).lower(),
        'period': period
    }
    if timestamp is not None:
        params['timestamp'] = timestamp
    result = await make_request('GET', f'/coins/percentage/{coins}', params)
    return str(result)

@mcp.tool()
async def get_first_price_record(coins: str) -> str:
    """GET /coins/prices/first/{coins}
    
    Get earliest timestamp price record for coins.
    
    Parameters:
        coins: comma-separated tokens in format {chain}:{address}
    """
    result = await make_request('GET', f'/coins/prices/first/{coins}')
    return str(result)

@mcp.tool()
async def get_closest_block(chain: str, timestamp: int) -> str:
    """GET /coins/block/{chain}/{timestamp}
    
    Get the closest block to a timestamp.
    
    Parameters:
        chain: chain identifier
        timestamp: UNIX timestamp to find closest block for
    """
    result = await make_request('GET', f'/coins/block/{chain}/{timestamp}')
    return str(result)

@mcp.tool()
async def get_dex_overview(
    exclude_total_data_chart: bool = True,
    exclude_total_data_chart_breakdown: bool = True
) -> str:
    """GET /api/overview/dexs
    
    List all dexs along with summaries of their volumes and dataType history data.
    
    Parameters:
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower()
    }
    result = await make_request('GET', '/api/overview/dexs', params)
    return str(result)

@mcp.tool()
async def get_dex_overview_by_chain(
    chain: str,
    exclude_total_data_chart: bool = True,
    exclude_total_data_chart_breakdown: bool = True
) -> str:
    """GET /api/overview/dexs/{chain}
    
    List all dexs along with summaries of their volumes and dataType history data filtering by chain.
    
    Parameters:
        chain: chain name (e.g., 'ethereum')
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower()
    }
    result = await make_request('GET', f'/api/overview/dexs/{chain}', params)
    return str(result)

@mcp.tool()
async def get_dex_summary(
    protocol: str,
    exclude_total_data_chart: bool = True,
    exclude_total_data_chart_breakdown: bool = True
) -> str:
    """GET /api/summary/dexs/{protocol}
    
    Get summary of dex volume with historical data.
    
    Parameters:
        protocol: protocol slug (e.g., 'uniswap')
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower()
    }
    result = await make_request('GET', f'/api/summary/dexs/{protocol}', params)
    return str(result)

@mcp.tool()
async def get_options_overview(
    exclude_total_data_chart: bool = True,
    exclude_total_data_chart_breakdown: bool = True,
    data_type: Literal['dailyPremiumVolume', 'dailyNotionalVolume'] = 'dailyNotionalVolume'
) -> str:
    """GET /api/overview/options
    
    List all options dexs along with summaries of their volumes and dataType history data.
    
    Parameters:
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
        data_type: desired data type (default: 'dailyNotionalVolume')
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower(),
        'dataType': data_type
    }
    result = await make_request('GET', '/api/overview/options', params)
    return str(result)

@mcp.tool()
async def get_options_overview_by_chain(
    chain: str,
    exclude_total_data_chart: bool = True,
    exclude_total_data_chart_breakdown: bool = True,
    data_type: Literal['dailyPremiumVolume', 'dailyNotionalVolume'] = 'dailyNotionalVolume'
) -> str:
    """GET /api/overview/options/{chain}
    
    List all options dexs along with summaries of their volumes and dataType history data filtering by chain.
    
    Parameters:
        chain: chain name (e.g., 'ethereum')
        exclude_total_data_chart: true to exclude aggregated chart from response
        exclude_total_data_chart_breakdown: true to exclude broken down chart from response
        data_type: desired data type (default: 'dailyNotionalVolume')
    """
    params = {
        'excludeTotalDataChart': str(exclude_total_data_chart).lower(),
        'excludeTotalDataChartBreakdown': str(exclude_total_data_chart_breakdown).lower(),
        'dataType': data_type
    }
    result = await make_request('GET', f'/api/overview/options/{chain}', params)
    return str(result)

@mcp.tool()
async def get_options_summary(
    protocol: str,
    data_type: Literal['dailyPremiumVolume', 'dailyNotionalVolume'] = 'dailyNotionalVolume'
) -> str:
    """GET /api/summary/options/{protocol}
    
    Get summary of options dex volume with historical data.
    
    Parameters:
        protocol: protocol slug (e.g., 'lyra')
        data_type: desired data type (default: 'dailyNotionalVolume')
    """
    params = {'dataType': data_type}
    result = await make_request('GET', f'/api/summary/options/{protocol}', params)
    return str(result)

@mcp.tool()
async def get_fees_summary(
    protocol: str,
    data_type: Literal['dailyFees', 'dailyRevenue'] = 'dailyFees'
) -> str:
    """GET /api/summary/fees/{protocol}
    
    Get summary of protocol fees and revenue with historical data.
    
    Parameters:
        protocol: protocol slug (e.g., 'lyra')
        data_type: desired data type (default: 'dailyFees')
    """
    params = {'dataType': data_type}
    result = await make_request('GET', f'/api/summary/fees/{protocol}', params)
    return str(result)

if __name__ == "__main__":
    mcp.run(transport='stdio') 