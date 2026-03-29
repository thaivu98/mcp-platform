# 🌽 Personal MCP Intelligence Platform (Django + MySQL Edition)

> Surgical code intelligence. Semantic memory. Analytics Dashboard.  
> **Stop burning tokens.** Start managing your AI tools with a premium personal hub.

---

## 🌟 Overview

**Personal MCP** is a lightweight yet powerful Model Context Protocol (MCP) server and real-time analytics dashboard. Inspired by CornMCP but rebuilt for Python/Django enthusiasts, it gives your AI agents (Cursor, Claude, Antigravity) a structured memory and a high-end monitoring interface.

### Key Features
- 🧠 **Persistent Memory** — AI remembers context across sessions via MySQL.
- 📊 **Premium Dashboard** — Glassmorphic, dark-mode UI to track every tool call and latency.
- 📋 **Session Tracking** — Group activities into sessions to measure "token efficiency".
- 💾 **Native MySQL 8** — Industrial-grade data persistence via Docker.
- ⚡ **FastMCP Engine** — Built on top of Anthropic's high-level Python SDK.

---

## 🏗️ Project Structure

```text
personal-mcp-django/
├── docker-compose.yml    # Orchestrates MySQL 8 & Django Web
├── Dockerfile            # Python 3.12 environment with MCP SDK
├── requirements.txt      # Django, mysqlclient, mcp...
├── mysql_data/           # Persistent MySQL storage (Mounted volume)
└── src/                  # Django Source Code
    ├── manage.py
    ├── mymcp/            # Core Settings & URLs
    ├── mcp_server/       # MCP logic & Database Models
    │   ├── management/commands/run_mcp.py  # The MCP Server Entry Point
    │   └── models.py     # SQL Schema (Sessions, Logs, Memory, Knowledge)
    └── dashboard/        # Analytics UI (Glassmorphic Templates)
        ├── templates/    # Tailwind CSS + Django Templates
        └── views.py      # Real-time telemetry processing
```

---

## 🚀 Getting Started

### Prerequisites
- **Docker** & **Docker Compose** installed.
- An IDE that supports MCP (Cursor, VS Code with Antigravity, etc.).

### 1. Installation
Clone the repository and spin up the containers:

```bash
cd personal-mcp-django
docker compose up -d
```

### 2. Initialization
Run migrations to set up the MySQL schema and create a superuser for the Admin panel:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### 3. Accessing the Platform
- **Dashboard:** [http://localhost:8000/](http://localhost:8000/)
- **Django Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/) (Manage your Knowledge/Memory manually)
- **MySQL Direct:** `localhost:3307` (See `docker-compose.yml` for credentials)

---

## 🤖 IDE Integration (MCP Config)

To connect your AI agent to this server, add the following to your MCP configuration file (e.g., `antigravity-mcp.json` or Cursor Settings):

```json
{
  "mcpServers": {
    "personal-mcp": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "personal-mcp-web",
        "python",
        "manage.py",
        "run_mcp"
      ]
    }
  }
}
```

---

## 🔧 Available Tools

| Tool | Category | Description |
|---|---|---|
| `session_start` | Session | Begins a tracked work session for the agent. |
| `session_end` | Session | Ends session and logs a final summary to MySQL. |
| `memory_store` | Memory | Saves content/snippets for cross-task recall. |
| `memory_search` | Memory | Keyword search across all stored agent memories. |
| `knowledge_list` | Knowledge | Lists all pre-defined bug-fix patterns or rules. |
| `get_system_stats`| System | Returns CPU/RAM usage of the host server. |

---

## 🎨 Dashboard Aesthetics
The system uses a custom **Glassmorphism** design system:
- **Dark Mode:** Deep slate palette (`slate-950`).
- **Gradients:** Amber/Gold accents for high-end intelligence feel.
- **Responsiveness:** Built with Tailwind CSS for seamless viewing on dev monitors.

---

## 📄 License
MIT © 2026 Personal MCP Intelligence Platform.
