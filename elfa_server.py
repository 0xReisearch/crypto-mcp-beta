from typing import Any, Dict, List, Optional, Union, Literal
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import httpx
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("elfa")

# Configuration
API_KEY = os.getenv("ELFA_API_KEY")
BASE_URL = "https://api.elfa.ai/v1"

# HTTP client
client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={"x-elfa-api-key": API_KEY},
    timeout=30.0
)

async def make_request(method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Make a request to the Elfa API."""
    try:
        response = await client.request(method, endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_mentions(
    limit: int = 100,
    offset: int = 0
) -> str:
    """GET /v1/mentions
    
    Query tweets by smart accounts with at least 10 other smart interaction (comment, RT, QT). 
    Updated every 1 hour.
    
    Parameters:
        limit: Number of results to return (default: 100)
        offset: Number of results to skip (default: 0)
    """
    params = {
        'limit': limit,
        'offset': offset
    }
    result = await make_request('GET', '/mentions', params)
    return str(result)

@mcp.tool()
async def get_top_mentions(
    ticker: str,
    timeWindow: str = "1h",
    page: int = 1,
    pageSize: int = 10,
    includeAccountDetails: bool = False
) -> str:
    """GET /v1/top-mentions
    
    Query tweets that mentioned a specified ticker. Ranked by view count. 
    Updated every 1 hour.
    
    Parameters:
        ticker: The ticker symbol to get mentions for. Prefixing with $ will only return cashtag matches.
        timeWindow: Time window for mentions (e.g., "1h", "24h", "7d") (default: "1h")
        page: Page number for pagination (default: 1)
        pageSize: Number of items per page (default: 10)
        includeAccountDetails: Include account details (default: False)
    """
    params = {
        'ticker': ticker,
        'timeWindow': timeWindow,
        'page': page,
        'pageSize': pageSize,
        'includeAccountDetails': includeAccountDetails
    }
    result = await make_request('GET', '/top-mentions', params)
    return str(result)

@mcp.tool()
async def search_mentions(
    keywords: str,
    from_: int,
    to: int,
    limit: int = 20,
    searchType: Optional[str] = None,
    cursor: Optional[str] = None
) -> str:
    """GET /v1/mentions/search
    
    Query tweets that mentioned up to 5 keywords within a 30-days window. 
    Up to 6-months worth of tweets. Updated every 5 mins.
    
    Parameters:
        keywords: Up to 5 keywords to search for, separated by commas. Phrases accepted
        from_: Start date (unix timestamp)
        to: End date (unix timestamp)
        limit: Number of results to return (default: 20, max 30)
        searchType: Type of search (and, or)
        cursor: Cursor for pagination, expires after 10 seconds
    """
    params = {
        'keywords': keywords,
        'from': from_,
        'to': to,
        'limit': limit
    }
    if searchType:
        params['searchType'] = searchType
    if cursor:
        params['cursor'] = cursor
    result = await make_request('GET', '/mentions/search', params)
    return str(result)

@mcp.tool()
async def get_social_trending_tokens(
    timeWindow: str = "24h",
    page: int = 1,
    pageSize: int = 50,
    minMentions: int = 5
) -> str:
    """GET /v1/trending-tokens
    
    Query tokens most discussed in a particular time period. 
    Ranked by smart mentions count. Updated every 5 mins.
    
    Parameters:
        timeWindow: Time window for trending analysis (default: "24h")
        page: Page number for pagination (default: 1)
        pageSize: Number of items per page (default: 50)
        minMentions: Minimum number of mentions required (default: 5)
    """
    params = {
        'timeWindow': timeWindow,
        'page': page,
        'pageSize': pageSize,
        'minMentions': minMentions
    }
    result = await make_request('GET', '/trending-tokens', params)
    return str(result)

@mcp.tool()
async def get_smart_account_stats(username: str) -> str:
    """GET /v1/account/smart-stats
    
    Retrieve smart stats (smart following count) and social metrics 
    (engagement score & ratio) for a given username
    
    Parameters:
        username: Twitter username to get stats for
    """
    params = {
        'username': username
    }
    result = await make_request('GET', '/account/smart-stats', params)
    return str(result)

if __name__ == "__main__":
    mcp.run(transport='stdio') 