# MCP app to get clean markdown from a url

I wanted to try MCP and used the repository [MCP-searxng](https://github.com/SecretiveShell/MCP-searxng) by [SecretiveShell](https://github.com/SecretiveShell) as a starting point.

Install

```bash
git clone https://github.com/reuteras/mcp-clean-url.git
cd mcp-clean-url
uv sync
source .venv/bin/activate
mcp install --with markdownify src/mcp_clean_url/server.py
```
