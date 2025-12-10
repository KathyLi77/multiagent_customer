"""
Entrypoint to serve the two A2A agents (Customer Data + Support) via uvicorn.
"""

import threading
import time

import uvicorn

from src.agents.customer_data_agent import build_customer_data_agent
from src.agents.support_agent import build_support_agent
from src.a2a.agent_cards import get_customer_agent_card, get_support_agent_card
from src.a2a.build_app import build_a2a_app
from src.config.settings import CUSTOMER_AGENT_PORT, SUPPORT_AGENT_PORT


def serve_agent(agent, card, port: int):
    """
    Run one A2A agent service on the given port.
    """
    app = build_a2a_app(agent, card)
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
        log_level="warning",
    )


def run_all_agents():
    """
    Start both agents in background threads.
    """
    customer_agent = build_customer_data_agent()
    support_agent = build_support_agent()

    customer_card = get_customer_agent_card()
    support_card = get_support_agent_card()

    t1 = threading.Thread(
        target=serve_agent,
        args=(customer_agent, customer_card, CUSTOMER_AGENT_PORT),
        daemon=True,
    )
    t2 = threading.Thread(
        target=serve_agent,
        args=(support_agent, support_card, SUPPORT_AGENT_PORT),
        daemon=True,
    )

    t1.start()
    t2.start()

    # Give servers time to start
    time.sleep(5)
    print("✅ A2A agent services started.")
    print(f"  - Customer Data Agent: http://127.0.0.1:{CUSTOMER_AGENT_PORT}")
    print(f"  - Support Agent:       http://127.0.0.1:{SUPPORT_AGENT_PORT}")


if __name__ == "__main__":
    run_all_agents()