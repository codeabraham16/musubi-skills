# musubi-skills

Catálogo curado de **skills** (conjuntos de reglas/convenciones) para
[Musubi](https://github.com/codeabraham16/musubi) — el servidor MCP de memoria
para agentes de IA.

Musubi consume este catálogo vía su herramienta `musubi_search_skills`: detecta
el stack del proyecto, baja este `index.json`, aplica un **gate de aplicabilidad
duro** (una skill solo pasa si sus `triggers` matchean archivos reales del
proyecto + su `deps` está en las dependencias reales + `capabilities` en PATH) y
le devuelve al agente solo las candidatas relevantes. El agente las rankea por
valor, las confirma con el usuario y las guarda. **El catálogo provee; Musubi
filtra por proyecto.**

## Formato

`index.json` es un objeto con `catalog_version` y `entries[]`. Cada entrada:

| Campo | Req. | Descripción |
|-------|------|-------------|
| `id` | ✅ | slug único (`[a-z0-9][a-z0-9-]*`) |
| `name` | ✅ | nombre legible |
| `description` | ✅ | qué cubre la skill |
| `stacks` | ✅ | ecosistemas; **capitalización EXACTA** del detector (`Go`, `Node.js`, `Python`, `Rust`, `Docker`, `Java`, `Ruby`, `PHP`, `.NET`, …) |
| `triggers` | ✅ | globs que deben matchear archivos reales (`*.go`, `*.tsx`, `Dockerfile`) |
| `rules_url` | ✅ | URL a la fuente (preferir **docs oficiales**) |
| `excerpt` | ✅ | resumen de 1-3 líneas de las reglas (sin red) |
| `deps` | — | dependencias requeridas (al menos una presente); vacío = nivel de ecosistema |
| `capabilities` | — | herramientas en PATH (`go`, `cargo`, `node`) |
| `tags` | — | etiquetas informativas |
| `source` | — | origen (ej. `official-docs`) |

El esquema completo está en [`schema.json`](schema.json).

## Cómo lo usa Musubi

Por defecto Musubi apunta su `sourcing.catalog_url` al `index.json` de este repo
(servido por `raw.githubusercontent.com`). Para usar otro catálogo, editá
`.musubi/config.yaml`:

```yaml
sourcing:
  enabled: true
  catalog_url: https://raw.githubusercontent.com/codeabraham16/musubi-skills/main/index.json
  max_candidates: 20
```

## Contribuir

Querés agregar skills para un stack/framework? Mirá [CONTRIBUTING.md](CONTRIBUTING.md)
— incluye el flujo de investigación y una plantilla de entrada. Cada PR se valida
en CI contra `schema.json` (`validate.py`).

Validación local:

```bash
pip install jsonschema
python validate.py
```
