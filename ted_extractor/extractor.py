"""
Core TED transcript extraction functionality.
"""

import json
import requests
import time
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup

from .models import TEDTalk, TranscriptSegment
from .utils import validate_ted_url, clean_transcript_text


class TEDTranscriptExtractor:
    """
    Main class for extracting transcripts from TED talks.
    
    Features:
    - Extract transcripts from individual TED talk URLs
    - Batch processing of multiple talks
    - Multiple output formats (JSON, CSV, TXT)
    - Robust error handling and retry logic
    - Rate limiting to respect TED's servers
    """
    
    def __init__(self, 
                 delay_between_requests: float = 2.0,
                 timeout: int = 30,
                 max_retries: int = 3,
                 user_agent: str = None):
        """
        Initialize the extractor.
        
        Args:
            delay_between_requests: Seconds to wait between requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            user_agent: Custom user agent string
        """
        self.delay = delay_between_requests
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Setup session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def extract_single(self, url: str) -> TEDTalk:
        """
        Extract transcript from a single TED talk URL.
        
        Args:
            url: TED talk URL
            
        Returns:
            TEDTalk object with extracted data
        """
        talk = TEDTalk(url=url, extracted_at=datetime.now())
        
        try:
            # Validate URL
            if not validate_ted_url(url):
                talk.error_message = f"Invalid TED URL: {url}"
                return talk
            
            self.logger.info(f"Extracting transcript from: {url}")
            
            # Fetch page content
            response = self._fetch_page(url)
            if not response:
                talk.error_message = "Failed to fetch page content"
                return talk
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata and transcript
            self._extract_metadata(soup, talk)
            self._extract_transcript(soup, talk)
            
            if talk.transcript:
                talk.success = True
                talk.extraction_method = "json_parsing"
                self.logger.info(f"Successfully extracted transcript ({len(talk.transcript)} characters)")
            else:
                talk.error_message = "No transcript found"
                self.logger.warning(f"No transcript found for: {url}")
            
        except Exception as e:
            talk.error_message = f"Extraction error: {str(e)}"
            self.logger.error(f"Error extracting {url}: {e}")
        
        return talk
    
    def extract_batch(self, urls: List[str], 
                     progress_callback: Optional[callable] = None) -> List[TEDTalk]:
        """
        Extract transcripts from multiple TED talk URLs.
        
        Args:
            urls: List of TED talk URLs
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of TEDTalk objects
        """
        results = []
        total = len(urls)
        
        self.logger.info(f"Starting batch extraction of {total} talks")
        
        for i, url in enumerate(urls):
            try:
                talk = self.extract_single(url)
                results.append(talk)
                
                # Progress callback
                if progress_callback:
                    progress_callback(i + 1, total, talk)
                
                # Rate limiting
                if i < total - 1:  # Don't delay after last request
                    time.sleep(self.delay)
                    
            except Exception as e:
                self.logger.error(f"Batch extraction error for {url}: {e}")
                # Create failed talk object
                failed_talk = TEDTalk(
                    url=url,
                    extracted_at=datetime.now(),
                    error_message=f"Batch extraction error: {str(e)}"
                )
                results.append(failed_talk)
        
        successful = sum(1 for talk in results if talk.success)
        self.logger.info(f"Batch extraction completed: {successful}/{total} successful")
        
        return results
    
    def _fetch_page(self, url: str) -> Optional[requests.Response]:
        """Fetch page content with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return response
                else:
                    self.logger.warning(f"HTTP {response.status_code} for {url}, attempt {attempt + 1}")
                    
            except requests.RequestException as e:
                self.logger.warning(f"Request failed for {url}, attempt {attempt + 1}: {e}")
            
            if attempt < self.max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def _extract_metadata(self, soup: BeautifulSoup, talk: TEDTalk) -> None:
        """Extract metadata from page."""
        try:
            # Find JSON data
            script_tags = soup.find_all('script', type='application/json')
            
            for script in script_tags:
                try:
                    json_data = json.loads(script.get_text())
                    
                    # Extract from pageProps.videoData
                    if 'props' in json_data and 'pageProps' in json_data['props']:
                        video_data = json_data['props']['pageProps'].get('videoData', {})
                        
                        if video_data:
                            talk.talk_id = str(video_data.get('id', ''))
                            talk.title = video_data.get('title', '')
                            talk.speaker = video_data.get('presenterDisplayName', '')
                            talk.description = video_data.get('description', '')
                            talk.duration = video_data.get('duration')
                            talk.views = video_data.get('viewedCount')
                            talk.recorded_date = video_data.get('recordedOn', '')
                            talk.published_date = video_data.get('publishedAt', '')
                            talk.event = video_data.get('videoContext', '')
                            break
                            
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Error extracting metadata: {e}")
    
    def _extract_transcript(self, soup: BeautifulSoup, talk: TEDTalk) -> None:
        """Extract transcript from page JSON data."""
        try:
            script_tags = soup.find_all('script', type='application/json')
            
            for script in script_tags:
                try:
                    content = script.get_text()
                    
                    if 'transcript' in content.lower():
                        json_data = json.loads(content)
                        
                        # Navigate to transcript data
                        if 'props' in json_data and 'pageProps' in json_data['props']:
                            transcript_data = json_data['props']['pageProps'].get('transcriptData')
                            
                            if transcript_data and isinstance(transcript_data, dict):
                                translation = transcript_data.get('translation')
                                
                                if translation and isinstance(translation, dict):
                                    paragraphs = translation.get('paragraphs')
                                    
                                    if paragraphs and isinstance(paragraphs, list):
                                        transcript_parts = []
                                        segments = []
                                        
                                        for para_idx, paragraph in enumerate(paragraphs):
                                            if isinstance(paragraph, dict):
                                                cues = paragraph.get('cues')
                                                
                                                if cues and isinstance(cues, list):
                                                    paragraph_text = []
                                                    
                                                    for cue in cues:
                                                        if isinstance(cue, dict):
                                                            text = cue.get('text', '').strip()
                                                            if text:
                                                                paragraph_text.append(text)
                                                                
                                                                # Create segment
                                                                segment = TranscriptSegment(
                                                                    text=text,
                                                                    start_time=cue.get('startTime'),
                                                                    end_time=cue.get('endTime'),
                                                                    paragraph_index=para_idx
                                                                )
                                                                segments.append(segment)
                                                    
                                                    if paragraph_text:
                                                        transcript_parts.append(' '.join(paragraph_text))
                                        
                                        if transcript_parts:
                                            talk.transcript = '\n\n'.join(transcript_parts)
                                            talk.transcript_segments = segments
                                            
                                            # Clean transcript
                                            talk.transcript = clean_transcript_text(talk.transcript)
                                            
                                            # Extract language info
                                            lang_info = translation.get('language', {})
                                            if isinstance(lang_info, dict):
                                                talk.language = lang_info.get('languageCode', 'en')
                                            
                                            return
                                            
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Error extracting transcript: {e}")
    
    def save_results(self, talks: List[TEDTalk], 
                    output_file: str, 
                    format: str = 'json') -> str:
        """
        Save extraction results to file.
        
        Args:
            talks: List of TEDTalk objects
            output_file: Output file path
            format: Output format ('json', 'csv', 'txt')
            
        Returns:
            Path to saved file
        """
        if format.lower() == 'json':
            return self._save_json(talks, output_file)
        elif format.lower() == 'csv':
            return self._save_csv(talks, output_file)
        elif format.lower() == 'txt':
            return self._save_txt(talks, output_file)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _save_json(self, talks: List[TEDTalk], output_file: str) -> str:
        """Save results as JSON."""
        import json
        
        data = [talk.to_dict() for talk in talks]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def _save_csv(self, talks: List[TEDTalk], output_file: str) -> str:
        """Save results as CSV."""
        import pandas as pd
        
        data = []
        for talk in talks:
            row = talk.to_dict()
            # Flatten transcript_segments for CSV
            if row.get('transcript_segments'):
                row['transcript_segments'] = str(len(row['transcript_segments']))
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        return output_file
    
    def _save_txt(self, talks: List[TEDTalk], output_file: str) -> str:
        """Save transcripts as plain text."""
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, talk in enumerate(talks):
                if talk.success and talk.transcript:
                    f.write(f"=== TED Talk {i+1} ===\n")
                    f.write(f"Title: {talk.title or 'Unknown'}\n")
                    f.write(f"Speaker: {talk.speaker or 'Unknown'}\n")
                    f.write(f"URL: {talk.url}\n")
                    f.write(f"Duration: {talk.duration or 'Unknown'} seconds\n")
                    f.write(f"Views: {talk.views or 'Unknown'}\n")
                    f.write("\n--- Transcript ---\n")
                    f.write(talk.transcript)
                    f.write("\n\n" + "="*50 + "\n\n")
        
        return output_file
