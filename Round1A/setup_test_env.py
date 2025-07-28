#!/usr/bin/env python3
"""
Setup script to create test environment and directories
"""

import os
import json

def setup_test_directories():
    """Create input and output directories for testing"""
    directories = ["input", "output", "test_results"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create a sample expected output for reference
    sample_expected = {
        "title": "Sample Document",
        "outline": [
            {"level": "H1", "text": "Chapter 1: Introduction", "page": 1},
            {"level": "H2", "text": "1.1 Overview", "page": 1},
            {"level": "H3", "text": "1.1.1 Background", "page": 2},
            {"level": "H1", "text": "Chapter 2: Methodology", "page": 3},
            {"level": "H2", "text": "2.1 Approach", "page": 3}
        ]
    }
    
    with open("sample_expected.json", "w", encoding="utf-8") as f:
        json.dump(sample_expected, f, indent=2, ensure_ascii=False)
    
    print("Created sample_expected.json for reference")
    
    # Create instructions file
    instructions = """
# Testing Instructions

## Manual Testing Steps:

1. Place your PDF files in the 'input' directory
2. Run the extraction:
   python extract_outline.py
3. Check results in the 'output' directory
4. Validate results:
   python validate_output.py output/

## Docker Testing (if Docker is available):

1. Build the image:
   docker build --platform linux/amd64 -t pdf-outline-extractor .

2. Run the container:
   docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor

3. Validate results:
   python validate_output.py output/

## File Structure:
input/          - Place PDF files here
output/         - JSON results will appear here
test_results/   - For storing test outputs
"""
    
    with open("TESTING.md", "w") as f:
        f.write(instructions)
    
    print("Created TESTING.md with instructions")

if __name__ == "__main__":
    setup_test_directories()
    print("\nTest environment setup complete!")
    print("You can now place PDF files in the 'input' directory and run tests.")