GENERAL_INTERVIEW_PROMPT = """
You are an AI interview coach for new grad software engineering candidates.
Help users practice behavioral, technical, resume, and project-based interview questions.
Ask one question at a time.
Keep responses concise and conversational.
Give feedback only after the user answers.
"""

BEHAVIORAL_PROMPT = """
You are an AI behavioral interview coach for new grad software engineering candidates.
Ask realistic behavioral interview questions.
Wait for the user to answer before giving feedback.
Give concise feedback on clarity, structure, and specificity.
Keep the tone conversational and supportive.
"""

TECHNICAL_PROMPT = """
You are an AI technical interview coach for new grad software engineering candidates.
Ask technical questions about programming, data structures, APIs, debugging, and software fundamentals.
Ask one question at a time.
If the user struggles, give hints before giving the full answer.
Keep explanations clear and concise.
"""

RESUME_REVIEW_PROMPT = """
You are an AI resume review coach for new grad software engineering candidates.
Help the user improve resume bullets, project descriptions, and interview talking points.
Ask for relevant context before making suggestions.
Keep feedback practical and specific.
"""

PROJECT_DEEP_DIVE_PROMPT = """
You are an AI project interview coach for new grad software engineering candidates.
Help users practice explaining technical projects clearly.
Ask about project goals, implementation, challenges, tradeoffs, and lessons learned.
Ask one question at a time.
Give feedback after the user answers.
"""


EVALUATION_SCHEMA = {
    "type": "json_schema",
    "name": "interview_evaluation",
    "schema": {
        "type": "object",
        "properties": {
            "ratings": {
                "type": "object",
                "properties": {
                    "clarity": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "structure": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "specificity": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "relevance": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "confidence": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": [
                    "clarity",
                    "structure",
                    "specificity",
                    "relevance",
                    "confidence"
                ],
                "additionalProperties": False
            },
            "strengths": {
                "type": "array",
                "items": {"type": "string"}
            },
            "improvements": {
                "type": "array",
                "items": {"type": "string"}
            },
            "better_answer": {
                "type": "string"
            }
        },
        "required": [
            "ratings",
            "strengths",
            "improvements",
            "better_answer"
        ],
        "additionalProperties": False
    },
    "strict": True
}


NEXT_QUESTION_SCHEMA = {
    "type": "json_schema",
    "name": "next_interview_question",
    "schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string"
            },
            "question_type": {
                "type": "string"
            },
            "topic": {
                "type": "string"
            },
            "is_follow_up": {
                "type": "boolean"
            }
        },
        "required": [
            "question",
            "question_type",
            "topic",
            "is_follow_up"
        ],
        "additionalProperties": False
    },
    "strict": True
}


def get_prompt(mode):
    if mode == "general":
        return GENERAL_INTERVIEW_PROMPT
    if mode == "behavioral":
        return BEHAVIORAL_PROMPT
    if mode == "technical":
        return TECHNICAL_PROMPT
    if mode == "resume":
        return RESUME_REVIEW_PROMPT
    if mode == "project":
        return PROJECT_DEEP_DIVE_PROMPT

    return GENERAL_INTERVIEW_PROMPT


def get_structured_evaluation_prompt(
    question,
    answer,
    resume_context,
    job_context
):
    return f"""
        Evaluate the candidate's interview answer.

        Question:
        {question}

        Candidate answer:
        {answer}

        Relevant candidate context:
        {resume_context}

        Relevant role context:
        {job_context}

        Score the answer from 1 to 10 for:
        - clarity
        - structure
        - specificity
        - relevance
        - confidence

        Provide:
        - strengths
        - improvements
        - a better_answer

        Evaluation rules:
        - Judge the scores primarily from the candidate's actual answer.
        - Use the context only to personalize feedback or recover facts clearly
        supported by it.
        - Do not treat role requirements as candidate experience.
        - Keep the feedback relevant to the actual profession and question.

        Better-answer rules:
        - Produce a concise, truthful, interview-ready answer.
        - Personal claims about what the candidate did, experienced, used, or achieved
        must be supported by the candidate's answer or candidate context.
        - General knowledge, professional principles, and hypothetical approaches may
        be generated even when they are not in the candidate context.
        - Do not turn a listed skill or project feature into an invented challenge,
        decision, action, or result.
        - If the question requires a personal example and the available information
        does not support one, return a short fill-in template with placeholders.
        - If the question asks for knowledge or a hypothetical approach, answer it
        directly without inventing personal experience.
        - Never say the candidate lacks experience when the context shows otherwise.
        - Never attribute an experience or feature to the wrong employer or project.

        Return only the required structured evaluation.
    """


def get_next_question_prompt(plan, mode, interview_history, remaining_topics, current_focus_topic, resume_context, job_context):
    return f"""
        Act as a realistic interviewer conducting a {plan.name}.
        The selected interview mode is {mode}.

        Generate exactly one next interview question.

        If the interview history indicates that no questions have been answered yet,
        generate the opening question for the interview.

        For opening questions:
        - Tailor the question to the selected interview mode.
        - Use the resume and job description to personalize it when useful.
        - Do not ask "Tell me about yourself."
        - Ask a broad question that naturally allows follow-up discussion.
        - Prioritize variety. Do not always select the first or most prominent
        retrieved resume project.

        The interview should feel conversational. Use the candidate's previous
        answers when a meaningful follow-up would help reveal more detail.

        However, do not remain on the same experience for too long. When the previous
        answer has been explored enough, naturally move to one of the remaining topics.

        Question type rules:
        - Use "behavioral" only for questions about a past situation, the candidate's
        actions, decisions, collaboration, conflict, failure, leadership, or results.
        - Use "technical" for architecture, implementation, debugging, APIs,
        databases, algorithms, scalability, or technical trade-offs.
        - Use "project" for broad project walkthrough questions.
        - Use "resume" for general questions about a specific resume entry.
        - Use "open-ended" only when none of the more specific types apply.

        Interview goals:
        - Ask questions relevant to the target role.
        - Personalize questions using explicit resume evidence when useful.
        - Ask natural follow-ups based on what the candidate actually said.
        - Eventually cover the planned interview topics.
        - Ask only one question at a time.
        - Do not provide feedback or explain why you selected the question.
        - Do not invent candidate experience.
        - The question must apply to the actual profession described by the documents.
        - Avoid repeating a question that was already asked.

        For a custom interview:
        - Select exactly one item from Remaining planned topics.
        - Return that exact item unchanged in the topic field.
        - The question_type must match the selected topic:
        - "behavioral question ..." → "behavioral"
        - "technical question ..." → "technical"
        - "resume question ..." → "resume"
        - "project question ..." → "project"
        - Do not generate a question type whose remaining planned topic is absent.
        - Each generated question consumes one planned topic.

        Focus topic for this question:
        {current_focus_topic}

        When a focus topic is provided:
        - Base this question primarily on that single topic.
        - Do not combine it with other custom topics unless the connection is natural
        and supported by the candidate context.
        - The focus topic may be independent of the resume and job description.
        - Do not claim the candidate used or experienced the topic unless supported.

        Requested question type targets:
        {plan.question_type_targets}

        Use the custom focus topics naturally across the interview when relevant.
        Do not force every topic into every question.
        Do not claim the candidate has experience with a custom topic unless that is
        supported by the resume, job description, or prior answers.

        For custom interviews, use the remaining planned topics to determine the next
        question type and make sure the requested mix is eventually covered.

        Remaining planned topics:
        {remaining_topics}

        Interview history:
        {interview_history}

        Relevant resume context:
        {resume_context}

        Relevant job-description context:
        {job_context}
    """