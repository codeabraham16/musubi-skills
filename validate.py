#!/usr/bin/env python3
"""Valida index.json del catálogo de Musubi.

Comprueba:
  1. Esquema JSON (schema.json).
  2. IDs únicos.
  3. Stacks dentro del conjunto soportado por el detector de Musubi
     (la capitalización debe coincidir EXACTAMENTE, o el gate no matchea).

Uso: python validate.py [ruta_index]   (por defecto: index.json)
Sale con código 1 si hay errores.
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("Falta la dependencia 'jsonschema'. Instalá: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

# Debe coincidir con los Ecosystem que devuelve internal/detector de Musubi.
KNOWN_STACKS = {
    "Go", "Node.js", "Python", "Rust", "Docker",
    "Java", "Ruby", "PHP", ".NET", "C/C++", "Dart", "Elixir",
}

root = Path(__file__).parent
index_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "index.json"
schema_path = root / "schema.json"

errors = []

schema = json.loads(schema_path.read_text(encoding="utf-8"))
data = json.loads(index_path.read_text(encoding="utf-8"))

# 1. Esquema
validator = Draft7Validator(schema)
for e in sorted(validator.iter_errors(data), key=lambda x: list(x.path)):
    loc = "/".join(str(p) for p in e.path) or "(raíz)"
    errors.append(f"[schema] {loc}: {e.message}")

entries = data.get("entries", [])

# 2. IDs únicos
seen = set()
for entry in entries:
    eid = entry.get("id")
    if eid in seen:
        errors.append(f"[id duplicado] {eid}")
    seen.add(eid)

# 3. Stacks conocidos
for entry in entries:
    for stack in entry.get("stacks", []):
        if stack not in KNOWN_STACKS:
            errors.append(
                f"[stack desconocido] entrada '{entry.get('id')}': '{stack}' "
                f"(¿capitalización? conocidos: {', '.join(sorted(KNOWN_STACKS))})"
            )

if errors:
    print(f"[ERROR] Catalogo INVALIDO ({len(errors)} error(es)):", file=sys.stderr)
    for err in errors:
        print("  - " + err, file=sys.stderr)
    sys.exit(1)

print(f"[OK] Catalogo valido: {len(entries)} entradas.")
