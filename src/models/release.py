"""Release domain model for normalized MusicBrainz metadata."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.models.track import Track


class Release(BaseModel):
    """Represents a normalized MusicBrainz release and its tracks."""

    model_config = ConfigDict(extra="forbid")

    release_id: UUID
    title: str = Field(min_length=1)
    artist_credit: str = Field(min_length=1)
    tracks: list[Track] = Field(min_length=1)
    total_tracks: int | None = Field(default=None, ge=1)
    release_group_id: UUID | None = None
    date: str | None = None
    country: str | None = None
    barcode: str | None = None
    media_format: str | None = None

    @model_validator(mode="after")
    def set_or_validate_total_tracks(self) -> "Release":
        """Ensure total_tracks matches the normalized track list size."""
        actual_total = len(self.tracks)
        if self.total_tracks is None:
            self.total_tracks = actual_total
            return self

        if self.total_tracks != actual_total:
            raise ValueError("total_tracks must match the number of tracks")

        return self
