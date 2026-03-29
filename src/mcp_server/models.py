from django.db import models
from django.utils import timezone

class Session(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='active') # active, completed, cancelled
    total_tokens_used = models.IntegerField(default=0)
    total_tokens_saved = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.status})"

class ToolLog(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='tool_logs', null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    tool_name = models.CharField(max_length=100)
    input_data = models.TextField(blank=True)
    output_data = models.TextField(blank=True)
    latency_ms = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='success') # success, error
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    tokens_saved = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.timestamp} - {self.tool_name}"

class Memory(models.Model):
    content = models.TextField()
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    importance = models.IntegerField(default=1) # 1-5 level

    def __str__(self):
        return f"Memory: {self.content[:50]}..."

class Knowledge(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100, default='general')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
