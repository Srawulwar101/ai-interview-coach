import chromadb

class VectorStore:
    def __init__(
        self,
        collection_name="interview_documents",
        persist_directory="chroma_db"
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, document, chunks, embeddings):
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Each chunk must have one corresponding embedding."
            )

        ids = []
        metadatas = []

        for index in range(len(chunks)):
            chunk_id = (
                f"{document.document_type}-"
                f"{document.source_name}-"
                f"{index}"
            )

            ids.append(chunk_id)

            metadatas.append({
                "document_type": document.document_type,
                "source_name": document.source_name,
                "chunk_index": index
            })

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, number_of_results=3, document_type=None):
        if not query_embedding:
            return []

        query_arguments = {
            "query_embeddings": [query_embedding],
            "n_results": number_of_results
        }

        if document_type:
            query_arguments["where"] = {
                "document_type": document_type
            }

        return self.collection.query(**query_arguments)

    def count(self):
        return self.collection.count()