Objetivo.
Quiero crear un agente que pueda acceder a mi biblioteca de bases de datos que esta en distintas colecciones dentro de varias bases de datos en mongodb. Para ello quiero que el agente tenga un contexto que le indique de qué fuentes debe sacar la información para responder las preguntas con el mayor contexto y precisión posible. Tiene que ser capaz de citar textualmente hacer recopilaciones.

Instrucciones.

Quiero que generes el plan de trabajo para discutirlo con el objetivo de crear un agente que sea capaz de usar la información disponible de forma eficiente.

Comentarios/ideas

Como flujo ideal, me gustaría poder pedirle al agente que me responda a un requerimiento y se estudie primero la biblioteca disponible para crearse el contexto con el que responder de la forma más adecuada posible.

---

## Cuestionario para la Definición del Agente

Estas preguntas servirán como base para definir el alcance y la funcionalidad del agente.

**1. Sobre los Datos en MongoDB:**

*   **Estructura y Contenido:** ¿Podrías describir la estructura de tus bases de datos y colecciones en MongoDB? ¿Qué tipo de información contienen (texto, documentos estructurados, etc.)? ¿Hay algún esquema o un ejemplo de documento que puedas compartir?
*   **Volumen:** ¿Qué volumen de datos estamos manejando aproximadamente? (Número de documentos, tamaño total).
*   **Organización:** ¿Cómo se relacionan las distintas colecciones o bases de datos entre sí, si es que lo hacen?

**2. Sobre las Capacidades del Agente:**

*   **Generación de Material:** Cuando dices "generar material", ¿a qué te refieres exactamente? ¿Crear resúmenes de uno o varios documentos? ¿Redactar nuevos textos basados en la información existente? ¿Construir tablas comparativas?
*   **Tipos de Preguntas:** ¿Qué clase de preguntas le harías al agente?
    *   **Búsqueda simple:** "Busca el documento que habla sobre X".
    *   **Preguntas directas:** "¿Cuál es la definición de Y según la fuente Z?".
    *   **Síntesis:** "Resume los puntos clave sobre el tema A de todas las fuentes disponibles".
    *   **Análisis:** "Compara las opiniones de la fuente X y la fuente Y sobre el tema B".
*   **Citación de Fuentes:** ¿Cómo debería el agente citar sus fuentes? ¿Basta con el nombre del documento o colección? ¿Debería incluir un fragmento del texto original o un enlace/ID del documento?
*   **Recopilaciones:** ¿Qué esperas cuando pides una "recopilación"? ¿Una lista de documentos relevantes? ¿Un único documento que fusione información de varias fuentes?

**3. Sobre la Interacción y el Resultado:**

*   **Interfaz e Infraestructura:**
        *   **Plataforma:** Una aplicación web con una interfaz de chat, accesible desde cualquier navegador en ordenadores y dispositivos móviles (diseño responsivo).
        *   **Diseño y Usabilidad (UX):** La apariencia y experiencia de uso deben ser modernas e intuitivas, tomando como modelo de referencia a asistentes conversacionales como ChatGPT o Gemini.
        *   **Funcionalidad Avanzada:** La interfaz permitirá al usuario enriquecer sus preguntas adjuntando enlaces web o subiendo archivos directamente en el chat.
        *   **Infraestructura de Despliegue:** La solución se desplegará en un servidor propio gestionado con **Portainer**. Esto sugiere una arquitectura basada en contenedores (Docker), lo que facilitará la separación del servicio de `backend` (el agente en Python) y el `frontend` (la interfaz web).
*   **Formato de Respuesta:** ¿En qué formato prefieres recibir las respuestas? ¿Texto plano, Markdown (con formato como títulos y listas), JSON?
*   **Manejo de Incertidumbre:** ¿Qué debería hacer el agente si no encuentra una respuesta o si la información es ambigua? ¿Debería indicarlo, pedir más detalles o presentar la información parcial que ha encontrado?

---

## Hoja de Ruta del Proyecto

### Resumen del Análisis de Datos

1.  **Colección `normas`**:
    *   **Estructura**: JSON complejo y anidado.
    *   **Contenido Clave**: El texto está fragmentado en un array (`texto.p`).
    *   **Acción Requerida**: Necesita un parser específico para extraer y unir el texto.
    *   **Fortaleza**: Metadatos muy ricos (`titulo`, `identificador`, `referencias`) para búsquedas precisas.

2.  **Colección `preguntas`**:
    *   **Estructura**: JSON simple y plano.
    *   **Contenido Clave**: Campos directos como `pregunta`, `opciones`, `correcta`.
    *   **Acción Requerida**: Ninguna, lista para ser usada.
    *   **Fortaleza**: Metadatos excelentes para filtrado (`tema`, `oposición`, `nivel_dificultad`).

3.  **Colección de Textos (San Josemaría)**:
    *   **Estructura**: JSON con campos bien definidos.
    *   **Contenido Clave**: El texto principal (`text`) contiene HTML.
    *   **Acción Requerida**: Necesita un proceso de limpieza para eliminar las etiquetas HTML.
    *   **Fortaleza**: Metadatos temáticos (`subject`) de gran valor para búsquedas conceptuales.

### Propuesta de Plan de Trabajo

Se propone un desarrollo en fases usando **Python**.

**Fase 1: Cimientos del Proyecto**
1.  **Entorno de Desarrollo**: Configurar un proyecto en Python.
2.  **Librerías Esenciales**: Instalar `pymongo` (para MongoDB) y `beautifulsoup4` (para limpiar HTML).
3.  **Módulo de Conexión**: Crear un script seguro que gestione la conexión a MongoDB.

**Fase 2: "Adaptadores" para cada Fuente de Datos**
El objetivo es que el programa principal reciba datos limpios y estandarizados sin importar la fuente.
1.  **Crear `NormasAdapter`**: Script para leer un documento de `normas`, extraer y unir el texto del array `texto.p`.
2.  **Crear `PreguntasAdapter`**: Script para leer directamente los documentos de `preguntas`.
3.  **Crear `TextosAdapter`**: Script que use `beautifulsoup4` para limpiar el campo `text` de HTML.

**Fase 3: Motor de Búsqueda Inicial**
1.  **Búsqueda por Palabra Clave**: Implementar una función que reciba texto del usuario y construya consultas en MongoDB a través de los "Adaptadores".
2.  **Búsqueda por Metadatos**: Crear funciones que permitan búsquedas filtradas (ej: por tema, por título).

**Fase 4: Interfaz de Usuario (Web)**
1.  **Desarrollo del Frontend**: Crear la aplicación web de chat (usando un framework como React o Vue.js).
2.  **Creación de API Backend**: El backend de Python expondrá una API (usando un framework como FastAPI o Flask) que el frontend consumirá.
3.  **Integración**: Conectar el frontend con el backend para enviar preguntas y recibir respuestas de forma asíncrona.

**Fase 5: Evolución y Mejoras**
1.  **Indexación**: Optimizar MongoDB creando índices en los campos de búsqueda más comunes.
2.  **Búsqueda Semántica**: Explorar el uso de embeddings para encontrar textos por significado, no solo por palabras clave.

---

## Próximos Pasos

**Punto de Reanudación:** Fin de la fase de planificación.

**Siguiente Acción:** Iniciar la **Fase 1: Cimientos del Proyecto**. Las tareas inmediatas son:
1.  Crear la estructura de carpetas para el proyecto.
2.  Generar un archivo `requirements.txt` con las librerías iniciales: `pymongo` y `beautifulsoup4`.