"""
Support Agent definition.

This agent focuses on explaining situations, triaging issues,
and suggesting next steps while optionally using MCP tools.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from src.config.settings import MCP_URL


def build_support_agent() -> LlmAgent:
    """
    Create and configure the Support Agent with MCP tools.
    """
    model = LiteLlm(model="gpt-4o-mini")

    from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams

    mcp_toolset = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(url=MCP_URL)
    )

    return LlmAgent(
        model=model,
        name="support_agent",
        description="Agent that explains account situations and suggests next steps for the user.",
        tools=[mcp_toolset],
        instruction="""
You are the Support Agent.

You focus on:
- Explaining account status and history in simple language.
- Suggesting reasonable next actions (updates, escalations, tickets).
- Deciding whether an issue feels low, medium, or high priority.

You may also call MCP tools directly when it helps you reason about the case.
Always speak in a friendly, concise, customer-facing tone.
""",
    )