from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_AGENT_TWO")
)

def analyze_slide_c(slide_text, visual_details):

    prompt = f"""
    Analyze this pitch deck slide.

    You are provided:

    1. OCR extracted text
    2. Visual analysis of the slide

    Use BOTH sources.

    Visual Details:

    {json.dumps(visual_details, indent=2)}

    Return ONLY valid JSON.

    {{
        "slide_type": "",
        "summary": "",
        "strengths": [],
        "weaknesses": [],
        "investor_concerns": []
    }}

    OCR Text:

    {slide_text}
    """

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
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