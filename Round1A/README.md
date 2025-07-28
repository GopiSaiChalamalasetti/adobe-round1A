# PDF Outline Extractor - Adobe Connecting the Dots Challenge

## Overview

This solution extracts structured outlines from PDF documents, identifying the title and hierarchical headings (H1, H2, H3) with their corresponding page numbers. The extracted information is output in JSON format as specified in the challenge requirements.

## Approach

### 1. Title Extraction
- **Primary Method**: Extract title from PDF metadata
- **Fallback Method**: Identify the largest font size text on the first page as the title

### 2. Heading Detection Strategy
The solution uses a multi-layered approach to identify headings:

#### Font-Based Analysis
- Analyzes font sizes across the document
- Identifies the most common font size as body text
- Maps larger font sizes to heading levels (H1, H2, H3)
- Uses a threshold-based approach to handle font size variations

#### Content-Based Pattern Recognition
- **Numbered Sections**: Detects patterns like "1. Introduction", "2.1 Overview"
- **Bold Text**: Identifies bold-formatted text as potential headings
- **Capitalization Patterns**: Recognizes ALL CAPS and Title Case patterns
- **Structural Patterns**: Uses regex to identify common heading formats

#### Validation and Filtering
- Filters out non-heading content (page numbers, URLs, emails)
- Validates heading length (2-200 characters)
- Removes duplicates while preserving document order
- Excludes text that's mostly numbers or symbols

### 3. Multilingual Support
- Uses UTF-8 encoding for proper character handling
- Supports various character sets including Japanese, Chinese, and other non-Latin scripts
- Pattern recognition works across different languages

## Libraries Used

- **PyMuPDF (fitz)**: Primary PDF processing library
  - Lightweight and fast
  - Excellent font and formatting analysis capabilities
  - Supports text extraction with detailed formatting information
  - Model size: ~15MB (well under the 200MB limit)

## Key Features

1. **Robust Font Analysis**: Doesn't rely solely on font sizes, uses multiple indicators
2. **Pattern Recognition**: Identifies common heading patterns across different document styles
3. **Error Handling**: Graceful handling of malformed or complex PDFs
4. **Performance Optimized**: Processes documents efficiently within time constraints
5. **Offline Operation**: No network calls, works completely offline

## Architecture

```
PDFOutlineExtractor
├── extract_title_and_outline()     # Main extraction method
├── _extract_title_from_metadata()  # Title from PDF metadata
├── _extract_text_blocks()          # Extract formatted text blocks
├── _extract_title_from_content()   # Title from content analysis
├── _extract_headings()             # Main heading extraction logic
├── _detect_heading_by_content()    # Content-based heading detection
├── _matches_heading_pattern()      # Pattern matching for headings
└── _is_valid_heading()             # Heading validation
```

## Building and Running

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### Run the Solution
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:latest
```

### Expected Input/Output Structure
```
input/
├── document1.pdf
├── document2.pdf
└── ...

output/
├── document1.json
├── document2.json
└── ...
```

## Output Format

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

## Performance Characteristics

- **Execution Time**: < 10 seconds for 50-page PDFs
- **Model Size**: ~15MB (PyMuPDF library)
- **Memory Usage**: Optimized for 16GB RAM systems
- **CPU Architecture**: AMD64 (x86_64) compatible
- **Network**: Completely offline operation

## Testing Strategy

The solution has been designed to handle various PDF types:
- Academic papers with clear heading hierarchies
- Business documents with numbered sections
- Reports with mixed formatting styles
- Documents with complex layouts
- Multilingual documents

## Error Handling

- Graceful handling of corrupted or malformed PDFs
- Fallback mechanisms for title extraction
- Robust validation to prevent false positive headings
- Comprehensive logging for debugging

## Limitations and Considerations

1. **Complex Layouts**: Very complex multi-column layouts might require additional processing
2. **Image-based PDFs**: Scanned documents without text layers are not supported
3. **Custom Fonts**: Unusual font configurations might affect heading detection accuracy
4. **Language-specific Patterns**: Some heading patterns might be language-specific

## Future Enhancements

- Machine learning-based heading classification
- Support for more heading levels (H4, H5, H6)
- Enhanced table of contents extraction
- Better handling of image-based PDFs with OCR

## Compliance

- ✅ AMD64 architecture compatibility
- ✅ No GPU dependencies
- ✅ Model size ≤ 200MB
- ✅ Offline operation (no network calls)
- ✅ CPU-only execution
- ✅ Performance within specified limits