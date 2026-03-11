# Narrative Chunker

**Narrative Chunker** is a semantic NLP metadata orchestration library designed to prepare documents for high-quality Vector indexing.

Instead of arbitrarily slicing documents by strict token limits—which often cuts sentences in half and ruins semantic meaning—`Narrative Chunker` intelligently isolates content by boundaries (like punctuation and paragraphs). Furthermore, it provides native metadata injection, automatically stamping arbitrary context dictionaries directly onto the resulting AST nodes.

## Features
- ✂️ **Semantic Splitting**: Preserves sentence boundaries and narrative flow using customizable sizes and overlaps.
- 📦 **Metadata Orchestration**: Pass a custom python Dictionary, and the chunker will deterministically stamp it onto every resulting node without requiring you to manually loop over trees.
- 🔌 **Interface Agnostic**: Override the default `SentenceSplitter` and `SimpleDirectoryReader` by pushing your own parsers directly into the API (e.g., PyPDF or MarkdownNodeParser).

## Installation
```bash
pip install narrative-chunker
```

## Quick Start

### 1. Basic Narrative Splitting
Parse a physical file natively:

```python
from narrative_chunker import NarrativeChunker

chunker = NarrativeChunker(chunk_size=1024, chunk_overlap=200)
nodes = chunker.parse_and_chunk(file_path="novel.epub", filename="novel.epub")

print(f"Generated {len(nodes)} perfectly sliced context nodes.")
```

### 2. Multi-Tenant Metadata Injection
Easily attach user identifiers or domain context straight into the LlamaIndex schema for downstream Vector filtering:

```python
context = {
    "tenant_id": "ABC-123",
    "access_level": "confidential"
}

nodes = chunker.parse_and_chunk(
    file_path="contract.pdf", 
    filename="contract.pdf", 
    metadata=context
)

# Every extracted chunk natively contains {'tenant_id': 'ABC-123', ...} in its metadata!
```

### 3. Customizable Chunking Algorithms
By default, `NarrativeChunker` uses a robust `SentenceSplitter`. However, you can seamlessly inject **any** LlamaIndex `NodeParser` algorithm into the constructor to adapt to your specific domain (e.g., Semantic Chunking, Token Splitting, or Markdown Splitting):

```python
from narrative_chunker import NarrativeChunker
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. Initialize a state-of-the-art semantic AI chunker
embed_model = OpenAIEmbedding(model="text-embedding-3-small", embed_batch_size=100)
semantic_parser = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)

# 2. Inject the semantic algorithm into the Narrative orchestrator
chunker = NarrativeChunker(parser=semantic_parser)

# 3. All chunks will now be intelligently sliced by semantic cosine-similarity!
nodes = chunker.parse_and_chunk(file_path="dune.epub", filename="dune.epub")
```
