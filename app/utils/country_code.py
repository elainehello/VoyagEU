import pycountry
from geopy.geocoders import Nominatim

def get_country_code(city: str) -> str:
    """
    Uses geopy to geocode the city and extract the country code.
    Falls back to 'IN' if not found.
    """
    geolocator = Nominatim(user_agent="voyageu-app")
    try:
        location = geolocator.geocode(city, language="en", addressdetails=True)
        if location and "country" in location.raw["address"]:
            country_name = location.raw["address"]["country"]
            country = pycountry.countries.get(name=country_name)
            if country:
                return country.alpha_2
    except Exception as e:
        print(f"Geocoding error: {e}")
    return "IN"  # Default fallback
