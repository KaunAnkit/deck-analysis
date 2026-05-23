from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROK_GROK")
)


import base64

def encode_image(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")

def analyze_slide(slide_text,image_path,deck_content):

    base64_image = encode_image(image_path)


    prompt = f"""
    You are an expert startup investor, sales strategist, and presentation consultant.

    Be brutally honest - most slides score 3-6/10. Penalize vague claims, missing data, and 
    investor-unfriendly design. Do NOT give benefit of the doubt for missing information.

    Analyze this slide in the context of the entire deck and the user's stated goals.

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

    OCR Text:

    {slide_text}
    """

    

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
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
    
