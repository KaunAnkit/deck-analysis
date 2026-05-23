from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_BACKUP")
)

def analyze_slide_d(slide_text, visual_details,deck_content):

    prompt = f"""
    You are an expert startup investor, sales strategist, and presentation consultant.

    Be brutally honest - most slides score 3-6/10. Penalize vague claims, missing data, and 
    investor-unfriendly design. Do NOT give benefit of the doubt for missing information.

    Analyze this slide using BOTH:

    1. OCR extracted text
    2. Visual analysis of the slide

    Deck Context:

    - Goal: {deck_content["deck_goal"]}
    - Deck Type: {deck_content["deck_type"]}
    - Fund Size: {deck_content["fund_size"]}
    - Growth Focus: {deck_content["growth_focus"]}
    - Usage Timeline: {deck_content["deck_timeline"]}
    
    IMPORTANT:
    Return ONLY valid JSON 

    JSON FORMAT:
    {{
        "slide_type": "",
        "summary": "",
        "strengths": [],
        "weaknesses": [],
        "missing_information": [],
        "investor_concerns": [],
        "goal_alignment": "",
        "overall_score": 0
    }}

    Visual Details:

    {json.dumps(visual_details, indent=2)}

    OCR Text:

    {slide_text}

    Return ONLY valid JSON.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
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

        print("JSON PARSE ERROR")
        print(response_text)

        return {
            "error": str(e),
            "raw_response": response_text
        }