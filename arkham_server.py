from typing import Any, Dict, List, Optional, Union, Literal
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import httpx
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("arkham")

# Configuration
API_KEY = os.getenv("ARKHAM_API_KEY")
BASE_URL = "https://api.arkhamintelligence.com"

# HTTP client
client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={"API-Key": API_KEY},
    timeout=30.0
)

async def make_request(method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Make a request to the Arkham API."""
    try:
        response = await client.request(method, endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_swaps(
    base: List[str] = None,
    chains: List[str] = None,
    flow: Literal["in", "out", "all"] = "all",
    from_: List[str] = None,
    to: List[str] = None,
    tokens: List[str] = None,
    timeGte: int = None,
    timeLte: int = None,
    timeLast: str = None,
    valueGte: float = None,
    valueLte: float = None,
    usdGte: float = None,
    usdLte: float = None,
    sortKey: Literal["time", "value", "usd"] = "time",
    sortDir: Literal["asc", "desc"] = "desc",
    limit: int = 20,
    offset: int = 0,
    sold: List[str] = None,
    bought: List[str] = None,
    counterparties: List[str] = None,
    senders: List[str] = None,
    receivers: List[str] = None,
    protocols: List[str] = None
) -> str:
    """GET /swaps

    base: Entities/addresses you want to see transactions either from or to
    chains: Optional, if empty it will default to all chains
    flow: Flow is with respect to base so if you choose e.g. out you will only see transactions coming from base
    from_: Filter for only transactions from certain entities/addresses
    to: Filter for only transactions to certain entities/addresses
    tokens: Filter for only transactions involving particular tokens
    timeGte: Filter for transactions with a block_timestamp greater than or equal to a certain time
    timeLte: Filter for transactions with a block_timestamp less than or equal to a certain time
    timeLast: Filter for transfers within a particular duration (e.g. "1h", "3d", "10m")
    valueGte: Filters for transfers above a certain token unit value
    valueLte: Filters for transfers below a certain token unit value
    usdGte: Same as valueGte except for USD value
    usdLte: Same as usdGte
    sortKey: Sort results by this key
    sortDir: Sort results either in either ascending or descending order
    limit: Number of transfers to return
    offset: Ignores offset transfers before returning limit
    sold: Filter for where certain assets are sold
    bought: Filter for where certain assets are bought
    counterparties: Filter for transactions involving certain counterparties
    senders: Filter for where certain addresses are the sender
    receivers: Filter for where certain addresses are the receiver
    protocols: Filter for swaps that occur on certain protocols
    """
    params = {}
    if base is not None:
        params['base'] = base
    if chains is not None:
        params['chains'] = chains
    if flow is not None:
        params['flow'] = flow
    if from_ is not None:
        params['from'] = from_
    if to is not None:
        params['to'] = to
    if tokens is not None:
        params['tokens'] = tokens
    if timeGte is not None:
        params['timeGte'] = timeGte
    if timeLte is not None:
        params['timeLte'] = timeLte
    if timeLast is not None:
        params['timeLast'] = timeLast
    if valueGte is not None:
        params['valueGte'] = valueGte
    if valueLte is not None:
        params['valueLte'] = valueLte
    if usdGte is not None:
        params['usdGte'] = usdGte
    if usdLte is not None:
        params['usdLte'] = usdLte
    if sortKey is not None:
        params['sortKey'] = sortKey
    if sortDir is not None:
        params['sortDir'] = sortDir
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if sold is not None:
        params['sold'] = sold
    if bought is not None:
        params['bought'] = bought
    if counterparties is not None:
        params['counterparties'] = counterparties
    if senders is not None:
        params['senders'] = senders
    if receivers is not None:
        params['receivers'] = receivers
    if protocols is not None:
        params['protocols'] = protocols
    result = await make_request('GET', '/swaps', params)
    return str(result)

@mcp.tool()
async def get_transfers_histogram() -> str:
    """GET /transfers/histogram"""
    result = await make_request('GET', '/transfers/histogram')
    return str(result)

@mcp.tool()
async def get_intelligence_address(address: str, chains: List[str] = None) -> str:
    """GET /intelligence/address/{address}?chain={chain}

    address: As a path parameter.
    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/intelligence/address/{address}', params)
    return str(result)

@mcp.tool()
async def get_intelligence_address_all(address: str) -> str:
    """GET /intelligence/address/{address}/all

    address: This is passed as a path parameter.
    """
    result = await make_request('GET', f'/intelligence/address/{address}/all')
    return str(result)

@mcp.tool()
async def get_intelligence_address_with_extra_enrichment(address: str, tags: bool = None, chains: List[str] = None) -> str:
    """GET /intelligence/address_with_extra_enrichment/{address}

    address: Passed as a path parameter.
    tags: Optional, defaults to false.
    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if tags is not None:
        params['tags'] = tags
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/intelligence/address_with_extra_enrichment/{address}', params)
    return str(result)

@mcp.tool()
async def get_intelligence_entity(entity: str) -> str:
    """GET /intelligence/entity/{entity}

    entity: This is passed as a path parameter.
    """
    result = await make_request('GET', f'/intelligence/entity/{entity}')
    return str(result)

@mcp.tool()
async def get_intelligence_contract(chain: str, address: str) -> str:
    """GET /intelligence/contract/{chain}/{address}"""
    result = await make_request('GET', f'/intelligence/contract/{chain}/{address}')
    return str(result)

@mcp.tool()
async def get_intelligence_token_by_pricing_id(coinGeckoPricingId: str) -> str:
    """GET /intelligence/token/{coinGeckoPricingId}"""
    result = await make_request('GET', f'/intelligence/token/{coinGeckoPricingId}')
    return str(result)

@mcp.tool()
async def get_intelligence_token_by_chain_address(chain: str, address: str) -> str:
    """GET /intelligence/token/{chain}/{address}"""
    result = await make_request('GET', f'/intelligence/token/{chain}/{address}')
    return str(result)

@mcp.tool()
async def get_history_entity(entity: str, chains: List[str] = None) -> str:
    """GET /history/entity/{entity}

    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/history/entity/{entity}', params)
    return str(result)

@mcp.tool()
async def get_history_address(address: str, chains: List[str] = None) -> str:
    """GET /history/address/{address}

    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/history/address/{address}', params)
    return str(result)

@mcp.tool()
async def get_portfolio_entity(entity: str, chains: List[str] = None) -> str:
    """GET /portfolio/entity/{entity}

    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/portfolio/entity/{entity}', params)
    return str(result)

@mcp.tool()
async def get_portfolio_address(address: str, chains: List[str] = None) -> str:
    """GET /portfolio/address/{address}

    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/portfolio/address/{address}', params)
    return str(result)

@mcp.tool()
async def get_transfers_by_tx_hash(hash: str, chain: str, transferType: str) -> str:
    """GET /transfers/tx/{hash}

    hash: The hash of a transaction as a path parameter.
    chain: The chain which the transaction occurred on (e.g. ethereum).
    transferType: The type of transfer. Can be either `token`, `internal`, or `external`.
    """
    params = {
        'chain': chain,
        'transferType': transferType
    }
    result = await make_request('GET', f'/transfers/tx/{hash}', params)
    return str(result)

@mcp.tool()
async def get_tx(hash: str) -> str:
    """GET /tx/{hash}

    hash: Represents the transaction hash as a path parameter.
    """
    result = await make_request('GET', f'/tx/{hash}')
    return str(result)

@mcp.tool()
async def get_balances_address(address: str) -> str:
    """GET /balances/address/{address}"""
    result = await make_request('GET', f'/balances/address/{address}')
    return str(result)

@mcp.tool()
async def get_balances_entity(entity: str, chains: List[str] = None) -> str:
    """GET /balances/entity/{entity}

    chains: Optional, if empty it will default to all chains
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/balances/entity/{entity}', params)
    return str(result)

@mcp.tool()
async def get_loans_address(address: str) -> str:
    """GET /loans/address/{address}"""
    result = await make_request('GET', f'/loans/address/{address}')
    return str(result)

@mcp.tool()
async def get_loans_entity(entity: str, chains: List[str] = None) -> str:
    """GET /loans/entity/{entity}

    entity: The entity you want to see transactions from or to.
    chains: Optional, if empty it will default to all chains.
    """
    params = {}
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/loans/entity/{entity}', params)
    return str(result)

@mcp.tool()
async def get_counterparties_address(address: str, flow: Literal["all", "in", "out", "self"] = None, tokens: List[str] = None, chains: List[str] = None) -> str:
    """GET /counterparties/address/{address}

    flow: Used to filter the counterparties by their flow of transactions.
    tokens: Used to filter the counterparties by the tokens they have transacted with.
    chains: Used to filter the counterparties by the chains they have transacted on.
    """
    params = {}
    if flow is not None:
        params['flow'] = flow
    if tokens is not None:
        params['tokens'] = tokens
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/counterparties/address/{address}', params)
    return str(result)

@mcp.tool()
async def get_counterparties_entity(entity: str, flow: Literal["all", "in", "out", "self"] = None, tokens: List[str] = None, chains: List[str] = None) -> str:
    """GET /counterparties/entity/{entity}

    flow: Used to filter the counterparties by their flow of transactions.
    tokens: Used to filter the counterparties by the tokens they have transacted with.
    chains: Used to filter the counterparties by the chains they have transacted on.
    """
    params = {}
    if flow is not None:
        params['flow'] = flow
    if tokens is not None:
        params['tokens'] = tokens
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/counterparties/entity/{entity}', params)
    return str(result)

@mcp.tool()
async def get_portfolio_time_series_entity(entity: str, pricingId: str) -> str:
    """GET /portfolio/timeSeries/entity/{entity}

    entity: An alternative to `address`
    pricingId: Note: This does not support unpriced tokens via `chain` + `address` combination.
    """
    params = {
        'pricingId': pricingId
    }
    result = await make_request('GET', f'/portfolio/timeSeries/entity/{entity}', params)
    return str(result)

@mcp.tool()
async def get_portfolio_time_series_address(address: List[str], pricingId: str) -> str:
    """GET /portfolio/timeSeries/address/{address}

    address: This is either a single address or a list of addresses
    pricingId: Note: This does not support unpriced tokens via `chain` + `address` combination.
    """
    params = {
        'pricingId': pricingId
    }
    result = await make_request('GET', f'/portfolio/timeSeries/address/{",".join(address)}', params)
    return str(result)

@mcp.tool()
async def get_token_holders_by_pricing_id(pricing_id: str) -> str:
    """GET /token/holders/{pricing_id}

    pricing_id: As path parameter. It's a CoinGecko pricing ID.
    """
    result = await make_request('GET', f'/token/holders/{pricing_id}')
    return str(result)

@mcp.tool()
async def get_token_holders_by_chain_address(chain: str, address: str) -> str:
    """GET /token/holders/{chain}/{address}"""
    result = await make_request('GET', f'/token/holders/{chain}/{address}')
    return str(result)

@mcp.tool()
async def get_token_top_flow_by_id(id: str, timeLast: str = None, chains: List[str] = None) -> str:
    """GET /token/top_flow/{id}

    id: Either `id` or `chain` and `address` as path parameters. The `id` is a CoinGecko pricing ID.
    timeLast: Required
    """
    params = {}
    if timeLast is not None:
        params['timeLast'] = timeLast
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/token/top_flow/{id}', params)
    return str(result)

@mcp.tool()
async def get_token_top_flow_by_chain_address(chain: str, address: str, timeLast: str = None, chains: List[str] = None) -> str:
    """GET /token/top_flow/{chain}/{address}

    timeLast: Required
    """
    params = {}
    if timeLast is not None:
        params['timeLast'] = timeLast
    if chains is not None:
        params['chains'] = chains
    result = await make_request('GET', f'/token/top_flow/{chain}/{address}', params)
    return str(result)

@mcp.tool()
async def get_networks_status() -> str:
    """GET /networks/status"""
    result = await make_request('GET', '/networks/status')
    return str(result)

@mcp.tool()
async def get_networks_history(chain: str) -> str:
    """GET /networks/history/{chain}"""
    result = await make_request('GET', f'/networks/history/{chain}')
    return str(result)

@mcp.tool()
async def get_api_important_entities() -> str:
    """GET /api/importantEntities"""
    result = await make_request('GET', '/api/importantEntities')
    return str(result)

@mcp.tool()
async def get_tag(id: str) -> str:
    """GET /tag/{id}"""
    result = await make_request('GET', f'/tag/{id}')
    return str(result)

@mcp.tool()
async def get_tag_params(id: str) -> str:
    """GET /tag/{id}/params"""
    result = await make_request('GET', f'/tag/{id}/params')
    return str(result)

@mcp.tool()
async def get_tag_top() -> str:
    """GET /tag/top"""
    result = await make_request('GET', '/tag/top')
    return str(result)

@mcp.tool()
async def get_tag_all() -> str:
    """GET /tag/all"""
    result = await make_request('GET', '/tag/all')
    return str(result)

if __name__ == "__main__":
    mcp.run(transport='stdio')
