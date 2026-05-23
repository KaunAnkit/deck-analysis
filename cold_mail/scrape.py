import requests
import os

def get_linkedin_profile(url):
    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA')}",
        "Content-Type": "application/json"
    }

    payload = [{"url": url}]

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape",
        headers=headers,
        json=payload,
        params={
            "dataset_id": os.getenv("DATASET_ID")
        }
    )

    response.raise_for_status()

    return response.json()