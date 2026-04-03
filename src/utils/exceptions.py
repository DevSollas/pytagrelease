"""Typed domain exceptions for service and API layers."""

from typing import Any

from src.api.schemas import ErrorDetail, ErrorEnvelope


class AppError(Exception):
    """Base application exception that can be converted into an error envelope."""

    code = "app_error"

    def __init__(self, message: str, *, details: list[ErrorDetail] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or []

    def to_error_envelope(self) -> ErrorEnvelope:
        """Convert the exception into a transport-safe API error envelope."""
        return ErrorEnvelope(code=self.code, message=self.message, details=self.details)


class RequestValidationError(AppError):
    """Raised when a request cannot be accepted by the workflow."""

    code = "request_validation_error"


class NoMatchFoundError(AppError):
    """Raised when no local album candidate satisfies the release query."""

    code = "no_match_found"


class MultipleMatchesFoundError(AppError):
    """Raised when more than one local candidate requires user selection."""

    code = "multiple_matches_found"

    def __init__(self, message: str, *, candidate_count: int) -> None:
        super().__init__(
            message,
            details=[ErrorDetail(field="candidates", reason="ambiguous_match", value=candidate_count)],
        )


class TaggingFailureError(AppError):
    """Raised when copying or writing tags fails irrecoverably."""

    code = "tagging_failure"


def build_error_detail(field: str | None, reason: str, value: Any | None = None) -> ErrorDetail:
    """Build a reusable error detail entry."""
    return ErrorDetail(field=field, reason=reason, value=value)
