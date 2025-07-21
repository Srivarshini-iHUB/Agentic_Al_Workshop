import ast

def analyze_python_code(code: str) -> str:
    try:
        tree = ast.parse(code)
        issues = []

        if any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print' 
               for node in ast.walk(tree)):
            issues.append("⚠️ Found `print()` - Use logging in production.")

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append("⚠️ Found bare `except:` - Specify exception types.")

        return "✅ No syntax errors found. Code looks good!" if not issues else "Found issues:\n" + "\n".join(issues)
    
    except SyntaxError as e:
        return f"❌ Syntax Error: {e.msg} (Line {e.lineno})"
