from app.documents.document_chunker import chunk_text

class DocumentIndexer:
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_document(
        self,
        document,
        chunk_size=500,
        overlap=100
    ):
        chunks = chunk_text(
            document.text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        embeddings = self.embedding_service.create_embeddings(
            chunks
        )

        self.vector_store.add_chunks(
            document=document,
            chunks=chunks,
            embeddings=embeddings
        )

        return len(chunks)