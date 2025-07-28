#!/usr/bin/env python3
"""
Output validation script to ensure JSON format compliance
"""

import json
import sys
import os

def validate_json_structure(json_data):
    """Validate that the JSON structure matches the expected format"""
    errors = []
    
    # Check required top-level keys
    if "title" not in json_data:
        errors.append("Missing 'title' field")
    elif not isinstance(json_data["title"], str):
        errors.append("'title' must be a string")
    
    if "outline" not in json_data:
        errors.append("Missing 'outline' field")
    elif not isinstance(json_data["outline"], list):
        errors.append("'outline' must be a list")
    else:
        # Validate outline entries
        for i, entry in enumerate(json_data["outline"]):
            if not isinstance(entry, dict):
                errors.append(f"Outline entry {i} must be a dictionary")
                continue
            
            # Check required fields in outline entry
            required_fields = ["level", "text", "page"]
            for field in required_fields:
                if field not in entry:
                    errors.append(f"Outline entry {i} missing '{field}' field")
            
            # Validate field types and values
            if "level" in entry:
                if entry["level"] not in ["H1", "H2", "H3"]:
                    errors.append(f"Outline entry {i} has invalid level: {entry['level']}")
            
            if "text" in entry and not isinstance(entry["text"], str):
                errors.append(f"Outline entry {i} 'text' must be a string")
            
            if "page" in entry:
                if not isinstance(entry["page"], int) or entry["page"] < 1:
                    errors.append(f"Outline entry {i} 'page' must be a positive integer")
    
    return errors

def validate_file(json_file_path):
    """Validate a single JSON file"""
    print(f"Validating: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {json_file_path}")
        return False
    
    errors = validate_json_structure(json_data)
    
    if errors:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Validation passed!")
        print(f"  Title: {json_data['title']}")
        print(f"  Outline entries: {len(json_data['outline'])}")
        
        # Show outline summary
        if json_data['outline']:
            print("  Outline structure:")
            for entry in json_data['outline']:
                print(f"    {entry['level']}: {entry['text']} (page {entry['page']})")
        
        return True

def validate_directory(directory_path):
    """Validate all JSON files in a directory"""
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return
    
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    
    if not json_files:
        print(f"No JSON files found in {directory_path}")
        return
    
    print(f"Found {len(json_files)} JSON files to validate")
    print("=" * 50)
    
    valid_count = 0
    for json_file in json_files:
        json_path = os.path.join(directory_path, json_file)
        if validate_file(json_path):
            valid_count += 1
        print("-" * 30)
    
    print(f"\nValidation Summary: {valid_count}/{len(json_files)} files passed validation")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_output.py <json_file_or_directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        validate_file(path)
    elif os.path.isdir(path):
        validate_directory(path)
    else:
        print(f"Path not found: {path}")