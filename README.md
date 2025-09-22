# TED Transcript Extractor

A powerful Python library for extracting transcripts from TED talks. Extract transcripts from individual talks or process multiple talks in batch with support for various output formats.

> **Note**: This project is adapted from [corralm/ted-scraper](https://github.com/corralm/ted-scraper) and updated to work with the current TED website structure.

## Features

- **Single Talk Extraction**: Extract transcript from any TED talk URL
- **Batch Processing**: Process multiple TED talks efficiently
- **Multiple Output Formats**: Save results as JSON, CSV, or plain text
- **Robust Error Handling**: Graceful handling of network issues and invalid URLs
- **Rate Limiting**: Respectful request timing to avoid overwhelming TED servers
- **Detailed Metadata**: Extract talk information including title, speaker, duration, views, etc.
- **Transcript Segments**: Access individual transcript segments with timing information
- **Command Line Interface**: Easy-to-use CLI for quick extractions
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Installation

### From Source

```bash
git clone https://github.com/Xintong120/ted-transcript-extractor.git
cd ted-transcript-extractor
pip install -r requirements.txt
```

### Using pip (when published)

```bash
pip install ted-transcript-extractor
```

## Quick Start

### Basic Usage

```python
from ted_extractor import TEDTranscriptExtractor

# Initialize extractor
extractor = TEDTranscriptExtractor()

# Extract transcript from a single TED talk
url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
talk = extractor.extract_single(url)

if talk.success:
    print(f"Title: {talk.title}")
    print(f"Speaker: {talk.speaker}")
    print(f"Transcript: {talk.transcript[:200]}...")
else:
    print(f"Failed: {talk.error_message}")
```

### Batch Processing

```python
# Extract multiple talks
urls = [
    "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
    "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action",
    "https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are"
]

talks = extractor.extract_batch(urls)

# Save results
extractor.save_results(talks, "results.json", "json")
extractor.save_results(talks, "results.csv", "csv")
```

### Command Line Interface

```bash
# Extract single talk
python -m ted_extractor.cli --url "https://www.ted.com/talks/..." --output results.json

# Batch extract from file
python -m ted_extractor.cli --file urls.txt --output results.csv --format csv

# With custom settings
python -m ted_extractor.cli --url "..." --delay 3 --timeout 60 --verbose
```

### Interactive Extractor

For a user-friendly interactive experience, use the interactive extractor:

```bash
# Run interactive extractor
python examples/interactive_extractor.py
```

Features:
- **Interactive Interface**: Easy-to-use command-line interface
- **Single & Batch Extraction**: Extract one or multiple talks
- **Multiple Output Formats**: Save as JSON, CSV, or TXT
- **Extraction History**: View and manage extracted talks
- **Auto-save Options**: Automatically save individual files
- **Chinese/English Support**: Bilingual interface

## API Reference

### TEDTranscriptExtractor

Main class for extracting TED transcripts.

#### Constructor

```python
TEDTranscriptExtractor(
    delay_between_requests=2.0,  # Seconds between requests
    timeout=30,                  # Request timeout
    max_retries=3,              # Maximum retry attempts
    user_agent=None             # Custom user agent
)
```

#### Methods

- `extract_single(url: str) -> TEDTalk`: Extract transcript from single URL
- `extract_batch(urls: List[str], progress_callback=None) -> List[TEDTalk]`: Extract from multiple URLs
- `save_results(talks: List[TEDTalk], output_file: str, format: str) -> str`: Save results to file

### TEDTalk

Data model representing a TED talk with metadata and transcript.

#### Properties

- `url`: TED talk URL
- `title`: Talk title
- `speaker`: Speaker name
- `description`: Talk description
- `duration`: Duration in seconds
- `views`: View count
- `transcript`: Full transcript text
- `transcript_segments`: List of transcript segments with timing
- `success`: Whether extraction was successful
- `error_message`: Error message if extraction failed

#### Methods

- `get_clean_transcript() -> str`: Get cleaned transcript text
- `get_word_count() -> int`: Get word count
- `get_reading_time_minutes(wpm=200) -> float`: Estimate reading time
- `to_dict() -> dict`: Convert to dictionary for serialization

## Examples

See the `examples/` directory for comprehensive usage examples:

- `basic_usage.py`: Basic extraction and processing
- `advanced_usage.py`: Advanced features and configurations
- `interactive_extractor.py`: Interactive command-line interface for easy extraction

## Configuration

### Custom Extractor Settings

```python
extractor = TEDTranscriptExtractor(
    delay_between_requests=1.0,  # Faster requests
    timeout=60,                  # Longer timeout
    max_retries=5,              # More retries
    user_agent="MyApp/1.0"      # Custom user agent
)
```

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Output Formats

### JSON Format

```json
{
  "url": "https://www.ted.com/talks/...",
  "title": "Talk Title",
  "speaker": "Speaker Name",
  "duration": 1234,
  "views": 1000000,
  "transcript": "Full transcript text...",
  "success": true,
  "extracted_at": "2024-01-01T12:00:00"
}
```

### CSV Format

Tabular format with columns for all metadata fields and transcript text.

### TXT Format

Plain text format with talk metadata and full transcript.

## Error Handling

The library includes comprehensive error handling:

- **Network Issues**: Automatic retries with exponential backoff
- **Invalid URLs**: Validation and clear error messages
- **Missing Transcripts**: Graceful handling of talks without transcripts
- **Rate Limiting**: Built-in delays to respect server limits

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/Xintong120/ted-transcript-extractor.git
cd ted-transcript-extractor

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run examples
python examples/basic_usage.py

# Run interactive extractor
python examples/interactive_extractor.py
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- pandas (for CSV output)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes. Please respect TED's terms of service and use responsibly. The authors are not affiliated with TED.

## Changelog

### Version 1.0.0
- Initial release
- Single and batch transcript extraction
- Multiple output formats (JSON, CSV, TXT)
- Command line interface
- Comprehensive error handling
- Rate limiting and retry logic

## Support

If you encounter any issues or have questions:

1. Check the [examples](examples/) for usage patterns
2. Review the [API documentation](#api-reference)
3. Open an issue on GitHub

## Acknowledgments

- TED for providing amazing talks and transcripts
- [corralm/ted-scraper](https://github.com/corralm/ted-scraper) - This project is adapted from the original TED scraper, updated to work with current TED website structure
- The open-source community for inspiration and tools
