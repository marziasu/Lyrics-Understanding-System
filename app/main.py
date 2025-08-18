from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Harmoni Hub")

app.include_router(router, prefix="/Extraction", tags=["Generate"])