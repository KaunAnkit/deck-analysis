from groq import Groq
from dotenv import load_dotenv
import os
import json
import base64

load_dotenv()

client = Groq(
    api_key=os.getenv("GROK_GROK")
)


def encode_image(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def describe_slide(image_path, ocr_text=""):

    base64_image = encode_image(image_path)

    prompt = f"""
You are a pitch deck visual analysis agent.

Your ONLY job is to describe what exists on the slide.

Do NOT evaluate.
Do NOT critique.
Do NOT give investment advice.

Extract factual information only.

Return ONLY valid JSON.

{{
    "slide_type": "",
    "summary": "",
    "visual_elements": [],
    "charts_present": false,
    "screenshots_present": false,
    "logos_present": false,
    "metrics": [],
    "claims": [],
    "key_text": []
}}

OCR Text:

{ocr_text}
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

        print("VISUALIZER JSON ERROR")
        print(response_text)

        return {
            "error": str(e),
            "raw_response": response_text
        }


if __name__ == "__main__":

    result = describe_slide(
        "slides/page_1.png"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )