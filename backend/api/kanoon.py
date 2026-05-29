import requests
import os

API_KEY = os.getenv("KANOON_API_KEY")

def search_kanoon(query):

    url = "https://api.indiankanoon.org/search/"

    headers = {
        "Authorization": f"Token {API_KEY}"
    }

    data = {
        "formInput": query
    }

    response = requests.post(
        url,
        headers=headers,
        data=data
    )

    return response.json()