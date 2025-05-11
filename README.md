# REI Crypto MCP Server - Beta

FastMCP implementation of the in-house MCP servers used by Units of the Rei Network.
You can use them without providing API keys at app.reisearch.box or you can use them with other MCP clients deploying them yourself.

Everything is to be considered still in beta. Expect things to be added or changed with no warnings.

<a href="https://glama.ai/mcp/servers/@0xReisearch/crypto-mcp-beta">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@0xReisearch/crypto-mcp-beta/badge" alt="REI Crypto Server MCP server" />
</a>

## Current MCP servers:
- DefiLlama Pro API
- CoinGecko Pro API
- Arkham Intelligence API
- Elfa AI API
- Codex API

Codex at the moment is just used for searching a contract address from the name. Deeper implementation will come in the near future.
Codex uses GraphQL for it's query system. Edit the query to hardcode some parameters in case you need stricter filtering.

## Prerequisites

- Python 3.12
- `uv` package manager
- API keys for the services you plan to use

## Installation

1. Clone the repository:
```bash
git clone https://github.com/0xReisearch/crypto-mcp-beta
cd crypto-mcp-beta
```

2. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate a virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

4. Install dependencies from pyproject.toml:
```bash
uv pip install .
```

5. Set up your environment variables:
```bash
cp .env_example .env
```

Edit `.env` with your API keys:
```
ARKHAM_API_KEY=<YOUR ARKHAM_API_KEY>
CG_API_KEY=<YOUR_CG_API_KEY>
DEFILLAMA_API_KEY=<YOUR_DEFILLAMA_API_KEY>
CODEX_API_KEY=<YOUR_CODEX_API_KEY>
ELFA_API_KEY=<YOUR_ELFA_API_KEY>
```

## Running the Servers

You can run each server individually:

```bash
# Run DefiLlama server
uv run defillama_server.py

# Run CoinGecko server
uv run cg_server.py

# Run Arkham server
uv run arkham_server.py

# Run Codex server
uv run codex_server.py

# Run Elfa AI server
uv run elfa_server.py
```

## Configuring Claude Desktop

To use these servers with Claude Desktop, you need to configure the `claude_desktop_config.json` file. This file is typically located in:
- Windows: `%APPDATA%/claude-desktop/claude_desktop_config.json`
- macOS: `~/Library/Application Support/claude-desktop/claude_desktop_config.json`
- Linux: `~/.config/claude-desktop/claude_desktop_config.json`

Example configuration:
```json
{
    "mcpServers": {
        "arkham": {
            "command": "ssh",
            "args": [
                "user@your-host",
                "cd /path/to/crypto_mcp && /path/to/uv run arkham_server.py"
            ]
        },
        "coingecko": {
            "command": "ssh",
            "args": [
                "user@your-host",
                "cd /path/to/crypto_mcp && /path/to/uv run cg_server.py"
            ]
        },
        "defillama": {
            "command": "ssh",
            "args": [
                "user@your-host",
                "cd /path/to/crypto_mcp && /path/to/uv run defillama_server.py"
            ]
        },
        "codex": {
            "command": "ssh",
            "args": [
                "user@your-host",
                "cd /path/to/crypto_mcp && /path/to/uv run codex_server.py"
            ]
        },
        "elfa": {
            "command": "ssh",
            "args": [
                "user@your-host",
                "cd /path/to/crypto_mcp && /path/to/uv run elfa_server.py"
            ]
        }
    }
}
```

Replace the following:
- `user@your-host`: Your SSH username and host
- `/path/to/crypto_mcp`: The absolute path to where you cloned this repository
- `/path/to/uv`: The absolute path to your uv installation (usually in `~/.local/bin/uv` on Unix systems)

## API Documentation

- [DefiLlama API Documentation](https://defillama.com/pro-api/docs)
- [CoinGecko API Documentation](https://docs.coingecko.com/reference/introduction)
- [Codex API Documentation](https://docs.codex.io/reference/overview)
- [Elfa AI Api Documentation](https://www.elfa.ai/) - Contact Elfa directly for api access.
- [Arkham Intelligence](https://intel.arkm.com/) - You need to contact Arkham directly for api access.

## Feedback

If you encounter any issues or have suggestions for improvements:

1. For bug reports or feature requests, please open an issue in this repository
2. For general feedback or questions, you can leave a comment in the repository discussions

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

Made with ❤️ by [Rei Network](https://reisearch.box)