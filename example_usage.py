#!/usr/bin/env python3
"""
Example usage of the PDF Extractor

This script demonstrates how to use the PDFExtractor class to extract text
from PDF files and organize them into the book sections.
"""

import os
from pathlib import Path
from pdf_extractor import PDFExtractor

def extract_pdf_to_section(pdf_path: str, section_number: int) -> bool:
    """
    Extract PDF text and save it to a specific book section.
    
    Args:
        pdf_path: Path to the PDF file
        section_number: Which section (1-12) to save the text to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create extractor
        extractor = PDFExtractor(pdf_path)
        
        # Extract text
        print(f"Extracting text from: {pdf_path}")
        results = extractor.extract_text(method='auto')
        
        # Create output directory
        section_dir = Path(f"book sections/{section_number}")
        section_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the extracted text
        pdf_name = Path(pdf_path).stem
        output_file = section_dir / f"{pdf_name}_extracted.txt"
        extractor.save_text_to_file(output_file)
        
        # Also save page-by-page files
        pages_dir = section_dir / f"{pdf_name}_pages"
        extractor.save_page_by_page(pages_dir)
        
        print(f"✓ Successfully extracted to section {section_number}")
        print(f"  - Main text: {output_file}")
        print(f"  - Page files: {pages_dir}")
        print(f"  - Total pages: {results['total_pages']}")
        print(f"  - Total characters: {results['total_chars']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error extracting {pdf_path}: {e}")
        return False

def main():
    """
    Main function to demonstrate PDF extraction.
    """
    print("PDF Extraction Example")
    print("=" * 50)
    
    # Example: Extract a PDF to section 1
    # Replace 'example.pdf' with your actual PDF file path
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"Please place a PDF file named '{pdf_file}' in this directory")
        print("Or modify this script to use your PDF file path")
        return
    
    # Extract to section 1
    success = extract_pdf_to_section(pdf_file, 1)
    
    if success:
        print("\n✓ Extraction completed successfully!")
        print("\nTo extract multiple PDFs to different sections:")
        print("- Call extract_pdf_to_section(pdf_path, section_number)")
        print("- Section numbers should be 1-12")
        print("- Each section will contain the extracted text and page files")
    else:
        print("\n✗ Extraction failed!")

# Example of batch processing multiple PDFs
def batch_extract_pdfs():
    """
    Example of how to batch process multiple PDFs into different sections.
    """
    # Example mapping of PDF files to sections
    pdf_section_mapping = {
        "chapter1.pdf": 1,
        "chapter2.pdf": 2,
        "chapter3.pdf": 3,
        # Add more mappings as needed
    }
    
    successful_extractions = 0
    
    for pdf_path, section_num in pdf_section_mapping.items():
        if os.path.exists(pdf_path):
            if extract_pdf_to_section(pdf_path, section_num):
                successful_extractions += 1
        else:
            print(f"Warning: {pdf_path} not found, skipping...")
    
    print(f"\nBatch extraction completed: {successful_extractions} successful")

if __name__ == "__main__":
    main()
    
    # Uncomment to run batch extraction
    # batch_extract_pdfs() 