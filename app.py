import json
import streamlit as st
from tools import grade_answer,generate_question,parse_job_description

st.set_page_config(page_title="Interview Prep Agent")
st.title("Interview-Preparation-Agent")

st.subheader("1.Paste the Job description")
jd_text=st.text_area("Job decsription",height=200)

if st.button("Generate question") and jd_text.strip():
    with st.spinner("Parsing Job Description"):
        parsed=json.loads(parse_job_description.invoke({'jd_text':jd_text}))
        st.session_state['parsed']=parsed

    with st.spinner("Generating questions...."):
        question_raw=generate_question.invoke({
            'role':parsed['role'],
            'skills':",".join(parsed['skills']),
            'seniority':parsed['seniority'],
            'num_questions':5
        })
        st.session_state['question']=json.loads(question_raw)
        st.session_state['grades']={}

if "parsed" in st.session_state:
    p=st.session_state['parsed']
    st.info(f"Role:{p['role']} | Seniority {p['seniority']} | Skills:{','.join(p['skills'])}")

if "question" in st.session_state:

    st.header("2.Answer The questions")
    for q in st.session_state['question']:
        qid=q['id']
        st.subheader(f"Q{qid} and {q['question']}")
        answer=st.text_area(f"Your answer to {qid}",key=f"answer_{qid}",height=120)

        if st.button(f"Grade q{qid}",key=f"grade_btn_{qid}"):
            grade_raw=grade_answer.invoke({
                'question':q['question'],
                "answer":answer,
                'skill_tested':q['skill'],
            })
            st.session_state['grades'][qid]=json.loads(grade_raw)

        if qid in st.session_state['grades']:
            grade=st.session_state['grades'][qid]
            st.metric("Score",f"{grade['score']}/10")
            st.write(grade['overall_feedback'])

            highlighted=answer
            for span in grade.get("weak_spans",[]):
                if span['text'] in highlighted:
                    highlighted=highlighted.replace(span['text'],f'<span style="background-color:#f7c1c1;">{span['text']}</span>')

            for span in grade.get("strong_span",[]):
                if span['text'] in highlighted:
                    highlighted=highlighted.replace(span['text'],f'<span style="background-color:#c0dd97;">{span['text']} </spab>')

            st.markdown(f"**Highlighted answer:**<br>{highlighted}",unsafe_allow_html=True)















