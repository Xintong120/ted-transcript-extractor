"""
Utility functions for TED transcript extraction.
"""

import re
from typing import List
from urllib.parse import urlparse


def validate_ted_url(url: str) -> bool:
    """
    Validate if URL is a valid TED talk URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid TED URL, False otherwise
    """
    try:
        parsed = urlparse(url)
        
        # Check domain
        if parsed.netloc not in ['www.ted.com', 'ted.com']:
            return False
        
        # Check path pattern
        if not parsed.path.startswith('/talks/'):
            return False
        
        return True
        
    except Exception:
        return False


def clean_transcript_text(text: str) -> str:
    """
    Clean and normalize transcript text.
    
    Args:
        text: Raw transcript text
        
    Returns:
        Cleaned transcript text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove multiple consecutive line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Clean up common transcript artifacts
    text = re.sub(r'\(Laughter\)\s*', '(Laughter)\n\n', text)
    text = re.sub(r'\(Applause\)\s*', '(Applause)\n\n', text)
    text = re.sub(r'\(Music\)\s*', '(Music)\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_talk_id_from_url(url: str) -> str:
    """
    Extract talk ID/slug from TED URL.
    
    Args:
        url: TED talk URL
        
    Returns:
        Talk ID/slug or empty string if not found
    """
    try:
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) >= 2 and path_parts[0] == 'talks':
            return path_parts[1]
        
        return ""
        
    except Exception:
        return ""


def get_ted_urls_from_text(text: str) -> List[str]:
    """
    Extract TED URLs from text using regex.
    
    Args:
        text: Text containing potential TED URLs
        
    Returns:
        List of valid TED URLs found in text
    """
    # Regex pattern for TED URLs
    pattern = r'https?://(?:www\.)?ted\.com/talks/[^\s<>"\']+'
    
    urls = re.findall(pattern, text)
    
    # Validate each URL
    valid_urls = [url for url in urls if validate_ted_url(url)]
    
    return valid_urls


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "12:34")
    """
    if not seconds or seconds < 0:
        return "0:00"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    return f"{minutes}:{remaining_seconds:02d}"


def estimate_reading_time(text: str, words_per_minute: int = 200) -> float:
    """
    Estimate reading time for text.
    
    Args:
        text: Text to analyze
        words_per_minute: Average reading speed
        
    Returns:
        Estimated reading time in minutes
    """
    if not text:
        return 0.0
    
    word_count = len(text.split())
    return word_count / words_per_minute


def get_language_name(language_code: str) -> str:
    """
    Get full language name from language code.
    
    Args:
        language_code: ISO language code (e.g., 'en', 'es')
        
    Returns:
        Full language name
    """
    language_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'tr': 'Turkish',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'da': 'Danish',
        'no': 'Norwegian',
        'fi': 'Finnish',
        'pl': 'Polish',
        'cs': 'Czech',
        'hu': 'Hungarian',
        'ro': 'Romanian',
        'bg': 'Bulgarian',
        'hr': 'Croatian',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'et': 'Estonian',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
        'mt': 'Maltese',
        'el': 'Greek',
        'cy': 'Welsh',
        'ga': 'Irish',
        'eu': 'Basque',
        'ca': 'Catalan',
        'gl': 'Galician',
        'pt-br': 'Portuguese (Brazilian)',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)'
    }
    
    return language_map.get(language_code.lower(), language_code.upper())
