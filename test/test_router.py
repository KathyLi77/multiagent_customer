"""
Very simple smoke test for the router runner.

This assumes the MCP server and A2A agents are already running.
For full integration tests, run src/runner/router_runner.py instead.
"""

import pytest

from google.adk.runners import InMemoryRunner

from src.agents.router_agent import build_router_agent
from src.runner.router_runner import run_router
from src.config.settings import APP_NAME, USER_ID

import asyncio
from google.genai import types as genai_types


def create_runner_and_session():
    router_agent = build_router_agent()
    runner = InMemoryRunner(agent=router_agent, app_name=APP_NAME)

    loop = asyncio.get_event_loop()
    session = loop.run_until_complete(
        runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="test-session-001",
        )
    )
    return runner, session.id


@pytest.mark.skip(reason="Requires MCP server + A2A agents running")
def test_router_basic():
    runner, session_id = create_runner_and_session()
    text = run_router(runner, session_id, "Get customer information for ID 5")
    assert "A2A LOG" in text