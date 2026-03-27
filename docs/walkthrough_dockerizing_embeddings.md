# Reporte Final: Arquitectura RAG Itheca Completada

Hemos pasado de una PoC local a una infraestructura de microservicios robusta en servidor.

## 1. Microservicio de Embeddings (TEI en Docker)
- **Implementado:** Mediante Hugging Face *Text Embeddings Inference* (TEI).
- **Modelo:** `multilingual-e5-large` (dimensión 1024).
- **Endpoint:** `http://194.61.28.46:8080`.

## 2. Almacenamiento Persistente (MongoDB)
- **Base de datos:** `itheca` | **Colección:** `knowledge_base`.
- **Volumen:** **10,423 documentos** procesados y persistidos.

## 3. Indexación Vectorial (Qdrant)
- **Estado:** Validación exitosa de ingesta de vectores generados por el microservicio TEI hacia la colección `doctrina_itheca`.

## 4. Pipeline de Ingesta y Conversión
- **HTML a Markdown:** `ParserHTML.py` optimizado para eliminar ruido y preservar integridad de caracteres (UTf-8).

---

### Arquitectura Final Sugerida:
1. **Trigger:** Consulta de usuario.
2. **Embeddings:** Llamada al microservicio TEI en el servidor.
3. **Retrieval:** Búsqueda en Qdrant.
4. **Contexto:** Recuperación de texto completo desde MongoDB para el LLM.
