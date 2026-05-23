from .scrape import get_linkedin_profile
from .llm_mail import generate_email


def generate_cold_email(linkedin_url):

    profile = get_linkedin_profile(linkedin_url)

    email = generate_email(profile)

    return email