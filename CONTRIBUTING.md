# Contribuir al catálogo

Esta es la **herramienta de llenado**: un flujo repetible (humano o asistido por
un agente como Claude) para convertir convenciones reales de un stack en una
entrada del catálogo que Musubi pueda aprovechar.

## Principio

El catálogo se **cura**, no se scrapea a ciegas. Cada entrada apunta a una
**fuente confiable** (preferentemente documentación oficial) y resume sus reglas
clave. Musubi después decide por proyecto cuáles aplican (gate de aplicabilidad).

## Flujo para agregar una skill

1. **Elegí un objetivo** no cubierto aún (un lenguaje, framework o herramienta).
   Revisá `index.json` para no duplicar.
2. **Investigá la fuente oficial.** Priorizá en este orden:
   - Documentación oficial (ej. `go.dev`, `react.dev`, `docs.python.org`).
   - Guías de estilo oficiales / linters oficiales.
   - Listas reputadas como complemento (ej. `awesome-cursorrules`,
     `awesome-claude-skills`) — pero la `rules_url` debe ir a la fuente autoritativa.
3. **Extraé 3-5 reglas concretas y accionables.** Nada genérico ("escribí buen
   código"); reglas que cambien decisiones (ej. "usá `select_related` para evitar
   N+1").
4. **Completá los campos de matching con cuidado** (esto define el foco):
   - `stacks`: capitalización EXACTA del detector (ver tabla del README).
   - `deps`: nombres reales de paquetes (ej. `react`, `django`, `github.com/gin-gonic/gin`).
     Dejá vacío solo si aplica a todo el ecosistema (ej. estilo del lenguaje).
   - `triggers`: globs de los archivos donde la regla importa (`*.tsx`, `Dockerfile`).
   - `capabilities`: solo si la skill realmente necesita una herramienta en PATH.
5. **Escribí `excerpt`** (1-3 líneas, ≤ ~600 chars) resumiendo las reglas, y
   `rules_url` a la fuente.
6. **Validá** antes de abrir el PR:
   ```bash
   pip install jsonschema
   python validate.py
   # o con el binario de Musubi:
   musubi catalog validate index.json
   ```
7. **Abrí el PR.** La CI vuelve a validar (`schema.json` + ids únicos + stacks conocidos).

## Plantilla de entrada

```json
{
  "id": "framework-tema",
  "name": "Framework — Tema",
  "description": "Qué cubre, en una línea.",
  "stacks": ["Node.js"],
  "deps": ["nombre-del-paquete"],
  "triggers": ["*.ts"],
  "capabilities": [],
  "tags": ["tag1", "tag2"],
  "rules_url": "https://docs.oficiales.example/guia",
  "excerpt": "Regla 1. Regla 2. Regla 3 — concretas y accionables.",
  "source": "official-docs"
}
```

## Prompt sugerido (para llenado asistido por agente)

> "Investigá las convenciones oficiales de **<stack/framework>**. Extraé 3-5
> reglas concretas y accionables de la documentación oficial. Devolvé UNA entrada
> JSON siguiendo la plantilla de CONTRIBUTING.md: `stacks` con la capitalización
> exacta del detector de Musubi, `deps` con los nombres reales de paquetes,
> `triggers` con los globs correctos, `rules_url` a la fuente oficial, y un
> `excerpt` de 1-3 líneas. No inventes reglas: citá la doc."

## Calidad antes que cantidad

Una entrada vaga es peor que ninguna: agrega ruido sin valor. Si una regla no
cambiaría una decisión de código, no la incluyas.
