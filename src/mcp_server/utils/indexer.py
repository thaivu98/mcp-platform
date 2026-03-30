import ast
import os
from django.utils import timezone
from mcp_server.models import Repository, Symbol, SymbolRelation

class CornIndexer:
    def __init__(self, repo_name, repo_path):
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.repo_obj = None
        self.symbols_map = {} # (file_path, symbol_name) -> Symbol object

    def get_or_create_repo(self):
        repo, created = Repository.objects.get_or_create(
            name=self.repo_name,
            defaults={'path': self.repo_path}
        )
        self.repo_obj = repo
        return repo

    def index_project(self):
        self.get_or_create_repo()
        # Clean existing symbols for this repo to re-index
        self.repo_obj.symbols.all().delete()
        
        python_files = []
        for root, dirs, files in os.walk(self.repo_path):
            if 'venv' in root or '__pycache__' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        # First pass: Extract all symbols
        for file_path in python_files:
            self.extract_symbols(file_path)

        # Second pass: Extract relations
        for file_path in python_files:
            self.extract_relations(file_path)

        # Update metadata
        self.repo_obj.last_indexed = timezone.now()
        self.repo_obj.symbol_count = self.repo_obj.symbols.count()
        self.repo_obj.save()
        return self.repo_obj.symbol_count

    def extract_symbols(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except Exception:
            return

        rel_path = os.path.relpath(file_path, self.repo_path)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbol_type = 'class' if isinstance(node, ast.ClassDef) else 'function'
                name = node.name
                
                # Simple full name (module.name)
                module_name = rel_path.replace('.py', '').replace(os.sep, '.')
                full_name = f"{module_name}.{name}"
                
                symbol = Symbol.objects.create(
                    repository=self.repo_obj,
                    name=name,
                    full_name=full_name,
                    symbol_type=symbol_type,
                    file_path=rel_path,
                    line_number=node.lineno,
                    docstring=ast.get_docstring(node) or ""
                )
                self.symbols_map[(rel_path, name)] = symbol

    def extract_relations(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except Exception:
            return

        rel_path = os.path.relpath(file_path, self.repo_path)

        # Find which symbol we are currently in
        class RelationVisitor(ast.NodeVisitor):
            def __init__(self, indexer, file_path, symbols_map):
                self.indexer = indexer
                self.file_path = file_path
                self.symbols_map = symbols_map
                self.current_symbol = None

            def visit_ClassDef(self, node):
                prev_symbol = self.current_symbol
                self.current_symbol = self.symbols_map.get((self.file_path, node.name))
                self.generic_visit(node)
                self.current_symbol = prev_symbol

            def visit_FunctionDef(self, node):
                prev_symbol = self.current_symbol
                self.current_symbol = self.symbols_map.get((self.file_path, node.name))
                self.generic_visit(node)
                self.current_symbol = prev_symbol

            def visit_AsyncFunctionDef(self, node):
                self.visit_FunctionDef(node)

            def visit_Call(self, node):
                if self.current_symbol and isinstance(node.func, ast.Name):
                    target_name = node.func.id
                    # Search for target in same file or common symbols
                    # This is a VERY simplified resolver
                    target_symbol = None
                    for (f, n), sym in self.symbols_map.items():
                        if n == target_name:
                            target_symbol = sym
                            break
                    
                    if target_symbol:
                        SymbolRelation.objects.get_or_create(
                            from_symbol=self.current_symbol,
                            to_symbol=target_symbol,
                            relation_type='calls'
                        )
                self.generic_visit(node)

        visitor = RelationVisitor(self, rel_path, self.symbols_map)
        visitor.visit(tree)
