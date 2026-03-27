# Plan de Implementación - Agente Universal MCP (Estrategia Meta-Contexto)

Este plan define una arquitectura de orquestación donde **Qdrant** actúa como el núcleo de direccionamiento semántico.

## Estrategia de Meta-Contexto Puro
El sistema utiliza **Qdrant** como un mapa semántico maestro (`context_map`) que direcciona al agente hacia las fuentes de datos exactas.

1.  **Enrutamiento Semántico**: El agente busca en `context_map` para identificar el "puntero" semántico (resumen + ruta de acceso).
2.  **Recuperación Híbrida**: 
    - **Adaptador Nativo**: Acceso directo y estable a MongoDB para el conocimiento core (Pioteca, OposicionesDB).
    - **MCP (Model Context Protocol)**: Orquestación de herramientas externas (Web, SQL, etc.).
3.  **Síntesis con Citas**: El `StudyLibrarian` procesa la información recuperada y genera la respuesta final con Gemini 2.0 Flash.

## Proposed Changes

### [Componente] Meta-Orquestador (Python)

#### [MODIFY] `src/core/meta_router.py`(file:///e:/OneDrive/MiCodigo/VS/Agente/src/core/meta_router.py)
Orquestador que utiliza `context_map` en Qdrant y decide el plan de recuperación (Nativo o MCP). Incluye limpieza recursiva de JSON para estabilidad.

## Proposed Changes

### [Componente] Infraestructura Docker

#### [MODIFY] `docker-compose.yml`(file:///e:/OneDrive/MiCodigo/VS/Agente/docker-compose.yml)
Se simplificará para contener solo el **Backend del Agente** y los **Servidores MCP**, ya que las bases de datos existen externamente en Portainer.

#### [NEW] `.env`(file:///e:/OneDrive/MiCodigo/VS/Agente/.env)
Configuración de las `URL` y `API_KEYS` proporcionadas por el usuario.

### [Componente] Backend del Agente (Python)

#### [NEW] `src/core/mcp_client.py`(file:///e:/OneDrive/MiCodigo/VS/Agente/src/core/mcp_client.py)
Cliente universal para conectar con los múltiples servidores MCP y exponer sus herramientas al LLM.

#### [NEW] `scripts/run_indexing.py`(file:///e:/OneDrive/MiCodigo/VS/Agente/scripts/run_indexing.py)
Script para el estudio autónomo de bases de datos remotas y generación de punteros en Qdrant.

#### [NEW] `src/core/semantic_indexer.py`(file:///e:/OneDrive/MiCodigo/VS/Agente/src/core/semantic_indexer.py)
Motor de embeddings y resúmenes semánticos usando Gemini 2.0 Flash.

## Verification Plan

### Automated Tests
- `tests/test_mcp_orchestration.py`: Verificar que el agente puede llamar a herramientas de diferentes servidores MCP en una misma sesión.
- `tests/test_data_sources.py`: Validar conectividad con MongoDB, Qdrant y SQL.

### Manual Verification
- Probar flujos donde el agente necesite combinar información de SQL y Qdrant para responder.
