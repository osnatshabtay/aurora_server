from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os

from app.routes.user_routes import router as user_route
from app.routes.post_routes import router as post_routes
from app.routes.enrichment_content_routes import router as enrichment_content_routes

app = FastAPI()

app.include_router(user_route, prefix="/users", tags=["Users"])
app.include_router(post_routes, prefix="/feed", tags=["Post"])
app.include_router(enrichment_content_routes, prefix="/recommendations", tags=["Recommendations"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}
