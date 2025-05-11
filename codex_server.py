from typing import Any, Dict, List, Optional, Union, Literal, TypedDict
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import httpx
import json
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("codex")

# Configuration
API_KEY = os.getenv("CODEX_API_KEY")
BASE_URL = "https://graph.codex.io"

# Network IDs for reference
NETWORKS = {
    "Metis": 1088,
    "HyperEVM": 999,
    "Swellchain": 1923,
    "Mantle": 5000,
    "Klaytn": 8217,
    "Plume": 98866,
    "Over Protocol": 54176,
    "opBNB": 204,
    "Odyssey Chain": 153153,
    "Wanchain": 888,
    "Shibarium": 109,
    "Telos": 40,
    "Zircuit": 48900,
    "Polygon Mumbai": 80001,
    "Celo": 42220,
    "Evmos": 9001,
    "Base Sepolia": 84532,
    "Dogechain": 2000,
    "Aptos": 49705,
    "Saigon": 2021,
    "Vector": 420042,
    "Vana": 1480,
    "Sophon": 50104,
    "OEC": 66,
    "Aurora": 1313161554,
    "CheeseChain": 383353,
    "Velas": 106,
    "Manta": 169,
    "Ethereum": 1,
    "Ethereum Sepolia": 11155111,
    "Arbitrum Nova": 42170,
    "Chiliz": 88888,
    "Oasis Emerald": 42262,
    "Sei": 531,
    "Linea": 59144,
    "Plume Legacy": 98865,
    "Energi": 39797,
    "Echos": 4321,
    "Milkomeda": 2001,
    "Blast Sepolia": 168587773,
    "Berachain Artio": 80085,
    "Berachain bArtio": 80084,
    "Abstract Testnet": 11124,
    "Treasure": 61166,
    "Unichain": 130,
    "Scroll": 534352,
    "zkSync": 324,
    "Meter": 82,
    "Polygon": 137,
    "Conwai": 668668,
    "Base": 8453,
    "KardiaChain": 24,
    "Energy Web": 246,
    "Smartbch": 10000,
    "Monad Testnet": 10143,
    "Echelon": 3000,
    "Sonic": 146,
    "Fantom": 250,
    "Blast": 81457,
    "Story": 1514,
    "Polygon zkEVM": 1101,
    "MELD": 333000333,
    "Heco": 128,
    "Sei Arctic": 713715,
    "Goerli": 5,
    "Ronin": 2020,
    "Mode": 34443,
    "Polis": 333999,
    "Shiden": 336,
    "IoTeX": 4689,
    "xDai": 100,
    "Moonbeam": 1284,
    "Yominet": 428962,
    "Abstract": 2741,
    "re.al": 111188,
    "Sui": 101,
    "Tron": 728126428,
    "Moonriver": 1285,
    "Sanko Sepolia": 1992,
    "Starknet": 57420037,
    "Degen Chain": 666666666,
    "Ham": 5112,
    "Solana": 1399811149,
    "World Chain": 480,
    "ZYX": 55,
    "Xai": 660279,
    "Zora": 7777777,
    "Ink": 57073,
    "BNB Chain": 56,
    "Hoo Smart Chain": 70,
    "Berachain": 80094,
    "Avalanche": 43114,
    "Boba": 288,
    "Elastos": 20,
    "Harmony": 1666600000,
    "Avalanche DFK": 53935,
    "Core": 1116,
    "Callisto": 820,
    "Story Iliad": 1513,
    "Sanko": 1996,
    "Pulsechain": 369,
    "KuCoin Community Chain": 321,
    "Arbitrum": 42161,
    "Cronos": 25,
    "ApeChain": 33139,
    "Astar": 592,
    "Superposition": 55244,
    "Optimism": 10,
    "Syscoin": 57,
    "Berachain Old": 80089,
    "Conflux": 1030,
    "Flow EVM Testnet": 545,
    "Canto": 7700,
    "Flow EVM": 747,
    "Fuse": 122
}

# HTTP client
client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    },
    timeout=30.0
)

async def make_graphql_request(query: str, variables: Optional[Dict[str, Any]] = None) -> Any:
    """Make a GraphQL request to the Codex API."""
    try:
        payload = {
            "query": query,
            "variables": variables or {}
        }
        response = await client.post("/graphql", json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        print(error_msg)  # For debugging
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)  # For debugging
        return {"error": error_msg}

@mcp.tool()
async def get_token_info(
    phrase: Optional[str] = None,
    tokens: Optional[List[str]] = None,
    excludeTokens: Optional[List[str]] = None,
    network: Optional[List[int]] = None,
    limit: int = 10,
    offset: int = 0,
    statsType: Optional[str] = None
) -> str:
    """GET token information from Codex API
    
    Use this endpoint to search for tokens based on various filters and criteria.
    It can search by token name, address, or symbol and filter by network IDs.
    
    Args:
        phrase: A phrase to search for. Can match a token contract address or partially match a token's name or symbol.
        tokens: A list of token IDs (address:networkId) or addresses. Can be left blank to discover new tokens.
        excludeTokens: A list of token IDs (address:networkId) to exclude from results
        network: A list of network IDs to filter tokens by. See NETWORKS constant for available networks.
        limit: The maximum number of tokens to return (default: 10)
        offset: Where in the list the server should start when returning items (default: 0)
        statsType: The type of statistics returned. Can be FILTERED or UNFILTERED
    
    Returns:
        JSON string with token information based on the provided filters
    """
    filters = {}
    
    # Add network to filters if provided
    if network:
        filters["network"] = network
    
    # Always sort by 24h volume in descending order
    rankings = [{"attribute": "volume24", "direction": "DESC"}]
    
    # Construct GraphQL query
    query = """
    query FilterTokens($filters: TokenFilters, $phrase: String, $tokens: [String], $excludeTokens: [String], $limit: Int, $offset: Int, $statsType: TokenPairStatisticsType, $rankings: [TokenRanking]) {
      filterTokens(
        filters: $filters
        phrase: $phrase
        tokens: $tokens
        excludeTokens: $excludeTokens
        limit: $limit
        offset: $offset
        statsType: $statsType
        rankings: $rankings
      ) {
        count
        page
        results {
          buyCount1
          buyCount4
          buyCount24
          high1
          high24
          txnCount1
          txnCount24
          uniqueTransactions1
          uniqueTransactions24
          volume1
          volume24
          liquidity
          marketCap
          priceUSD
          pair {
            token0
            token1
          }
          exchanges {
            name
          }
          token {
            address
            decimals
            name
            networkId
            symbol
            info {
              circulatingSupply
              totalSupply
            }
          }
        }
      }
    }
    """
    
    variables = {
        "filters": filters,
        "phrase": phrase,
        "tokens": tokens,
        "excludeTokens": excludeTokens,
        "limit": limit,
        "offset": offset,
        "statsType": statsType,
        "rankings": rankings
    }
    
    # Remove None values from variables
    variables = {k: v for k, v in variables.items() if v is not None}
    
    print(f"Making GraphQL request with variables: {variables}")  # For debugging
    result = await make_graphql_request(query, variables)
    
    return json.dumps(result)

if __name__ == "__main__":
    mcp.run(transport='stdio') 