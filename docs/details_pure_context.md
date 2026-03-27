# Plan de Estrategia: Qdrant como Generador de Contexto Puro

Este plan redefine el rol de Qdrant como una "Capa de Direccionamiento Semántico" (LDS) que mapea todas las fuentes de datos disponibles.

## Concepto: Capa de Direccionamiento Semántico
En lugar de guardar todo el contenido en Qdrant, guardaremos **Índices Semánticos** y **Metadatos de Enrutamiento**.

### Ejemplo de Flujo:
1.  **Pregunta**: "¿Qué dice el Génesis sobre la creación?"
2.  **Qdrant Recall**: Encuentra un vector cuyo resumen es "Libro del Génesis - Antiguo Testamento" y tiene metadatos: `{source: "mongodb", collection: "biblia", filter: {libro: "Génesis"}}`.
3.  **Action**: El agente usa el MCP de MongoDB para traer el texto exacto del Génesis.

## Componentes a Desarrollar

### 1. `ContextGenerator` (Módulo de Indexación)
Un script que procesará las fuentes de forma iterativa:
*   **Iteración 1 (Descubrimiento)**: Mapear nombres de colecciones, tablas y archivos.
*   **Iteración 2 (Resumen Semántico)**: Usar el LLM para generar resúmenes cortos de cada documento/bloque.
*   **Iteración 3 (Vectores)**: Generar los vectores de estos resúmenes y subirlos a Qdrant.

### 2. Estructura de Metadatos en Qdrant
Cada punto en Qdrant tendrá:
*   `text`: Resumen semántico del bloque/documento.
*   `access_path`: `{protocol: "mcp-mongodb", server: "...", params: {...}}`.
*   `content_type`: "texto_doctrinal", "registro_sql", "archivo_pdf", etc.
*   `hierarchy`: Ubicación en el árbol de conocimientos (ej: "Biblia > AT > Génesis").

### 3. MetaRouter 2.0
El router ahora será más "astuto":
1.  Consulta a Qdrant por el "Mapa del Conocimiento".
2.  Identifica el `access_path`.
3.  Orquesta la recuperación precisa.

## Próximos Pasos (Propuesta)
1.  **Módulo Indexador**: Crear un script que lea la base de datos de "normas" y "biblia" y cree estos resúmenes en Qdrant.
2.  **Refinamiento de Payloads**: Estandarizar cómo se guardan las rutas de acceso en los metadatos de Qdrant.

---
**¿Deseas que comience con el diseño del Módulo Indexador (`ContextGenerator`) para procesar una fuente de ejemplo (ej. la Biblia)?**
