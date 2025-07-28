#!/usr/bin/env python3
"""
Local testing script for PDF outline extraction
"""

import os
import json
import sys
from extract_outline import PDFOutlineExtractor

def test_extraction(pdf_path: str):
    """Test the extraction on a single PDF file"""
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return
    
    print(f"Testing extraction on: {pdf_path}")
    
    extractor = PDFOutlineExtractor()
    result = extractor.extract_title_and_outline(pdf_path)
    
    print("\n" + "="*50)
    print("EXTRACTION RESULT")
    print("="*50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*50)
    
    # Save result to file
    output_file = pdf_path.replace('.pdf', '_result.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nResult saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_local.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    test_extraction(pdf_path)