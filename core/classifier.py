import os
import json
from groq import Groq
from dotenv import load_dotenv
from core.schema import TriageResult , Category , Priority , Team

load_dotenv()

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

System_Prompt = f"""You are TriageAI, an IT support ticket classifier.

Given a raw IT support ticket, classify it into a structured format.

You MUST respond with ONLY a valid JSON object, no other text, matching this exact schema:
{{
    "category": one of {[c.value for c in Category]}, 

    "priority": one of {[p.value for p in Priority]},
    "suggested_team": one of {[t.value for t in Team]},
    "confidence": a float between 0.0 and 1.0,
    "reasoning": a short 1-2 sentence explanation of your classification
}}

Guidelines:
- "Critical" priority is for outages, security incidents, or anything affecting many users/customers.
- "High" priority is for issues blocking a single user's core work (e.g. can't log in, VPN down).
- "Medium"/"Low" are for inconveniences or non-urgent requests (e.g. printer jam, new account setup).
- Security-related tickets (phishing, suspicious activity) should route to the Security team regardless of category.
"""

def classify_ticket(ticket_text: str) -> TriageResult:
    """
    Sends a ticket to the LLM and returns a validated TriageResult.
    Raises ValueError if the LLM output doesn't match the schema.
    """
    response = client.chat.completions.create(
        model = MODEL,
        messages = [
            {"role" : "system" , "content" : System_Prompt},
            {"role" : "user" , "content" : ticket_text},
        ],
        temperature = 0.2,
        response_format = {"type": "json_object"}, # Groq's JSON mode. This constrains the raw output to be valid JSON, but doesn't guarantee it matches your schema — that's why we still validate with Pydantic afterward.
    )

    raw_output = response.choices[0].message.content

    try:
        parsed = json.loads(raw_output)
        return TriageResult(**parsed)
    # Two separate except blocks — one for malformed JSON, one for valid JSON that doesn't match your schema (e.g. LLM invents a category that doesn't exist). This distinction is exactly the kind of "don't swallow errors with a bare except".
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"LLM returned invalid JSON: {raw_output}") from e
    except Exception as e:
        # Pydantic validation error - LLM returned JSON but wrong shape/values
        raise ValueError(f"LLM output failed schema validation: {raw_output}") from e