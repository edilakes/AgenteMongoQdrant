# Capacidades del Agente Universal MCP

El agente ha sido diseñado bajo una arquitectura de **Meta-Contexto Puro**, lo que le permite actuar como un bibliotecario experto con las siguientes capacidades:

### 1. Búsqueda Semántica de "Mapa Maestro"
- El agente no busca por palabras clave al azar. Utiliza una colección especializada en Qdrant llamada `context_map`.
- Esta colección contiene "punteros" semánticos que resumen el contenido de grandes volúmenes de datos.
- Sabe distinguir entre un libro de la Biblia, una norma jurídica o una reflexión temática antes de ir a buscar el detalle.

### 2. Recuperación Híbrida de Alta Precisión
- **Conocimiento Core (MongoDB)**: Accede de forma nativa a colecciones remotas (`Pioteca`, `OposicionesDB`) para extraer fragmentos exactos basados en los punteros semánticos.
- **Conectividad Externa (MCP)**: Puede conectarse a servidores externos para realizar búsquedas en la web, ejecutar código o consultar bases de datos SQL.

### 3. Síntesis Inteligente con Citas
- Utiliza **Gemini 2.0 Flash** para leer el contexto recuperado y redactar respuestas coherentes.
- Está instruido para priorizar citas textuales entre comillas, asegurando que la información sea fiel a la fuente original.

### 4. Estabilidad y Rendimiento
- **Sanitización JSON**: Limpia recursivamente todos los datos recuperados de bases de datos para evitar errores de visualización.
- **Diseño Glassmorphism**: Una interfaz moderna y fluida que permite interacciones premium.
- **Indexación Autónoma**: Capacidad para estudiar nuevas fuentes de datos y añadirlas a su mapa mental automáticamente.
