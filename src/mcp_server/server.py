"""
FastMCP server that exposes DB tools for the customer support system.
"""

import threading
import time
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from src.config.settings import DB_PATH, MCP_HOST, MCP_PORT, MCP_PATH
from src.mcp_server import tools


def create_mcp() -> FastMCP:
    """
    Build and return a FastMCP instance with registered tools.
    """
    mcp = FastMCP(
        name="customer_support_mcp",
        instructions="MCP tools for customer + ticket DB.",
    )

    @mcp.tool()
    def get_customer(id: int) -> Dict[str, Any]:
        return tools.get_customer(DB_PATH, id)

    @mcp.tool()
    def list_customers(
        status: str | None = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        return tools.list_customers(DB_PATH, status, limit)

    @mcp.tool()
    def update_customer(id: int, fields: Dict[str, Any]) -> Dict[str, Any]:
        return tools.update_customer(DB_PATH, id, fields)

    @mcp.tool()
    def create_ticket(id: int, issue: str, priority: str = "medium") -> Dict[str, Any]:
        return tools.create_ticket(DB_PATH, id, issue, priority)

    @mcp.tool()
    def get_customer_history(id: int) -> Dict[str, Any]:
        return tools.get_customer_history(DB_PATH, id)

    return mcp


def run_mcp_blocking():
    """
    Run the MCP server in the foreground.
    """
    from src.config.settings import MCP_HOST, MCP_PORT, MCP_PATH

    mcp = create_mcp()
    print(f"Starting MCP server at http://{MCP_HOST}:{MCP_PORT}{MCP_PATH}")
    mcp.run(transport="streamable-http")


def run_mcp_in_background():
    """
    Helper to start MCP server in a background thread.
    """
    thread = threading.Thread(target=run_mcp_blocking, daemon=True)
    thread.start()
    time.sleep(3)
    print("✅ MCP server should now be running.")


if __name__ == "__main__":
    run_mcp_blocking()