from pypdf import PdfReader
import docx
import os
import re
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO)

def extract_text(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == ".pdf":
            return extract_pdf(filepath)
        elif ext == ".docx":
            return extract_docx(filepath)
        elif ext == ".doc":
            return extract_doc(filepath)
        else:  # Text files
            with open(filepath, "r", encoding="utf-8", errors="replace") as file:
                return clean_text(file.read())
    except Exception as e:
        logging.error(f"Error extracting {filepath}: {str(e)}")
        return ""

def extract_pdf(filepath):
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        logging.error(f"PDF extraction error: {str(e)}")
    return clean_text(text)

def extract_docx(filepath):
    try:
        doc = docx.Document(filepath)
        return clean_text("\n".join([para.text for para in doc.paragraphs]))
    except Exception as e:
        logging.error(f"DOCX extraction error: {str(e)}")
        return ""

def extract_doc(filepath):
    """Platform-agnostic .doc extraction"""
    try:
        # Try using antiword if available
        if shutil.which('antiword'):
            result = subprocess.run(
                ['antiword', filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return clean_text(result.stdout)
        
        # Fallback to text extraction
        logging.warning("antiword not available, using fallback text extraction")
        with open(filepath, 'rb') as f:
            content = f.read().decode('ascii', errors='ignore')
            return clean_text(content)
    except Exception as e:
        logging.error(f"DOC extraction error: {str(e)}")
        return ""

def clean_text(text):
    # Remove excessive whitespace and non-printable characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()