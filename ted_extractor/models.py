"""
Data models for TED transcript extraction.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class TranscriptSegment:
    """Represents a single segment of transcript text."""
    text: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    paragraph_index: Optional[int] = None


@dataclass
class TEDTalk:
    """Represents a complete TED talk with metadata and transcript."""
    
    # Basic information
    url: str
    title: Optional[str] = None
    speaker: Optional[str] = None
    talk_id: Optional[str] = None
    
    # Metadata
    description: Optional[str] = None
    duration: Optional[int] = None  # in seconds
    views: Optional[int] = None
    recorded_date: Optional[str] = None
    published_date: Optional[str] = None
    event: Optional[str] = None
    
    # Transcript data
    transcript: Optional[str] = None
    transcript_segments: Optional[List[TranscriptSegment]] = None
    language: Optional[str] = None
    
    # Processing metadata
    extracted_at: Optional[datetime] = None
    extraction_method: Optional[str] = None
    success: bool = False
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, list) and value and isinstance(value[0], TranscriptSegment):
                result[key] = [segment.__dict__ for segment in value]
            else:
                result[key] = value
        return result
    
    def get_clean_transcript(self) -> str:
        """Get transcript with basic cleaning applied."""
        if not self.transcript:
            return ""
        
        # Remove extra whitespace and normalize line breaks
        cleaned = self.transcript.strip()
        cleaned = '\n'.join(line.strip() for line in cleaned.split('\n') if line.strip())
        
        return cleaned
    
    def get_word_count(self) -> int:
        """Get approximate word count of transcript."""
        if not self.transcript:
            return 0
        return len(self.transcript.split())
    
    def get_reading_time_minutes(self, words_per_minute: int = 200) -> float:
        """Estimate reading time in minutes."""
        word_count = self.get_word_count()
        return word_count / words_per_minute if word_count > 0 else 0.0
