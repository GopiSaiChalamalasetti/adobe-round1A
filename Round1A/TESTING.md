
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
