"""Application entrypoint for the MusicBrainz metadata tagger API."""

from fastapi import FastAPI

from src.api.routes import register_routes
from src.config.settings import get_settings
from src.utils.logger import configure_logging, get_logger


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(
        title="pytagrelease",
        version="0.1.0",
        description="API-first metadata tagging service for music releases.",
    )

    register_routes(app)
    logger = get_logger(__name__)
    logger.info(
        "application_initialized",
        app_env=settings.app_env,
        host=settings.app_host,
        port=settings.app_port,
    )
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
    )
