import json
from langchain_community.tools import tool
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import os
load_dotenv()

groq_llm=ChatGroq(model='openai/gpt-oss-120b',api_key=os.getenv('GROQ_API_KEY'),temperature=0.3)
gemini_llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature=0.2)

@tool
def parse_job_description(jd_text:str)->str:
    """Extract role,seniority,skills from a job description.
    Returns a json string."""
    prompt=ChatPromptTemplate.from_template("""
Read the job description below and extract :
1."role":the job title
2."seniority":one of ["intern","junior","mid","senior"]
3."skills":a list of 5-8 core skills mentioned
Return only valid JSON,nothing more than that,no markdown,no explaination.

job description
{jd_text}
""")
    formatted=prompt.invoke({'jd_text':jd_text})
    response=groq_llm.invoke(formatted)
    return response.content

@tool
def generate_question(role:str,seniority:str,skills:str,num_questions:int=5)->str:
    """Generate interview questions tailored to a role, skills set ,and
    the seniority level.Returns a JSON String (list of objects)"""
    prompt=ChatPromptTemplate.from_template("""

Generate {num_questions} technical interview questions on the {seniority}-level 
{role} position.The question must specifically testing these skills {skills}.

Mix questions types: 2 conceptual, 2 applied/scenario-based, and 1-behavioural
but tied to a technical decision.
Also Include only the relevant question and the most asked questions.
AVOID HALLUCINATING.
The question should be the famous one that recruiter love to ask . 
Returns a valid JSON list like:
[{{"id":1,"question":"...","skill":"...","type":"conceptual"}}]
No markdown, no explaination
""")
    formatted=prompt.invoke({
        'role':role,
        'skills':skills,
        'seniority':seniority,
        'num_questions':num_questions,
    })
    response=groq_llm.invoke(formatted)
    return response.content

@tool
def grade_answer(question:str,answer:str,skill_tested:str)->str:
    """ Grade a candidate's answer. Returns a JSON String with a score,
    overall feedbacks, and weak/strong spans (exact substrings) with reasons --
    this is what powers the highlighted feedback in the UI."""
    prompt=ChatPromptTemplate.from_template("""
You are a strict technical interview grading an answer.

1.Question:{question}
2.Skill being tested:{skill_tested}
3.Candidate's Answer:{answer}

Grade this answer out of 10.Then identify specific weak spans -
exact short substrings copied verbatim from the candidate's answer
that are vague,incorrect ,or incomplete - and explain why each its weak and how and what to improve. 
Also identify one strong span if exists.

Returns ONLY valid JSON in this exact shape:
{{
  "score":7,
  "overall_feedback":"one paragraph summary",
  "weak_spans":[
      {{"text":"exact substring from the answer","reason":"why it's weak"}}
    ],
    "strong_spans":[
        {{"text":"exact substring from the answer","reason":"why it's strong"}}
    ]
}}
No markdown, no explaination outside the JSON.
""")
    formatted=prompt.invoke({'question':question,'answer':answer,'skill_tested':skill_tested})
    response=groq_llm.invoke(formatted)
    return response.content




    





