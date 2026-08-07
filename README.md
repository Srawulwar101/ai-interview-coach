# AI Interview Coach

An AI-powered interview preparation platform that generates personalized software engineering interviews using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), semantic search, and automated answer evaluation.

The platform tailors interview questions using an uploaded resume and job description, conducts realistic interview sessions, provides detailed feedback, and stores interview results for later review.

---

## Features

- Personalized interview generation using uploaded resumes and job descriptions
- Retrieval-Augmented Generation (RAG) for context-aware questioning
- Semantic search powered by OpenAI embeddings and ChromaDB
- Practice, Mock, and fully Custom interview modes
- Behavioral, Technical, Resume, and Project interview categories
- Automated evaluation with detailed scoring and actionable feedback
- Session persistence with complete interview history saved as JSON
- Modular architecture designed for extensibility

---

## Interview Modes

### Practice

Practice a specific interview category while receiving immediate feedback after every answer.

Available practice areas:

- General
- Behavioral
- Technical
- Resume
- Project

Each response is evaluated across:

- Clarity
- Structure
- Specificity
- Relevance
- Confidence

The platform also generates:

- strengths
- improvement suggestions
- an improved sample answer

---

### Mock Interview

Simulates a realistic interview experience.

Unlike Practice mode, no feedback is shown until the interview is complete, creating a more authentic interview environment.

After completion, the platform generates an overall interview report including:

- overall score
- per-question scores
- category averages
- strengths
- areas for improvement

---

### Custom Interview

Create a personalized interview by selecting:

- custom technical topics
- behavioral topics
- project topics
- resume topics

Users can also choose exactly how many questions they want from each category.

Example:

```
Topics:
- API Design
- Databases
- Cloud Technologies

Question Distribution

Behavioral: 1
Technical: 2
Resume: 1
Project: 1
```

---

# Architecture

```
Resume + Job Description
            │
            ▼
      Document Loader
            │
            ▼
         Chunking
            │
            ▼
 OpenAI Embeddings API
            │
            ▼
       ChromaDB
(Vector Database)
            │
            ▼
 Semantic Retrieval (RAG)
            │
            ▼
      GPT Question Generation
            │
            ▼
 Interview Session
            │
            ▼
 User Responses
            │
            ▼
 AI Evaluation + Feedback
            │
            ▼
 JSON Session Results
```

---

## Tech Stack

### Languages

- Python

### AI

- OpenAI GPT
- OpenAI Embeddings
- Retrieval-Augmented Generation (RAG)

### Vector Database

- ChromaDB

### Document Processing

- PyPDF

### Supporting Libraries

- python-dotenv

---

## How It Works

### 1. Load Documents

The user may provide:

- a resume
- a job description

Sample documents are included for demonstration, or users can upload their own.

---

### 2. Index Documents

Each document is:

- loaded
- chunked
- embedded using OpenAI embeddings
- stored inside a temporary ChromaDB collection

Each interview creates its own vector collection to ensure retrieved context only comes from the current session.

---

### 3. Retrieve Context

Before generating each question, the application retrieves the most relevant resume and job description chunks using semantic search.

This allows interview questions to adapt to:

- previous work experience
- projects
- technologies
- job requirements

instead of relying on generic prompts.

---

### 4. Generate Interview Questions

Questions are generated using GPT while incorporating:

- retrieved resume context
- retrieved job description context
- interview mode
- requested interview category
- custom focus topics (if applicable)

---

### 5. Evaluate Responses

Each response is evaluated across five dimensions:

- Clarity
- Structure
- Specificity
- Relevance
- Confidence

The system also produces:

- strengths
- improvement suggestions
- an improved interview response

---

### 6. Save Interview Results

Every interview is automatically saved as JSON.

Saved information includes:

- interview type
- interview mode
- interview questions
- user responses
- AI evaluations
- overall statistics
- resume used
- job description used

Custom interviews additionally save:

- requested focus topics
- requested question distribution

---

## Project Structure

```
app/
    ai/
    documents/
    interview/
    retrieval/

examples/
    practice_session.json
    mock_session.json
    custom_session.json

job_descriptions/
    sample_job_description.txt

resumes/
    sample_resume.txt

main.py
requirements.txt
```

---

## Example Outputs

Example interview sessions are included in the `examples/` directory.

These demonstrate:

- Practice interview
- Mock interview
- Custom interview

Each example contains the complete interview transcript, AI evaluation, and performance summary.

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/Srawulwar101/ai-interview-coach.git
cd ai-interview-coach
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Run the application:

```bash
python main.py
```

---

## Future Improvements

Potential future enhancements include:

- Web-based user interface
- Voice interview mode
- Company-specific interview generation
- Expanded interview categories
- Additional evaluation metrics
- Dashboard for tracking interview progress over time

---

## What I Learned

This project was built to deepen my understanding of modern AI application development while reinforcing software engineering fundamentals through the design of a modular, end-to-end interview preparation platform.

Key concepts explored include:

- Retrieval-Augmented Generation (RAG)
- semantic search
- vector databases
- OpenAI embeddings
- prompt engineering
- modular software architecture
- structured LLM outputs
- automated evaluation pipelines

This project also reinforced software engineering principles such as separation of concerns, modular design, and building extensible systems.

---

## License

This project is intended for educational and portfolio purposes.