# Generalizing Metadata Extraction for Itheca Library

The goal is to transform the downloaded HTML documents into an interconnected Markdown library with rich metadata. We will generalize the extraction process to handle diverse document types beyond the Bible, such as the Catechism and Papal messages.

## Proposed Changes

### Core Extraction Pipeline

We will implement a modular pipeline that detects the document type and applies a specific parsing strategy.

#### [MODIFY] [ParserHTML.py](file:///e:/OneDrive/MiCodigo/GitHub/ListarArchivos/ParserHTML.py)
Update to include:
- **Document Type Detector**: Identification of `doc_type` (Bible, Catechism, PapalMessage, Index, etc.) based on directory path and filename pattern.
- **Source vs Index Distinction**: Explicit classification of documents as `is_source: true` (for texts like Genesis, Angelus, Catechism) or `is_index: true` (for directory indices, thematic indices like IndiceSE). 
- **Link Preservation Engine**: 
    - Convert HTML anchors and relative links to Markdown-compatible formats.
    - Ensure verse-level anchors (e.g., `#C0101`) are mapped correctly to the target document's header or reference point.
- **Specific Parsers**:
    - **Biblical Parser**: Extracts book, chapter, and verse anchors (e.g., `<a id="C0101">`).
    - **Catechism Parser**: Extracts paragraph numbers (e.g., `<a id="C0001">`) and internal cross-references.
    - **Papal Message Parser**: Extracts dates from filenames (e.g., `ang050515.html` -> 2005-05-15) and speaker (Benedict XVI for `B16` folder).
- **Metadata Schema**:
    - `title`: Extracted from index pages or document headers.
    - `date`: For temporal documents like papal messages.
    - `canonical_id`: A standard identifier (e.g., `Gn 1:1`, `CEC 1`, `Ang B16 2005-05-15`).
    - `relationships`: A list of outgoing links to other library documents.

#### [NEW] [ExtractorRelaciones.py](file:///e:/OneDrive/MiCodigo/GitHub/ListarArchivos/ExtractorRelaciones.py)
A script to pre-process indices and commentaries:
- **Thematic Index Mapper**: Maps concepts (from files like `IndiceSE/A.html`) to biblical verses.
- **Commentary Linker**: Extracts relationships between commentaries and the sources they discuss.
- **Link Integrity System**: Scans source documents for all outgoing links (`<a href="...">`) to ensure they are captured in the document's metadata relationship graph.
- **Output**: Generates a JSON mapping of relationships to be injected into the final Markdown files.

#### [NEW] [MetadataInjector.py](file:///e:/OneDrive/MiCodigo/GitHub/ListarArchivos/MetadataInjector.py)
A tool to merge the extracted metadata and relationships into the Markdown frontmatter.

---

### Library Structure
Markdown files will be saved in a structured way, mirroring the original directory hierarchy, but enriched with YAML frontmatter:

```yaml
---
title: "Génesis 1"
doc_type: "biblia"
book: "Gn"
chapter: 1
canonical_id: "Gn 1"
relationships:
  - type: "comentario"
    target: "Comentarios/Gn"
  - type: "tema"
    target: "IndiceSE/Creacion"
---
```

## Verification Plan

### Automated Tests
- **Link Checker**: Verify that all `relationships` in the frontmatter point to existing files in the library.
- **Schema Validation**: Ensure all generated Markdown files have the required YAML fields.

### Manual Verification
- Review a sample of converted files from each `doc_type` to ensure content and metadata accuracy.
- Check that link references (e.g., `Jn 14, 16`) are correctly parsed and preserved.
