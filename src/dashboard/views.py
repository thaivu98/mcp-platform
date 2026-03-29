from django.shortcuts import render, get_object_or_404
from mcp_server.models import Session, ToolLog, Memory, Knowledge
from django.db.models import Sum, Count

def index(request):
    sessions = Session.objects.all().order_by('-start_time')[:10]
    total_logs = ToolLog.objects.count()
    recent_logs = ToolLog.objects.all().order_by('-timestamp')[:20]
    
    total_tokens = ToolLog.objects.aggregate(
        total_in=Sum('tokens_input'),
        total_out=Sum('tokens_output'),
        total_saved=Sum('tokens_saved')
    )
    
    total_used = (total_tokens['total_in'] or 0) + (total_tokens['total_out'] or 0)
    total_saved = total_tokens['total_saved'] or 0
    
    efficiency = 0
    if (total_used + total_saved) > 0:
        efficiency = (total_saved / (total_used + total_saved)) * 100
    
    context = {
        'sessions': sessions,
        'total_logs': total_logs,
        'recent_logs': recent_logs,
        'total_used': total_used,
        'total_saved': total_saved,
        'efficiency': round(efficiency, 1),
        'title': 'MCP Intelligence Dashboard'
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

def session_list(request):
    query = request.GET.get('q', '')
    if query:
        sessions_list = Session.objects.filter(name__icontains=query).order_by('-start_time')
    else:
        sessions_list = Session.objects.all().order_by('-start_time')
    
    total_sessions = sessions_list.count()
    
    context = {
        'sessions': sessions_list,
        'query': query,
        'total_sessions': total_sessions,
        'title': 'Session Explorer'
    }
    return render(request, 'dashboard/sessions.html', context)
