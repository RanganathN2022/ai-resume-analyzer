import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from parser.resume_parser import extract_text_from_pdf, extract_experience
from parser.jd_parser import parse_job_description
from nlp.skill_extractor import extract_skills
from models.embedding_model import get_embedding
from utils.similarity import compute_similarity
from scoring.ats_score import calculate_ats
from utils.feedback import generate_feedback
from utils.pdf_report import generate_pdf
from agents.resume_agent import run_resume_agent

# ------------------ CONFIG ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.markdown("""
# 🚀 AI Resume Analyzer  
### 🤖 Agentic Recruiter Dashboard
""")

# ------------------ INPUT ------------------
resume_files = st.file_uploader(
    "Upload Multiple Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

jd_text = st.text_area("Paste Job Description")

# ------------------ HELPERS ------------------
def get_color(score):
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"

def get_label(score):
    if score >= 80:
        return "🟢 Strong Fit"
    elif score >= 60:
        return "🟡 Moderate Fit"
    else:
        return "🔴 Low Fit"

# ------------------ MAIN ------------------
if resume_files and jd_text:

    with st.spinner("🤖 Agent is analyzing resumes..."):

        jd_data = parse_job_description(jd_text)
        jd_skills = jd_data["skills"]
        jd_exp = jd_data["experience"]

        emb_jd = get_embedding(jd_text)

        results = []

        # -------- PROCESS EACH RESUME --------
        for file in resume_files:

            resume_text = extract_text_from_pdf(file)

            # 🤖 Agent Processing (NO FAKE MODIFICATION)
            agent_output = run_resume_agent(
                resume_text,
                jd_text,
                jd_skills
            )

            resume_skills = agent_output["original_skills"]
            missing_skills = agent_output["missing_skills"]
            agent_history = agent_output["history"]
            suggestions = agent_output["suggestions"]
            bullets = agent_output["bullets"]

            resume_exp = extract_experience(resume_text)

            # Matching logic
            skill_match = len(set(resume_skills) & set(jd_skills)) / max(len(jd_skills), 1)
            exp_match = min(resume_exp / max(jd_exp, 1), 1)

            emb_resume = get_embedding(resume_text)
            similarity = compute_similarity(emb_resume, emb_jd)

            ats_score = calculate_ats(skill_match, exp_match, similarity, 0.8, 0.9)
            ats_score = round(ats_score, 2)

            feedback = generate_feedback(missing_skills, jd_exp - resume_exp)

            results.append({
                "name": file.name,
                "score": ats_score,
                "skills": resume_skills,
                "missing": missing_skills,
                "feedback": feedback,
                "history": agent_history,
                "suggestions": suggestions,
                "bullets": bullets
            })

    # -------- SORT --------
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.success(f"🏆 Top Candidates (Analyzed {len(results)})")

    # -------- SUMMARY --------
    top_score = results[0]["score"]
    st.info(f"""
📊 Summary:
- Total Candidates: {len(results)}
- Top Score: {top_score}
""")

    # -------- TABS --------
    tab1, tab2 = st.tabs(["📋 Results", "📊 Analytics"])

    # ================== RESULTS ==================
    with tab1:

        for i, r in enumerate(results):

            st.markdown(f"## #{i+1} - {r['name']}")
            st.markdown(f"### {get_label(r['score'])}")

            # SCORE CARD
            color = get_color(r["score"])
            st.markdown(f"""
            <div style="
                background-color:#f0f2f6;
                padding:20px;
                border-radius:10px;
                text-align:center;
            ">
                <h3>ATS Score</h3>
                <h1 style="color:{color};">{r['score']}</h1>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])

            # ✅ Skills
            with col1:
                st.markdown("#### ✅ Matched Skills")
                for skill in r["skills"]:
                    st.success(skill)

            # ❌ Missing
            with col2:
                st.markdown("#### ❌ Missing Skills")
                if r["missing"]:
                    for skill in r["missing"]:
                        st.error(skill)
                else:
                    st.success("No missing skills 🎉")

            # 💡 Feedback
            st.markdown("### 💡 Feedback")
            for f in r["feedback"]:
                st.info(f)

            # 🤖 Agent Suggestions
            st.markdown("### 🤖 Agent Suggestions")
            for s in r["suggestions"]:
                st.info(s)

            # ✨ Improved Bullets
            st.markdown("### ✨ Suggested Resume Improvements")
            for b in r["bullets"]:
                st.success(b)

            # 🤖 Reasoning
            with st.expander("🤖 Agent Reasoning"):
                for step in r["history"]:
                    st.write(step)

            st.progress(min(int(r["score"]), 100))

            # 📄 PDF
            pdf_file = generate_pdf(r)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label=f"📄 Download Report - {r['name']}",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf",
                    key=r["name"]
                )

            st.divider()

    # ================== ANALYTICS ==================
    with tab2:

        df = pd.DataFrame(results)

        st.markdown("## 📊 Candidate Comparison")
        st.caption("Sorted by ATS Score (Descending)")

        st.dataframe(df[["name", "score"]])

        fig, ax = plt.subplots()
        ax.bar(df["name"], df["score"])
        ax.set_ylabel("ATS Score")

        st.pyplot(fig)

# ------------------ SAFE MESSAGE ------------------
elif resume_files or jd_text:
    st.warning("⚠️ Please upload resumes AND paste job description")