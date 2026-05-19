from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

from google import genai

client2 = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


import base64

def encode_image(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")

def analyze_slide(slide_text,image_path):

    base64_image = encode_image(image_path)


    prompt = f"""
    Analyze this pitch deck slide.

    You are provided:

    1. OCR extracted text
    2. The actual slide image

    Use BOTH sources.

    Pay attention to:
    - charts
    - screenshots
    - diagrams
    - branding
    - design quality
    - visual hierarchy
    - metrics shown visually

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
    
import PIL.Image

def analyse_slide2(slide_text,image_path):

    base64_image = PIL.Image.open(image_path)


    prompt = f"""
    Analyze this pitch deck slide.

    You are provided:

    1. OCR extracted text
    2. The actual slide image

    Use BOTH sources.

    Pay attention to:
    - charts
    - screenshots
    - diagrams
    - branding
    - design quality
    - visual hierarchy
    - metrics shown visually

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


    response = client2.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[prompt, base64_image]
    )


    response_text = response.text

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
    