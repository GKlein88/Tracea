from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.routes import router


app = FastAPI(
    title="Tracéa API",
    description="Generate premium SVG posters from GPX activities.",
    version="0.1.0",
)

Path("outputs").mkdir(
    parents=True,
    exist_ok=True
)

templates = Jinja2Templates(
    directory="app/templates"
)

app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

app.include_router(router)


@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Tracéa"
        }
    )


@app.get("/health", include_in_schema=False)
def health():
    return {
        "status": "ok"
    }
