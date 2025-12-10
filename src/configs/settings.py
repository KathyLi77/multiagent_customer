"""
Global configuration for the multi-agent customer support system.
"""

import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# Path to the SQLite database
DB_PATH = os.getenv("DB_PATH", "customer_support.db")

# API key for OpenAI (used by LiteLlm through google-adk)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# MCP server config
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
MCP_PATH = os.getenv("MCP_PATH", "/mcp")
MCP_URL = f"http://{MCP_HOST}:{MCP_PORT}{MCP_PATH}"

# A2A agent ports
CUSTOMER_AGENT_PORT = int(os.getenv("CUSTOMER_AGENT_PORT", "8101"))
SUPPORT_AGENT_PORT = int(os.getenv("SUPPORT_AGENT_PORT", "8102"))

# Router runner config
APP_NAME = "customer_support_app"
USER_ID = "demo-user"
SESSION_ID = "session-001"