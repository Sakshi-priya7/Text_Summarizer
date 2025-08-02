import docx2txt
import fitz  # PyMuPDF

def read_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def read_docx(file):
    return docx2txt.process(file)

def clean_text(text):
    return text.replace('\n', ' ').strip()