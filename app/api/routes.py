# This file defines API endpoints using FastAPI's APIRouter.
# Each endpoint is decorated with @router.<method> to handle HTTP requests.

# API endpoint definitions

from fastapi import APIRouter
from typing import List
from app.api import schemas
from app.tools.transport import search_transport
from config.settings import DATA_PATH
import json
import os

router = APIRouter(prefix="/api/v1")

def load_mock(filename: str):
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
@router.post("/transport", response_model=List[schemas.TransportOption])
def get_transport(request: schemas.TransportRequest):
    return search_transport(request.origin, request.destination, request.date)

@router.post("/accomodation", response_model=List[schemas.AccommodationOption])
def get_accommodation(request: schemas.AccommodationRequest):
    hotels = load_mock("hotels.json")
    return hotels

@router.post("/activities", response_model=List[schemas.ActivityOption])
def get_activity(request: schemas.ActivitiesRequest):
    activities = load_mock("activities.json")
    return activities

@router.post("/food", response_model=List[schemas.FoodOption])
def get_food(request: schemas.FoodRequest):
    food_data = load_mock("food.json")
    return food_data

@router.post("/shows", response_model=List[schemas.ShowOption])
def get_show(request: schemas.ShowsRequest):
    shows = load_mock("shows.json")
    return shows
