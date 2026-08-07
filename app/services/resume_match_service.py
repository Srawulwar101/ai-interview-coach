from app.ai.prompt_builders import build_resume_match_prompt


class ResumeMatchService:
    def __init__(self, rag_service, chatbot):
        self.rag_service = rag_service
        self.chatbot = chatbot

    def compare(self, query):
        job_context = self.rag_service.retrieve_context(
            query=query,
            number_of_results=3,
            document_type="job_description"
        )

        resume_context = self.rag_service.retrieve_context(
            query=query,
            number_of_results=6,
            document_type="resume"
        )

        prompt = build_resume_match_prompt(
            query=query,
            job_context=job_context,
            resume_context=resume_context
        )

        return self.chatbot.get_response(prompt)