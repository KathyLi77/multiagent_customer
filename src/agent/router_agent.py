"""
Router agent that orchestrates the Customer Data Agent and Support Agent.
"""

from google.adk.agents import SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

from src.config.settings import CUSTOMER_AGENT_PORT, SUPPORT_AGENT_PORT


def build_remote_customer_agent() -> RemoteA2aAgent:
    """
    Build RemoteA2aAgent pointing to the Customer Data Agent A2A endpoint.
    """
    url = f"http://127.0.0.1:{CUSTOMER_AGENT_PORT}{AGENT_CARD_WELL_KNOWN_PATH}"
    return RemoteA2aAgent(
        name="customer_data_remote",
        description="Remote A2A customer data specialist.",
        agent_card=url,
    )


def build_remote_support_agent() -> RemoteA2aAgent:
    """
    Build RemoteA2aAgent pointing to the Support Agent A2A endpoint.
    """
    url = f"http://127.0.0.1:{SUPPORT_AGENT_PORT}{AGENT_CARD_WELL_KNOWN_PATH}"
    return RemoteA2aAgent(
        name="support_remote",
        description="Remote A2A support and explanation specialist.",
        agent_card=url,
    )


def build_router_agent() -> SequentialAgent:
    """
    Create the router as a SequentialAgent that runs:
    1) Customer Data Agent
    2) Support Agent
    """
    remote_customer = build_remote_customer_agent()
    remote_support = build_remote_support_agent()

    router = SequentialAgent(
        name="router_agent",
        sub_agents=[remote_customer, remote_support],
    )
    return router