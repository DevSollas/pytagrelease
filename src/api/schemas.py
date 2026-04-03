"""API request and response schemas for tag job workflows."""

from pathlib import Path
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from src.models import MatchCandidate, Release


JobStatus = Literal["queued", "matching", "awaiting_selection", "completed", "failed"]


class TagJobRequest(BaseModel):
    """Input payload for starting a tagging workflow."""

    model_config = ConfigDict(extra="forbid")

    musicbrainz_url: HttpUrl
    clear_metadata: bool | None = None
    selected_candidate_path: Path | None = None

    @field_validator("musicbrainz_url")
    @classmethod
    def validate_musicbrainz_release_url(cls, value: HttpUrl) -> HttpUrl:
        """Accept only MusicBrainz release URLs for this workflow."""
        path = value.path or ""
        if value.host != "musicbrainz.org" or "/release/" not in path:
            raise ValueError("musicbrainz_url must point to a MusicBrainz release")
        return value


class TagJobResult(BaseModel):
    """Response payload representing the current state of a tag job."""

    model_config = ConfigDict(extra="forbid")

    job_id: UUID = Field(default_factory=uuid4)
    status: JobStatus
    release: Release | None = None
    selected_candidate: MatchCandidate | None = None
    candidates: list[MatchCandidate] = Field(default_factory=list)
    output_path: Path | None = None
    clear_metadata: bool = False
    message: str | None = None


class ErrorDetail(BaseModel):
    """Machine-readable error detail payload."""

    model_config = ConfigDict(extra="forbid")

    field: str | None = None
    reason: str
    value: Any | None = None


class ErrorEnvelope(BaseModel):
    """Top-level error response envelope for API failures."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)
