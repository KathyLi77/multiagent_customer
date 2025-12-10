"""
Customer Data Agent definition.

This agent focuses on database interactions via MCP tools.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from src.config.settings import MCP_URL


def build_customer_data_agent() -> LlmAgent:
    """
    Create and configure the Customer Data Agent with MCP tools.
    """
    model = LiteLlm(model="gpt-4o-mini")

    from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams

    mcp_toolset = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(url=MCP_URL)
    )

    return LlmAgent(
        model=model,
        name="customer_data_agent",
        description="Agent dedicated to reading and updating customer and ticket data via MCP tools.",
        tools=[mcp_toolset],
        instruction="""
You are the Customer Data Agent.

You interact with the customer_support.db database via MCP tools:

- get_customer(id)
- list_customers(status, limit)
- update_customer(id, fields)
- create_ticket(id, issue, priority)
- get_customer_history(id)

Your job:
- Decide which MCP tools to call and with what arguments.
- Summarize the results in a clear, compact format that other agents can reuse.
- For write operations, explain which fields were changed.

If important identifiers (like id) are missing, state that clearly.
""",
    )