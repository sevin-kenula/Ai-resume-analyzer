import streamlit as st
import ollama
import json
from fpdf import FPDF

from resume_parser import extract_text_from_pdf
from analyser import analyze_resume


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# PDF REPORT
# =========================================================

def create_pdf_report(result):

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    # -----------------------------------------------------
    # SAFE TEXT
    # -----------------------------------------------------

    def safe_text(value):

        if value is None:
            return ""

        text = str(value)

        replacements = {
            "\u2013": "-",
            "\u2014": "-",
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2022": "-",
            "\u00a0": " ",
            "\u2026": "...",
            "\u2011": "-"
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # Remove unsupported characters
        text = text.encode(
            "latin-1",
            "replace"
        ).decode(
            "latin-1"
        )

        return text


    # -----------------------------------------------------
    # SAFE TEXT WRITER
    # -----------------------------------------------------

    def write_text(value):

        text = safe_text(value)

        if not text.strip():
            return

        # Reset X position
        pdf.set_x(pdf.l_margin)

        # Explicit width prevents FPDF horizontal-space error
        pdf.multi_cell(
            pdf.epw,
            7,
            text
        )


    # -----------------------------------------------------
    # SECTION HEADING
    # -----------------------------------------------------

    def section(title):

        pdf.ln(4)

        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(
            pdf.epw,
            9,
            safe_text(title)
        )

        pdf.set_font(
            "Arial",
            "",
            11
        )


    # -----------------------------------------------------
    # LIST WRITER
    # -----------------------------------------------------

    def write_list(items):

        if not isinstance(items, list):

            if items:
                items = [items]
            else:
                items = []


        if not items:

            write_text(
                "No information found."
            )

            return


        for item in items:

            if isinstance(item, dict):

                item = ", ".join(
                    f"{key}: {value}"
                    for key, value in item.items()
                )

            write_text(
                "- " + str(item)
            )


    # =====================================================
    # TITLE
    # =====================================================

    pdf.set_font(
        "Arial",
        "B",
        20
    )

    pdf.set_x(pdf.l_margin)

    pdf.multi_cell(
        pdf.epw,
        12,
        "AI Resume Analyzer Report",
        align="C"
    )

    pdf.ln(5)


    # =====================================================
    # PERSONAL INFORMATION
    # =====================================================

    section(
        "Personal Information"
    )

    write_text(
        "Name: " +
        str(
            result.get(
                "name",
                "Not found"
            )
        )
    )

    write_text(
        "Email: " +
        str(
            result.get(
                "email",
                "Not found"
            )
        )
    )

    write_text(
        "Phone: " +
        str(
            result.get(
                "phone",
                "Not found"
            )
        )
    )


    # =====================================================
    # INDUSTRY
    # =====================================================

    section(
        "Industry"
    )

    write_text(
        result.get(
            "industry",
            "Not found"
        )
    )


    # =====================================================
    # RESUME SCORE
    # =====================================================

    section(
        "Resume Score"
    )

    score = result.get(
        "resume_score",
        0
    )

    try:
        score = int(score)
    except:
        score = 0

    score = min(
        max(score, 0),
        100
    )

    write_text(
        f"{score}/100"
    )


    # =====================================================
    # TECHNICAL SKILLS
    # =====================================================

    section(
        "Technical Skills"
    )

    write_list(
        result.get(
            "technical_skills",
            []
        )
    )


    # =====================================================
    # SOFT SKILLS
    # =====================================================

    section(
        "Soft Skills"
    )

    write_list(
        result.get(
            "soft_skills",
            []
        )
    )


    # =====================================================
    # TOOLS & TECHNOLOGIES
    # =====================================================

    section(
        "Tools & Technologies"
    )

    write_list(
        result.get(
            "tools_and_technologies",
            []
        )
    )


    # =====================================================
    # EDUCATION
    # =====================================================

    section(
        "Education"
    )

    write_list(
        result.get(
            "education",
            []
        )
    )


    # =====================================================
    # WORK EXPERIENCE
    # =====================================================

    section(
        "Work Experience"
    )

    write_list(
        result.get(
            "work_experience",
            []
        )
    )


    # =====================================================
    # CERTIFICATIONS
    # =====================================================

    section(
        "Certifications"
    )

    write_list(
        result.get(
            "certifications",
            []
        )
    )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    section(
        "Suggestions for Improvement"
    )

    write_list(
        result.get(
            "suggestions",
            []
        )
    )


    # =====================================================
    # RETURN PDF
    # =====================================================

    return bytes(
        pdf.output()
    )


# =========================================================
# APP TITLE
# =========================================================

st.title(
    "📄 AI Resume Analyzer"
)

st.write(
    "Upload your resume and get an AI-powered analysis."
)


# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)


if uploaded_file is not None:


    # =====================================================
    # EXTRACT TEXT
    # =====================================================

    text = extract_text_from_pdf(
        uploaded_file
    )

    st.success(
        "Resume uploaded successfully!"
    )


    # =====================================================
    # AI ANALYSIS
    # =====================================================

    with st.spinner(
        "🤖 AI is analyzing your resume..."
    ):

        result = analyze_resume(
            text
        )


    # =====================================================
    # PERSONAL INFORMATION
    # =====================================================

    st.header(
        "👤 Personal Information"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.write(
            "**Name**"
        )

        st.write(
            result.get(
                "name",
                "Not found"
            )
        )


    with col2:

        st.write(
            "**Email**"
        )

        st.write(
            result.get(
                "email",
                "Not found"
            )
        )


    with col3:

        st.write(
            "**Phone**"
        )

        st.write(
            result.get(
                "phone",
                "Not found"
            )
        )


    # =====================================================
    # INDUSTRY
    # =====================================================

    st.header(
        "🏢 Industry"
    )

    st.info(
        result.get(
            "industry",
            "Not found"
        )
    )


    # =====================================================
    # RESUME SCORE
    # =====================================================

    st.header(
        "📊 Resume Score"
    )

    score = result.get(
        "resume_score",
        0
    )

    try:

        score = int(score)

    except:

        score = 0


    score = min(
        max(score, 0),
        100
    )


    col1, col2 = st.columns(
        [1, 2]
    )


    with col1:

        st.metric(
            "Overall Score",
            f"{score}/100"
        )


    with col2:

        if score >= 80:

            st.success(
                "🌟 Excellent Resume"
            )

        elif score >= 60:

            st.info(
                "👍 Good Resume"
            )

        else:

            st.warning(
                "⚠️ Needs Improvement"
            )


        st.progress(
            score
        )


    # =====================================================
    # TECHNICAL SKILLS
    # =====================================================

    st.header(
        "🛠️ Technical Skills"
    )

    technical_skills = result.get(
        "technical_skills",
        []
    )


    if not isinstance(
        technical_skills,
        list
    ):

        technical_skills = [
            technical_skills
        ]


    if technical_skills:

        cols = st.columns(3)

        for i, skill in enumerate(
            technical_skills
        ):

            with cols[i % 3]:

                st.info(
                    f"🛠️ {skill}"
                )

    else:

        st.write(
            "No technical skills found"
        )


    # =====================================================
    # SOFT SKILLS
    # =====================================================

    st.header(
        "🤝 Soft Skills"
    )

    soft_skills = result.get(
        "soft_skills",
        []
    )


    if not isinstance(
        soft_skills,
        list
    ):

        soft_skills = [
            soft_skills
        ]


    if soft_skills:

        cols = st.columns(3)

        for i, skill in enumerate(
            soft_skills
        ):

            with cols[i % 3]:

                st.info(
                    f"🤝 {skill}"
                )

    else:

        st.write(
            "No soft skills found"
        )


    # =====================================================
    # TOOLS & TECHNOLOGIES
    # =====================================================

    st.header(
        "💻 Tools & Technologies"
    )

    tools = result.get(
        "tools_and_technologies",
        []
    )


    if not isinstance(
        tools,
        list
    ):

        tools = [
            tools
        ]


    if tools:

        cols = st.columns(3)

        for i, tool in enumerate(
            tools
        ):

            with cols[i % 3]:

                st.info(
                    f"💻 {tool}"
                )

    else:

        st.write(
            "No tools found"
        )


    # =====================================================
    # EDUCATION
    # =====================================================

    st.header(
        "🎓 Education"
    )

    education = result.get(
        "education",
        []
    )


    if not isinstance(
        education,
        list
    ):

        education = [
            education
        ]


    if education:

        for item in education:

            st.write(
                "🎓",
                item
            )

    else:

        st.write(
            "No education information found"
        )


    # =====================================================
    # WORK EXPERIENCE
    # =====================================================

    st.header(
        "💼 Work Experience"
    )

    experience = result.get(
        "work_experience",
        []
    )


    if not isinstance(
        experience,
        list
    ):

        experience = [
            experience
        ]


    if experience:

        for item in experience:

            st.write(
                "💼",
                item
            )

    else:

        st.write(
            "No work experience found"
        )


    # =====================================================
    # CERTIFICATIONS
    # =====================================================

    st.header(
        "📜 Certifications"
    )

    certifications = result.get(
        "certifications",
        []
    )


    if not isinstance(
        certifications,
        list
    ):

        certifications = [
            certifications
        ]


    if certifications:

        for item in certifications:

            st.write(
                "📜",
                item
            )

    else:

        st.write(
            "No certifications found"
        )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.header(
        "💡 Suggestions for Improvement"
    )

    suggestions = result.get(
        "suggestions",
        []
    )


    if not isinstance(
        suggestions,
        list
    ):

        suggestions = [
            suggestions
        ]


    if suggestions:

        for suggestion in suggestions:

            st.write(
                "💡",
                suggestion
            )

    else:

        st.write(
            "No suggestions available"
        )


    # =====================================================
    # JOB DESCRIPTION MATCHER
    # =====================================================

    st.header(
        "💼 Job Description Matcher"
    )


    job_description = st.text_area(
        "Paste the Job Description here",
        height=200,
        placeholder=(
            "Paste the job description "
            "you want to compare with "
            "this resume..."
        )
    )


    if st.button(
        "🔍 Analyze Job Match"
    ):

        if job_description.strip():

            with st.spinner(
                "🤖 AI is comparing your "
                "resume with the job description..."
            ):

                match_prompt = f"""
Compare the following resume with the job description.

Return ONLY valid JSON using exactly these fields:

{{
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "recommendations": []
}}

Rules:
- match_percentage must be a number from 0 to 100.
- Identify skills and requirements that match.
- Identify important skills or requirements missing from the resume.
- Give practical recommendations to improve the resume for this job.
- Do not invent information.
- Return ONLY JSON.
- Do not use markdown.
- Do not use ```.

RESUME:
{text}

JOB DESCRIPTION:
{job_description}
"""


                try:

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": match_prompt
                            }
                        ],
                        format="json"
                    )


                    match_result = response[
                        "message"
                    ][
                        "content"
                    ]


                    match_data = json.loads(
                        match_result
                    )


                    # =================================
                    # MATCH PERCENTAGE
                    # =================================

                    match_percentage = match_data.get(
                        "match_percentage",
                        0
                    )


                    try:

                        match_percentage = int(
                            match_percentage
                        )

                    except:

                        match_percentage = 0


                    match_percentage = min(
                        max(
                            match_percentage,
                            0
                        ),
                        100
                    )


                    st.subheader(
                        "📊 Job Match Result"
                    )


                    st.metric(
                        "Job Match",
                        f"{match_percentage}%"
                    )


                    st.progress(
                        match_percentage
                    )


                    # =================================
                    # MATCHING SKILLS
                    # =================================

                    st.subheader(
                        "✅ Matching Skills"
                    )


                    matching_skills = match_data.get(
                        "matching_skills",
                        []
                    )


                    if not isinstance(
                        matching_skills,
                        list
                    ):

                        matching_skills = [
                            matching_skills
                        ]


                    if matching_skills:

                        cols = st.columns(3)

                        for i, skill in enumerate(
                            matching_skills
                        ):

                            with cols[i % 3]:

                                st.success(
                                    f"✅ {skill}"
                                )

                    else:

                        st.write(
                            "No matching skills found"
                        )


                    # =================================
                    # MISSING SKILLS
                    # =================================

                    st.subheader(
                        "❌ Missing Skills"
                    )


                    missing_skills = match_data.get(
                        "missing_skills",
                        []
                    )


                    if not isinstance(
                        missing_skills,
                        list
                    ):

                        missing_skills = [
                            missing_skills
                        ]


                    if missing_skills:

                        cols = st.columns(3)

                        for i, skill in enumerate(
                            missing_skills
                        ):

                            with cols[i % 3]:

                                st.warning(
                                    f"❌ {skill}"
                                )

                    else:

                        st.write(
                            "No missing skills found"
                        )


                    # =================================
                    # RECOMMENDATIONS
                    # =================================

                    st.subheader(
                        "💡 Recommendations"
                    )


                    recommendations = match_data.get(
                        "recommendations",
                        []
                    )


                    if not isinstance(
                        recommendations,
                        list
                    ):

                        recommendations = [
                            recommendations
                        ]


                    if recommendations:

                        for recommendation in recommendations:

                            st.write(
                                "💡",
                                recommendation
                            )

                    else:

                        st.write(
                            "No recommendations available"
                        )


                except Exception as e:

                    st.error(
                        f"Job matching failed: {str(e)}"
                    )

        else:

            st.warning(
                "Please paste a job description first."
            )


    # =====================================================
    # PDF DOWNLOAD
    # =====================================================

    st.header(
        "📥 Download Report"
    )


    try:

        pdf_data = create_pdf_report(
            result
        )


        st.download_button(
            label="📄 Download Professional PDF Report",
            data=pdf_data,
            file_name="AI_Resume_Analysis_Report.pdf",
            mime="application/pdf"
        )


    except Exception as e:

        st.error(
            f"PDF generation failed: {str(e)}"
        )

        st.code(
            str(e)
        )