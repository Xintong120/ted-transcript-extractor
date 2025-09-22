"""
Command-line interface for TED transcript extraction.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

from .extractor import TEDTranscriptExtractor
from .utils import validate_ted_url, get_ted_urls_from_text


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def progress_callback(current: int, total: int, talk) -> None:
    """Progress callback for batch processing."""
    status = "SUCCESS" if talk.success else "FAILED"
    print(f"[{current}/{total}] {talk.url} - {status}")
    
    if talk.success and talk.transcript:
        print(f"  Title: {talk.title}")
        print(f"  Speaker: {talk.speaker}")
        print(f"  Transcript: {len(talk.transcript)} characters")
    elif talk.error_message:
        print(f"  Error: {talk.error_message}")


def extract_single_talk(args) -> None:
    """Extract transcript from a single TED talk."""
    if not validate_ted_url(args.url):
        print(f"Error: Invalid TED URL: {args.url}")
        sys.exit(1)
    
    extractor = TEDTranscriptExtractor(
        delay_between_requests=args.delay,
        timeout=args.timeout,
        max_retries=args.retries
    )
    
    print(f"Extracting transcript from: {args.url}")
    talk = extractor.extract_single(args.url)
    
    if talk.success:
        print(f"SUCCESS: Extracted transcript ({len(talk.transcript)} characters)")
        print(f"Title: {talk.title}")
        print(f"Speaker: {talk.speaker}")
        print(f"Duration: {talk.duration} seconds")
        print(f"Views: {talk.views}")
        
        # Save results
        if args.output:
            output_file = extractor.save_results([talk], args.output, args.format)
            print(f"Results saved to: {output_file}")
        
        # Print transcript preview
        if args.preview and talk.transcript:
            print("\n--- Transcript Preview ---")
            print(talk.transcript[:500] + "..." if len(talk.transcript) > 500 else talk.transcript)
    else:
        print(f"FAILED: {talk.error_message}")
        sys.exit(1)


def extract_batch_talks(args) -> None:
    """Extract transcripts from multiple TED talks."""
    # Read URLs from file
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Extract URLs from content
    urls = []
    for line in content.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):  # Skip comments
            if validate_ted_url(line):
                urls.append(line)
            else:
                # Try to extract URLs from text
                found_urls = get_ted_urls_from_text(line)
                urls.extend(found_urls)
    
    if not urls:
        print("Error: No valid TED URLs found in file")
        sys.exit(1)
    
    print(f"Found {len(urls)} TED talk URLs")
    
    # Extract transcripts
    extractor = TEDTranscriptExtractor(
        delay_between_requests=args.delay,
        timeout=args.timeout,
        max_retries=args.retries
    )
    
    talks = extractor.extract_batch(urls, progress_callback if args.verbose else None)
    
    # Summary
    successful = sum(1 for talk in talks if talk.success)
    print(f"\nBatch extraction completed:")
    print(f"  Total: {len(talks)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(talks) - successful}")
    
    # Save results
    if args.output:
        output_file = extractor.save_results(talks, args.output, args.format)
        print(f"Results saved to: {output_file}")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract transcripts from TED talks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract single talk
  ted-extractor --url "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability"
  
  # Extract and save as JSON
  ted-extractor --url "https://www.ted.com/talks/..." --output results.json
  
  # Batch extract from file
  ted-extractor --file urls.txt --output results.csv --format csv
  
  # Extract with custom settings
  ted-extractor --url "..." --delay 3 --timeout 60 --retries 5 --verbose
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--url', help='Single TED talk URL to extract')
    input_group.add_argument('--file', help='File containing TED talk URLs (one per line)')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'txt'], 
                       default='json', help='Output format (default: json)')
    
    # Extraction options
    parser.add_argument('--delay', type=float, default=2.0,
                       help='Delay between requests in seconds (default: 2.0)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds (default: 30)')
    parser.add_argument('--retries', type=int, default=3,
                       help='Maximum retry attempts (default: 3)')
    
    # Display options
    parser.add_argument('--preview', action='store_true',
                       help='Show transcript preview for single extractions')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Execute based on input type
    if args.url:
        extract_single_talk(args)
    elif args.file:
        extract_batch_talks(args)


if __name__ == '__main__':
    main()
