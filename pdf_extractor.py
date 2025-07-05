#!/usr/bin/env python3
"""
Comprehensive PDF Text Extraction Tool

This script provides multiple methods for extracting text from PDF files
with high accuracy, including fallback methods for challenging PDFs.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union, Any
import argparse

# PDF extraction libraries
try:
    import fitz  # PyMuPDF
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False
    print("Warning: PyMuPDF not available. Install with: pip install PyMuPDF")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    print("Warning: pdfplumber not available. Install with: pip install pdfplumber")

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    print("Warning: PyPDF2 not available. Install with: pip install PyPDF2")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFExtractor:
    """
    A comprehensive PDF text extraction class with multiple extraction methods.
    """
    
    def __init__(self, pdf_path: Union[str, Path]):
        """
        Initialize the PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.text_content = ""
        self.page_texts = []
        self.metadata = {}
        
    def extract_with_pymupdf(self) -> Dict[str, Any]:
        """
        Extract text using PyMuPDF (most accurate for most PDFs).
        
        Returns:
            Dict containing extracted text and metadata
        """
        if not FITZ_AVAILABLE:
            raise ImportError("PyMuPDF not available")
        
        try:
            doc = fitz.open(self.pdf_path)
            page_texts = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Extract text with formatting preservation
                text = page.get_text()
                
                # Alternative: Extract text blocks for better structure
                blocks = page.get_text("blocks")
                structured_text = ""
                for block in blocks:
                    if len(block) >= 5:  # Text block
                        structured_text += block[4] + "\n"
                
                page_texts.append({
                    'page_number': page_num + 1,
                    'text': text,
                    'structured_text': structured_text,
                    'char_count': len(text)
                })
            
            doc.close()
            
            # Combine all text
            full_text = "\n".join([page['text'] for page in page_texts])
            
            return {
                'method': 'PyMuPDF',
                'full_text': full_text,
                'page_texts': page_texts,
                'total_pages': len(page_texts),
                'total_chars': len(full_text)
            }
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            raise
    
    def extract_with_pdfplumber(self) -> Dict[str, Any]:
        """
        Extract text using pdfplumber (good for tables and structured data).
        
        Returns:
            Dict containing extracted text and metadata
        """
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber not available")
        
        try:
            page_texts = []
            
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract text
                    text = page.extract_text() or ""
                    
                    # Extract tables if present
                    tables = page.extract_tables()
                    table_text = ""
                    for table in tables:
                        for row in table:
                            table_text += "\t".join([cell or "" for cell in row]) + "\n"
                    
                    page_texts.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'table_text': table_text,
                        'char_count': len(text)
                    })
            
            # Combine all text
            full_text = "\n".join([page['text'] for page in page_texts])
            
            return {
                'method': 'pdfplumber',
                'full_text': full_text,
                'page_texts': page_texts,
                'total_pages': len(page_texts),
                'total_chars': len(full_text)
            }
            
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            raise
    
    def extract_with_pypdf2(self) -> Dict[str, Any]:
        """
        Extract text using PyPDF2 (fallback method).
        
        Returns:
            Dict containing extracted text and metadata
        """
        if not PYPDF2_AVAILABLE:
            raise ImportError("PyPDF2 not available")
        
        try:
            page_texts = []
            
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    
                    page_texts.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'char_count': len(text)
                    })
            
            # Combine all text
            full_text = "\n".join([page['text'] for page in page_texts])
            
            return {
                'method': 'PyPDF2',
                'full_text': full_text,
                'page_texts': page_texts,
                'total_pages': len(page_texts),
                'total_chars': len(full_text)
            }
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            raise
    
    def extract_text(self, method: str = 'auto') -> Dict[str, Any]:
        """
        Extract text from PDF using specified method or auto-select best method.
        
        Args:
            method: Extraction method ('auto', 'pymupdf', 'pdfplumber', 'pypdf2')
        
        Returns:
            Dict containing extracted text and metadata
        """
        results = {}
        
        if method == 'auto':
            # Try methods in order of preference
            methods_to_try = []
            if FITZ_AVAILABLE:
                methods_to_try.append('pymupdf')
            if PDFPLUMBER_AVAILABLE:
                methods_to_try.append('pdfplumber')
            if PYPDF2_AVAILABLE:
                methods_to_try.append('pypdf2')
            
            for method_name in methods_to_try:
                try:
                    if method_name == 'pymupdf':
                        results = self.extract_with_pymupdf()
                    elif method_name == 'pdfplumber':
                        results = self.extract_with_pdfplumber()
                    elif method_name == 'pypdf2':
                        results = self.extract_with_pypdf2()
                    
                    # If we got reasonable results, use them
                    if results.get('total_chars', 0) > 0:
                        logger.info(f"Successfully extracted text using {method_name}")
                        break
                        
                except Exception as e:
                    logger.warning(f"Method {method_name} failed: {e}")
                    continue
        
        else:
            # Use specific method
            if method == 'pymupdf':
                results = self.extract_with_pymupdf()
            elif method == 'pdfplumber':
                results = self.extract_with_pdfplumber()
            elif method == 'pypdf2':
                results = self.extract_with_pypdf2()
            else:
                raise ValueError(f"Unknown method: {method}")
        
        # Store results
        self.text_content = results.get('full_text', '')
        self.page_texts = results.get('page_texts', [])
        self.metadata = {
            'file_path': str(self.pdf_path),
            'extraction_method': results.get('method', 'unknown'),
            'total_pages': results.get('total_pages', 0),
            'total_chars': results.get('total_chars', 0)
        }
        
        return results
    
    def save_text_to_file(self, output_path: Union[str, Path], 
                         include_metadata: bool = True) -> None:
        """
        Save extracted text to a file.
        
        Args:
            output_path: Path to save the text file
            include_metadata: Whether to include metadata in the output
        """
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if include_metadata:
                f.write(f"PDF Extraction Results\n")
                f.write(f"{'='*50}\n")
                f.write(f"Source File: {self.metadata.get('file_path', 'Unknown')}\n")
                f.write(f"Extraction Method: {self.metadata.get('extraction_method', 'Unknown')}\n")
                f.write(f"Total Pages: {self.metadata.get('total_pages', 0)}\n")
                f.write(f"Total Characters: {self.metadata.get('total_chars', 0)}\n")
                f.write(f"{'='*50}\n\n")
            
            f.write(self.text_content)
        
        logger.info(f"Text saved to: {output_path}")
    
    def save_page_by_page(self, output_dir: Union[str, Path]) -> None:
        """
        Save each page's text to separate files.
        
        Args:
            output_dir: Directory to save page files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for page_data in self.page_texts:
            page_num = page_data['page_number']
            filename = f"page_{page_num:03d}.txt"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Page {page_num}\n")
                f.write(f"{'='*20}\n")
                f.write(page_data['text'])
        
        logger.info(f"Page files saved to: {output_dir}")


def main():
    """
    Command-line interface for the PDF extractor.
    """
    parser = argparse.ArgumentParser(description='Extract text from PDF files')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output text file path')
    parser.add_argument('-m', '--method', choices=['auto', 'pymupdf', 'pdfplumber', 'pypdf2'],
                       default='auto', help='Extraction method (default: auto)')
    parser.add_argument('--pages', action='store_true', 
                       help='Save each page to separate files')
    parser.add_argument('--page-dir', help='Directory for page files (used with --pages)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create extractor
        extractor = PDFExtractor(args.pdf_path)
        
        # Extract text
        logger.info(f"Extracting text from: {args.pdf_path}")
        results = extractor.extract_text(method=args.method)
        
        # Print summary
        print(f"\nExtraction completed!")
        print(f"Method used: {results['method']}")
        print(f"Total pages: {results['total_pages']}")
        print(f"Total characters: {results['total_chars']}")
        
        # Save results
        if args.output:
            extractor.save_text_to_file(args.output)
        else:
            # Default output name
            pdf_name = Path(args.pdf_path).stem
            output_path = f"{pdf_name}_extracted.txt"
            extractor.save_text_to_file(output_path)
        
        # Save page-by-page if requested
        if args.pages:
            page_dir = args.page_dir or f"{Path(args.pdf_path).stem}_pages"
            extractor.save_page_by_page(page_dir)
        
        print(f"\nText extraction successful!")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 