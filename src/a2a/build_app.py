"""
Utility to wrap google-adk LLM agents into A2A-compatible Starlette apps.
"""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.a2a.executor.a2a_agent_executor import (
    A2aAgentExecutor,
    A2aAgentExecutorConfig,
)

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from a2a.types import AgentCard


def build_a2a_app(agent, card: AgentCard):
    """
    Build an A2AStarletteApplication for the given agent and AgentCard.
    """
    runner = Runner(
        app_name=agent.name,
        agent=agent,
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
        artifact_service=InMemoryArtifactService(),
    )

    executor = A2aAgentExecutor(
        runner=runner,
        config=A2aAgentExecutorConfig(),
    )

    handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=None,
    )

    # build() returns a Starlette app
    return A2AStarletteApplication(agent_card=card, http_handler=handler).build()