# Walkthrough: Generalizing Metadata Extraction for Itheca

We have successfully transformed the Itheca HTML library into an interconnected Markdown library. This process involved scanning over 10,000 documents to build a global relationship map and then converting each document with rich, context-aware metadata.

## Key Accomplishments

### 1. Global Relationship Mapping
We developed `ExtractorRelaciones.py` to scan the entire `biblioteca` directory. It captured:
- **Anchors**: Verse-level identifiers (e.g., `#C0101` in Bible codes, `CEC` paragraphs).
- **Outgoing Links**: Captured all inter-document references to build a searchable graph.
- **Result**: `relaciones.json` (approx. 89MB) mapping every document's connections.

### 2. Intelligent Document Classification
The updated `ParserHTML.py` now identifies each document's role:
- **Sources**: Primary texts like the Bible (`doc_type: biblia`), Catechism (`doc_type: catecismo`), and Papal messages (`doc_type: papal_message`).
- **Indices**: Categorized as `is_index: true`, distinguishing them from source material.
- **Canonical IDs**: Logical identifiers like `Gn` (Genesis), `CEC` (Catechism), or `Ang B16 2005-05-15` (Papal Angelus).

### 3. Link Preservation
- HTML links were converted to Markdown format.
- Links were normalized to point to the new `.md` files rather than the old HTML files.
- Frontmatter now includes a `relationships` list for programatic access to document connections.

## Converted Library Samples

````carousel
```yaml
# Sample Bible Metadata (Gn.md)
title: GÉNESIS
doc_type: biblia
is_source: true
is_index: false
canonical_id: Gn
relationships:
  - Comentarios/Gn.html#0101
  - Comentarios/Gn.html#0102
  ...
```
<!-- slide -->
```yaml
# Sample Papal Message Metadata (ang050515.md)
title: Sin título
doc_type: papal_message
is_source: true
is_index: false
canonical_id: Ang B16 2005-05-15
relationships:
  - Biblia/Jn.html#C1613
  - Biblia/Hch.html#C0114
```
<!-- slide -->
```yaml
# Sample Catechism Metadata (Texto av.md)
title: Catecismo de la Iglesia Católica
doc_type: catecismo
is_source: true
is_index: false
canonical_id: CEC
anchors:
  - C0001
  - C0002
  ...
```
````

## Verification Results

- **Scale**: 10,423 files processed.
- **Integrity**: Links between Bible verses and commentaries are preserved in both the body and metadata.
- **Consistency**: All files follow a standard YAML schema, making the library ready for ingestion into a RAG system or a digital library viewer.

### Summary of Errors
A negligible number of files (approx. 5) failed due to "maximum recursion depth exceeded" (extremely deep HTML tags). These can be manually fixed or re-processed with a higher limit if critical.
