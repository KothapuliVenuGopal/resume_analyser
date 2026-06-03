import streamlit as st
import pdfplumber
from groq import Groq
from dotenv import load_dotenv
import os

# API Key load cheyadam
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.markdown("Analyze your resume against a job description and get improvement suggestions.")

# --- UI Setup ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: Upload Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type="pdf")

with col2:
    st.subheader("Step 2: Job Description")
    job_description = st.text_area("Paste the job description here:", height=200)

# --- Analysis Logic ---
if st.button("Analyze Resume"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing your resume..."):
            # PDF nundi text extract cheyadam
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = "".join([page.extract_text() for page in pdf.pages])
            
            # AI Prompt
            prompt = f"""
            As an expert ATS (Applicant Tracking System) and Career Coach, analyze the following resume against the job description.
            
            Job Description: {job_description}
            Resume Text: {resume_text}
            
            Please provide:
            1. Skill Match Score (0 to 100%)
            2. Missing Keywords/Skills
            3. Improvement Suggestions (Bullet points)
            4. Suggested Resume Bullet Points to add for this role
            """

            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant", # Latest model
                )
                
                st.divider()
                st.subheader("Analysis Results:")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload a resume and paste a job description first!")