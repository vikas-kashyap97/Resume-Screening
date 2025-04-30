# [Live link]()

# 📄 AI-Powered Resume Screening & Salary Estimator

Welcome to the **AI-Powered Resume Screening & Salary Estimator**, a Streamlit-based app that analyzes your resume against job descriptions, estimates salary ranges, and generates ATS (Applicant Tracking System) compatibility reports — all with a single click. Perfect for job seekers, career coaches, and HR professionals!

---

## 🚀 Features

- 📄 **Resume Screening**:
  - Matches your resume against job descriptions.
  - Analyzes skills gap and suggests improvements.
  - Detects keywords missing for ATS optimization.

- 💰 **Salary Estimation**:
  - Estimates salary ranges based on job role and location.
  - Powered by live salary data scraping.

- 📝 **Top 5 Job Matches (from different portals)**:
  - Shows relevant job postings with role, location, salary, and skills.
  - Aggregates data from sources like Glassdoor, Indeed, ZipRecruiter, and others.

- 📄 **Export Reports**:
  - Download **PDF** report including salary, skills gap, and ATS score.
  
---

## ⚙️ Tech Stack

- 🧠 `LangChain` (for prompt engineering)
- 🌐 `Streamlit` (for frontend UI)
- 🔎 `Serper API` or custom scraping (for live job & salary data)
- 📄 `python-docx`, `reportlab` (for exporting reports)
- 📝 `PyMuPDF` (for resume parsing)
- 🎯 `re`, `nltk` (for keyword and skills extraction)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install the required packages

```bash
pip install -r requirements.txt
```
### 4. Add your Google Generative AI API key

```bash
SERPER_API_KEY=your-serper-api-key
GOOGLE_API_KEY=your-google-api-key
```
### 5. Run the application

```bash
streamlit run prompt_ui.py
```

## How to Use:

- Upload your resume (PDF).

- Enter a job title and location.

- Paste the job description (optional but recommended).

- Click "Analyze & Estimate Salary".

- See:

      * Estimated Salary 💰

      * Skills Gap Analysis 📊

      * ATS Compatibility Report ✅

      * Top 5 Job Matches 🔎

      * Download PDF report instantly.

## Acknowledgements

- LangChain

- Streamlit

- Serper API

- Google Generative AI

- ReportLab

- PyMuPDF

## 📄 License

This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.



