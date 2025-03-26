import PyPDF2
import docx2txt
import io
import os
from typing import Dict, Any

def parse_document(uploaded_file, filename):
    """
    Parse document content from various file formats.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        filename: The name of the uploaded file
        
    Returns:
        Dictionary with parsed text and metadata
    """
    try:
        # Get file extension
        file_ext = filename.split('.')[-1].lower()
        
        # Parse based on file type
        if file_ext == 'pdf':
            return parse_pdf(uploaded_file)
        elif file_ext in ['docx', 'doc']:
            return parse_docx(uploaded_file)
        elif file_ext == 'txt':
            return parse_txt(uploaded_file)
        else:
            return {
                "success": False,
                "error": f"Unsupported file format: {file_ext}",
                "text": "",
                "metadata": {}
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": "",
            "metadata": {}
        }

def parse_pdf(pdf_file):
    """Parse content from PDF file"""
    try:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.getvalue()))
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
        
        # Extract metadata
        metadata = {
            "pages": len(pdf_reader.pages),
            "format": "PDF"
        }
        
        return {
            "success": True,
            "text": text,
            "metadata": metadata,
            "error": None
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing PDF: {str(e)}",
            "text": "",
            "metadata": {}
        }

def parse_docx(docx_file):
    """Parse content from DOCX file"""
    try:
        # Extract text from DOCX
        text = docx2txt.process(io.BytesIO(docx_file.getvalue()))
        
        # Create metadata
        metadata = {
            "format": "DOCX"
        }
        
        return {
            "success": True,
            "text": text,
            "metadata": metadata,
            "error": None
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing DOCX: {str(e)}",
            "text": "",
            "metadata": {}
        }

def parse_txt(txt_file):
    """Parse content from TXT file"""
    try:
        # Read text file
        text = txt_file.getvalue().decode("utf-8")
        
        # Create metadata
        metadata = {
            "format": "TXT"
        }
        
        return {
            "success": True,
            "text": text,
            "metadata": metadata,
            "error": None
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing TXT: {str(e)}",
            "text": "",
            "metadata": {}
        }

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> list:
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text: The text to split into chunks
        chunk_size: Maximum chunk size in characters
        overlap: Overlap size between chunks in characters
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        # Don't create tiny chunks at the end
        if end == text_length and end - start < chunk_size / 2:
            # Extend the previous chunk instead
            if chunks:
                chunks[-1] = text[start - chunk_size + overlap:end]
            else:
                chunks.append(text[start:end])
            break
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks 