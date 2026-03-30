# 🌽 Personal MCP Intelligence Platform v2.0

A high-performance Model Context Protocol (MCP) server integrated with a Django-powered analytics dashboard. Features the **Corn Intelligence** toolset for comprehensive AI interaction tracking, AST code analysis, and real-time token efficiency metrics.

## 🚀 Key Features

### 1. Intelligence Dashboard
- **Real-time Monitoring**: Every tool call is logged with latency, token usage, and efficiency metrics.
- **Auto-Reload**: Dashboard refreshes every 15 seconds with a visual countdown indicator.
- **Token Analytics**: Visualize direct token costs vs. context savings with efficiency scoring.
- **Session Explorer**: Browse and drill into past sessions at `/sessions/`.

### 2. Corn Intelligence Toolset (v2.0) — 19 Tools

| # | Tool | Category | Description |
|---|---|---|---|
| 1 | `corn_health` | Core | System health — CPU, RAM, uptime |
| 2 | `corn_session_start` | Core | Begin a tracked work session |
| 3 | `corn_session_end` | Core | End session with summary |
| 4 | `corn_memory_store` | Memory | Store agent memory with tags |
| 5 | `corn_memory_search` | Memory | Keyword search over memories |
| 6 | `corn_knowledge_store` | Knowledge | Store a shared knowledge item |
| 7 | `corn_knowledge_search` | Knowledge | Semantic search over knowledge base |
| 8 | `corn_code_read` | Code | Read raw source code from any file path |
| 9 | `corn_detect_changes` | Code | Uncommitted git changes cross-referenced with AST graph |
| 10 | `corn_list_repos` | Code | List indexed repositories with symbol counts (auto-indexes on first call) |
| 11 | `corn_code_search` | Code | Hybrid AST symbol search by name |
| 12 | `corn_code_context` | Code | 360° symbol view: callers, callees, hierarchy |
| 13 | `corn_code_impact` | Code | Blast radius analysis — which files depend on a given file |
| 14 | `corn_cypher` | Code | Graph-style queries: `(a)-[:CALLS]->(b)` |
| 15 | `corn_tool_stats` | Analytics | Usage analytics over last 50 tool calls |
| 16 | `corn_quality_report` | Quality | Submit a 3-dimension quality report (Clarity/Efficiency/Security) |
| 17 | `corn_record_conversation` | Analytics | Log raw conversation token usage to Dashboard |
| 18 | `corn_plan_quality` | Quality | Score a plan text against 8 quality criteria (must ≥80%) |
| 19 | `corn_changes` | Analytics | Check recent git commits by agents (`git log -n 5`) |

### 3. AST Code Intelligence Engine
- **Auto-Indexing**: `corn_list_repos` automatically scans and indexes Python source files on first call.
- **Symbol Graph**: Stores `Function`, `Class`, and `Method` nodes with `CALLS` / `INHERITS` relationships in MySQL.
- **Blast Radius**: `corn_code_impact` identifies all callers transitively affected by changes to a file.

### 4. Token Efficiency Metrics
- **Accurate Counting**: Heuristic blends character density and word count — `max(chars/4, words × 1.35)` — for reliable estimation across code and natural language.
- **Context Saved**: For search tools (`memory_search`, `knowledge_search`, `code_search`), tokens saved = total DB tokens − tokens returned. Reflects real context reduction.
- **Efficiency (%)**: `Saved / (Used + Saved)`. Aim for >80%!

## 🏛️ Architecture

```
IDE (Antigravity / Claude)
    │  stdio (MCP protocol)
    ▼
Docker: personal-mcp-web
    ├── Django MCP Server (run_mcp management command)
    │       └── 19 Corn Intelligence Tools
    ├── AST Indexer (mcp_server/utils/indexer.py)
    └── Django Dashboard (http://localhost:8000)
            └── Real-time Activity Log, Sessions, Token Analytics
    │
    ▼
Docker: mcp_mysql_db (MySQL 8)
    ├── Session, ToolLog
    ├── Memory, Knowledge
    └── Repository, Symbol, SymbolRelation, PlanQuality
```

## 🏃 Getting Started

1. **Launch Services**:
    ```bash
    docker-compose up -d
    ```

2. **Connect IDE** — add to your MCP config (`mcp_config.json`):
    ```json
    {
      "mcpServers": {
        "personal-mcp-v2": {
          "command": "/usr/local/bin/docker",
          "args": ["exec", "-i", "personal-mcp-web", "python", "manage.py", "run_mcp", "--verbosity", "0", "--no-color", "--skip-checks"]
        }
      }
    }
    ```

3. **Run Migrations** (first-time setup):
    ```bash
    docker exec personal-mcp-web python manage.py migrate
    ```

4. **Explore Dashboard**: [http://localhost:8000/](http://localhost:8000/)

## 🛠️ Development

**Apply new migrations after model changes:**
```bash
docker exec personal-mcp-web python manage.py makemigrations mcp_server
docker exec personal-mcp-web python manage.py migrate mcp_server
```

**Check Django config inside container:**
```bash
docker exec personal-mcp-web python manage.py check
```

**View live logs:**
```bash
docker logs -f personal-mcp-web
```

---
*Powered by Antigravity — Premium AI Engineering.*
