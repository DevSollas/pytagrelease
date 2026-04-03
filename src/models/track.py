"""Track domain model for normalized release metadata."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Track(BaseModel):
    """Represents a single track within a MusicBrainz release."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    track_number: int = Field(ge=1)
    position: int = Field(ge=1)
    artist_credit: str | None = None
    length_ms: int | None = Field(default=None, ge=0)
    recording_id: UUID | None = None
