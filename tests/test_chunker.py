import pytest
import os
from unittest.mock import MagicMock
from narrative_chunker import NarrativeChunker

def test_narrative_chunker_initialization():
    chunker = NarrativeChunker(chunk_size=500, chunk_overlap=50)
    assert chunker.chunk_size == 500
    assert chunker.chunk_overlap == 50
    assert chunker.parser is not None

def test_narrative_chunker_custom_parser():
    mock_parser = MagicMock()
    chunker = NarrativeChunker(parser=mock_parser)
    assert chunker.parser == mock_parser

def test_parse_and_chunk_with_metadata(tmp_path):
    # Setup a dummy text file
    dummy_file = tmp_path / "dummy.txt"
    dummy_file.write_text("Hello world.")
    
    chunker = NarrativeChunker(chunk_size=500)
    
    custom_metadata = {
        "tenant_id": "ABC-123",
        "doc_type": "contract"
    }
    
    # The read natively should work and attach metadata
    nodes = chunker.parse_and_chunk(
        file_path=str(dummy_file), 
        filename="dummy.txt", 
        metadata=custom_metadata
    )
    
    assert len(nodes) > 0
    node = nodes[0]
    
    # Assert custom dictionary properties were safely stamped
    assert node.metadata.get("tenant_id") == "ABC-123"
    assert node.metadata.get("doc_type") == "contract"
    assert node.metadata.get("filename") == "dummy.txt"
