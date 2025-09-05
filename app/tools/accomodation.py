import os
import httpx
import json
from typing import List
from app.api import schemas  # Import your schemas

BOOKING_API_HOST = os.getenv("BOOKING_API_HOST")
BOOKING_API_KEY = os.getenv("BOOKING_API_KEY")

async def search_destination(query: str) -> List[schemas.AccommodationOption]:
    """
    Calls the Booking.com searchDestination API to get destination info for a query.
    Returns a list of AccommodationOption objects.
    """
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    headers = {
        "x-rapidapi-host": BOOKING_API_HOST,
        "x-rapidapi-key": BOOKING_API_KEY,
    }
    params = {"query": query}
    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Save API response to a file
        with open("booking_api_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        destinations = data.get("data", [])
        hotels = []
        for dest in destinations:
            if "name" in dest:
                hotels.append(schemas.AccommodationOption(
                    name=dest.get("name"),
                    price_per_night=0.0,  # No price info in this endpoint, so use 0.0
                    location=dest.get("label", dest.get("region", "")),
                ))
        return hotels
    except Exception as e:
        print("Booking API searchDestination error:", e)
        return []