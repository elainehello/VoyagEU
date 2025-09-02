from dotenv import load_dotenv
import os

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "data")
FLIGHT_API_URL = os.getenv("FLIGHT_API_URL")
FLIGHT_API_KEY = os.getenv("FLIGHT_API_KEY")