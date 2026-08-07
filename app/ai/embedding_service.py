class EmbeddingService:
    def __init__(self, client, model="text-embedding-3-small"):
        self.client = client
        self.model = model

    def create_embeddings(self, texts):
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )

        sorted_data = sorted(
            response.data,
            key=lambda item: item.index
        )

        return [
            item.embedding
            for item in sorted_data
        ]