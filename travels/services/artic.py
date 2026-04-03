import requests

def validate_place(external_id: int):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    response = requests.get(url)

    return response.status_code == 200