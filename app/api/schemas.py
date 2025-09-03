# This file defines Pydantic schemas for request and response validation.
# Schemas ensure that all data received and sent by the API matches the expected structure and types.

from pydantic import BaseModel, Field
from typing import List, Optional

# Request model for searching transport options (flights/trains)
class TransportRequest(BaseModel):
    origin: str = Field(..., description="Departure city")
    destination: str = Field(..., description="Arrival city")
    date_from: str = Field(..., description="Outbound travel date in YYYY-MM-DD format")
    date_to: str = Field(None, description="Return travel date in YYYY-MM-DD format (optional)")

# Response model for a single transport option
class TransportOption(BaseModel):
    from_city: str = Field(..., description="Departure city")
    to_city: str = Field(..., description="Arrival city")
    price: float = Field(..., description="Price in EUR")
    duration: str = Field(..., description="Travel duration, e.g., 2.5h")
    type: str = Field(..., description="Transport type: 'flight' or 'train'")

# Request model for searching accommodation
class AccommodationRequest(BaseModel):
    city: str = Field(..., description="City to stay in")
    budget: str = Field(..., description="Budget category: low, medium, high")
    zone_preference: Optional[str] = Field(None, description="Preferred neighborhood/area")

# Response model for a single accommodation option
class AccommodationOption(BaseModel):
    name: str = Field(..., description="Hotel or apartment name")
    price_per_night: float = Field(..., description="Price per night in EUR")
    location: str = Field(..., description="Neighborhood or address")

# Request model for searching activities
class ActivitiesRequest(BaseModel):
    city: str = Field(..., description="City where activities are planned")
    interests: List[str] = Field(..., description="List of interests, e.g., ['history', 'architecture']")

# Response model for a single activity option
class ActivityOption(BaseModel):
    name: str = Field(..., description="Name of the monument, museum, or activity")
    description: str = Field(..., description="Brief description")
    location: str = Field(..., description="Neighborhood or address")

# Request model for searching food options
class FoodRequest(BaseModel):
    city: str = Field(..., description="City to explore food in")
    cuisine_type: str = Field(..., description="Type of cuisine, e.g., 'tapas', 'paella'")

# Response model for a single food recommendation
class FoodOption(BaseModel):
    restaurant: str = Field(..., description="Restaurant or bar name")
    dish: str = Field(..., description="Recommended dish")
    neighborhood: str = Field(..., description="Neighborhood or street")

# Request model for searching shows/events
class ShowsRequest(BaseModel):
    city: str = Field(..., description="City where the show takes place")
    show_type: str = Field(..., description="Type of show, e.g., 'flamenco', 'concert'")

# Response model for a single show/event option
class ShowOption(BaseModel):
    name: str = Field(..., description="Event or show name")
    price: float = Field(..., description="Price per ticket in EUR")
    location: str = Field(..., description="Venue or address")
    time: Optional[str] = Field(None, description="Show time, e.g., '20:00'")
