import io
import pypdf
import docx2txt
import os
from typing import Dict, Any

def parse_document(file_stream, file_name: str) -> Dict[str, Any]:
    """
    Parse uploaded document and extract text content.
    
    Args:
        file_stream: The uploaded file stream
        file_name: The name of the uploaded file
        
    Returns:
        A dictionary containing the document metadata and extracted text
    """
    file_extension = os.path.splitext(file_name)[1].lower()
    
    document_info = {
        "file_name": file_name,
        "extension": file_extension,
        "text": "",
        "pages": 0,
        "success": False,
        "error": None
    }
    
    try:
        if file_extension == ".pdf":
            # Handle PDF files
            pdf_reader = pypdf.PdfReader(file_stream)
            document_info["pages"] = len(pdf_reader.pages)
            
            text_content = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content.append(page.extract_text())
            
            document_info["text"] = "\n".join(text_content)
            document_info["success"] = True
            
        elif file_extension in [".docx", ".doc"]:
            # Handle Word documents
            text = docx2txt.process(file_stream)
            document_info["text"] = text
            document_info["success"] = True
            
        elif file_extension in [".txt"]:
            # Handle plain text files
            text = file_stream.read().decode('utf-8')
            document_info["text"] = text
            document_info["success"] = True
            
        else:
            document_info["error"] = f"Unsupported file format: {file_extension}"
            
    except Exception as e:
        document_info["error"] = f"Error parsing document: {str(e)}"
    
    return document_info

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> list:
    """
    Split the document text into overlapping chunks for processing.
    
    Args:
        text: The full document text
        chunk_size: The maximum size of each chunk
        overlap: The number of characters to overlap between chunks
        
    Returns:
        A list of text chunks
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If we're not at the end of the text, try to find a good breaking point
        if end < len(text):
            # Try to find a period or newline to break at
            break_point = text.rfind('. ', start + chunk_size - overlap, start + chunk_size)
            if break_point == -1:
                break_point = text.rfind('\n', start + chunk_size - overlap, start + chunk_size)
            
            if break_point != -1:
                end = break_point + 1
        
        # Add the chunk to our list
        chunks.append(text[start:end])
        
        # Move the start pointer, ensuring we have overlap
        start = max(start, end - overlap)
        
        # If we're near the end, just include the rest of the text
        if start + chunk_size >= len(text):
            start = min(start, len(text) - 1)
    
    return chunks 