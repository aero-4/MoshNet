from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from core.settings import settings
from domains.presentation.api import router as api_router_domains

app = FastAPI(
    root_path=settings.API_V1
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router_domains, prefix="/domains")

MEDIA_ROOT = Path(__file__).resolve().parents[2] / "media"
app.mount("/media", StaticFiles(directory=MEDIA_ROOT, check_dir=False), name="media")
