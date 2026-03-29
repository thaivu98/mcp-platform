# 🌽 Personal MCP Intelligence Platform

A high-performance Model Context Protocol (MCP) server integrated with a Django-powered analytics dashboard. Designed to provide deep insights into AI tool interactions, memory efficiency, and token economics.

## 🚀 Key Features

- **Intelligence Dashboard**: Real-time monitoring of every AI tool call, including inputs, outputs, and latency.
- **Token Intelligence**: 
  - **Usage Tracking**: Automatically estimates and logs token consumption for all MCP activities.
  - **Context Efficiency**: New "Context Saved" metric that visualizes the savings achieved by using MCP-based targeted retrieval instead of context-stuffing.
  - **Chat Tracking**: Integrated `record_conversation` tool to include general chat costs in your analytics.
- **Session Explorer**: Dedicated page to manage and analyze past interactions with full history, search, and efficiency metrics.
- **Memory & Knowledge**: Persistent storage for long-term AI memory and structured knowledge base access.
- **Automated Lifecycle**: Self-cleaning session logic that detects and resolves stale connections on server restart.

## 🛠 Tech Stack

- **Backend**: Django 5.0+, Python 3.12
- **Database**: MySQL 8.0 (Dockerized)
- **MCP Framework**: FastMCP
- **UI/UX**: TailwindCSS with specialized Glassmorphism & Gold/Emerald accents.

## 🏃 Running the Platform

1.  **Start Services**:
    ```bash
    docker-compose up -d
    ```
2.  **Access Dashboard**: Open `http://localhost:8000` in your browser.
3.  **MCP Connection**: Use the following command in your MCP-compatible IDE:
    ```bash
    docker exec -i personal-mcp-web python manage.py run_mcp
    ```

## 📊 Analytics & Insights

The metrics you see on the dashboard help you understand your AI usage:
- **Tokens Used**: Direct cost associated with the session.
- **Context Saved**: How much data was managed via MCP instead of sent to the LLM.
- **Efficiency (%)**: A ratio calculated by `Saved / (Used + Saved)`. The higher this number, the more optimized your AI context management is!

---
*Created by Antigravity - Your Agentic AI Coding Assistant.*
