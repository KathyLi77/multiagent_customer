# Multi-Agent Customer Support System (A2A + MCP)

This repository implements a complete **multi-agent customer support system** using:

- **Google ADK (Agent Development Kit)**
- **A2A (Agent-to-Agent communication)**
- **MCP (Model Context Protocol)** with FastMCP
- **SQLite** for customer/ticket storage
- **OpenAI GPT models** via LiteLLM
- A central **Router Agent** that coordinates two remote A2A agents

This project showcases a real-world, production-like enterprise customer-support automation pipeline.

## 📂 Project Structure

multiagent_customer/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── genai_kathy.ipynb
│
├── src/
│   ├── database_setup.py
│   │
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── tools.py
│   │
│   ├── agents/
│   │   ├── customer_data_agent.py
│   │   ├── support_agent.py
│   │   └── router_agent.py
│   │
│   ├── a2a/
│   │   ├── serve_agents.py
│   │   ├── agent_cards.py
│   │   └── build_app.py
│   │
│   ├── runner/
│   │   ├── router_runner.py
│   │   └── utils.py
│   │
│   └── config/
│       └── settings.py
│
├── tests/
│   └── test_router.py
│
└── diagrams/
    └── architecture.png

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/multiagent_customer.git
cd multiagent_customer
```

## 2️⃣ Create & Activate a Virtual Environment

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4️⃣ Configure Environment Variables

Create a file `.env` in the project root:

```
OPENAI_API_KEY=your_openai_key_here
```

## 5️⃣ Initialize the Database

```bash
python src/database_setup.py
```

## 6️⃣ Start the MCP Server

```bash
python src/mcp_server/server.py
```

## 7️⃣ Start the A2A Agents

```bash
python src/a2a/serve_agents.py
```

## 8️⃣ Run the Router Agent

```bash
python src/runner/router_runner.py
```

Example queries:

```
Get customer information for ID 5
I was charged twice, please help
I'm customer 12345 and need help upgrading my account
Open a high priority ticket for customer 12345
```

## 🧪 Run Tests

```bash
pytest tests/
```

## 📜 requirements.txt

```
google-adk[a2a]
mcp
litellm
uvicorn
nest_asyncio
python-dotenv
requests
google-genai
fastapi
pytest
```

MIT License.