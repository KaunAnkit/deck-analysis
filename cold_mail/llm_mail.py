from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_email(profile):

    prompt = f"""
    Write a personalized cold email.

    Name:
    {profile.get("name")}

    About:
    {profile.get("about")}

    Company:
    {profile.get("current_company_name")}

    Education:
    {profile.get("educations_details")}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content