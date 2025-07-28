#!/usr/bin/env python3
"""
Quick start script to run the PDF outline extractor
"""

import os
import sys
import subprocess
import shutil

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_python_deps():
    """Check if Python dependencies are installed"""
    try:
        import fitz  # PyMuPDF
        return True
    except ImportError:
        return False

def setup_directories():
    """Set up input and output directories"""
    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    print("✅ Created input/ and output/ directories")

def run_with_docker():
    """Run using Docker"""
    print("🐳 Running with Docker...")
    
    # Check if input directory has PDFs
    pdf_files = [f for f in os.listdir('input') if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in input/ directory")
        print("Please add some PDF files to the input/ directory first")
        return False
    
    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    
    # Build Docker image
    print("Building Docker image...")
    build_cmd = ['docker', 'build', '--platform', 'linux/amd64', '-t', 'pdf-outline-extractor', '.']
    result = subprocess.run(build_cmd)
    
    if result.returncode != 0:
        print("❌ Docker build failed")
        return False
    
    # Run Docker container
    print("Running Docker container...")
    run_cmd = [
        'docker', 'run', '--rm',
        '-v', f'{os.getcwd()}/input:/app/input',
        '-v', f'{os.getcwd()}/output:/app/output',
        '--network', 'none',
        'pdf-outline-extractor'
    ]
    
    result = subprocess.run(run_cmd)
    
    if result.returncode != 0:
        print("❌ Docker run failed")
        return False
    
    print("✅ Docker execution completed!")
    return True

def run_with_python():
    """Run using local Python"""
    print("🐍 Running with local Python...")
    
    # Check dependencies
    if not check_python_deps():
        print("Installing PyMuPDF...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyMuPDF==1.23.8'])
        if result.returncode != 0:
            print("❌ Failed to install PyMuPDF")
            return False
    
    # Check if input directory has PDFs
    pdf_files = [f for f in os.listdir('input') if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in input/ directory")
        print("Please add some PDF files to the input/ directory first")
        return False
    
    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    
    # Run the simulation
    result = subprocess.run([sys.executable, 'simulate_docker_run.py'])
    
    if result.returncode != 0:
        print("❌ Python execution failed")
        return False
    
    print("✅ Python execution completed!")
    return True

def validate_results():
    """Validate the output results"""
    print("\n🔍 Validating results...")
    
    if not os.path.exists('output'):
        print("❌ Output directory not found")
        return False
    
    output_files = [f for f in os.listdir('output') if f.endswith('.json')]
    if not output_files:
        print("❌ No JSON output files found")
        return False
    
    # Run validation
    result = subprocess.run([sys.executable, 'validate_output.py', 'output/'])
    return result.returncode == 0

def main():
    """Main function"""
    print("🎯 PDF Outline Extractor - Quick Start")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Check what's available
    has_docker = check_docker()
    has_python = check_python_deps()
    
    print(f"Docker available: {'✅' if has_docker else '❌'}")
    print(f"Python + PyMuPDF: {'✅' if has_python else '❌'}")
    
    # Choose execution method
    if len(sys.argv) > 1 and sys.argv[1] == '--docker':
        if not has_docker:
            print("❌ Docker not available but --docker flag specified")
            return
        success = run_with_docker()
    elif len(sys.argv) > 1 and sys.argv[1] == '--python':
        success = run_with_python()
    else:
        # Auto-choose
        if has_docker:
            print("\n🐳 Using Docker (recommended)")
            success = run_with_docker()
        else:
            print("\n🐍 Using local Python")
            success = run_with_python()
    
    if success:
        validate_results()
        print("\n" + "=" * 50)
        print("✅ Extraction completed successfully!")
        print("📁 Check the output/ directory for results")
    else:
        print("\n" + "=" * 50)
        print("❌ Extraction failed")
        print("Please check the error messages above")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Usage:")
        print("  python quick_start.py           # Auto-detect and run")
        print("  python quick_start.py --docker  # Force Docker")
        print("  python quick_start.py --python  # Force local Python")
        print("\nMake sure to place PDF files in the input/ directory first!")
    else:
        main()