from backend.app.main import app
import json

schema = app.openapi()
paths = schema.get('paths', {})
print(f"Total OpenAPI paths: {len(paths)}")
backend_endpoints = []
for path, methods in sorted(paths.items()):
    for method, op in methods.items():
        if method.lower() not in ['head', 'options']:
            summary = op.get('summary') or op.get('operation_id') or ''
            backend_endpoints.append((method.upper(), path, summary))
            print(f"  {method.upper():6} {path:<50} ({summary})")

print(f"\nTotal Backend Route Operations: {len(backend_endpoints)}")
