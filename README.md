# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that extracts important information from PDF resumes and provides intelligent insights using **Google Gemini AI**.

## 🚀 Features

* 📄 Upload PDF resumes
* 🤖 AI-powered resume analysis
* 👤 Extract personal information
* 🏢 Identify the candidate's industry
* 🛠️ Identify technical skills
* 🤝 Identify soft skills
* 💻 Identify tools and technologies
* 🎓 Extract education details
* 💼 Extract work experience
* 📜 Extract certifications
* 📊 Generate a Resume Score out of 100
* 💡 Provide resume improvement suggestions
* 🎯 Compare a resume with a Job Description
* 📈 Calculate Job Match percentage
* ✅ Identify matching skills
* ❌ Identify missing skills
* 📄 Generate a downloadable PDF report
* 🌍 Supports resumes from different industries

## 🧠 AI Technology

This project uses:

* **Python**
* **Streamlit**
* **Google Gemini AI**
* **Gemini API**
* **PyMuPDF**
* **FPDF2**

The application uses the **Google Gemini API** to perform AI-powered resume analysis.

## 🏭 Supported Industries

The analyzer is designed to work with resumes from different industries, including:

* Information Technology
* Software Engineering
* Marketing
* Finance
* Banking
* Healthcare
* Engineering
* Human Resources
* Education
* Hospitality
* Tourism
* Sales
* Administration
* Construction
* Legal
* Media
* Design
* And other professional industries

## 📂 Project Structure

```text
AI Resume Analyzer/
│
├── app.py
├── analyser.py
├── resume_parser.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `app.py`

Main Streamlit application and user interface.

### `analyser.py`

Uses the **Google Gemini API** to analyze resume content and return structured information.

### `resume_parser.py`

Extracts text from uploaded PDF resumes using **PyMuPDF**.

### `requirements.txt`

Contains the Python dependencies required to run the project.

### `.gitignore`

Contains files and folders that should not be uploaded to GitHub, such as environment variables and sensitive configuration files.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sevin-kenula/Ai-resume-analyzer.git
```

### 2. Open the project folder

```bash
cd Ai-resume-analyzer
```

### 3. Install the required Python packages

```bash
pip install -r requirements.txt
```

### 4. Set up the Gemini API Key

This project uses the **Google Gemini API** for AI-powered analysis.

Create a Gemini API key and store it securely as an environment variable.

For example, on Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual Gemini API key.

> ⚠️ Never upload your Gemini API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🖥️ How It Works

1. Upload a PDF resume.
2. The application extracts text from the PDF.
3. The extracted resume content is sent to the **Google Gemini AI model**.
4. Gemini analyzes the resume.
5. Resume information is displayed in structured sections.
6. A Resume Score is generated.
7. The user can paste a Job Description.
8. The AI compares the resume with the Job Description.
9. Matching and missing skills are identified.
10. A PDF analysis report can be downloaded.

## 📊 Resume Analysis

The application analyzes:

* Personal Information
* Industry
* Technical Skills
* Soft Skills
* Tools & Technologies
* Education
* Work Experience
* Certifications
* Resume Score
* Improvement Suggestions

## 🎯 Job Description Matching

Users can paste a job description to compare it with their resume.

The system provides:

* Job Match Percentage
* Matching Skills
* Missing Skills
* Recommendations

## 🔒 Privacy & Security

The application uses the **Google Gemini API** for AI-powered analysis.

Resume content is sent to the Gemini API for processing. Users should avoid uploading highly sensitive personal information and should keep their API key secure.

API keys should never be committed to GitHub or included directly in source code.

## 🛠️ Technologies Used

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| Python           | Core programming language    |
| Streamlit        | Web application interface    |
| Google Gemini AI | AI-powered resume analysis   |
| Gemini API       | Communication with Gemini AI |
| PyMuPDF          | PDF text extraction          |
| FPDF2            | PDF report generation        |

## 📌 Project Status

🚧 **Currently under development**

Future improvements may include:

* 🎨 Professional UI improvements
* 🧠 Improved AI analysis accuracy
* 📊 More advanced resume scoring
* 🎯 Improved Job Description matching
* 📄 Enhanced PDF report design
* 🌐 Cloud deployment
* 📈 Additional resume analytics

## 👨‍💻 Author

**Sevin Kenula**
AI with Computer Science Student