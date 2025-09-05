import os
import httpx
import json
from typing import List
from app.utils.country_code import get_country_code
from app.api import schemas  # Import your schemas


GOOGLE_API_HOST = os.getenv("GOOGLE_API_HOST")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_URL = os.getenv("GOOGLE_API_URL")

async def search_activities(city: str, interests: List[str]) -> List[schemas.ActivityOption]:
    """
    Calls the Google Places Autocomplete API to get place suggestions for the city and interests.
    Returns a list of ActivityOption objects.
    """
    input_text = f"{city} " + " ".join(interests)
    country_code = get_country_code(city)
    headers = {
        "x-rapidapi-host": GOOGLE_API_HOST,
        "x-rapidapi-key": GOOGLE_API_KEY,
    }
    params = {
        "input": input_text,
        "components": f"country:{country_code}"
    }
    try:
        response = httpx.get(GOOGLE_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        with open("google_place_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        predictions = data.get("predictions", [])
        results = []
        # For each prediction, fetch details using the place_id
        for pred in predictions:
            place_id = pred.get("place_id")
            if not place_id:
                continue
            # Call Place Details API
            details_url = "https://google-place-autocomplete-and-place-info.p.rapidapi.com/maps/api/place/details/json"
            details_params = {"place_id": place_id}
            details_resp = httpx.get(details_url, headers=headers, params=details_params, timeout=10)
            details_data = details_resp.json()
            result = details_data.get("result", {})
            results.append(schemas.ActivityOption(
                name=result.get("name", ""),
                description=result.get("adr_address", ""),
                location=result.get("vicinity", ""),
                place_id=result.get("place_id", ""),
                category=result.get("types", []),
                formatted_address=result.get("formatted_address", ""),
                lat=result.get("geometry", {}).get("location", {}).get("lat", 0.0),
                lng=result.get("geometry", {}).get("location", {}).get("lng", 0.0),
                photos=[photo.get("photo_reference", "") for photo in result.get("photos", [])],
                url=result.get("url", ""),
            ))
        return results
    except Exception as e:
        print("Google Places API error:", e)
        return []