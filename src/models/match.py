"""Album match candidate domain model."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class MatchCandidate(BaseModel):
    """Represents a possible local-album match for a requested release."""

    model_config = ConfigDict(extra="forbid")

    album_path: Path
    confidence: float = Field(ge=0.0, le=1.0)
    matched_track_count: int = Field(ge=0)
    total_track_count: int = Field(ge=0)
    reasons: list[str] = Field(default_factory=list)
