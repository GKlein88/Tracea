from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Tracéa API",
    description="Generate premium SVG posters from GPX activities.",
    version="0.1.0",
)


app.include_router(router)


@app.get("/", include_in_schema=False)
def home():
    return {
        "message": "Tracéa API is running"
    }


@app.get("/health", include_in_schema=False)
def health():
    return {
        "status": "ok"
    }