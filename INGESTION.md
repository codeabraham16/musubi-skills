# Ingestión de skills al catálogo

Esta guía explica cómo **llenar el catálogo** (`index.json`) ingiriendo reglas desde
librerías, documentación oficial y repositorios de skills que ya existen — manteniendo
la calidad y el foco. Para el detalle de cada campo de una entrada, ver
[CONTRIBUTING.md](CONTRIBUTING.md) y [schema.json](schema.json).

> **Importante:** la ingestión es **tiempo de autoría** (llenar el catálogo). No tiene
> nada que ver con el *runtime* de Musubi (el gate/sourcing que corre en cada proyecto).
> Llenar el catálogo nunca cambia cómo se resuelven las skills en un proyecto.

---

## Las dos capas

### Capa 1 — Merge determinístico (formato compatible)

Si la fuente ya publica un catálogo **en nuestro schema** (otro `index.json` compatible,
p. ej. un catálogo comunitario o un fork), se ingiere con un comando:

```bash
musubi catalog merge <url> [--output <ruta>]
```

- Baja el catálogo remoto y lo **funde** en el `index.json` local.
- **Dedupe por `id`** (la entrada entrante pisa la local) con reporte `[overwrite] <id>`.
- **Valida antes de escribir**: si el resultado es inválido, no escribe nada.
- Escritura atómica y salida determinística (ordenada por `id`).

Ejemplo:
```bash
cd musubi-skills
musubi catalog merge https://raw.githubusercontent.com/otro/catalogo/main/index.json
python validate.py            # revalidar (chequea también maxLength del excerpt)
```

### Capa 2 — Conversión asistida (formato libre)

La realidad: **casi ningún pack de terceros usa nuestro schema**. Los formatos comunes son
texto plano o markdown sin estructura:

- `.cursorrules` (texto plano)
- archivos `.mdc` de Cursor (markdown con frontmatter opcional)
- `CLAUDE.md` / `AGENTS.md`
- listas markdown de "awesome-*"

Para estos, la ingestión es un paso **humano + IA**: se leen las reglas reales y se
**convierten** a entradas del schema. No hay parser automático porque mapear formatos
arbitrarios a `stacks`/`deps`/`triggers` correctos requiere criterio.

---

## Flujo de conversión asistida (recomendado)

1. **Elegí un objetivo concreto** (una librería/framework que el detector reconozca:
   Go, Node.js, Python, Rust, Docker, Java, Ruby, PHP, .NET, C/C++, Dart, Elixir).
   Priorizá lo que **no esté ya** en el catálogo (evitá duplicar `id`/tema).

2. **Descubrí la fuente, en este orden de prioridad:**
   - **Docs oficiales** (la mejor fuente — siempre `source: "official-docs"`).
   - Repos/listas de skills como complemento: `awesome-cursorrules`, `cursor.directory`,
     colecciones de "claude skills", topics de GitHub (`cursorrules`, `ai-rules`).
   - Usá las listas solo para **descubrir qué cubrir**, no para copiar reglas vagas.

3. **Extraé 3–5 reglas concretas y accionables** de la doc oficial. Cada regla debe
   cambiar una decisión de código (no "escribí buen código").

4. **Mapeá a una entrada del schema** con cuidado en los 3 campos críticos:
   - `stacks`: capitalización **exacta** del detector.
   - `deps`: nombres reales de paquetes (npm / PyPI / crate / módulo Go). El dep-gating
     solo funciona para Node.js/Go/Python/Rust; para Java/Ruby/PHP/.NET usá `deps: []`.
   - `triggers`: globs de archivos reales (`*.tsx`, `*.py`, `*.rs`, `Dockerfile`).
   - `excerpt`: ≤ **600 caracteres** (lo enforcea `schema.json`), `rules_url` a la doc oficial.

5. **Validá** localmente con **ambos**:
   ```bash
   musubi catalog validate index.json   # rápido (Go)
   python validate.py                   # jsonschema (chequea también maxLength)
   ```

6. **Commit + PR.** La CI revalida con `validate.py` en cada push/PR.

---

## Prompt para un agente (conversión asistida)

Pegá esto en una sesión de Claude para generar una entrada lista:

> Investigá las convenciones/optimización oficiales de **\<librería\>**. Leé la doc
> oficial (no inventes). Devolveme UNA entrada JSON para el catálogo de musubi-skills con:
> `id` (slug), `name`, `description`, `stacks` (capitalización exacta: Go, Node.js, Python,
> Rust, Docker, Java, Ruby, PHP, .NET, C/C++, Dart, Elixir), `deps` (nombres reales de
> paquetes), `triggers` (globs correctos), `tags`, `rules_url` (doc oficial verificada),
> `excerpt` (3–5 reglas concretas, ≤600 chars) y `source: "official-docs"`.

---

## Regla de oro: una entrada canónica por tema

- **Mismo `id`** → la CI lo rechaza (id duplicado).
- **Mismo tema con otro `id`** → pasa validación pero ensucia (el gate puede inyectar las
  dos). **Actualizá la entrada existente** en vez de duplicar.
- Una segunda entrada solo se justifica si es un **sub-tema con scope distinto**
  (p. ej. reglas generales vs. testing), diferenciado por `triggers`.

Calidad > cantidad: una entrada vaga suma ruido sin valor.
