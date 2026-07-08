from fastapi import APIRouter, UploadFile, File

from app.services.poster_service import generate_poster
from app.models.response import PosterResponse


router = APIRouter()


@router.post(
    "/generate",
    tags=["Poster"],
    summary="Generate an SVG poster from GPX",
    response_model=PosterResponse,
)
async def generate(
    file: UploadFile = File(...)
):
    return await generate_poster(file)