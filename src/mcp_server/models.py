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

class Repository(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    last_indexed = models.DateTimeField(null=True, blank=True)
    symbol_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Symbol(models.Model):
    SYMBOL_TYPES = (
        ('class', 'Class'),
        ('function', 'Function'),
        ('method', 'Method'),
        ('module', 'Module'),
    )
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='symbols')
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=1024)
    symbol_type = models.CharField(max_length=20, choices=SYMBOL_TYPES)
    file_path = models.CharField(max_length=1024)
    line_number = models.IntegerField()
    docstring = models.TextField(blank=True)

    def __str__(self):
        return f"{self.symbol_type}: {self.full_name}"

class SymbolRelation(models.Model):
    RELATION_TYPES = (
        ('calls', 'Calls'),
        ('inherits', 'Inherits from'),
        ('contains', 'Contains'),
    )
    from_symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='outgoing_relations')
    to_symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='incoming_relations')
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPES)

    def __str__(self):
        return f"{self.from_symbol} --[{self.relation_type}]--> {self.to_symbol}"

class PlanQuality(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='plan_qualities')
    timestamp = models.DateTimeField(default=timezone.now)
    scores_json = models.TextField() # stores JSON with detailed scores
    average_score = models.FloatField()
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f"Quality: {self.average_score}% in {self.session.name}"
