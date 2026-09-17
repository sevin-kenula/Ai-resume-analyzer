# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that extracts important information from PDF resumes and provides intelligent insights using local AI.

## 🚀 Features

- 📄 Upload PDF resumes
- 🤖 AI-powered resume analysis
- 👤 Extract personal information
- 🏢 Identify the candidate's industry
- 🛠️ Identify technical skills
- 🤝 Identify soft skills
- 💻 Identify tools and technologies
- 🎓 Extract education details
- 💼 Extract work experience
- 📜 Extract certifications
- 📊 Generate a Resume Score out of 100
- 💡 Provide resume improvement suggestions
- 🎯 Compare a resume with a Job Description
- 📈 Calculate Job Match percentage
- ✅ Identify matching skills
- ❌ Identify missing skills
- 📄 Generate a downloadable PDF report
- 🌍 Supports resumes from different industries

## 🧠 AI Technology

This project uses:

- **Python**
- **Streamlit**
- **Ollama**
- **Llama 3.2**
- **PyMuPDF**
- **FPDF2**

The AI model runs locally using Ollama.

## 🏭 Supported Industries

The analyzer is designed to work with resumes from different industries, including:

- Information Technology
- Software Engineering
- Marketing
- Finance
- Banking
- Healthcare
- Engineering
- Human Resources
- Education
- Hospitality
- Tourism
- Sales
- Administration
- Construction
- Legal
- Media
- Design
- And other professional industries

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

##app.py##
  Main Streamlit application and user interface.

analyser.py
  Uses Ollama and Llama 3.2 to analyze resume content and return structured information.

resume_parser.py
  Extracts text from uploaded PDF resumes using PyMuPDF.

requirements.txt
  Contains the Python dependencies required to run the project.

## ⚙️ Installation

1. Clone the repository
git clone https://github.com/sevin-kenula/Ai-resume-analyzer.git
2. Open the project folder
cd Ai-resume-analyzer
3. Install the required Python packages
pip install -r requirements.txt
4. Install Ollama

Install Ollama and make sure it is running on your computer.

Then download the Llama 3.2 model:

ollama pull llama3.2
5. Run the application
streamlit run app.py

The application will open in your browser.

🖥️ How It Works

Upload a PDF resume.
The application extracts text from the PDF.
The extracted resume content is sent to the local Llama 3.2 model.
The AI analyzes the resume.
Resume information is displayed in structured sections.
A Resume Score is generated.
The user can paste a Job Description.
The AI compares the resume with the Job Description.
Matching and missing skills are identified.
A PDF analysis report can be downloaded.

📊 Resume Analysis

The application analyzes:

Personal Information
Industry
Technical Skills
Soft Skills
Tools & Technologies
Education
Work Experience
Certifications
Resume Score
Improvement Suggestions
🎯 Job Description Matching

Users can paste a job description to compare it with their resume.

The system provides:

Job Match Percentage
Matching Skills
Missing Skills
Recommendations

🔒 Privacy

The project is designed to use a local AI model through Ollama.
Resume content is processed locally when using the local Ollama setup.

🛠️ Technologies Used
| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| Streamlit  | Web application interface |
| Ollama     | Local AI runtime          |
| Llama 3.2  | AI language model         |
| PyMuPDF    | PDF text extraction       |
| FPDF2      | PDF report generation     |

📌 Project Status

🚧 Currently under development

   Future improvements may include:

   🎨 Professional UI improvements
   🧠 Improved AI analysis accuracy
   📊 More advanced resume scoring
   🎯 Improved Job Description matching
   📄 Enhanced PDF report design
   🌐 Cloud deployment
   📈 Additional resume analytics


👨‍💻 Author
Sevin Kenula
AI with Computer Science Student