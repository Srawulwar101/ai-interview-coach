from dataclasses import dataclass

@dataclass
class Document:
    text: str
    document_type: str
    source_name: str | None = None