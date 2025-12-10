# Multi-Agent Customer Support System (A2A + MCP)

This project implements a multi-agent customer support system using:

- **Google ADK** for agent orchestration
- **A2A (Agent-to-Agent)** protocol for inter-agent communication
- **MCP (Model Context Protocol)** for tool-based access to a SQLite customer support database

There are three main logical parts:

1. **MCP Server** – exposes tools like `get_customer`, `list_customers`, `update_customer`, `create_ticket`, and `get_customer_history` over a SQLite DB.
2. **Agents** – a Customer Data Agent and a Support Agent, both using MCP tools.
3. **Router** – a simple router agent that calls both agents in sequence and returns a cleaned response with an A2A log.

The `notebooks/genai_kathy.ipynb` notebook contains an end-to-end Colab version of this system.  
The `src/` directory contains a modular, script-based version suitable for GitHub and reuse.

## Repository Structure

```text
multi-agent-customer-support-system/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── genai_kathy.ipynb
├── src/
│   ├── database_setup.py
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── tools.py
│   ├── agents/
│   │   ├── customer_data_agent.py
│   │   ├── support_agent.py
│   │   └── router_agent.py
│   ├── a2a/
│   │   ├── serve_agents.py
│   │   ├── agent_cards.py
│   │   └── build_app.py
│   ├── runner/
│   │   ├── router_runner.py
│   │   └── utils.py
│   └── config/
│       └── settings.py
├── tests/
│   └── test_router.py
└── diagrams/
    └── architecture.png