from tools import generate_question,grade_answer,parse_job_description
from langchain_groq import ChatGroq
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
load_dotenv()

router_llm=ChatGroq(model='openai/gpt-oss-120b',api_key=("GROQ_API_KEY"))

tools=[generate_question,parse_job_description,grade_answer]

agent=create_agent(
    model=router_llm,
    tools=tools,
    system_prompt=("You are an interview preparation assistant. " \
    "When given a job description, first parse it ,then generate." \
    "questions.When given a question and an answer, grade it." \
    "Always call the appropriate tool rather than answering directly."\
    "Also one thing don't HALLUCINATE."
    ),
)



























