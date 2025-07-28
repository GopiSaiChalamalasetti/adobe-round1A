#!/usr/bin/env python3
"""
Simulate the Docker container execution locally
"""

import os
import sys
import tempfile
import shutil
from extract_outline import process_pdfs

def simulate_docker_environment():
    """Simulate the Docker container environment"""
    print("Simulating Docker container execution...")
    
    # Check if input directory exists
    if not os.path.exists("input"):
        print("❌ Input directory not found. Please run 'python setup_test_env.py' first.")
        return False
    
    # Check if there are PDF files
    pdf_files = [f for f in os.listdir("input") if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in input directory.")
        print("Please place some PDF files in the 'input' directory to test.")
        return False
    
    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    
    # Create temporary directories to simulate Docker volumes
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_input = os.path.join(temp_dir, "input")
        temp_output = os.path.join(temp_dir, "output")
        
        # Copy input files to temporary directory
        shutil.copytree("input", temp_input)
        os.makedirs(temp_output)
        
        # Temporarily modify the paths in the environment
        original_process_pdfs = process_pdfs
        
        def mock_process_pdfs():
            """Mock version that uses our temporary directories"""
            input_dir = temp_input
            output_dir = temp_output
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            from extract_outline import PDFOutlineExtractor
            import json
            import logging
            
            logger = logging.getLogger(__name__)
            extractor = PDFOutlineExtractor()
            
            # Process all PDF files in input directory
            for filename in os.listdir(input_dir):
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(input_dir, filename)
                    output_filename = filename.replace('.pdf', '.json')
                    output_path = os.path.join(output_dir, output_filename)
                    
                    logger.info(f"Processing {filename}...")
                    
                    try:
                        result = extractor.extract_title_and_outline(pdf_path)
                        
                        # Write result to JSON file
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2, ensure_ascii=False)
                        
                        logger.info(f"Successfully processed {filename} -> {output_filename}")
                        
                    except Exception as e:
                        logger.error(f"Failed to process {filename}: {str(e)}")
                        # Write error result
                        error_result = {
                            "title": "Error Processing Document",
                            "outline": []
                        }
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(error_result, f, indent=2, ensure_ascii=False)
        
        # Run the mock processing
        try:
            mock_process_pdfs()
            print("✅ Processing completed successfully!")
            
            # Copy results back to local output directory
            if os.path.exists("output"):
                shutil.rmtree("output")
            shutil.copytree(temp_output, "output")
            
            # Show results
            output_files = os.listdir("output")
            print(f"Generated {len(output_files)} output files:")
            for output_file in output_files:
                print(f"  - {output_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return False

def main():
    """Main function"""
    print("PDF Outline Extractor - Docker Simulation")
    print("=" * 50)
    
    success = simulate_docker_environment()
    
    if success:
        print("\n✅ Simulation completed successfully!")
        print("Check the 'output' directory for results.")
        print("Run 'python validate_output.py output/' to validate the results.")
    else:
        print("\n❌ Simulation failed.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()