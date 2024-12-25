from fastapi import FastAPI
from application import *
fastapi_app = FastAPI()
fastapi_app.include_router(basic_router)
fastapi_app.include_router(api_router)
