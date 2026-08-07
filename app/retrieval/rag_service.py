class RAGService:
    def __init__(self, retriever):
        self.retriever = retriever

    def retrieve_context(
        self,
        query,
        number_of_results=5,
        document_type=None
    ):
        results = self.retriever.search(
            query=query,
            number_of_results=number_of_results,
            document_type=document_type
        )

        return self._format_results(results)

    def _format_results(self, results):
        if not results or not results.get("documents"):
            return "No relevant context was retrieved."

        documents = results["documents"][0]

        if not documents:
            return "No relevant context was retrieved."

        metadatas = results["metadatas"][0]
        distances = results.get("distances", [[]])[0]

        sections = []

        for index, (document, metadata) in enumerate(
            zip(documents, metadatas)
        ):
            section = (
                f"Document type: {metadata.get('document_type', 'unknown')}\n"
                f"Source: {metadata.get('source_name', 'unknown')}\n"
                f"Chunk index: {metadata.get('chunk_index', 'unknown')}\n"
            )

            if index < len(distances):
                section += f"Distance: {distances[index]}\n"

            section += f"\nContent:\n{document}"

            sections.append(section)

        return "\n\n---\n\n".join(sections)