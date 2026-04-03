from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.api.schemas import ErrorEnvelope, TagJobRequest, TagJobResult
from src.models import MatchCandidate, Release, Track
from src.utils.exceptions import MultipleMatchesFoundError, build_error_detail


def build_track(number: int) -> Track:
    return Track(
        title=f"Track {number}",
        track_number=number,
        position=number,
        artist_credit="Artist",
        length_ms=180000,
        recording_id=uuid4(),
    )


def test_release_sets_total_tracks_from_track_count() -> None:
    release = Release(
        release_id=uuid4(),
        title="Album",
        artist_credit="Artist",
        tracks=[build_track(1), build_track(2)],
    )

    assert release.total_tracks == 2


def test_release_rejects_mismatched_total_tracks() -> None:
    with pytest.raises(ValidationError):
        Release(
            release_id=uuid4(),
            title="Album",
            artist_credit="Artist",
            tracks=[build_track(1), build_track(2)],
            total_tracks=3,
        )


def test_match_candidate_requires_confidence_between_zero_and_one() -> None:
    with pytest.raises(ValidationError):
        MatchCandidate(
            album_path=Path("/music/album"),
            confidence=1.5,
            matched_track_count=8,
            total_track_count=10,
        )


def test_tag_job_request_accepts_musicbrainz_release_url() -> None:
    request = TagJobRequest.model_validate(
        {"musicbrainz_url": "https://musicbrainz.org/release/12345678-1234-1234-1234-123456789012"}
    )

    assert str(request.musicbrainz_url) == (
        "https://musicbrainz.org/release/12345678-1234-1234-1234-123456789012"
    )


def test_tag_job_request_rejects_non_release_url() -> None:
    with pytest.raises(ValidationError):
        TagJobRequest.model_validate({"musicbrainz_url": "https://example.com/release/123"})


def test_tag_job_result_supports_awaiting_selection_state() -> None:
    candidate = MatchCandidate(
        album_path=Path("/music/album"),
        confidence=0.82,
        matched_track_count=8,
        total_track_count=10,
        reasons=["track_count_close"],
    )
    result = TagJobResult(status="awaiting_selection", candidates=[candidate], message="Select a candidate")

    assert result.status == "awaiting_selection"
    assert result.candidates == [candidate]


def test_multiple_matches_error_converts_to_error_envelope() -> None:
    error = MultipleMatchesFoundError("Multiple local albums matched", candidate_count=2)

    envelope = error.to_error_envelope()

    assert isinstance(envelope, ErrorEnvelope)
    assert envelope.code == "multiple_matches_found"
    assert envelope.details[0].field == "candidates"
    assert envelope.details[0].value == 2


def test_build_error_detail_creates_structured_error_detail() -> None:
    detail = build_error_detail("musicbrainz_url", "invalid_release_url", "https://example.com")

    assert detail.field == "musicbrainz_url"
    assert detail.reason == "invalid_release_url"
    assert detail.value == "https://example.com"
