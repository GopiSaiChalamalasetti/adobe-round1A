#!/usr/bin/env python3
"""
Test the main processing function without actual PDFs
"""

import os
import json
import tempfile
from extract_outline import PDFOutlineExtractor

def test_extractor_initialization():
    """Test that the extractor can be initialized"""
    try:
        extractor = PDFOutlineExtractor()
        print("✅ PDFOutlineExtractor initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize PDFOutlineExtractor: {e}")
        return False

def test_validation_functions():
    """Test the validation helper functions"""
    extractor = PDFOutlineExtractor()
    
    # Test heading validation
    valid_headings = [
        "Introduction",
        "Chapter 1: Overview",
        "1.1 Background",
        "Methodology and Approach"
    ]
    
    invalid_headings = [
        "1",  # Too short
        "a" * 201,  # Too long
        "123456",  # Mostly numbers
        "page 5",  # Page number
        "figure 1",  # Figure caption
    ]
    
    print("Testing heading validation...")
    
    for heading in valid_headings:
        if extractor._is_valid_heading(heading):
            print(f"✅ '{heading}' correctly identified as valid")
        else:
            print(f"❌ '{heading}' incorrectly rejected")
    
    for heading in invalid_headings:
        if not extractor._is_valid_heading(heading):
            print(f"✅ '{heading}' correctly rejected")
        else:
            print(f"❌ '{heading}' incorrectly accepted")

def test_pattern_matching():
    """Test heading pattern matching"""
    extractor = PDFOutlineExtractor()
    
    test_patterns = [
        ("1. Introduction", True),
        ("2.1 Overview", True),
        ("3.2.1 Details", True),
        ("CHAPTER ONE", True),
        ("Background Information", True),
        ("This is a long sentence that should not be a heading.", False),
        ("random text", False),
    ]
    
    print("\nTesting pattern matching...")
    
    for text, should_match in test_patterns:
        matches = extractor._matches_heading_pattern(text)
        if matches == should_match:
            print(f"✅ '{text}' pattern matching correct")
        else:
            print(f"❌ '{text}' pattern matching incorrect (expected {should_match}, got {matches})")

def test_directory_processing_structure():
    """Test the directory processing structure without actual PDFs"""
    print("\nTesting directory processing structure...")
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        output_dir = os.path.join(temp_dir, "output")
        
        os.makedirs(input_dir)
        os.makedirs(output_dir)
        
        # Create a fake PDF file (just for testing directory structure)
        fake_pdf = os.path.join(input_dir, "test.pdf")
        with open(fake_pdf, "w") as f:
            f.write("fake pdf content")
        
        # Test that our processing function can find the file
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        if pdf_files:
            print(f"✅ Found PDF files: {pdf_files}")
        else:
            print("❌ No PDF files found")
        
        # Test output path generation
        for filename in pdf_files:
            output_filename = filename.replace('.pdf', '.json')
            output_path = os.path.join(output_dir, output_filename)
            print(f"✅ Output path: {output_path}")

def run_all_tests():
    """Run all tests"""
    print("Running PDF Outline Extractor Tests")
    print("=" * 50)
    
    tests = [
        test_extractor_initialization,
        test_validation_functions,
        test_pattern_matching,
        test_directory_processing_structure,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
        print("-" * 30)
    
    print(f"\nTest Summary: {passed}/{len(tests)} tests passed")

if __name__ == "__main__":
    run_all_tests()