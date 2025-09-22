# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release of TED Transcript Extractor
- Core transcript extraction functionality from TED talk URLs
- Support for single talk extraction via `extract_single()` method
- Batch processing capabilities via `extract_batch()` method
- Multiple output formats: JSON, CSV, and plain text
- Comprehensive data model with `TEDTalk` and `TranscriptSegment` classes
- Robust error handling and retry logic with exponential backoff
- Rate limiting to respect TED's servers (configurable delay between requests)
- Command-line interface for easy usage
- Detailed logging and progress tracking
- Transcript segment extraction with timing information
- Metadata extraction including title, speaker, duration, views, etc.
- URL validation and cleaning utilities
- Comprehensive documentation and examples
- MIT license

### Features
- **Single Talk Extraction**: Extract transcript from any TED talk URL
- **Batch Processing**: Process multiple TED talks efficiently with progress callbacks
- **Multiple Output Formats**: Save results as JSON, CSV, or plain text
- **Robust Error Handling**: Graceful handling of network issues and invalid URLs
- **Rate Limiting**: Configurable delays between requests (default: 2 seconds)
- **Retry Logic**: Automatic retries with exponential backoff (default: 3 attempts)
- **Detailed Metadata**: Extract comprehensive talk information
- **Transcript Segments**: Access individual segments with timing data
- **Command Line Interface**: Easy-to-use CLI with multiple options
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **URL Validation**: Automatic validation of TED talk URLs
- **Text Cleaning**: Automatic cleaning and normalization of transcript text

### Technical Details
- Python 3.7+ compatibility
- Dependencies: requests, beautifulsoup4, pandas, lxml
- Modular architecture with separate modules for extraction, models, and utilities
- Comprehensive test coverage (planned for future releases)
- Type hints throughout the codebase
- Configurable user agents and request settings

### Examples Included
- Basic usage examples demonstrating core functionality
- Advanced usage examples showing custom configurations
- Command-line usage examples
- Error handling demonstrations
- Batch processing with progress tracking

### Documentation
- Comprehensive README with installation and usage instructions
- API reference documentation
- Example code for common use cases
- Contributing guidelines
- MIT license

## [Unreleased]

### Planned Features
- Unit tests and test coverage
- Support for additional TED content types
- Async/await support for improved performance
- Caching mechanisms for repeated requests
- Export to additional formats (XML, YAML)
- Integration with popular NLP libraries
- Docker containerization
- GitHub Actions CI/CD pipeline
