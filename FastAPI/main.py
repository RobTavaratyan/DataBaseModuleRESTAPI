from fastapi import FastAPI
from .router import app

fastapi_app = FastAPI()
fastapi_app.include_router(app)
