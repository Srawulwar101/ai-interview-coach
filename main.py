from uuid import uuid4

from config import get_client

from app.ai.chatbot import Chatbot
from app.ai.embedding_service import EmbeddingService

from app.documents.document import Document
from app.documents.document_loader import load_document

from app.interview.interview_context import InterviewContext
from app.interview.interview_session import InterviewSession
from app.interview.interview_plan import (
    create_practice_interview_plan,
    create_mock_interview_plan,
    create_custom_interview_plan
)

from app.retrieval.document_indexer import DocumentIndexer
from app.retrieval.rag_service import RAGService
from app.retrieval.retriever import Retriever
from app.retrieval.vector_store import VectorStore


def get_resume():
    sample_path = "resumes/sample_resume.txt"

    print("\nProvide a resume:")
    print("1. Use sample resume")
    print("2. Load my own resume")

    choice = input("Enter a number: ").strip()

    if choice == "1":
        file_path = sample_path

    elif choice == "2":
        file_path = input("\nEnter the resume file path: ").strip()

    else:
        print("\nInvalid choice. Using sample resume.")
        file_path = sample_path

    try:
        resume = load_document(
            file_path,
            "resume"
        )

        print("Resume loaded successfully.\n")
        return resume

    except (FileNotFoundError, ValueError, OSError) as error:
        print(
            f"Could not load that resume ({error}). "
            "Using sample resume instead.\n"
        )

        return load_document(
            sample_path,
            "resume"
        )


def get_job_description():
    sample_path = "job_descriptions/sample_job_description.txt"

    print("\nProvide a job description:")
    print("1. Use sample job description")
    print("2. Paste")
    print("3. Load from file")
    print("4. Skip")

    choice = input("Enter a number: ").strip()

    if choice == "1":
        try:
            job_description = load_document(
                sample_path,
                "job_description"
            )

            print("Sample job description loaded successfully.\n")
            return job_description

        except (FileNotFoundError, ValueError, OSError) as error:
            print(
                f"Could not load the sample job description ({error}).\n"
            )
            return None

    elif choice == "2":
        text = input("\nPaste the job description:\n").strip()

        if not text:
            print(
                "No job description was provided. "
                "Using sample job description instead.\n"
            )

            return load_document(
                sample_path,
                "job_description"
            )

        print("Job description pasted successfully.\n")

        return Document(
            text=text,
            document_type="job_description",
            source_name="pasted_text"
        )

    elif choice == "3":
        file_path = input(
            "\nEnter the job description file path: "
        ).strip()

        try:
            job_description = load_document(
                file_path,
                "job_description"
            )

            print("Job description loaded successfully.\n")
            return job_description

        except (FileNotFoundError, ValueError, OSError) as error:
            print(
                f"Could not load that job description ({error}). "
                "Using sample job description instead.\n"
            )

            return load_document(
                sample_path,
                "job_description"
            )

    elif choice == "4":
        print("Continuing without a job description.\n")
        return None

    print("\nInvalid choice. Using sample job description.\n")

    return load_document(
        sample_path,
        "job_description"
    )


client = get_client()

print("AI Interview Coach started.\n")

print("Choose an interview type:")
print("1. Practice")
print("2. Mock Interview")
print("3. Custom Interview")

interview_choice = input(
    "Enter a number or interview type: "
).lower().strip()


resume = get_resume()

job_description = get_job_description()

context = InterviewContext(
    resume=resume,
    job_description=job_description
)


# ---------------------------------------------------------
# Build and populate the RAG pipeline for this interview.
# ---------------------------------------------------------

embedding_service = EmbeddingService(
    client=client
)

# Use a unique collection so an older resume or job description
# cannot accidentally affect the current interview.
collection_name = f"interview_{uuid4().hex}"

vector_store = VectorStore(
    collection_name=collection_name
)

document_indexer = DocumentIndexer(
    embedding_service=embedding_service,
    vector_store=vector_store
)

resume_chunk_count = document_indexer.index_document(
    document=resume
)

print(f"Indexed {resume_chunk_count} resume chunks.")

if job_description:
    job_chunk_count = document_indexer.index_document(
        document=job_description
    )

    print(f"Indexed {job_chunk_count} job-description chunks.")
else:
    print("No job description was indexed.")

retriever = Retriever(
    embedding_service=embedding_service,
    vector_store=vector_store
)

rag_service = RAGService(
    retriever=retriever
)


# ---------------------------------------------------------
# Select the interview plan.
# ---------------------------------------------------------

if "practice" in interview_choice or interview_choice == "1":
    print("\nChoose a practice area:")
    print("1. General")
    print("2. Behavioral")
    print("3. Technical")
    print("4. Resume")
    print("5. Project")

    mode_choice = input(
        "Enter a number or mode name: "
    ).lower().strip()

    if "general" in mode_choice or mode_choice == "1":
        mode = "general"

    elif "behavioral" in mode_choice or mode_choice == "2":
        mode = "behavioral"

    elif "technical" in mode_choice or mode_choice == "3":
        mode = "technical"

    elif "resume" in mode_choice or mode_choice == "4":
        mode = "resume"

    elif "project" in mode_choice or mode_choice == "5":
        mode = "project"

    else:
        mode = "general"

    plan = create_practice_interview_plan(mode)


elif "mock" in interview_choice or interview_choice == "2":
    mode = "general"
    plan = create_mock_interview_plan()


elif "custom" in interview_choice or interview_choice == "3":
    mode = "custom"

    focus_input = input(
        "\nEnter topics you want covered, separated by commas "
        "(or press Enter to skip): "
    ).strip()

    custom_focus_topics = [
        topic.strip()
        for topic in focus_input.split(",")
        if topic.strip()
    ]

    print("\nChoose how many questions of each type you want:")

    while True:
        try:
            behavioral_count = int(
                input("Behavioral questions: ").strip()
            )
            technical_count = int(
                input("Technical questions: ").strip()
            )
            resume_count = int(
                input("Resume questions: ").strip()
            )
            project_count = int(
                input("Project questions: ").strip()
            )

            counts = [
                behavioral_count,
                technical_count,
                resume_count,
                project_count
            ]

            total_questions = sum(counts)

            if any(count < 0 for count in counts):
                print("\nQuestion counts cannot be negative. Try again.\n")
                continue

            if total_questions < 1 or total_questions > 10:
                print(
                    "\nThe total number of questions must be between "
                    "1 and 10. Try again.\n"
                )
                continue

            break

        except ValueError:
            print("\nPlease enter whole numbers only. Try again.\n")

    question_type_targets = {
        "behavioral": behavioral_count,
        "technical": technical_count,
        "resume": resume_count,
        "project": project_count
    }

    plan = create_custom_interview_plan(
        custom_focus_topics=custom_focus_topics,
        question_type_targets=question_type_targets
    )


else:
    print("\nInvalid choice. Starting General Practice.")

    mode = "general"
    plan = create_practice_interview_plan(mode)


# ---------------------------------------------------------
# Start the interview.
# ---------------------------------------------------------

bot = Chatbot(
    client=client,
    mode=mode,
    context=context
)

session = InterviewSession(
    chatbot=bot,
    plan=plan,
    context=context,
    rag_service=rag_service
)

session.run_session()
session.save_results()

print("Interview finished. Results saved.")