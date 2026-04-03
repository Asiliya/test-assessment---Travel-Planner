import requests

def get_valid_places(page=1, limit=50):
    url = f"https://api.artic.edu/api/v1/artworks?page={page}&limit={limit}"
    response = requests.get(url)

    if response.status_code != 200:
        print("error")
        return []

    data = response.json().get("data", [])

    valid_places = []
    for item in data:
        if "id" in item:
            valid_places.append({
                "external_id": item["id"],
                "title": item.get("title", "No title")
            })

    return valid_places


if __name__ == "__main__":
    places = get_valid_places()
    for p in places:
        print(f"{p['external_id']} - {p['title']}")