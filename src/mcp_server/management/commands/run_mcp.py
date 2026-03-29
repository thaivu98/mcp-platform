import os
import json
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from mcp.server.fastmcp import FastMCP
from mcp_server.models import Session, ToolLog, Memory, Knowledge
import psutil
from asgiref.sync import sync_to_async

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

            # Cleanup stale sessions on startup
            # Any session marked active when the server starts is stale (from previous run)
            stale_count = Session.objects.filter(status='active').update(status='completed')
            if stale_count > 0:
                print(f"Cleaned up {stale_count} stale sessions.")

            def calculate_tokens(text):
                if not text: return 0
                return len(str(text)) // 4

            async def log_tool_call(tool_name, input_params, output_data, latency_ms, status='success', tokens_saved=0):
                nonlocal current_session_id
                session = None
                
                t_in = calculate_tokens(json.dumps(input_params))
                t_out = calculate_tokens(output_data)
                
                if current_session_id:
                    session = await sync_to_async(Session.objects.filter(id=current_session_id).first)()
                    if session:
                        session.total_tokens_used += (t_in + t_out)
                        session.total_tokens_saved += tokens_saved
                        await sync_to_async(session.save)()
                
                await sync_to_async(ToolLog.objects.create)(
                    session=session,
                    tool_name=tool_name,
                    input_data=json.dumps(input_params, indent=2),
                    output_data=str(output_data),
                    latency_ms=latency_ms,
                    status=status,
                    tokens_input=t_in,
                    tokens_output=t_out,
                    tokens_saved=tokens_saved
                )

            @mcp.tool()
            async def session_start(name: str) -> str:
                """Starts a new work session to track activities."""
                start_time = time.time()
                nonlocal current_session_id
                session = await sync_to_async(Session.objects.create)(name=name, status='active')
                current_session_id = session.id
                
                res = f"Session '{name}' started (ID: {session.id})."
                await log_tool_call("session_start", {"name": name}, res, int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            async def session_end(summary: str) -> str:
                """Ends the current work session and saves a summary."""
                start_time = time.time()
                nonlocal current_session_id
                if not current_session_id:
                    return "No active session to end."
                
                session = await sync_to_async(Session.objects.get)(id=current_session_id)
                session.end_time = timezone.now()
                session.summary = summary
                session.status = 'completed'
                await sync_to_async(session.save)()
                
                res = f"Session '{session.name}' ended. Summary saved."
                await log_tool_call("session_end", {"summary": summary}, res, int((time.time() - start_time) * 1000))
                current_session_id = None
                return res

            @mcp.tool()
            async def memory_store(content: str, tags: str = "") -> str:
                """Stores a piece of information for later retrieval."""
                start_time = time.time()
                mem = await sync_to_async(Memory.objects.create)(content=content, tags=tags)
                res = f"Memory stored (ID: {mem.id}). content: {content[:30]}..."
                await log_tool_call("memory_store", {"content": content, "tags": tags}, res, int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            async def memory_search(query: str) -> str:
                """Searches stored memories by keywords."""
                start_time = time.time()
                mems = await sync_to_async(list)(Memory.objects.filter(content__icontains=query) | Memory.objects.filter(tags__icontains=query))
                
                results = []
                for m in mems:
                    results.append(f"[{m.created_at.strftime('%Y-%m-%d %H:%M')}] Tags: {m.tags}\nContent: {m.content}")
                
                res = "\n---\n".join(results) if results else "No memories found matching that query."
                t_saved = calculate_tokens(res) if results else 0
                await log_tool_call("memory_search", {"query": query}, f"Found {len(results)} items", int((time.time() - start_time) * 1000), tokens_saved=t_saved)
                return res

            @mcp.tool()
            async def knowledge_list() -> str:
                """Lists all available knowledge items."""
                start_time = time.time()
                items = await sync_to_async(list)(Knowledge.objects.all())
                res_list = [f"- {i.title} (ID: {i.id}, Category: {i.category})" for i in items]
                res = "Knowledge Base Items:\n" + "\n".join(res_list) if res_list else "Knowledge base is empty."
                await log_tool_call("knowledge_list", {}, f"Listed {len(items)} items", int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            async def get_system_stats() -> str:
                """Retrieves basic system resource usage."""
                start_time = time.time()
                cpu = psutil.cpu_percent()
                mem = psutil.virtual_memory().percent
                res = f"System Stats: CPU: {cpu}%, Memory: {mem}%"
                await log_tool_call("get_system_stats", {}, res, int((time.time() - start_time) * 1000))
                return res

            @mcp.tool()
            async def record_conversation(tokens_input: int, tokens_output: int) -> str:
                """Records the token usage of the current chat interaction."""
                start_time = time.time()
                await log_tool_call("conversation_chat", {"t_in": tokens_input, "t_out": tokens_output}, "Recorded successfully.", int((time.time() - start_time) * 1000))
                return f"Logged {tokens_input + tokens_output} tokens to Dashboard."


        # Run the server outside of the stdout redirect block
        mcp.run()


