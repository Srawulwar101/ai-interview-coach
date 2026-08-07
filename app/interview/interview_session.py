from app.ai.prompts import (
    get_structured_evaluation_prompt,
    get_next_question_prompt,
    EVALUATION_SCHEMA,
    NEXT_QUESTION_SCHEMA
)

import json
from datetime import datetime
import os

class InterviewSession:
    def __init__(self, chatbot, plan, context, rag_service):
        self.chatbot = chatbot
        self.plan = plan
        self.context = context
        self.rag_service = rag_service

        self.current_question_index = 0
        self.results = []
        self.covered_topics = []

    def run_session(self):
        print(f"\n{self.plan.name} started.")
        print("Type 'quit' anytime to end.\n")

        if (self.plan.interview_type == "mock" or self.chatbot.mode == "general"):
            question_data = {
                "question": "Tell me about yourself.",
                "question_type": "introduction",
                "topic": "introduction",
                "is_follow_up": False
            }

        else:
            question_data = self.generate_next_question()

        while self.current_question_index < self.plan.max_questions:
            question = question_data["question"]
            question_type = question_data["question_type"]
            topic = question_data["topic"]

            print(
                f"Question {self.current_question_index + 1} "
                f"({question_type.title()}): {question}"
            )

            answer = input("Your answer: ")

            if answer.lower() == "quit":
                break

            evaluation_query = (
                f"Interview question: {question} "
                f"Candidate answer: {answer}"
            )

            resume_evaluation_context = self.rag_service.retrieve_context(
                query=evaluation_query,
                number_of_results=3,
                document_type="resume"
            )

            job_evaluation_context = self.rag_service.retrieve_context(
                query=evaluation_query,
                number_of_results=2,
                document_type="job_description"
            )

            evaluation_prompt = get_structured_evaluation_prompt(
                question=question,
                answer=answer,
                resume_context=resume_evaluation_context,
                job_context=job_evaluation_context
            )

            feedback = self.chatbot.get_structured_response(
                prompt=evaluation_prompt,
                schema=EVALUATION_SCHEMA
            )

            feedback["overall_score"] = self.calculate_overall_score(
                feedback["ratings"]
            )

            self.results.append({
                "question_type": question_type,
                "topic": topic,
                "question": question,
                "answer": answer,
                "evaluation": feedback
            })

            if topic not in self.covered_topics:
                self.covered_topics.append(topic)

            self.current_question_index += 1

            if self.plan.interview_type == "practice":
                self.print_feedback(feedback)

            if self.current_question_index >= self.plan.max_questions:
                break

            question_data = self.generate_next_question()

        self.print_summary()
        print(f"{self.plan.name} ended.")


    def save_results(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        output_dir = f"interview_results/{self.plan.interview_type}"
        os.makedirs(output_dir, exist_ok=True)

        filename = (
            f"{output_dir}/"
            f"session_{self.chatbot.mode}_{timestamp}.json"
        )

        interview_data = {
            "mode": self.chatbot.mode,
            "plan_name": self.plan.name,
            "interview_type": self.plan.interview_type,
            "timestamp": timestamp,

            "custom_configuration": {
                "focus_topics": self.plan.custom_focus_topics,
                "question_type_targets": self.plan.question_type_targets
            } if self.plan.interview_type == "custom" else None,

            "results": self.results,
            "statistics": self.get_statistics(),
            "context": {
                "resume": {
                    "text": self.context.resume.text,
                    "document_type": self.context.resume.document_type,
                    "source_name": self.context.resume.source_name
                } if self.context.resume else None,

                "job_description": {
                    "text": self.context.job_description.text,
                    "document_type": self.context.job_description.document_type,
                    "source_name": self.context.job_description.source_name
                } if self.context.job_description else None
            }
        }

        with open(filename, "w") as file:
            json.dump(interview_data, file, indent=4)


    def calculate_overall_score(self, ratings):
        return round(sum(ratings.values()) / len(ratings))
    

    def get_statistics(self):
        if not self.results:
            return {
                "questions_answered": 0,
                "overall_average": None,
                "category_averages": {},
                "strongest_category": None,
                "weakest_category": None,
                "question_scores": []
            }

        overall_scores = []
        category_totals = {}
        question_scores = []

        for result in self.results:
            evaluation = result["evaluation"]
            overall_score = evaluation["overall_score"]

            overall_scores.append(overall_score)

            question_scores.append({
                "question": result["question"],
                "question_type": result["question_type"],
                "overall_score": overall_score
            })

            for category, score in evaluation["ratings"].items():
                if category not in category_totals:
                    category_totals[category] = []

                category_totals[category].append(score)

        category_averages = {}

        for category, scores in category_totals.items():
            category_averages[category] = round(sum(scores) / len(scores), 1)

        strongest_category = max(category_averages, key=category_averages.get)
        weakest_category = min(category_averages, key=category_averages.get)

        return {
            "questions_answered": len(self.results),
            "overall_average": round(sum(overall_scores) / len(overall_scores), 1),
            "category_averages": category_averages,
            "strongest_category": strongest_category,
            "weakest_category": weakest_category,
            "question_scores": question_scores
        }
    

    def print_summary(self):
        stats = self.get_statistics()

        print("\n====================================")
        print("Interview Summary")
        print("====================================")

        if stats["questions_answered"] == 0:
            print("No questions answered.")
            return

        print(f"\nQuestions answered: {stats['questions_answered']}")
        print(f"Overall interview score: {stats['overall_average']}/10")

        print("\nQuestion Scores:")
        for index, question_score in enumerate(stats["question_scores"], start=1):
            print(
                f"{index}. ({question_score['question_type'].title()}) "
                f"{question_score['overall_score']}/10 - "
                f"{question_score['question']}"
            )

        print("\nCategory Averages:")
        for category, average in stats["category_averages"].items():
            print(f"- {category.title()}: {average}/10")

        print("\nStrongest Area:")
        print(f"- {stats['strongest_category'].title()}")

        print("\nNeeds Most Improvement:")
        print(f"- {stats['weakest_category'].title()}")
        print()


    def generate_next_question(self):
        remaining_topics = [
            topic
            for topic in self.plan.topics
            if topic not in self.covered_topics
        ]

        history = self.format_interview_history()

        retrieval_query = self.build_retrieval_query(
            remaining_topics=remaining_topics
        )

        resume_context = self.rag_service.retrieve_context(
            query=retrieval_query,
            number_of_results=4,
            document_type="resume"
        )

        job_context = self.rag_service.retrieve_context(
            query=retrieval_query,
            number_of_results=3,
            document_type="job_description"
        )

        current_focus_topic = None

        if self.plan.custom_focus_topics:
            topic_index = (
                self.current_question_index
                % len(self.plan.custom_focus_topics)
            )

            current_focus_topic = self.plan.custom_focus_topics[topic_index]

        prompt = get_next_question_prompt(
            plan=self.plan,
            mode=self.chatbot.mode,
            interview_history=history,
            remaining_topics=remaining_topics,
            current_focus_topic=current_focus_topic,
            resume_context=resume_context,
            job_context=job_context
        )

        return self.chatbot.get_structured_response(
            prompt=prompt,
            schema=NEXT_QUESTION_SCHEMA
        )


    def build_retrieval_query(self, remaining_topics):
        if not self.results:
            return (
                "Retrieve candidate background information useful for generating "
                f"an opening {self.chatbot.mode} interview question. "
                f"Relevant interview topics: {', '.join(remaining_topics)}. "
                "Consider the candidate's professional experience, projects, skills, "
                "education, accomplishments, and responsibilities. "
                "Return information that best matches the selected interview mode."
            )

        last_result = self.results[-1]

        return (
            "Find information useful for generating the next interview question. "
            f"Remaining interview topics: {', '.join(remaining_topics)}. "
            f"The previous question was: {last_result['question']}. "
            f"The candidate answered: {last_result['answer']}"
        )


    def format_interview_history(self):
        recent_results = self.results[-3:]

        if not recent_results:
            return "No previous questions have been answered."

        formatted_history = []

        for index, result in enumerate(recent_results, start=1):
            formatted_history.append(
                f"Question {index}: {result['question']}\n"
                f"Candidate answer: {result['answer']}"
            )

        return "\n\n".join(formatted_history)
    

    def print_feedback(self, feedback):
        print("\nFeedback:")
        print(f"Overall Score: {feedback['overall_score']}/10")

        print("\nRatings:")
        for category, score in feedback["ratings"].items():
            print(f"- {category.title()}: {score}/10")

        print("\nStrengths:")
        for strength in feedback["strengths"]:
            print(f"- {strength}")

        print("\nImprovements:")
        for improvement in feedback["improvements"]:
            print(f"- {improvement}")

        print("\nBetter Answer:")
        print(feedback["better_answer"])
        print()