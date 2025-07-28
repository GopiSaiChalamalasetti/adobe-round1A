#!/usr/bin/env python3
"""
Docker testing script - creates sample directories and tests the Docker workflow
"""

import os
import json
import subprocess
import tempfile
import shutil

def create_sample_pdf_content():
    """Create a simple test PDF using reportlab if available, otherwise skip"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        def create_test_pdf(filename):
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Title
            c.setFont("Helvetica-Bold", 24)
            c.drawString(100, 750, "Sample Document Title")
            
            # H1 Heading
            c.setFont("Helvetica-Bold", 18)
            c.drawString(100, 700, "1. Introduction")
            
            # Body text
            c.setFont("Helvetica", 12)
            c.drawString(100, 670, "This is some body text content.")
            
            # H2 Heading
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 640, "1.1 Background")
            
            # More body text
            c.drawString(100, 610, "More content here.")
            
            # H3 Heading
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, 580, "1.1.1 Specific Details")
            
            c.showPage()
            
            # Page 2
            c.setFont("Helvetica-Bold", 18)
            c.drawString(100, 750, "2. Methodology")
            
            c.setFont("Helvetica", 12)
            c.drawString(100, 720, "Content for methodology section.")
            
            c.save()
        
        return create_test_pdf
    except ImportError:
        print("ReportLab not available - skipping PDF creation")
        return None

def test_docker_workflow():
    """Test the complete Docker workflow"""
    print("Testing Docker workflow...")
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        output_dir = os.path.join(temp_dir, "output")
        
        os.makedirs(input_dir)
        os.makedirs(output_dir)
        
        # Try to create a sample PDF
        create_pdf = create_sample_pdf_content()
        if create_pdf:
            sample_pdf = os.path.join(input_dir, "sample.pdf")
            create_pdf(sample_pdf)
            print(f"Created sample PDF: {sample_pdf}")
        else:
            print("No sample PDF created - you'll need to add PDFs manually to test")
            return
        
        # Build Docker image
        print("Building Docker image...")
        build_cmd = ["docker", "build", "--platform", "linux/amd64", "-t", "pdf-outline-test", "."]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Docker build failed: {result.stderr}")
            return
        
        print("Docker image built successfully!")
        
        # Run Docker container
        print("Running Docker container...")
        run_cmd = [
            "docker", "run", "--rm",
            "-v", f"{input_dir}:/app/input",
            "-v", f"{output_dir}:/app/output",
            "--network", "none",
            "pdf-outline-test"
        ]
        
        result = subprocess.run(run_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Docker run failed: {result.stderr}")
            return
        
        print("Docker container executed successfully!")
        print(f"Output: {result.stdout}")
        
        # Check output
        output_files = os.listdir(output_dir)
        print(f"Output files: {output_files}")
        
        for output_file in output_files:
            if output_file.endswith('.json'):
                output_path = os.path.join(output_dir, output_file)
                with open(output_path, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                print(f"\nResult for {output_file}:")
                print(json.dumps(result_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_docker_workflow()