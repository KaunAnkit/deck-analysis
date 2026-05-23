from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

clienty = Groq(
    api_key=os.getenv("GROQ_BACKUP_BACKUP")
)

def judge_deck(analysis_a,analysis_c,analysis_d,deck_content):

    prompt = f"""
    You are an expert startup investor, sales strategist, fundraising advisor, and presentation consultant.

    You are given analyses from multiple reviewers who evaluated the same deck.

    Your task is to evaluate the ENTIRE deck in the context of the user's stated goals.

    Deck Context:

    Goal: {deck_content["deck_goal"]}
    Deck Type: {deck_content["deck_type"]}
    Fund Size: {deck_content["fund_size"]}
    Growth Focus: {deck_content["growth_focus"]}
    Usage Timeline: {deck_content["deck_timeline"]}

    Important Evaluation Rules:

    Evaluate the deck relative to its stated purpose and audience.
    Consider content quality, presentation quality, consistency, narrative flow, and strategic effectiveness.
    Be critical but fair.
    
    Be brutally honest - most slides score 3-6/10. Penalize vague claims, missing data, and 
    investor-unfriendly design. Do NOT give benefit of the doubt for missing information.

    Return ONLY valid JSON.

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

        "reviewer_consensus": {{
            "agreement_level": "",
            "major_agreements": [],
            "major_disagreements": []
        }},

        "top_strengths": [],
        "top_weaknesses": [],

        "missing_sections": [],
        "red_flags": [],

        "goal_alignment": "",

        "investment_readiness": "",
        "confidence_level": "",

        "overall_recommendation": ""
    }}

    Scoring Guidelines:

    0-20 = Very Poor
    21-40 = Weak
    41-60 = Average
    61-80 = Strong
    81-100 = Exceptional

    investment_readiness must be one of:
    - Not Investment Ready
    - Early Stage
    - Seed Ready
    - Series A Ready

    confidence_level must be one of:
    - Low
    - Medium
    - High

    goal_alignment should explain how effectively the deck serves its intended purpose.

    Slide Analysis:

    Agent A Analysis:

    {json.dumps(analysis_a, indent=2)}

    Agent C Analysis:

    {json.dumps(analysis_c, indent=2)}

    Agent D Analysis:

    {json.dumps(analysis_d, indent=2)}
    """

    response = clienty.chat.completions.create(
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