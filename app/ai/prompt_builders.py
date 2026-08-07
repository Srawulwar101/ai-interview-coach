def build_grounded_qa_prompt(query, retrieved_context):
    return f"""
        Answer the user's question using only the retrieved context.

        Use facts explicitly stated in the context.
        Do not invent or infer unsupported experience, technologies, metrics,
        employers, projects, or job requirements.

        If the context does not contain enough information to answer the question,
        say so clearly.

        Retrieved context:
        {retrieved_context}

        User question:
        {query}
    """


def build_resume_match_prompt(
    query,
    job_context,
    resume_context
):
    return f"""
        Compare the candidate's resume against the target job description.

        Provide exactly these sections:

        1. Matching requirements
        For each match, state:
        - The job requirement
        - The explicit resume evidence supporting it

        2. Partial or unclear matches
        Include requirements where related evidence exists, but the requirement
        is not fully demonstrated.

        3. Unsupported requirements
        List requirements with no explicit supporting evidence in the resume context.

        Rules:
        - Use only facts explicitly stated in the retrieved context.
        - Do not infer technologies based on the type of project.
        - Do not invent experience, skills, metrics, technologies, or requirements.
        - A requirement may appear in only one section.
        - Cite explicitly listed skills directly instead of inferring them from tools.
        - Distinguish certifications, listed skills, and hands-on experience.
        - Do not attribute an accomplishment to a company or project unless that
        relationship is clear in the retrieved context.
        - Do not ask the user a follow-up question.

        Target job description:
        {job_context}

        Candidate resume:
        {resume_context}

        User question:
        {query}
    """