import json
import ollama


def analyze_resume(text):

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
12. suggestions must be a JSON array.
13. Identify the industry from the actual resume content.
14. Include relevant skills regardless of the candidate's industry.
15. Do not classify every skill as a technical skill.
16. Do not duplicate the same skill unnecessarily.
17. Suggestions should be practical and based on weaknesses found in the resume.
18. 18. suggested_job_titles must be a JSON array containing 3 to 5 realistic job titles based only on the resume.
19. Do NOT use Markdown.
20. Do NOT use ```json.
21. Do NOT add explanations before or after the JSON.

RESUME:
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

        # Try normal JSON parsing first
        try:

            result = json.loads(ai_result)

        except json.JSONDecodeError:

            # Try extracting JSON object
            start = ai_result.find("{")
            end = ai_result.rfind("}")

            if start == -1 or end == -1:
                raise ValueError(
                    "AI did not return a valid JSON object."
                )

            json_text = ai_result[start:end + 1]

            result = json.loads(json_text)


        # -------------------------------------------------
        # Required fields
        # -------------------------------------------------

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


        # -------------------------------------------------
        # Make sure list fields are actually lists
        # -------------------------------------------------

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


        # -------------------------------------------------
        # Clean empty values
        # -------------------------------------------------

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


        # -------------------------------------------------
        # Normalize resume score
        # -------------------------------------------------

        try:

            score = int(
                float(
                    result["resume_score"]
                )
            )

        except:

            score = 0


        score = min(
            max(score, 0),
            100
        )


        result["resume_score"] = score


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