from pathlib import Path
import ast, ctypes, hashlib, json

ROOT = Path(__file__).resolve().parent
tree = ast.parse((ROOT / 'read_inputs.py').read_text(encoding='utf-8'))
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'read_shared')
exec(compile(ast.Module(body=[function], type_ignores=[]), '<shared-read-only-helper>', 'exec'))
records = json.loads((ROOT / 'input-manifest.json').read_text(encoding='utf-8'))
result = {}
for key, record in records.items():
    digest = hashlib.sha256(read_shared(Path(record['source']))).hexdigest()
    assert digest == record['sha256'], 'Selected source changed during review: ' + key
    result[key] = {'unchanged': True, 'sha256': digest}
(ROOT / 'originals-after-review.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
