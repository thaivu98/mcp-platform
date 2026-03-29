from django.shortcuts import render, get_object_or_404
from mcp_server.models import Session, ToolLog, Memory, Knowledge
from django.db.models import Sum, Count

def index(request):
    sessions = Session.objects.all().order_by('-start_time')[:10]
    total_logs = ToolLog.objects.count()
    recent_logs = ToolLog.objects.all().order_by('-timestamp')[:20]
    
    context = {
        'sessions': sessions,
        'total_logs': total_logs,
        'recent_logs': recent_logs,
        'title': 'MCP Central Dashboard'
    }
    return render(request, 'dashboard/index.html', context)

def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)
    logs = session.tool_logs.all().order_by('timestamp')
    
    context = {
        'session': session,
        'logs': logs,
        'title': f'Session: {session.name}'
    }
    return render(request, 'dashboard/session_detail.html', context)
