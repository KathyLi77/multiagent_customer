"""
AgentCard definitions for A2A services.
"""

from a2a.types import AgentCard, AgentSkill, AgentCapabilities, TransportProtocol

from src.config.settings import CUSTOMER_AGENT_PORT, SUPPORT_AGENT_PORT


def get_customer_agent_card() -> AgentCard:
    """
    Define the AgentCard for the Customer Data Agent.
    """
    return AgentCard(
        name="Customer Data Agent",
        url=f"http://127.0.0.1:{CUSTOMER_AGENT_PORT}",
        description="Reads and updates customer and ticket data via MCP tools.",
        version="1.0",
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=["text/plain"],
        default_output_modes=["application/json"],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id="customer_data_ops",
                name="Customer Data Operations",
                description="Fetches and updates customer/ticket data using MCP tools.",
                tags=["database", "customers", "tickets"],
                examples=[
                    "Get customer information for ID 5",
                    "List active customers",
                    "Show ticket history for ID 12345",
                ],
            )
        ],
    )


def get_support_agent_card() -> AgentCard:
    """
    Define the AgentCard for the Support Agent.
    """
    return AgentCard(
        name="Support Agent",
        url=f"http://127.0.0.1:{SUPPORT_AGENT_PORT}",
        description="Explains issues, triages priority, and suggests next steps.",
        version="1.0",
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id="support_operations",
                name="Support Operations",
                description="Explains issues, investigates history, escalates tickets.",
                tags=["support", "billing", "workflow"],
                examples=[
                    "Explain why I was charged twice",
                    "Help me update contact info",
                    "Open a high priority ticket",
                ],
            )
        ],
    )