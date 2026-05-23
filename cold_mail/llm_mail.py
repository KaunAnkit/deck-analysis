from groq import Groq
import os
import json

from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_BACKUP_TH")
)

def extract_startup_details(final_analysis):

    prompt = f"""
You are an expert startup analyst.

You are given the final analysis of a startup pitch deck.

Your task is to extract information about the startup itself.

IMPORTANT:

- Do NOT evaluate the deck.
- Do NOT give improvement suggestions.
- Do NOT mention weaknesses unless they describe the business.
- Do NOT invent information.
- If information is missing return null.
- Return ONLY valid JSON.
- No markdown.
- No explanations.

If funding amount is mentioned in the analysis,
extract it into funding_ask.

If market size is mentioned,
extract it into market_size.

If the startup name is not explicitly known,
return null.

IMPORTANT:
Return ONLY valid JSON

{{
    "company_name": null,
    "industry": null,
    "problem": null,
    "solution": null,
    "value_proposition": null,
    "target_customers": [],
    "market_size": null,
    "business_model": null,
    "traction_summary": null,
    "competitive_advantages": [],
    "team_summary": null,
    "funding_ask": null,
    "growth_focus": null,
    "growth_strategy": null,
    "startup_pitch": null,
    "why_now": null,
    "investment_thesis": null
}}

FINAL ANALYSIS:

{json.dumps(final_analysis, indent=2)}

Return JSON only.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
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


def generate_email(startup_profile,profile):

    prompt = f"""
    You are an elite startup fundraising advisor.
    Your task is to write a highly personalized investor outreach email.

    STARTUP:
    Company:{startup_profile.get("company_name")}
    Industry:{startup_profile.get("industry")}
    Problem:{startup_profile.get("problem")}
    Solution:{startup_profile.get("solution")}
    Value Proposition:{startup_profile.get("value_proposition")}
    Target Customers:{startup_profile.get("target_customers")}
    Market Size:{startup_profile.get("market_size")}
    Business Model:{startup_profile.get("business_model")}
    Traction:{startup_profile.get("traction_summary")}
    Competitive Advantages:{startup_profile.get("competitive_advantages")}
    Team:{startup_profile.get("team_summary")}
    Funding Ask:{startup_profile.get("funding_ask")}
    Growth Focus:{startup_profile.get("growth_focus")}
    Investment Thesis:{startup_profile.get("investment_thesis")}

    INVESTOR

    Name:{profile.get("name")}
    About:{profile.get("about")}
    Company:{profile.get("current_company_name")}
    Education:{profile.get("educations_details")}

    IMPORTANT RULES

    Use ONLY facts explicitly present in STARTUP and INVESTOR data.
    Never infer investor interests, investments, research, publications, customers, funding history, or expertise unless explicitly stated.
    Never mention a post, article, paper, project, company achievement, or investment unless it appears in the provided profile data.
    If insufficient information exists for personalization, use a generic but professional opening.
    Accuracy is more important than personalization.

    EMAIL REQUIREMENTS

    1. Mention something relevant about the investor.
    2. Explain why this startup may align with their interests.
    3. Mention the startup's mission naturally.
    4. Mention traction if available.
    5. Mention the fundraising round if available.
    6. Keep it concise.
    7. Keep under 150 words.
    8. Sound like a founder, not a marketing agency.
    9. No buzzword stuffing.
    10. End with a meeting request.

    Return only the email text.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,

    )

    return response.choices[0].message.content