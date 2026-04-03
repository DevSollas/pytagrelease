"""Application entrypoint for the MusicBrainz metadata tagger API."""

from fastapi import FastAPI

from src.api.routes import register_routes
from src.utils.logger import configure_logging, get_logger


def create_app() -> FastAPI:
	"""Create and configure the FastAPI application instance."""
	configure_logging()
	app = FastAPI(
		title="pytagrelease",
		version="0.1.0",
		description="API-first metadata tagging service for music releases.",
	)

	register_routes(app)
	logger = get_logger(__name__)
	logger.info("application_initialized")
	return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
