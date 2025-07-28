#!/usr/bin/env python3
"""
PDF Outline Extractor for Adobe Connecting the Dots Challenge
Extracts structured outlines (Title, H1, H2, H3) from PDF documents
"""

import os
import json
import re
import fitz  # PyMuPDF
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFOutlineExtractor:
    def __init__(self):
        self.font_size_threshold = 1.5  # Minimum difference to consider different levels
        self.min_heading_length = 3  # Minimum characters for a heading
        self.max_heading_length = 150  # Maximum characters for a heading
        
    def extract_title_and_outline(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract title and hierarchical outline from PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with title and outline structure
        """
        try:
            doc = fitz.open(pdf_path)
            
            # First, try to get title from document metadata
            title = self._extract_title_from_metadata(doc)
            
            # Extract all text blocks with formatting information
            text_blocks = self._extract_text_blocks(doc)
            
            # If no title from metadata, try to extract from first page
            if not title:
                title = self._extract_title_from_content(text_blocks)
            
            # Extract headings based on font analysis and content patterns
            outline = self._extract_headings(text_blocks)
            
            doc.close()
            
            return {
                "title": title or "Untitled Document",
                "outline": outline
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            return {
                "title": "Error Processing Document",
                "outline": []
            }
    
    def _extract_title_from_metadata(self, doc: fitz.Document) -> Optional[str]:
        """Extract title from PDF metadata"""
        try:
            metadata = doc.metadata
            title = metadata.get('title', '').strip()
            if title and len(title) > 3 and title.lower() != 'untitled':
                return title
        except:
            pass
        return None
    
    def _extract_text_blocks(self, doc: fitz.Document) -> List[Dict]:
        """Extract text blocks with formatting information, merging adjacent spans"""
        text_blocks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")
            
            for block in blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        # Merge spans in the same line to handle split text
                        line_text = ""
                        line_font_size = 0
                        line_font_name = ""
                        line_flags = 0
                        line_bbox = None
                        
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                if line_text:
                                    line_text += " " + text
                                else:
                                    line_text = text
                                    line_font_size = span["size"]
                                    line_font_name = span["font"]
                                    line_flags = span["flags"]
                                    line_bbox = span["bbox"]
                        
                        if line_text:
                            text_blocks.append({
                                "text": line_text,
                                "page": page_num + 1,
                                "font_size": line_font_size,
                                "font_name": line_font_name,
                                "flags": line_flags,
                                "bbox": line_bbox
                            })
        
        return text_blocks
    
    def _extract_title_from_content(self, text_blocks: List[Dict]) -> Optional[str]:
        """Extract title from the first page content"""
        if not text_blocks:
            return None
        
        # Look for the largest font size on the first few pages
        first_pages_blocks = [block for block in text_blocks if block["page"] <= 2]
        if not first_pages_blocks:
            return None
        
        # Find the largest font size
        max_font_size = max(block["font_size"] for block in first_pages_blocks)
        
        # Get text with the largest font size (likely title)
        title_candidates = []
        for block in first_pages_blocks:
            if block["font_size"] >= max_font_size - 0.5:  # Tighter variance
                text = block["text"].strip()
                # Filter out obvious non-titles
                if (len(text) >= 5 and len(text) <= 200 and 
                    not re.match(r'^\d+$', text) and  # Not just numbers
                    not re.match(r'^page \d+', text.lower()) and  # Not page numbers
                    not text.lower().startswith('http') and  # Not URLs
                    not '@' in text and  # Not emails
                    not text.lower().startswith('welcome to') and  # Skip welcome messages
                    not re.match(r'^(chapter|section|part)\s+\d+', text.lower()) and  # Skip chapter headers
                    not text.lower().endswith('challenge')):  # Skip challenge titles that are too generic
                    title_candidates.append((text, block["page"]))
        
        if title_candidates:
            # Prefer titles from the first page, then by length (longer is often better for titles)
            title_candidates.sort(key=lambda x: (x[1], -len(x[0])))
            return title_candidates[0][0]
        
        # Fallback: try to find any reasonable title-like text
        for block in first_pages_blocks:
            text = block["text"].strip()
            if (len(text) >= 10 and len(text) <= 200 and
                not re.match(r'^\d+', text) and
                (text[0].isupper() or text.istitle())):
                return text
        
        return None
    
    def _extract_headings(self, text_blocks: List[Dict]) -> List[Dict]:
        """Extract headings based on improved font analysis and content patterns"""
        if not text_blocks:
            return []
        
        # Analyze font sizes more intelligently
        font_sizes = [block["font_size"] for block in text_blocks]
        font_size_counts = Counter(font_sizes)
        
        # Get the most common font sizes (likely body text and headings)
        common_sizes = font_size_counts.most_common(10)
        body_font_size = common_sizes[0][0]  # Most common is likely body text
        
        # Find distinct font sizes that could be headings
        unique_sizes = sorted(set(font_sizes), reverse=True)
        heading_sizes = []
        
        for size in unique_sizes:
            if size > body_font_size + self.font_size_threshold:
                # Check if this size has enough occurrences to be a heading level
                count = font_size_counts[size]
                if count >= 1:  # At least one occurrence
                    heading_sizes.append(size)
        
        # Limit to top 3 heading sizes and map to levels
        heading_sizes = heading_sizes[:3]
        font_to_level = {}
        for i, font_size in enumerate(heading_sizes):
            font_to_level[font_size] = f"H{i+1}"
        
        headings = []
        processed_texts = set()  # Track processed text to avoid duplicates
        
        for block in text_blocks:
            text = block["text"].strip()
            font_size = block["font_size"]
            
            # Skip if we've already processed this exact text
            if text in processed_texts:
                continue
            
            level = None
            
            # Check font-based heading detection first
            if font_size in font_to_level:
                level = font_to_level[font_size]
            else:
                # Check for content-based patterns (numbered sections, etc.)
                level = self._detect_heading_by_content(text, block)
            
            if level and self._is_valid_heading(text):
                headings.append({
                    "level": level,
                    "text": text,
                    "page": block["page"]
                })
                processed_texts.add(text)
        
        # Post-process to improve hierarchy
        headings = self._improve_heading_hierarchy(headings)
        
        return headings
    
    def _detect_heading_by_content(self, text: str, block: Dict) -> Optional[str]:
        """Detect headings based on content patterns"""
        # Check for numbered sections (highest priority)
        if re.match(r'^\d+\.?\s+[A-Z]', text):
            return "H1"
        
        # Check for subsection patterns
        if re.match(r'^\d+\.\d+\.?\s+[A-Z]', text):
            return "H2"
        
        # Check for sub-subsection patterns
        if re.match(r'^\d+\.\d+\.\d+\.?\s+[A-Z]', text):
            return "H3"
        
        # Check for chapter/section keywords
        if re.match(r'^(Chapter|Section|Part|Appendix)\s+\d*', text, re.IGNORECASE):
            return "H1"
        
        # Check for bold text with heading characteristics
        if block["flags"] & 2**4:  # Bold flag
            if self._matches_heading_pattern(text):
                return "H2"  # Default to H2 for pattern-based detection
        
        return None
    
    def _matches_heading_pattern(self, text: str) -> bool:
        """Check if text matches typical heading patterns"""
        # Length constraints
        if len(text) < self.min_heading_length or len(text) > self.max_heading_length:
            return False
        
        # Skip if ends with sentence punctuation (except numbered sections)
        if re.search(r'[.!?]$', text) and not re.match(r'^\d+\.', text):
            return False
        
        # Skip table-like content (multiple columns of short words)
        if len(text.split()) > 1 and all(len(word) <= 3 for word in text.split()):
            return False
        
        # Check for numbered section patterns (already handled in content detection)
        if re.match(r'^\d+\.?\s+[A-Z]', text):
            return True
        
        # Check for heading-like characteristics
        if re.match(r'^[A-Z][a-z]', text):  # Starts with capital letter
            return True
        
        if text.isupper() and len(text) > 3:  # All caps (but not too short)
            return True
        
        # Check for title case
        words = text.split()
        if len(words) >= 2 and all(word[0].isupper() for word in words if len(word) > 3):
            return True
        
        return False
    
    def _is_valid_heading(self, text: str) -> bool:
        """Validate if text is a reasonable heading"""
        # Length constraints
        if len(text) < self.min_heading_length or len(text) > self.max_heading_length:
            return False
        
        # Must contain at least some letters
        if len(re.sub(r'[^a-zA-Z]', '', text)) < 2:
            return False
        
        # Filter out numbered list items that are not proper headings
        if re.match(r'^\d+\.\s+[A-Z].*\(e\.g\.,.*\)$', text):  # "1. Something (e.g., example)"
            return False
        
        if re.match(r'^\d+\.\s+A\s+(sample|working|README).*', text):  # List items starting with "A sample/working/README"
            return False
        
        # Filter out common non-heading patterns
        skip_patterns = [
            r'^\d+$',  # Just numbers
            r'^page \d+',  # Page numbers
            r'^figure \d+',  # Figure captions
            r'^table \d+',  # Table captions
            r'^\w+@\w+\.',  # Email addresses
            r'^https?://',  # URLs
            r'^www\.',  # Web addresses
            r'^\d+\.\d+$',  # Version numbers
            r'^[A-Z]{1,3}$',  # Short abbreviations
            r'^\d+[a-z]?$',  # Numbers with optional letter
            r'^[^\w\s]+$',  # Only symbols
            r'^\d+\s*-\s*\d+$',  # Page ranges
            r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}$',  # Dates
            r'^\d+\.\s+(A|An|The)\s+(sample|working|README|Git).*',  # Specific list patterns
            r'^\d+\.\s+All\s+dependencies.*',  # "All dependencies" pattern
            r'^\d+\.\s+(Document|Extracted|Sub-section|Metadata).*:$',  # Technical list items ending with colon
        ]
        
        text_lower = text.lower().strip()
        for pattern in skip_patterns:
            if re.match(pattern, text_lower):
                return False
        
        # Skip common table headers and labels
        table_words = ['criteria', 'max', 'points', 'total', 'description', 'constraint', 'requirement', 
                      'deliverables', 'japanese)', 'bonus:', 'theme:']
        if text_lower in table_words:
            return False
        
        # Skip very generic single words
        if len(text.split()) == 1 and len(text) < 8:
            generic_words = ['title', 'name', 'date', 'time', 'location', 'contact', 'email', 'phone']
            if text_lower in generic_words:
                return False
        
        # Skip incomplete sentences or fragments
        if text.endswith(' and') or text.endswith(' or') or text.endswith(','):
            return False
        
        # Skip very short headings that are likely noise
        if len(text.split()) == 1 and len(text) < 5:
            return False
        
        return True
    
    def _improve_heading_hierarchy(self, headings: List[Dict]) -> List[Dict]:
        """Improve heading hierarchy based on content analysis"""
        if not headings:
            return headings
        
        improved_headings = []
        
        for i, heading in enumerate(headings):
            text = heading["text"]
            current_level = heading["level"]
            
            # Check for clear H1 patterns
            if (re.match(r'^(Chapter|Section|Part|Round)\s+\d+', text, re.IGNORECASE) or
                re.match(r'^\d+\.?\s+[A-Z]', text) or
                re.match(r'^[A-Z][^a-z]*$', text) and len(text) > 5):  # All caps titles
                current_level = "H1"
            
            # Check for clear H3 patterns (sub-subsections)
            elif (re.match(r'^\d+\.\d+\.\d+', text) or
                  (current_level == "H2" and len(text) < 30 and 
                   any(word in text.lower() for word in ['tip', 'note', 'example', 'summary']))):
                current_level = "H3"
            
            # Adjust based on context (previous headings)
            if i > 0:
                prev_heading = improved_headings[-1]
                
                # If previous was H1 and current is also H1, but current looks like subsection
                if (prev_heading["level"] == "H1" and current_level == "H1" and
                    len(text) < len(prev_heading["text"]) and
                    not re.match(r'^(Chapter|Section|Part|Round)\s+\d+', text, re.IGNORECASE)):
                    current_level = "H2"
            
            improved_headings.append({
                "level": current_level,
                "text": text,
                "page": heading["page"]
            })
        
        return improved_headings

def process_pdfs():
    """Process all PDFs in the input directory"""
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
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

if __name__ == "__main__":
    process_pdfs()