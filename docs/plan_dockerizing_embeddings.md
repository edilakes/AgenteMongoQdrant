# Implementación: Descargador Dual Recursivo (Pipeline Fase 1)

El objetivo es crear un script de PowerShell que descargue el contenido de las IDs válidas de Itheca, priorizando la versión web y usando una copia local como respaldo si la web falla.

## Proposed Changes

### [Corrección de Codificación (Mojibake)]

**Contexto del Problema:** El fallo ("quedarÃ©" en lugar de "quedaré") se debe a que el servidor de Itheca envía los bytes del HTML en `UTF-8`, pero al no especificarlo siempre en las cabeceras HTTP, el cmdlet `Invoke-WebRequest` de PowerShell asume erróneamente que los datos vienen en `ISO-8859-1` (Windows-1252 estándar). 

**Plan de Acción:**
- Modificar `Invoke-WebRequest` para usar `-OutFile`, guardando los bytes puros.
- Actualizar `ParserHTML.py` para usar `BeautifulSoup4` con detección automática de encoding via modo binario.

### [PoC: Chunking e Indexación Vectorial]

#### [NEW] [IndexadorQdrant.py](file:///e:/OneDrive/MiCodigo/GitHub/ListarArchivos/IndexadorQdrant.py)
Script para la inyección en Qdrant:
- **Modelo:** `intfloat/multilingual-e5-large` (Dimensión 1024).
- **Chunking:** Semántico con Langchain `RecursiveCharacterTextSplitter`.
- **Payload:** Texto + metadatos (URL, título).

## Verification Plan
- Verificar limpieza de HTML en archivos Markdown resultantes.
- Probar búsqueda semántica con `TestBusqueda.py`.
