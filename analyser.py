import json
import os
import time

import streamlit as st
from google import genai


# =========================================================
# GET GEMINI API KEY
# =========================================================

def get_api_key():

    # Streamlit Cloud Secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if api_key:
            return api_key

    except Exception:
        pass

    # Local environment variable
    return os.getenv("GEMINI_API_KEY")


# =========================================================
# EMPTY / ERROR RESULT
# =========================================================

def get_empty_result(message=None):

    suggestions = []

    if message:
        suggestions.append(message)

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

        "suggestions": suggestions
    }


# =========================================================
# ANALYZE RESUME
# =========================================================

def analyze_resume(text):

    # =====================================================
    # GET API KEY
    # =====================================================

    api_key = get_api_key()

    if not api_key:

        return get_empty_result(
            "GEMINI_API_KEY is not configured."
        )

    # =====================================================
    # CHECK RESUME TEXT
    # =====================================================

    if not text or not text.strip():

        return get_empty_result(
            "No text could be extracted from the resume PDF."
        )

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
You are an expert AI resume analysis system.

Analyze the resume below and return ONLY a valid JSON object.

The candidate may belong to ANY professional industry.

Do NOT assume the candidate is an IT professional.

Possible industries include:

IT, Software Engineering, Marketing, Finance, Banking,
Healthcare, Engineering, Human Resources, Education,
Hospitality, Tourism, Sales, Administration, Construction,
Legal, Media, Design, Retail, Manufacturing, Logistics,
Accounting, Customer Service, Aviation, Government,
and any other professional industry.

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
2. Do NOT invent information.
3. Do NOT guess missing information.
4. If a text field is missing, use "Not found".
5. If a list field is missing, return [].
6. resume_score must be a number between 0 and 100.
7. technical_skills must be a JSON array.
8. soft_skills must be a JSON array.
9. tools_and_technologies must be a JSON array.
10. education must be a JSON array.
11. work_experience must be a JSON array.
12. certifications must be a JSON array.
13. suggested_job_titles must be a JSON array.
14. suggestions must be a JSON array.
15. Identify the industry from the actual resume content.
16. Include relevant skills regardless of industry.
17. Do not use a fixed IT-only skills list.
18. Do not duplicate the same skill unnecessarily.
19. Do not classify every skill as a technical skill.
20. suggested_job_titles should contain 3 to 5 realistic job titles.
21. Job titles must be based ONLY on the candidate's resume.
22. Suggestions should be practical and based on weaknesses found in the resume.
23. Do not invent education, experience, certifications or skills.
24. Return ONLY JSON.
25. Do NOT use Markdown.
26. Do NOT use ```json.
27. Do NOT add explanations before or after the JSON.

RESUME:

{text}
"""

        # =================================================
        # GEMINI REQUEST
        # 3 ATTEMPTS
        # =================================================

        response = None
        last_error = None

        for attempt in range(3):

            try:

                print(
                    f"Gemini analysis attempt {attempt + 1}/3"
                )

                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=prompt,

                    config={
                        "response_mime_type": "application/json"
                    }
                )

                # -----------------------------------------
                # SUCCESS
                # -----------------------------------------

                if response is not None:
                    break

            except Exception as e:

                last_error = e

                error_text = str(e)

                print(
                    f"Gemini attempt {attempt + 1} failed: "
                    f"{error_text}"
                )

                # -----------------------------------------
                # RETRY TEMPORARY ERRORS
                # -----------------------------------------

                temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                )

                if temporary_error:

                    # Don't wait after final attempt
                    if attempt < 2:

                        time.sleep(3)

                        continue

                # -----------------------------------------
                # NON-RETRYABLE ERROR
                # -----------------------------------------

                raise

        # =================================================
        # IF ALL 3 ATTEMPTS FAILED
        # =================================================

        if response is None:

            if last_error:
                raise last_error

            raise ValueError(
                "Gemini returned no response after 3 attempts."
            )

        # =================================================
        # GET AI RESPONSE
        # =================================================

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

            # Try to find JSON object
            start = ai_result.find("{")
            end = ai_result.rfind("}")

            if start == -1 or end == -1:

                raise ValueError(
                    "Gemini did not return valid JSON."
                )

            result = json.loads(
                ai_result[
                    start:end + 1
                ]
            )

        # =================================================
        # ENSURE REQUIRED FIELDS
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
        # FIX LIST FIELDS
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
        # FIX TEXT FIELDS
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
                or str(
                    result[field]
                ).strip() == ""
            ):

                result[field] = "Not found"

        # =================================================
        # FIX RESUME SCORE
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
        # RETURN FINAL RESULT
        # =================================================

        return result

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        error_text = str(e)

        # -------------------------------------------------
        # 503 ERROR
        # -------------------------------------------------

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            message = (
                "Gemini is temporarily unavailable "
                "because the model is experiencing "
                "high demand. Three attempts were made. "
                "Please try again later."
            )

        # -------------------------------------------------
        # 429 ERROR
        # -------------------------------------------------

        elif (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):

            message = (
                "Gemini API request limit was reached. "
                "Please try again later."
            )

        # -------------------------------------------------
        # API KEY ERROR
        # -------------------------------------------------

        elif (
            "401" in error_text
            or "403" in error_text
            or "API key" in error_text
        ):

            message = (
                "Gemini API key is invalid or "
                "does not have access."
            )

        # -------------------------------------------------
        # OTHER ERROR
        # -------------------------------------------------

        else:

            message = (
                "Resume analysis failed."
            )

        # -------------------------------------------------
        # RETURN ERROR TO APP
        # -------------------------------------------------

        return get_empty_result(

            f"{message} "
            f"Error: {error_text}"
        )