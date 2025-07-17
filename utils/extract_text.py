from pypdf import PdfReader
import docx
import os
import re
import logging
import comtypes.client

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
    """Convert .doc to .docx using Word COM interface and extract text"""
    try:
        # Generate temporary file paths
        docx_path = os.path.splitext(filepath)[0] + ".docx"
        
        # Convert using Word COM interface
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(filepath))
        doc.SaveAs2(os.path.abspath(docx_path), FileFormat=16)  # 16 = wdFormatDOCX
        doc.Close()
        word.Quit()
        
        # Extract text from converted docx
        text = extract_docx(docx_path)
        
        # Cleanup temporary file
        os.remove(docx_path)
        return text
    except Exception as e:
        logging.error(f"DOC extraction error: {str(e)}")
        return ""
    finally:
        # Ensure Word process is closed
        try:
            word.Quit()
        except:
            pass

def clean_text(text):
    # Remove excessive whitespace and non-printable characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()