# PDF Extraction Tool for Book Creation

This toolkit provides accurate PDF text extraction capabilities for creating book sections from PDF documents.

## 📁 Project Structure

```
Cursor Entire Convo Book/
├── book sections/          # 12 organized sections for your book
│   ├── 1/                 # Section 1
│   ├── 2/                 # Section 2
│   ├── ...
│   └── 12/                # Section 12
├── pdf_extractor.py       # Main PDF extraction tool
├── example_usage.py       # Usage examples
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python pdf_extractor.py --help
   ```

## 📖 Usage

### Command Line Interface

Extract text from a PDF file:
```bash
python pdf_extractor.py your_file.pdf
```

Extract with specific method:
```bash
python pdf_extractor.py your_file.pdf -m pymupdf
```

Extract and save each page separately:
```bash
python pdf_extractor.py your_file.pdf --pages
```

Extract with custom output location:
```bash
python pdf_extractor.py your_file.pdf -o extracted_text.txt
```

### Python API

```python
from pdf_extractor import PDFExtractor

# Create extractor
extractor = PDFExtractor("your_file.pdf")

# Extract text (auto-selects best method)
results = extractor.extract_text()

# Save to file
extractor.save_text_to_file("output.txt")

# Save each page separately
extractor.save_page_by_page("pages_directory")
```

### Organizing into Book Sections

Use the example script to organize PDFs into book sections:

```python
from example_usage import extract_pdf_to_section

# Extract a PDF to section 1
extract_pdf_to_section("chapter1.pdf", 1)

# Extract multiple PDFs to different sections
extract_pdf_to_section("introduction.pdf", 1)
extract_pdf_to_section("methodology.pdf", 2)
extract_pdf_to_section("results.pdf", 3)
```

## 🔧 Extraction Methods

The tool supports multiple extraction methods for maximum accuracy:

1. **PyMuPDF** (Primary) - Most accurate for standard PDFs
2. **pdfplumber** - Excellent for tables and structured data
3. **PyPDF2** - Fallback method for difficult PDFs

The tool automatically selects the best method, but you can specify one:

```bash
python pdf_extractor.py file.pdf -m pymupdf    # Use PyMuPDF
python pdf_extractor.py file.pdf -m pdfplumber # Use pdfplumber
python pdf_extractor.py file.pdf -m pypdf2     # Use PyPDF2
python pdf_extractor.py file.pdf -m auto       # Auto-select (default)
```

## 📊 Features

- **Multiple extraction methods** for maximum accuracy
- **Automatic method selection** based on PDF characteristics
- **Page-by-page extraction** for detailed organization
- **Metadata preservation** including page counts and character counts
- **Structured output** with proper formatting
- **Error handling** with graceful fallbacks
- **Batch processing** capabilities
- **Command-line interface** for easy automation

## 🎯 Book Section Organization

The tool creates 12 numbered sections in the `book sections/` directory:

```
book sections/
├── 1/    # Section 1 content
├── 2/    # Section 2 content
├── ...
└── 12/   # Section 12 content
```

Each section can contain:
- Extracted text files
- Page-by-page text files
- Metadata about the extraction

## 🔍 Examples

### Extract Single PDF

```bash
python pdf_extractor.py document.pdf
```

Output:
```
Extraction completed!
Method used: PyMuPDF
Total pages: 25
Total characters: 45,123
Text extraction successful!
```

### Batch Process Multiple PDFs

```python
# In your Python script
from example_usage import batch_extract_pdfs

# Configure your PDF mappings
pdf_section_mapping = {
    "intro.pdf": 1,
    "chapter1.pdf": 2,
    "chapter2.pdf": 3,
    "conclusion.pdf": 12
}

batch_extract_pdfs()
```

### Extract with Verbose Output

```bash
python pdf_extractor.py document.pdf -v
```

## 🛠️ Troubleshooting

### Common Issues

1. **ImportError: No module named 'fitz'**
   ```bash
   pip install PyMuPDF
   ```

2. **Permission denied error**
   - Ensure you have read permissions for the PDF file
   - Check that the output directory is writable

3. **Empty extraction results**
   - Try a different extraction method: `-m pdfplumber`
   - The PDF might be image-based (consider OCR tools)

4. **Memory issues with large PDFs**
   - Use page-by-page extraction: `--pages`
   - Process in smaller chunks

### PDF Compatibility

The tool works best with:
- ✅ Text-based PDFs
- ✅ PDFs with embedded fonts
- ✅ Multi-column layouts
- ✅ PDFs with tables and structured data

Less optimal for:
- ❌ Image-only PDFs (scanned documents)
- ❌ Password-protected PDFs
- ❌ Heavily formatted PDFs with complex layouts

## 📝 Output Format

### Main Text File
```
PDF Extraction Results
==================================================
Source File: /path/to/your/document.pdf
Extraction Method: PyMuPDF
Total Pages: 25
Total Characters: 45,123
==================================================

[Extracted text content here...]
```

### Page Files
```
Page 1
====================
[Page 1 content here...]
```

## 🤝 Contributing

Feel free to improve this tool by:
- Adding new extraction methods
- Improving accuracy for specific PDF types
- Adding OCR capabilities
- Enhancing the book organization features

## 📄 License

This project is open source and available under the MIT License. 