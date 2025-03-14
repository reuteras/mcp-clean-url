"""Get clean url via MCP for LLMs."""

import re
import sys

from httpx import AsyncClient, Response
from markdownify import BeautifulSoup, MarkdownConverter
from mcp.server.fastmcp import FastMCP


# Create shorthand method for conversion
def md(soup, **options) -> str:
    """Convert soup to markdown."""
    return MarkdownConverter(**options).convert_soup(soup=soup)

async def get_clean_url(url: str) -> str:
    """Get clean data from url."""
    client = AsyncClient()
    text: str = ""

    matches: re.Match[str] | None = re.match(pattern=r"^https://github.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)$", string=url)
    if matches is not None:
        try:
            owner: str = matches.group(1)
            repo: str = matches.group(2)
            branch: str = matches.group(3)
            path: str = matches.group(4)
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        except IndexError:
            pass
        response: Response = await client.get(url=url)
        response.raise_for_status()
        text = response.text
    else:
        response: Response = await client.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(markup=response.text, features="html.parser")
        if soup.find(name="title") is not None and soup.title and not None and soup.title.string is not None:
            title: str = soup.title.string
            if title is not None:
                text += f"Title: {title}\n\nURL source: {url}\n\nMarkdown content:\n\n"
        elif soup.find(name="h1") is not None and soup.h1 and not None and soup.h1.string is not None:
            title: str = soup.h1.string
            if title is not None:
                text += f"Title: {title}\n\nURL source: {url}\n\nMarkdown content:\n\n"                
        text += md(soup=soup, strip=["script", "style"], bullets="-", codeblock="```", heading_style="ATX")
    return text


# Create a named server
mcp = FastMCP(name="Get clean url via MCP", dependencies=["toml"])

@mcp.tool()
async def clean_url(url: str) -> str:
    """Get clean url via MCP."""
    result: str = await get_clean_url(url=url)
    return result

if __name__ == "__main__":
    import asyncio

    print(asyncio.run(main=clean_url(url=sys.argv[1])))
