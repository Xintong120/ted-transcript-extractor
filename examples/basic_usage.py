"""
Basic usage examples for TED Transcript Extractor.
"""

from ted_extractor import TEDTranscriptExtractor


def example_single_extraction():
    """Example: Extract transcript from a single TED talk."""
    print("=== Single Talk Extraction ===")
    
    # Initialize extractor
    extractor = TEDTranscriptExtractor()
    
    # Extract transcript
    url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(url)
    
    if talk.success:
        print(f"Title: {talk.title}")
        print(f"Speaker: {talk.speaker}")
        print(f"Duration: {talk.duration} seconds")
        print(f"Views: {talk.views:,}")
        print(f"Transcript length: {len(talk.transcript)} characters")
        print(f"Word count: {talk.get_word_count()}")
        print(f"Reading time: {talk.get_reading_time_minutes():.1f} minutes")
        
        # Show transcript preview
        print("\n--- Transcript Preview ---")
        print(talk.transcript[:300] + "...")
    else:
        print(f"Failed to extract: {talk.error_message}")


def example_batch_extraction():
    """Example: Extract transcripts from multiple TED talks."""
    print("\n=== Batch Extraction ===")
    
    # List of TED talk URLs
    urls = [
        "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
        "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action",
        "https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are"
    ]
    
    # Initialize extractor with custom settings
    extractor = TEDTranscriptExtractor(
        delay_between_requests=1.0,  # Faster for demo
        timeout=30,
        max_retries=2
    )
    
    # Progress callback
    def progress_callback(current, total, talk):
        status = "SUCCESS" if talk.success else "FAILED"
        print(f"[{current}/{total}] {status}: {talk.title or 'Unknown'}")
    
    # Extract transcripts
    talks = extractor.extract_batch(urls, progress_callback)
    
    # Summary
    successful = [talk for talk in talks if talk.success]
    print(f"\nExtracted {len(successful)}/{len(talks)} transcripts successfully")
    
    # Show results
    for talk in successful:
        print(f"\n- {talk.title}")
        print(f"  Speaker: {talk.speaker}")
        print(f"  Words: {talk.get_word_count()}")


def example_save_results():
    """Example: Save extraction results in different formats."""
    print("\n=== Save Results ===")
    
    extractor = TEDTranscriptExtractor()
    
    # Extract a talk
    url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(url)
    
    if talk.success:
        # Save as JSON
        json_file = extractor.save_results([talk], "results.json", "json")
        print(f"Saved JSON: {json_file}")
        
        # Save as CSV
        csv_file = extractor.save_results([talk], "results.csv", "csv")
        print(f"Saved CSV: {csv_file}")
        
        # Save as TXT
        txt_file = extractor.save_results([talk], "results.txt", "txt")
        print(f"Saved TXT: {txt_file}")


def example_error_handling():
    """Example: Handle extraction errors gracefully."""
    print("\n=== Error Handling ===")
    
    extractor = TEDTranscriptExtractor()
    
    # Try invalid URL
    invalid_url = "https://www.ted.com/talks/nonexistent_talk"
    talk = extractor.extract_single(invalid_url)
    
    if not talk.success:
        print(f"Expected failure: {talk.error_message}")
    
    # Try valid URL with transcript
    valid_url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(valid_url)
    
    if talk.success:
        print(f"Success: {talk.title}")
    else:
        print(f"Unexpected failure: {talk.error_message}")


def example_transcript_analysis():
    """Example: Analyze extracted transcript."""
    print("\n=== Transcript Analysis ===")
    
    extractor = TEDTranscriptExtractor()
    
    url = "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
    talk = extractor.extract_single(url)
    
    if talk.success:
        print(f"Talk: {talk.title}")
        print(f"Speaker: {talk.speaker}")
        print(f"Language: {talk.language}")
        
        # Basic statistics
        transcript = talk.get_clean_transcript()
        words = transcript.split()
        sentences = transcript.split('.')
        
        print(f"\nStatistics:")
        print(f"  Characters: {len(transcript):,}")
        print(f"  Words: {len(words):,}")
        print(f"  Sentences: {len(sentences):,}")
        print(f"  Avg words per sentence: {len(words)/len(sentences):.1f}")
        print(f"  Reading time: {talk.get_reading_time_minutes():.1f} minutes")
        
        # Word frequency (top 10)
        from collections import Counter
        word_freq = Counter(word.lower().strip('.,!?";') for word in words if len(word) > 3)
        
        print(f"\nTop 10 words:")
        for word, count in word_freq.most_common(10):
            print(f"  {word}: {count}")


if __name__ == "__main__":
    # Run all examples
    example_single_extraction()
    example_batch_extraction()
    example_save_results()
    example_error_handling()
    example_transcript_analysis()
