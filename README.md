# AgenteMongoQdrant 🤖

Un agente inteligente diseñado para interactuar con bibliotecas de documentos almacenadas en **MongoDB**, utilizando **Qdrant** para búsquedas semánticas de alta precisión. El sistema permite realizar consultas en lenguaje natural, citar fuentes textualmente y generar síntesis de información compleja.

## 🚀 Características Principales

- **Búsqueda Semántica**: Integración con Qdrant para encontrar documentos por significado, no solo por palabras clave.
- **Contexto Multi-fuente**: Capacidad de consultar diversas colecciones de MongoDB (normas, preguntas, textos doctrinales) de forma simultánea.
- **MetaRouter y Orquestación**: Lógica avanzada para decidir qué fuentes consultar y cómo sintetizar la respuesta.
- **Interfaz Moderna**: Aplicación web responsiva construida con React y Vite, inspirada en ChatGPT/Gemini.
- **Citas Textuales**: El agente es capaz de referenciar fragmentos exactos de los documentos originales.

## 🛠️ Stack Tecnológico

- **Backend**: Python (FastAPI)
- **Frontend**: React + Vite (Framer Motion, Tailwind CSS)
- **Base de Datos NoSQL**: MongoDB
- **Base de Datos Vectorial**: Qdrant
- **IA/LLM**: Integración con modelos de lenguaje avanzados a través de un servicio dedicado.
- **Despliegue**: Docker & Docker Compose.

## 📂 Estructura del Proyecto

```text
├── src/                    # Backend (FastAPI)
│   ├── api/               # Rutas y controladores de la API
│   ├── core/              # Lógica central (SemanticIndexer, MetaRouter)
│   ├── database/          # Conexiones y modelos de datos
│   └── adapters/          # Adaptadores para limpiar y formatear datos
├── frontend/               # Frontend (React + Vite)
├── scripts/                # Scripts de utilidad (indexación, migraciones)
├── docker-compose.yml      # Orquestación de contenedores
└── GEMINI.md               # Documentación original del proyecto
```

## ⚙️ Instalación y Configuración

### Requisitos Previos

- Docker y Docker Compose
- Python 3.10+ (opcional para desarrollo local)
- Node.js 18+ (opcional para desarrollo local)

### Despliegue con Docker

1. Clona el repositorio:
   ```bash
   git clone https://github.com/edilakes/AgenteMongoQdrant.git
   cd AgenteMongoQdrant
   ```

2. Configura las variables de entorno:
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tus credenciales
   ```

3. Levanta los servicios:
   ```bash
   docker-compose up -d
   ```

## 🗺️ Hoja de Ruta (Roadmap)

- [x] Fase 1: Cimientos y Conexión MongoDB.
- [x] Fase 2: Adaptadores de Datos.
- [x] Fase 3: Motor de Búsqueda Inicial.
- [x] Fase 4: Interfaz de Usuario (Web).
- [/] Fase 5: Indexación Semántica con Qdrant (En progreso).

## 📄 Documentación Consolidada

Para una visión detallada de la evolución y arquitectura del proyecto, consulta los siguientes documentos en la carpeta `docs/`:

### Estrategia y Arquitectura Core
- [Estrategia de Meta-Contexto Puro](docs/plan_pure_context_strategy.md): Diseño de la Capa de Direccionamiento Semántico.
- [Walkthrough de Implementación Pure Context](docs/walkthrough_pure_context_strategy.md): Resultados de la orquestación semántica.
- [Resumen de Capacidades](docs/capabilities_summary.md): Qué puede hacer el agente actualmente.
- [Detalles Técnicos del Indexador](docs/details_pure_context.md): Cómo funciona el `ContextGenerator`.

### Infraestructura y Datos
- [Extracción de Metadatos (Itheca)](docs/plan_metadata_extraction.md): Pipeline de procesamiento de documentos HTML.
- [Walkthrough de Datos](docs/walkthrough_metadata_extraction.md): Resultados de la migración de 10k+ documentos.
- [Dockerización de Embeddings](docs/plan_dockerizing_embeddings.md): Microservicio para el modelo `multilingual-e5-large`.
- [Arquitectura RAG Final](docs/walkthrough_dockerizing_embeddings.md): Reporte de infraestructura completada.

### Gestión del Repositorio
- [Plan de GitHub y README](docs/plan_github_and_readme.md): Inicialización del repo y documentación raíz.
- [Walkthrough de Subida a GitHub](docs/walkthrough_github_and_readme.md): Verificación de la sincronización remota.

## 🔗 Integración con n8n

El proyecto incluye un flujo de trabajo preparado para **n8n** que permite conectar el agente con cualquier disparador externo (Webhooks, Telegram, Slack, etc.).

### Configuración del Workflow
1.  Importa el archivo [n8n_workflow.json](n8n_workflow.json) en tu instancia de n8n.
2.  Configura la variable de entorno `AGENT_API_URL` en n8n con la URL de tu backend (ej. `http://host.docker.internal:8000`).
3.  El workflow expone un Webhook en la ruta `/agent/chat` (POST) que acepta:
    ```json
    {
      "message": "¿Qué dice la norma X sobre Y?",
      "user_id": "opcional_id_usuario"
    }
### Chat en Vivo (n8n Interface)
1.  Importa el archivo [n8n_chat_workflow.json](n8n_chat_workflow.json).
2.  Este flujo utiliza el nodo **Chat Trigger**, que te permite chatear directamente desde n8n.
3.  Al abrir el flujo, haz clic en el icono de **Chat** en la parte inferior derecha de n8n para probarlo.

---

## 📄 Licencia

Este proyecto es de uso privado. Todos los derechos reservados.
