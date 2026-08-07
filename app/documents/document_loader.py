from pathlib import Path
from pypdf import PdfReader
from app.documents.document import Document
from app.documents.text_cleaner import clean_text

def load_document(file_path, document_type):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    file_extension = path.suffix.lower()

    if file_extension == ".txt":
        text = path.read_text(encoding="utf-8")

    elif file_extension == ".pdf":
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                pages.append(page_text)

        text = "\n".join(pages)

    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}. "
            "Only .txt and .pdf are supported."
        )

    text = clean_text(text)

    if not text.strip():
        raise ValueError(f"No readable text found in: {file_path}")

    return Document(
        text=text,
        document_type=document_type,
        source_name=path.name
    )