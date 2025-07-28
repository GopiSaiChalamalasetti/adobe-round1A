# Round 1A – Document Outline Extractor

## Objective
Extract a structured outline (Title, H1, H2, H3) from PDF documents and save it in a clean JSON format.
## What It Does
- Reads a PDF file
- Detects title and headings
- Outputs JSON with heading levels and page numbers
## Technologies Used
- Python
- PyMuPDF (fitz)
- Docker
## Input
Place all PDF files in the `input/` folder.
## Output
JSON files will be generated in the `output/` folder with the same base name as the PDFs.
## Docker Commands
```bash
docker build --platform linux/amd64 -t dotextractor:round1a .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none dotextractor:round1a
