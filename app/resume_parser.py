from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF resume.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(docx_path):
    """
    Extract text from a Word DOCX resume.
    """

    document = Document(docx_path)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text


def extract_text(file_path):
    """
    Extract text based on the file extension.
    """

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format.")