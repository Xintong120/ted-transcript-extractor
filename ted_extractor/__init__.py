"""
TED Transcript Extractor

A Python library for extracting transcripts from TED talks.
Supports single talk extraction, batch processing, and multiple output formats.
"""

from .extractor import TEDTranscriptExtractor
from .models import TEDTalk, TranscriptSegment
from .utils import validate_ted_url, clean_transcript_text

__version__ = "1.0.0"
__author__ = "Xintong120"
__email__ = "lxt2002120@gmail.com"

__all__ = [
    "TEDTranscriptExtractor",
    "TEDTalk", 
    "TranscriptSegment",
    "validate_ted_url",
    "clean_transcript_text"
]
