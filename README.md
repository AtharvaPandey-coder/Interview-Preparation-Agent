# Interview Prep Agent

An agentic AI tool that turns any job description into a tailored mock interview - generating role-specific questions and grading your answers with explainable, highlighted feedback.

## Problem it solves

Most interview prep tools ask generic questions. This agent reads the actual job description you're targeting, extracts the role, seniority level, and required skills, then generates questions that test exactly those skills - and grades your answers against them with span-level feedback showing precisely which parts were weak or strong.

## Features

- JD parsing - extracts role, seniority, and core skills from any pasted job description
- Tailored question generation - produces a mix of conceptual, applied/scenario-based, and behavioral questions matched to the parsed role and seniority
- Explainable grading - scores each answer out of 10 and highlights exact weak and strong substrings with reasons, instead of just a generic score
- Simple Streamlit UI - paste a JD, answer questions, get graded feedback, all in one page

## Tech stack

- LangChain - tool definitions and prompt templating
- Groq (Llama 3.3 70B) - fast, cheap generation for JD parsing and question generation
- Google Gemini - grading and span-level feedback, where deeper reasoning matters
- Streamlit - UI and session state management

## Architecture

1. Job description (pasted by user)
   -> parse_job_description (Groq)
   -> returns {role, seniority, skills}

2. generate_questions (Groq)
   -> takes {role, seniority, skills}
   -> returns tailored list of questions

3. User answers each question in the UI

4. grade_answer (Gemini)
   -> takes {question, answer, skill_tested}
   -> returns {score, feedback, weak_spans, strong_spans}

5. Streamlit renders the score and highlighted answer

## Setup

1. Clone the repo and install dependencies:

pip install -r requirements.txt

2. Create a .env file in the project root:

GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_gemini_key_here

3. Run the app:

streamlit run app.py

## Project structure

Interview_Agent/
- app.py       (Streamlit UI)
- tools.py     (Agent tools: parse_job_description, generate_questions, grade_answer)
- agent.py     (LangChain agent wiring the tools together)
- requirements.txt
- .env

## Future improvements

- Add answer history / progress tracking across sessions
- Support resume upload alongside JD for gap-analysis questions
- Add difficulty scaling based on grading history
