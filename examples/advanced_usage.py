"""
Advanced usage examples for TED Transcript Extractor.
"""

import logging
from pathlib import Path
from ted_extractor import TEDTranscriptExtractor
from ted_extractor.utils import get_ted_urls_from_text, format_duration


def example_custom_extractor():
    """Example: Create extractor with custom configuration."""
    print("=== Custom Extractor Configuration ===")
    
    # Custom extractor with specific settings
    extractor = TEDTranscriptExtractor(
        delay_between_requests=0.5,  # Faster requests
        timeout=60,                  # Longer timeout
        max_retries=5,              # More retries
        user_agent="MyApp/1.0 TED-Extractor"  # Custom user agent
    )
    
    url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(url)
    
    if talk.success:
        print(f"Extracted with custom settings: {talk.title}")
        print(f"Extraction method: {talk.extraction_method}")
        print(f"Extracted at: {talk.extracted_at}")


def example_url_extraction():
    """Example: Extract TED URLs from text content."""
    print("\n=== URL Extraction from Text ===")
    
    # Sample text with TED URLs
    text = """
    Check out these amazing TED talks:
    1. Brené Brown on vulnerability: https://www.ted.com/talks/brene_brown_the_power_of_vulnerability
    2. Simon Sinek on leadership: https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action
    3. Amy Cuddy on body language: https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are
    
    Also check out this non-TED link: https://www.youtube.com/watch?v=example
    """
    
    # Extract TED URLs
    ted_urls = get_ted_urls_from_text(text)
    
    print(f"Found {len(ted_urls)} TED URLs:")
    for i, url in enumerate(ted_urls, 1):
        print(f"  {i}. {url}")
    
    # Extract transcripts from found URLs
    if ted_urls:
        extractor = TEDTranscriptExtractor(delay_between_requests=1.0)
        talks = extractor.extract_batch(ted_urls[:2])  # Limit to first 2 for demo
        
        successful = [talk for talk in talks if talk.success]
        print(f"\nSuccessfully extracted {len(successful)} transcripts")


def example_file_processing():
    """Example: Process URLs from file and save results."""
    print("\n=== File Processing ===")
    
    # Create sample URL file
    urls_file = Path("sample_urls.txt")
    sample_urls = [
        "# TED Talks for processing",
        "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
        "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action",
        "",  # Empty line
        "# This is a comment and will be ignored",
        "https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are"
    ]
    
    # Write URLs to file
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_urls))
    
    print(f"Created sample file: {urls_file}")
    
    # Read and process URLs
    valid_urls = []
    with open(urls_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith('http'):
                    valid_urls.append(line)
    
    print(f"Found {len(valid_urls)} valid URLs in file")
    
    # Extract transcripts
    extractor = TEDTranscriptExtractor()
    talks = extractor.extract_batch(valid_urls[:1])  # Limit for demo
    
    # Save results in multiple formats
    if talks:
        extractor.save_results(talks, "batch_results.json", "json")
        extractor.save_results(talks, "batch_results.csv", "csv")
        print("Results saved in JSON and CSV formats")
    
    # Cleanup
    urls_file.unlink()


def example_logging_configuration():
    """Example: Configure detailed logging."""
    print("\n=== Logging Configuration ===")
    
    # Setup detailed logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ted_extractor.log'),
            logging.StreamHandler()
        ]
    )
    
    # Create extractor
    extractor = TEDTranscriptExtractor()
    
    # Extract with logging
    url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(url)
    
    if talk.success:
        print(f"Extraction logged: {talk.title}")
        print("Check 'ted_extractor.log' for detailed logs")


def example_transcript_segments():
    """Example: Work with transcript segments."""
    print("\n=== Transcript Segments ===")
    
    extractor = TEDTranscriptExtractor()
    
    url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(url)
    
    if talk.success and talk.transcript_segments:
        print(f"Talk has {len(talk.transcript_segments)} transcript segments")
        
        # Show first few segments
        print("\nFirst 5 segments:")
        for i, segment in enumerate(talk.transcript_segments[:5]):
            print(f"  {i+1}. [{segment.start_time}s] {segment.text[:50]}...")
        
        # Find segments with specific words
        keyword = "vulnerability"
        matching_segments = [
            seg for seg in talk.transcript_segments 
            if keyword.lower() in seg.text.lower()
        ]
        
        print(f"\nFound {len(matching_segments)} segments containing '{keyword}':")
        for segment in matching_segments[:3]:  # Show first 3
            print(f"  [{segment.start_time}s] {segment.text}")


def example_batch_with_progress():
    """Example: Batch processing with detailed progress tracking."""
    print("\n=== Batch Processing with Progress ===")
    
    urls = [
        "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
        "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action"
    ]
    
    # Custom progress callback
    def detailed_progress(current, total, talk):
        print(f"\n[{current}/{total}] Processing: {talk.url}")
        
        if talk.success:
            print(f"  SUCCESS: {talk.title}")
            print(f"  Speaker: {talk.speaker}")
            print(f"  Duration: {format_duration(talk.duration or 0)}")
            print(f"  Views: {talk.views:,}" if talk.views else "  Views: Unknown")
            print(f"  Transcript: {len(talk.transcript)} characters")
            print(f"  Word count: {talk.get_word_count()}")
        else:
            print(f"  FAILED: {talk.error_message}")
    
    # Extract with progress tracking
    extractor = TEDTranscriptExtractor(delay_between_requests=1.0)
    talks = extractor.extract_batch(urls, detailed_progress)
    
    # Final summary
    successful = [talk for talk in talks if talk.success]
    total_words = sum(talk.get_word_count() for talk in successful)
    total_duration = sum(talk.duration or 0 for talk in successful)
    
    print(f"\n=== Final Summary ===")
    print(f"Total talks processed: {len(talks)}")
    print(f"Successful extractions: {len(successful)}")
    print(f"Total words extracted: {total_words:,}")
    print(f"Total duration: {format_duration(total_duration)}")


def example_error_recovery():
    """Example: Handle various error scenarios."""
    print("\n=== Error Recovery ===")
    
    # Mix of valid and invalid URLs
    urls = [
        "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",  # Valid
        "https://www.ted.com/talks/nonexistent_talk_12345",                  # Invalid
        "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action",  # Valid
        "https://invalid-domain.com/talks/something",                        # Invalid domain
    ]
    
    extractor = TEDTranscriptExtractor(max_retries=2)
    
    def error_tracking_progress(current, total, talk):
        status = "SUCCESS" if talk.success else "FAILED"
        print(f"[{current}/{total}] {status}: {talk.url}")
        
        if not talk.success:
            print(f"  Error: {talk.error_message}")
    
    talks = extractor.extract_batch(urls, error_tracking_progress)
    
    # Analyze results
    successful = [talk for talk in talks if talk.success]
    failed = [talk for talk in talks if not talk.success]
    
    print(f"\nResults:")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    
    if failed:
        print(f"\nFailure reasons:")
        for talk in failed:
            print(f"  {talk.url}: {talk.error_message}")


if __name__ == "__main__":
    # Run advanced examples
    example_custom_extractor()
    example_url_extraction()
    example_file_processing()
    example_logging_configuration()
    example_transcript_segments()
    example_batch_with_progress()
    example_error_recovery()
