"""Init file."""

import sys

from mcp_clean_url.server import get_clean_url


def main() -> None:
    """Function not used."""
    import asyncio

    print(asyncio.run(main=get_clean_url(url=sys.argv[1])))
