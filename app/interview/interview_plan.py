class InterviewPlan:
    def __init__(
        self,
        name,
        interview_type,
        topics,
        max_questions,
        custom_focus_topics=None,
        question_type_targets=None
    ):
        self.name = name
        self.interview_type = interview_type
        self.topics = topics
        self.max_questions = max_questions
        self.custom_focus_topics = custom_focus_topics or []
        self.question_type_targets = question_type_targets or {}


def create_practice_interview_plan(mode):
    topics_by_mode = {
        "behavioral": [
            "introduction",
            "learning and adaptability",
            "teamwork",
            "challenges and problem solving",
            "feedback or conflict"
        ],
        "technical": [
            "technical background",
            "role-relevant technical knowledge",
            "technical decision making",
            "debugging and problem solving",
            "technical experience"
        ],
        "project": [
            "project overview",
            "candidate ownership",
            "technical or professional challenges",
            "decisions and tradeoffs",
            "lessons learned"
        ],
        "resume": [
            "background introduction",
            "relevant experience",
            "skills and accomplishments",
            "projects or work experience",
            "career direction"
        ],
        "general": [
            "introduction",
            "relevant experience",
            "behavioral experience",
            "role-relevant knowledge",
            "motivation and role fit"
        ]
    }

    topics = topics_by_mode.get(mode, topics_by_mode["general"])

    return InterviewPlan(
        name=f"{mode.title()} Practice",
        interview_type="practice",
        topics=topics,
        max_questions=5
    )


def create_mock_interview_plan():
    return InterviewPlan(
        name="General Mock Interview",
        interview_type="mock",
        topics=[
            "introduction",
            "resume and relevant experience",
            "behavioral experience",
            "project or accomplishment",
            "role-relevant knowledge",
            "motivation and role fit"
        ],
        max_questions=6
    )


def create_custom_interview_plan(custom_focus_topics, question_type_targets):
    max_questions = sum(question_type_targets.values())

    topics = []

    for question_type, count in question_type_targets.items():
        for number in range(1, count + 1):
            topics.append(
                f"{question_type} question {number}"
            )

    return InterviewPlan(
        name="Custom Interview",
        interview_type="custom",
        topics=topics,
        max_questions=max_questions,
        custom_focus_topics=custom_focus_topics,
        question_type_targets=question_type_targets
    )