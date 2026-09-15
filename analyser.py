import json
import ollama


def analyze_resume(text):

    prompt = f"""
Analyze this resume carefully.

Return ONLY a valid JSON object.

The resume can belong to ANY industry such as:
IT, Software, Marketing, Finance, Banking, Healthcare, Engineering,
Human Resources, Education, Hospitality, Tourism, Sales, Administration,
Construction, Legal, Media, Design, or any other industry.

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
    "resume_score": 0,
    "suggestions": []
}}

Rules:

1. Extract information ONLY from the resume.
2. Do NOT invent information.
3. If information is missing, use "Not found" for text fields.
4. For list fields, return [] if information is missing.
5. resume_score must be a number from 0 to 100.
6. All list fields MUST be JSON arrays.
7. Return ONLY valid JSON.
8. Do NOT use markdown.
9. Do NOT use ```json.
10. Do NOT add explanations before or after the JSON.

Resume:

{text}
"""

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json"
        )

        ai_result = response["message"]["content"].strip()

        # Try direct JSON parsing first
        try:
            result = json.loads(ai_result)

        except json.JSONDecodeError:

            # Try extracting JSON object from response
            start = ai_result.find("{")
            end = ai_result.rfind("}")

            if start != -1 and end != -1:
                json_text = ai_result[start:end + 1]
                result = json.loads(json_text)
            else:
                raise ValueError("No JSON object found")

        # Make sure all required fields exist
        result = {
            "name": result.get("name", "Not found"),
            "email": result.get("email", "Not found"),
            "phone": result.get("phone", "Not found"),
            "industry": result.get("industry", "Not found"),
            "technical_skills": result.get("technical_skills", []),
            "soft_skills": result.get("soft_skills", []),
            "tools_and_technologies": result.get(
                "tools_and_technologies", []
            ),
            "education": result.get("education", []),
            "work_experience": result.get(
                "work_experience", []
            ),
            "certifications": result.get(
                "certifications", []
            ),
            "resume_score": result.get("resume_score", 0),
            "suggestions": result.get("suggestions", [])
        }

        # Make sure list fields are actually lists
        list_fields = [
            "technical_skills",
            "soft_skills",
            "tools_and_technologies",
            "education",
            "work_experience",
            "certifications",
            "suggestions"
        ]

        for field in list_fields:

            if not isinstance(result[field], list):

                if result[field]:
                    result[field] = [str(result[field])]
                else:
                    result[field] = []

        # Make sure score is a number
        try:
            result["resume_score"] = int(
                result["resume_score"]
            )
        except:
            result["resume_score"] = 0

        result["resume_score"] = min(
            max(result["resume_score"], 0),
            100
        )

        return result

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
            "resume_score": 0,
            "suggestions": [
                f"Resume analysis failed: {str(e)}"
            ]
        }