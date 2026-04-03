"""Application API route definitions."""

from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Simple health endpoint used by smoke tests and runtime checks."""
    return {"status": "ok"}


def register_routes(app: FastAPI) -> None:
    """Attach all API routes to the application."""
    app.include_router(router)