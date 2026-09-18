import json
import os

import streamlit as st
from google import genai


def analyze_resume(text):

    # =====================================================
    # GET GEMINI API KEY
    # =====================================================

    api_key = None

    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "name": "Not found",
            "email": "Not found",
            "phone": "Not found",
            "industry": "Not found",
            "technical_skills": [],
            "soft_skills": [],
            "tools_and_technologies": [],
            "education": [],
            "work_experience": [],
            "certifications": [],
            "suggested_job_titles": [],
            "resume_score": 0,
            "suggestions": [
                "GEMINI_API_KEY is not configured."
            ]
        }

    try:

        # =================================================
        # CREATE GEMINI CLIENT
        # =================================================

        client = genai.Client(
            api_key=api_key
        )

        # =================================================
        # AI PROMPT
        # =================================================

        prompt = f"""
You are an expert resume analysis system.

Analyze the resume below and return ONLY a valid JSON object.

The candidate may belong to ANY professional industry.
Do not assume the candidate is an IT professional.

Possible industries include:
IT, Software Engineering, Marketing, Finance, Banking,
Healthcare, Engineering, Human Resources, Education,
Hospitality, Tourism, Sales, Administration, Construction,
Legal, Media, Design, Retail, Manufacturing, Logistics,
and any other industry.

Use exactly these fields:

{{
    "name": "",
    "email": "",
    "phone": "",
    "industry": "",
    "technical_skills": [],
    "soft_skills": [],
    "tools_and_technologies": [],
    "education": [],
    "work_experience": [],
    "certifications": [],
    "suggested_job_titles": [],
    "resume_score": 0,
    "suggestions": []
}}

IMPORTANT RULES:

1. Extract information ONLY from the resume.
2. Do NOT invent or guess information.
3. If a text field is missing, use "Not found".
4. If a list field is missing, return [].
5. resume_score must be a number between 0 and 100.
6. technical_skills must be a JSON array.
7. soft_skills must be a JSON array.
8. tools_and_technologies must be a JSON array.
9. education must be a JSON array.
10. work_experience must be a JSON array.
11. certifications must be a JSON array.
12. suggested_job_titles must be a JSON array.
13. suggestions must be a JSON array.
14. Identify the industry from the actual resume content.
15. Include relevant skills regardless of the candidate's industry.
16. Do not duplicate the same skill unnecessarily.
17. Do not classify every skill as a technical skill.
18. suggested_job_titles should contain 3 to 5 realistic job titles
    based only on the candidate's resume.
19. Suggestions should be practical and based on weaknesses
    found in the resume.
20. Return ONLY JSON.
21. Do NOT use Markdown.
22. Do NOT use ```json.
23. Do NOT add explanations before or after the JSON.

RESUME:
{text}
"""

        # =================================================
        # GEMINI AI REQUEST
        # =================================================

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        # =================================================
        # GET AI RESPONSE
        # =================================================

        if response is None:
            raise ValueError(
                "Gemini returned no response."
            )

        ai_result = response.text

        if not ai_result:
            raise ValueError(
                "Gemini returned an empty response."
            )

        ai_result = ai_result.strip()

        # =================================================
        # PARSE JSON
        # =================================================

        try:

            result = json.loads(
                ai_result
            )

        except json.JSONDecodeError:

            start = ai_result.find("{")
            end = ai_result.rfind("}")

            if start == -1 or end == -1:
                raise ValueError(
                    "Gemini did not return valid JSON."
                )

            result = json.loads(
                ai_result[start:end + 1]
            )

        # =================================================
        # STANDARDIZE RESULT
        # =================================================

        result = {
            "name": result.get(
                "name",
                "Not found"
            ),

            "email": result.get(
                "email",
                "Not found"
            ),

            "phone": result.get(
                "phone",
                "Not found"
            ),

            "industry": result.get(
                "industry",
                "Not found"
            ),

            "technical_skills": result.get(
                "technical_skills",
                []
            ),

            "soft_skills": result.get(
                "soft_skills",
                []
            ),

            "tools_and_technologies": result.get(
                "tools_and_technologies",
                []
            ),

            "education": result.get(
                "education",
                []
            ),

            "work_experience": result.get(
                "work_experience",
                []
            ),

            "certifications": result.get(
                "certifications",
                []
            ),

            "suggested_job_titles": result.get(
                "suggested_job_titles",
                []
            ),

            "resume_score": result.get(
                "resume_score",
                0
            ),

            "suggestions": result.get(
                "suggestions",
                []
            )
        }

        # =================================================
        # VALIDATE LIST FIELDS
        # =================================================

        list_fields = [
            "technical_skills",
            "soft_skills",
            "tools_and_technologies",
            "education",
            "work_experience",
            "certifications",
            "suggested_job_titles",
            "suggestions"
        ]

        for field in list_fields:

            if not isinstance(
                result[field],
                list
            ):

                if result[field]:

                    result[field] = [
                        str(result[field])
                    ]

                else:

                    result[field] = []

        # =================================================
        # VALIDATE TEXT FIELDS
        # =================================================

        text_fields = [
            "name",
            "email",
            "phone",
            "industry"
        ]

        for field in text_fields:

            if (
                result[field] is None
                or str(result[field]).strip() == ""
            ):

                result[field] = "Not found"

        # =================================================
        # VALIDATE SCORE
        # =================================================

        try:

            score = int(
                float(
                    result["resume_score"]
                )
            )

        except Exception:

            score = 0

        score = min(
            max(score, 0),
            100
        )

        result["resume_score"] = score

        # =================================================
        # RETURN RESULT
        # =================================================

        return result

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        return {
            "name": "Not found",
            "email": "Not found",
            "phone": "Not found",
            "industry": "Not found",
            "technical_skills": [],
            "soft_skills": [],
            "tools_and_technologies": [],
            "education": [],
            "work_experience": [],
            "certifications": [],
            "suggested_job_titles": [],
            "resume_score": 0,
            "suggestions": [
                "Resume analysis failed.",
                f"Error: {str(e)}"
            ]
        }