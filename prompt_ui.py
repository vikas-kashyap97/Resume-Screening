import streamlit as st
import fitz as ft
from io import BytesIO
from docx import Document
from docx.shared import Pt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import os

# Load API keys
load_dotenv()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest')

st.set_page_config(page_title="🚀 AI Resume Screener", layout="wide")
st.header('📝 AI-Powered Resume Screening & Salary Insights')

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'salary_range' not in st.session_state:
    st.session_state.salary_range = ""

# Upload Resume
uploaded_resume = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_resume is not None:
    resume_text = ""
    doc = ft.open(stream=uploaded_resume.read(), filetype="pdf")
    for page in doc:
        resume_text += page.get_text()
    st.session_state.resume_text = resume_text  # Save to session
    st.success("✅ Resume parsed successfully!")

# Job Role & Location Input
job_role = st.text_input("🎯 Enter Job Role (e.g., Node.js Developer):")
job_location = st.text_input("🌍 Enter Job Location (e.g., New York):")

# Fetch Job Data function
def fetch_job_data(job_title, location):
    url = "https://jsearch.p.rapidapi.com/estimated-salary"
    querystring = {
        "job_title": job_title,
        "location": location,
        "location_type": "ANY",
        "years_of_experience": "ALL"
    }
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "⏰ Request timed out. Try again later."}
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Failed to fetch job data: {e}"}

# Job Description & Salary (Show 5 guaranteed results)
if st.button("🔎 Fetch Job Insights"):
    if job_role.strip() == "" or job_location.strip() == "":
        st.warning("⚠️ Please enter both job role and location.")
    else:
        job_data = fetch_job_data(job_role, job_location)

        if "error" in job_data:
            st.error(job_data["error"])
        else:
            data_list = job_data.get('data', [])
            unique_results = []

            if data_list:
                st.session_state.job_description = ""

                # Iterate through job data and collect unique results
                for salary_data in data_list:
                    # Extract key details from the job data
                    publisher = salary_data.get('publisher_name', 'Unknown')
                    publisher_link = salary_data.get('publisher_link', '#')
                    role_title = salary_data.get('job_title', job_role)
                    loc = salary_data.get('location', job_location)

                    min_salary = salary_data.get('min_salary')
                    max_salary = salary_data.get('max_salary')
                    median_salary = salary_data.get('median_salary')

                    # Only consider results with valid salary range
                    if median_salary:
                        salary_range = f"${min_salary:,.2f} - ${max_salary:,.2f} (Median: ${median_salary:,.2f})"
                        job_info = {
                            "source": publisher,
                            "link": publisher_link,
                            "role": role_title,
                            "location": loc,
                            "salary_range": salary_range
                        }

                        # Add this job info to unique_results if it's not already added
                        if job_info not in unique_results:
                            unique_results.append(job_info)

                    # Stop if we have already 5 unique results
                    if len(unique_results) >= 5:
                        break

                # Display the results (up to 5 unique entries)
                if unique_results:
                    for job in unique_results:
                        st.markdown(f"### 🔗 [Source: {job['source']}]({job['link']})")
                        st.markdown(f"**Role:** {job['role']}")
                        st.markdown(f"**Location:** {job['location']}")
                        st.markdown(f"**Estimated Salary:** {job['salary_range']}")
                        st.markdown(f"Skills required include Node.js, JavaScript, REST APIs, and cloud services.")
                        st.markdown("---")

                    # Set job description for AI analysis (using the first result)
                    st.session_state.job_description = f"Role: {unique_results[0]['role']}\nLocation: {unique_results[0]['location']}\nEstimated Salary: {unique_results[0]['salary_range']}\n\nSkills required include Node.js, JavaScript, REST APIs, and cloud services."
                    st.text_area("📄 Job Description (used for AI analysis)", value=st.session_state.job_description, height=300)
                else:
                    st.warning("⚠️ No valid salary data found.")
            else:
                st.warning("⚠️ No job data found for this role & location. Try changing search terms.")


# Skills Gap & ATS Analysis
if st.button("⚡ Run Skills Gap & ATS Analysis"):
    if st.session_state.resume_text.strip() == "" or st.session_state.job_description.strip() == "":
        st.warning("⚠️ Please upload a resume and fetch job insights first.")
    else:
        with st.spinner("Analyzing..."):

            # Skills Gap Analysis
            skills_prompt = f"""
You are an expert career coach and HR recruiter. Compare the following **Resume** and **Job Description**. 
Identify:
- Skills MATCHED
- Skills MISSING (important ones not in resume)
- Suggestions to improve resume to better fit this job

Resume:
\"\"\"{st.session_state.resume_text}\"\"\"

Job Description:
\"\"\"{st.session_state.job_description}\"\"\"

Provide your analysis in bullet points.
"""
            skills_result = model.invoke(skills_prompt)
            skills_analysis = skills_result.content

            st.subheader("🛠️ Skills Gap Analysis")
            st.write(skills_analysis)

            # ATS Compatibility Check
            ats_prompt = f"""
Simulate an Applicant Tracking System (ATS) parsing the following **Resume** against this **Job Description**.
- Give an ATS Score (out of 100)
- Provide reasons for the score
- Highlight issues like formatting errors, missing keywords, improper sections, etc.

Resume:
\"\"\"{st.session_state.resume_text}\"\"\"

Job Description:
\"\"\"{st.session_state.job_description}\"\"\"

Output should be in report format.
"""
            ats_result = model.invoke(ats_prompt)
            ats_report = ats_result.content

            st.subheader("📊 ATS Compatibility Report")
            st.write(ats_report)

            # Export Functions
            def generate_docx(text):
                buffer = BytesIO()
                doc = Document()
                doc.add_heading("AI Resume Screening Report", level=0)
                style = doc.styles['Normal']
                font = style.font
                font.name = 'Arial'
                font.size = Pt(11)
                for para in text.split("\n"):
                    doc.add_paragraph(para.strip())
                doc.save(buffer)
                buffer.seek(0)
                return buffer

            def generate_pdf(text):
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = [Paragraph("AI Resume Screening Report", styles['Title']), Spacer(1, 12)]
                for para in text.split("\n"):
                    if para.strip():
                        story.append(Paragraph(para.strip(), styles['BodyText']))
                        story.append(Spacer(1, 8))
                doc.build(story)
                buffer.seek(0)
                return buffer

            final_report = f"## Estimated Salary\n\n💰 {st.session_state.salary_range}\n\n" + "## Skills Gap Analysis\n\n" + skills_analysis + "\n\n## ATS Compatibility Report\n\n" + ats_report

            st.markdown("### 📥 Export Report")
            col1, col2 = st.columns(2)

            with col1:
                docx_file = generate_docx(final_report)
                st.download_button(
                    label="💾 Download DOCX",
                    data=docx_file,
                    file_name="resume_screening_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            with col2:
                pdf_file = generate_pdf(final_report)
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_file,
                    file_name="resume_screening_report.pdf",
                    mime="application/pdf"
                )
