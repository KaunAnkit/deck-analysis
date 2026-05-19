from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_JUDGE")
)


def judge_deck(slide_analysis):

    prompt = f"""
You are an experienced startup investor.

You are given slide-by-slide analysis of a startup pitch deck.

Evaluate the ENTIRE deck and return ONLY valid JSON.

Use scores from 0-100.

JSON FORMAT:

{{
    "overall_score": 0,

    "dimension_scores": {{
        "clarity": 0,
        "market_opportunity": 0,
        "traction": 0,
        "team": 0,
        "pitch_quality": 0,
        "competitive_positioning": 0
    }},

    "improvement_suggestions": {{
        "clarity": "",
        "market_opportunity": "",
        "traction": "",
        "team": "",
        "pitch_quality": "",
        "competitive_positioning": ""
    }},

    "top_strengths": [],
    "top_weaknesses": [],

    "missing_sections": [],
    "red_flags": [],

    "investment_readiness": "",
    "confidence_level": "",

    "overall_recommendation": ""
}}

Guidelines:

- Score each category from 0 to 100.
- Be critical but fair.
- Focus on investor readiness.
- Mention missing information if important sections are absent.
- Add red flags only if they are significant concerns.
- investment_readiness should be one of:
  - Not Investment Ready
  - Early Stage
  - Seed Ready
  - Series A Ready

- confidence_level should be:
  - Low
  - Medium
  - High

Slide Analysis:

{json.dumps(slide_analysis, indent=2)}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = response.choices[0].message.content

    
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")

    try:

        start = response_text.find("{")
        end = response_text.rfind("}") + 1

        json_text = response_text[start:end]

        return json.loads(json_text)

    except Exception as e:

        print(response_text)
        

        return {
            "error": str(e),
            "raw_response": response_text
        }