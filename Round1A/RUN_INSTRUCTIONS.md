# How to Run the PDF Outline Extractor

## 🚀 Quick Start (Easiest Way)

1. **Place your PDF files in the input directory:**
   ```bash
   # Create input directory if it doesn't exist
   mkdir input
   
   # Copy your PDF files
   cp your-document.pdf input/
   ```

2. **Run the quick start script:**
   ```bash
   python quick_start.py
   ```
   
   This will automatically detect if you have Docker or Python available and run the appropriate method.

3. **Check results:**
   - Results will be in the `output/` directory
   - Each PDF will have a corresponding JSON file

## 🐳 Method 1: Using Docker (Recommended)

This matches the competition environment exactly.

### Prerequisites:
- Docker installed and running

### Steps:
```bash
# 1. Build the Docker image
docker build --platform linux/amd64 -t pdf-outline-extractor .

# 2. Create input directory and add PDFs
mkdir input
cp your-document.pdf input/

# 3. Run the container
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor

# 4. Validate results
python validate_output.py output/
```

## 🐍 Method 2: Using Local Python

### Prerequisites:
- Python 3.7+ installed

### Steps:
```bash
# 1. Install dependencies
pip install PyMuPDF==1.23.8

# 2. Set up environment
python setup_test_env.py

# 3. Add PDF files to input directory
cp your-document.pdf input/

# 4. Run the extractor
python simulate_docker_run.py

# 5. Validate results
python validate_output.py output/
```

## 🧪 Method 3: Test Single PDF

For quick testing with one PDF file:

```bash
# Install dependencies first
pip install PyMuPDF==1.23.8

# Test single file
python test_local.py path/to/your/document.pdf
```

## 📁 Expected Directory Structure

```
your-project/
├── input/                 # Place your PDF files here
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
├── output/                # JSON results appear here
│   ├── document1.json
│   ├── document2.json
│   └── ...
├── extract_outline.py     # Main script
├── Dockerfile            # Docker configuration
└── ...
```

## 📋 Output Format

Each PDF will generate a JSON file like this:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## 🔧 Troubleshooting

### Docker Issues:
- **"docker: command not found"**: Install Docker Desktop
- **Build fails**: Make sure you're in the project directory with the Dockerfile
- **Permission denied**: On Linux/Mac, you might need `sudo`

### Python Issues:
- **"ModuleNotFoundError: No module named 'fitz'"**: Run `pip install PyMuPDF==1.23.8`
- **"No PDF files found"**: Make sure PDFs are in the `input/` directory
- **Import errors**: Make sure you're using Python 3.7+

### General Issues:
- **No output files**: Check if input PDFs are valid and readable
- **Empty outline**: Some PDFs might not have clear heading structure
- **Validation fails**: Check the JSON format with `python validate_output.py output/`

## 🎯 For Competition Submission

The exact commands that will be used in the competition:

```bash
# Build
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .

# Run
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

## 📞 Need Help?

1. Run `python quick_start.py --help` for usage options
2. Check the comprehensive `README.md` for detailed documentation
3. Use the testing scripts to debug issues:
   - `python test_processing.py` - Run unit tests
   - `python validate_output.py output/` - Validate JSON format