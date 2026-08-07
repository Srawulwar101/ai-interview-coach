class Retriever:
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(self, query, number_of_results=3, document_type=None):
        if not query.strip():
            return []

        query_embedding = self.embedding_service.create_embeddings(
            [query]
        )[0]

        return self.vector_store.search(
            query_embedding=query_embedding,
            number_of_results=number_of_results,
            document_type=document_type
        )