from fastapi import FastAPI
from .basic_router import basic_router
from .api_requests import api_router
fastapi_app = FastAPI()
fastapi_app.include_router(basic_router)
fastapi_app.include_router(api_router)
