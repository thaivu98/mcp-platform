import os
import json
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from mcp.server.fastmcp import FastMCP
from mcp_server.models import Session, ToolLog, Memory, Knowledge
import psutil

class Command(BaseCommand):
    help = 'Runs the Personal MCP Server'

    def handle(self, *args, **options):
        import sys
        import contextlib

        # Redirect all stdout to stderr during setup to avoid polluting the MCP stream
        with contextlib.redirect_stdout(sys.stderr):
            # Initialize FastMCP server
            mcp = FastMCP("PersonalMCP")

            # Global storage for current session
            current_session_id = None

            def log_tool_call(tool_name, input_params, output_data, latency_ms, status='success'):
                nonlocal current_session_id
                session = None
                if current_session_id:
                    session = Session.objects.filter(id=current_session_id).first()
                
                ToolLog.objects.create(
                    session=session,
                    tool_name=tool_name,
                    input_data=json.dumps(input_params, indent=2),
                    output_data=str(output_data),
                    latency_ms=latency_ms,
                    status=status
                )

            @mcp.tool()
            def session_start(name: str) -> str:
                """Starts a new work session to track activities."""
                start_time = time.time()
                nonlocal current_session_id
                session = Session.objects.create(name=name, status='active')
                current_session_id = session.id
                
                res = f"Session '{name}' started (ID: {session.id})."
                log_tool_call("session_start", {"name": name}, res, int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            def session_end(summary: str) -> str:
                """Ends the current work session and saves a summary."""
                start_time = time.time()
                nonlocal current_session_id
                if not current_session_id:
                    return "No active session to end."
                
                session = Session.objects.get(id=current_session_id)
                session.end_time = timezone.now()
                session.summary = summary
                session.status = 'completed'
                session.save()
                
                res = f"Session '{session.name}' ended. Summary saved."
                log_tool_call("session_end", {"summary": summary}, res, int((time.time() - start_time) * 1000))
                current_session_id = None
                return res

            @mcp.tool()
            def memory_store(content: str, tags: str = "") -> str:
                """Stores a piece of information for later retrieval."""
                start_time = time.time()
                mem = Memory.objects.create(content=content, tags=tags)
                res = f"Memory stored (ID: {mem.id}). content: {content[:30]}..."
                log_tool_call("memory_store", {"content": content, "tags": tags}, res, int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            def memory_search(query: str) -> str:
                """Searches stored memories by keywords."""
                start_time = time.time()
                mems = Memory.objects.filter(content__icontains=query) | Memory.objects.filter(tags__icontains=query)
                
                results = []
                for m in mems:
                    results.append(f"[{m.created_at.strftime('%Y-%m-%d %H:%M')}] Tags: {m.tags}\nContent: {m.content}")
                
                res = "\n---\n".join(results) if results else "No memories found matching that query."
                log_tool_call("memory_search", {"query": query}, f"Found {len(results)} items", int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            def knowledge_list() -> str:
                """Lists all available knowledge items."""
                start_time = time.time()
                items = Knowledge.objects.all()
                res_list = [f"- {i.title} (ID: {i.id}, Category: {i.category})" for i in items]
                res = "Knowledge Base Items:\n" + "\n".join(res_list) if res_list else "Knowledge base is empty."
                log_tool_call("knowledge_list", {}, f"Listed {len(items)} items", int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            def get_system_stats() -> str:
                """Retrieves basic system resource usage."""
                start_time = time.time()
                cpu = psutil.cpu_percent()
                mem = psutil.virtual_memory().percent
                res = f"System Stats: CPU: {cpu}%, Memory: {mem}%"
                log_tool_call("get_system_stats", {}, res, int((time.time() - start_time) * 1000))
                return res


        # Run the server outside of the stdout redirect block
        mcp.run()


