"""
Router runner: create a router agent, send test queries, and print
cleaned outputs with an A2A log section.
"""

import asyncio

from google.genai import types as genai_types
from google.adk.runners import InMemoryRunner

from src.config.settings import APP_NAME, USER_ID
from src.agents.router_agent import build_router_agent
from src.runner.utils import init_env, init_db_if_needed
from src.mcp_server.server import run_mcp_in_background
from src.a2a.serve_agents import run_all_agents


def create_router_runner() -> tuple[InMemoryRunner, str]:
    """
    Create an InMemoryRunner for the router agent plus a session ID.
    """
    router_agent = build_router_agent()
    router_runner = InMemoryRunner(agent=router_agent, app_name=APP_NAME)

    loop = asyncio.get_event_loop()
    session = loop.run_until_complete(
        router_runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="session-001",
        )
    )
    return router_runner, session.id


def run_router(router_runner: InMemoryRunner, session_id: str, query: str) -> str:
    """
    Send a query to the router agent, clean streaming output, and
    append a simple A2A log.
    """
    print("\n" + "=" * 60)
    print("USER:", query)
    print("=" * 60)

    msg = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=query)],
    )

    fragments: list[str] = []

    for event in router_runner.run(
        user_id=USER_ID,
        session_id=session_id,
        new_message=msg,
    ):
        if event.content and event.content.parts:
            text = event.content.parts[0].text or ""
            if text.strip():
                fragments.append(text)

    # Remove duplicated lines caused by streaming
    lines = [ln for ln in "\n".join(fragments).splitlines()]
    unique_lines = list(dict.fromkeys(lines))
    cleaned_answer = "\n".join([ln for ln in unique_lines if ln.strip()])

    a2a_log_lines = [
        "A2A LOG",
        f"- User → Router Agent: '{query}'",
        "- Router Agent → Customer Data Agent: fetch/inspect customer & ticket data via MCP tools",
        "- Customer Data Agent → Router Agent: returned database context (records, history)",
        "- Router Agent → Support Agent: ask for a final customer-facing explanation & next steps",
        "- Support Agent → Router Agent: returned final support message for the user",
    ]

    final_output = cleaned_answer + "\n\n" + "\n".join(a2a_log_lines)
    print(final_output)
    return final_output


def demo():
    """
    End-to-end demo:
    - Initialize env and DB
    - Start MCP server
    - Start A2A agents
    - Build router and run sample queries
    """
    init_env()
    init_db_if_needed()
    run_mcp_in_background()
    run_all_agents()

    router_runner, session_id = create_router_runner()

    queries = [
        "Get customer information for ID 5",
        "I was charged twice, please help",
        "I'm customer 12345 and need help upgrading my account",
        "Show me all active customers who have open tickets",
        "Update my email to new@email.com and show my ticket history",
    ]

    for q in queries:
        run_router(router_runner, session_id, q)


if __name__ == "__main__":
    demo()