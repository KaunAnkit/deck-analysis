from .scrape import get_linkedin_profile
from .llm_mail import generate_email


def generate_cold_email(
    linkedin_url,
    startup_profile
):

    profile = get_linkedin_profile(
        linkedin_url
    )

    if isinstance(profile, list):
        profile = profile[0]

    email = generate_email(
        startup_profile,
        profile
    )

    return email