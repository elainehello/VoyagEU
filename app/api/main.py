from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="VoyagEU Travel Planner")
app.include_router(routes.router, prefix="/app/v1")
