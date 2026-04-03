## Plan: API-First MusicBrainz FLAC Tagger

Build an MVP Python project scaffold for an API-first service that takes a MusicBrainz release URL, finds matching local FLAC album content, copies it to a configured output root, and writes standardized metadata. The approach prioritizes clean layering (API -> services -> adapters), deterministic matching flow with explicit candidate selection when ambiguous, and test coverage around URL parsing, matching, and tagging.

**Steps**

**Phase 1 — Project foundation**
1. Create packaging and runtime baseline with pyproject.toml, dependency lock strategy, .gitignore, env template, and logging/config bootstrap. This is blocking for all later phases.
2. Define typed settings model for source scan roots, dedicated output root, clear_metadata default false, and MusicBrainz client settings (user-agent, timeout, rate constraints). Depends on task 1.1.

**Phase 2 — Domain and service layer**
1. Add domain schemas for Release, Track, MatchCandidate, TagJobRequest, TagJobResult, and error envelopes. Depends on task 1.2.
2. Implement MusicBrainz adapter to parse release URL and fetch normalized release metadata. Depends on task 2.1.
3. Implement local scanner service for FLAC discovery and album grouping with pathlib-only path handling. Depends on task 2.1.
4. Implement matcher service returning ranked candidates and requiring explicit selection when >1 candidate. Depends on tasks 2.2 and 2.3.
5. Implement copier service that creates a tagged copy under configured output root and preserves folder structure safely. Depends on task 2.4.
6. Implement FLAC tag writer with mutagen, preserving existing tags by default and clearing only when clear_metadata=true. Depends on task 2.5.

**Phase 3 — API surface**
1. Build API endpoints: health, scan preview, tag job create, candidate selection finalize, and job status/error payloads. Depends on tasks 2.2–2.6.
2. Add request/response validation and consistent error mapping for invalid URL, no matches, multiple matches, and file/tag failures. Parallel with task 3.1 after schemas are stable.

**Phase 4 — Tests and delivery hardening**
1. Unit tests for URL parsing, metadata normalization, FLAC scanning/grouping, candidate scoring, and tag-write policy. Depends on tasks 2.2–2.6.
2. Integration tests for end-to-end flow with mocked MusicBrainz responses and temp file fixtures. Depends on tasks 3.1–3.2.
3. Add runnable developer workflow (lint/test/run) and README usage examples for API-only MVP. Depends on tasks 3.1–4.2.

**Relevant files**
- /home/lazlo/projects/pytagrelease/app.py - API bootstrap entrypoint and route registration.
- /home/lazlo/projects/pytagrelease/README.md - Update with setup, config keys, endpoint contract, and MVP limitations.
- /home/lazlo/projects/pytagrelease/pyproject.toml - Dependencies, project metadata, optional tool config.
- /home/lazlo/projects/pytagrelease/.env.example - Required environment variables and defaults.
- /home/lazlo/projects/pytagrelease/src/api/routes.py - Endpoint handlers and orchestration boundaries.
- /home/lazlo/projects/pytagrelease/src/api/schemas.py - Request/response and error models.
- /home/lazlo/projects/pytagrelease/src/services/musicbrainz.py - Release URL parsing and metadata retrieval.
- /home/lazlo/projects/pytagrelease/src/services/scanner.py - FLAC discovery and album candidate extraction.
- /home/lazlo/projects/pytagrelease/src/services/matcher.py - Candidate scoring and ambiguity handling.
- /home/lazlo/projects/pytagrelease/src/services/copier.py - Destination folder preparation and copy semantics.
- /home/lazlo/projects/pytagrelease/src/services/tagger.py - FLAC metadata write/clear policy.
- /home/lazlo/projects/pytagrelease/src/utils/logger.py - Structured logging setup.
- /home/lazlo/projects/pytagrelease/src/utils/exceptions.py - Typed domain/service errors.
- /home/lazlo/projects/pytagrelease/tests/unit - Unit suite by service.
- /home/lazlo/projects/pytagrelease/tests/integration - End-to-end API workflow tests.

**Verification**
1. Run static and unit checks: lint/type/test commands defined in pyproject.
2. Validate endpoint contracts with local server + curl for health, scan preview, tag create, and candidate selection finalize.
3. Run integration tests against fixture albums and mocked MusicBrainz payloads.
4. Manual filesystem assertion: tagged output is created in configured global output root, source remains unchanged.
5. Manual metadata assertion: default mode preserves unrelated existing tags; clear_metadata=true removes old tags before writing new ones.

**Decisions**
- Scope includes API-only MVP and excludes CLI wrapper.
- Multiple matches return candidates and require explicit user selection.
- Default output target is a dedicated global output folder from config.
- Existing metadata is preserved unless clear_metadata=true.
- Scope excludes MP3 writing in MVP; architecture keeps codec abstraction ready for future addition.

**Further Considerations**
1. Candidate selection persistence: keep in-memory for MVP vs. durable job store if multi-instance deployment is expected.
2. Matching strictness defaults: tune threshold conservatively to avoid false-positive tagging.
3. Throughput strategy: start single-worker tagging for correctness, then add bounded concurrency behind feature flag.

**Detailed Test Plan By Phase**

**Phase 1 - Project foundation**
- Test objectives:
	- Verify project bootstraps consistently across fresh environments.
	- Validate configuration parsing, default values, and required settings enforcement.
	- Confirm developer quality gates are wired and executable.
- Test scope:
	- Packaging and dependency resolution from `pyproject.toml`.
	- Environment variable loading and typed settings validation.
	- Logging initialization behavior at startup.
- Test cases:
	- P1-T01: Install dependencies in clean env succeeds with no conflicts.
	- P1-T02: Missing required config fails fast with actionable error message.
	- P1-T03: Optional config falls back to documented defaults.
	- P1-T04: Invalid config types are rejected with field-level details.
	- P1-T05: App startup initializes logger once and uses configured level/format.
	- P1-T06: Lint, type-check, and test commands are runnable from repo root.
- Test data:
	- Valid and invalid `.env` variants (missing, malformed, and full).
- Automation:
	- Unit tests for settings model and startup helpers.
	- CI step for `lint`, `type`, and `test` command execution.
- Exit criteria:
	- All P1 tests pass.
	- Fresh clone can run quality gates without manual fixups.

**Phase 2 - Domain and service layer**
- Test objectives:
	- Prove correctness of metadata retrieval, local scan, matching, copy, and tagging.
	- Ensure ambiguous matches are deterministic and safe.
	- Validate metadata write policy for preserve vs clear mode.
- Test scope:
	- Domain schemas and validation rules.
	- MusicBrainz adapter behavior with normal and failure responses.
	- Scanner grouping logic, matcher scoring, copier semantics, and tag writer behavior.
- Test cases:
	- P2-T01: MusicBrainz release URL parser extracts valid release IDs and rejects invalid URLs.
	- P2-T02: Adapter normalizes MusicBrainz payload into internal schema.
	- P2-T03: Adapter handles upstream timeout/rate-limit/server errors with typed exceptions.
	- P2-T04: Scanner finds only FLAC files and ignores unsupported extensions.
	- P2-T05: Scanner handles nested folders and special characters in paths.
	- P2-T06: Matcher returns single best match when confidence threshold is met.
	- P2-T07: Matcher returns ranked candidates when multiple plausible matches exist.
	- P2-T08: Copier writes to configured global output root without mutating source files.
	- P2-T09: Copier is idempotent or conflict-safe for existing destination folders.
	- P2-T10: Tagger writes canonical tags from release metadata for FLAC files.
	- P2-T11: Tagger preserves unrelated existing tags when `clear_metadata=false`.
	- P2-T12: Tagger clears existing tags before write when `clear_metadata=true`.
	- P2-T13: Corrupt FLAC file handling produces controlled skip/fail behavior per policy.
- Test data:
	- Mocked MusicBrainz payloads: complete, partial, malformed, and empty tracks.
	- Local fixture albums: exact match, near match, and mismatch sets.
	- FLAC fixtures: valid files with legacy tags and intentionally corrupt samples.
- Automation:
	- Unit tests for each service module with mocked I/O and API calls.
	- Property-style tests for matcher scoring stability with tie scenarios.
- Exit criteria:
	- Critical path services pass all unit tests.
	- No source directory mutation observed in copy/tag workflows.

**Phase 3 - API surface**
- Test objectives:
	- Verify endpoint contracts, status codes, and error schema consistency.
	- Confirm candidate-selection flow is correct for ambiguous matches.
	- Ensure input validation blocks bad requests before service execution.
- Test scope:
	- Endpoints: health, scan preview, tag job create, candidate selection finalize, job status.
	- Request/response schemas and exception-to-HTTP mapping.
- Test cases:
	- P3-T01: Health endpoint returns success quickly and without dependencies on external APIs.
	- P3-T02: Scan preview returns deterministic album candidate summary for fixed fixtures.
	- P3-T03: Tag create with valid URL and deterministic local match returns success payload.
	- P3-T04: Tag create with ambiguous match returns candidates and required next action.
	- P3-T05: Candidate finalize accepts valid selection and completes tagging workflow.
	- P3-T06: Invalid URL returns validation error format defined in API schema.
	- P3-T07: No local match returns not-found style error payload.
	- P3-T08: Upstream MusicBrainz failure maps to expected retryable/non-retryable API errors.
	- P3-T09: File/tagging failures surface sanitized, actionable error messages.
	- P3-T10: Concurrent requests do not corrupt shared state or cross-contaminate job context.
- Test data:
	- HTTP request fixtures for valid and invalid payload permutations.
	- Service mocks for deterministic success/failure paths.
- Automation:
	- API integration tests with test client and dependency overrides.
	- Contract snapshot tests for representative success and error responses.
- Exit criteria:
	- All endpoint contract tests pass.
	- Error payload shape is consistent across failure classes.

**Phase 4 - Tests and delivery hardening**
- Test objectives:
	- Validate end-to-end behavior under realistic conditions.
	- Establish release confidence with quality gates and baseline performance checks.
	- Ensure documentation and runbook instructions are executable.
- Test scope:
	- Full workflow: URL -> scan -> match/select -> copy -> tag -> verify output metadata.
	- CI pipeline, coverage reporting, and developer command ergonomics.
	- Non-functional checks (performance baseline and robustness).
- Test cases:
	- P4-T01: Full happy path end-to-end using mocked MusicBrainz and fixture album.
	- P4-T02: Ambiguous path end-to-end requiring candidate selection before completion.
	- P4-T03: Failure injection at each stage returns expected status and logs root cause.
	- P4-T04: Re-run same request validates idempotency/conflict strategy expectations.
	- P4-T05: Performance baseline run meets target envelopes for scan/match/tag operations.
	- P4-T06: README setup steps work on clean machine from clone to first successful API call.
	- P4-T07: Coverage threshold meets agreed target for core service modules.
- Reporting and artifacts:
	- Test report with pass/fail summary by phase and case ID.
	- Coverage artifact and trend baseline.
	- Defect log with severity and fix status.
- Exit criteria:
	- All blocking defects closed.
	- End-to-end suite green in CI.
	- Documentation validated against real setup/test execution.

**Missing Execution Controls**

1. Phase gates and deliverables
- Define concrete outputs per phase (for example: phase 2 service contracts frozen, phase 3 endpoint contract published, phase 4 CI green with coverage threshold).
- Add explicit gate checks before moving to the next phase.

2. Ownership and timeline
- Assign an owner for each phase and major task group.
- Add target start/end dates and rough effort estimates.

3. Risk register and mitigation plan
- Track each risk with: impact, likelihood, trigger, mitigation, and fallback.
- Start with top risks: wrong album matching, metadata loss, external API failures, and long-running file operations.

4. API operational model
- Specify synchronous vs asynchronous execution for tag jobs.
- Define job lifecycle: create, running, waiting-for-selection, completed, failed, expired.
- Define idempotency strategy, retry policy, and job retention/TTL.

5. Security and abuse controls
- Define authentication requirements for non-local usage.
- Add rate limits and request size limits.
- Enforce path safety constraints to prevent traversal and writes outside approved roots.

6. Observability baseline
- Define required structured log fields (for example: request_id, job_id, release_id, source_path, destination_path, error_code).
- Define metrics (success/failure counts, job duration, scan duration, ambiguous match rate).
- Define alert thresholds for repeated failures and API instability.

7. Release and rollback policy
- Define semantic versioning policy for API and behavior changes.
- Define release checklist and rollback procedure.
- Include migration notes when request/response contracts change.

8. Environment matrix and reproducibility
- Define supported Python versions and OS matrix for local/CI validation.
- Define fixture strategy for repeatable tests (small, deterministic FLAC fixtures and mocked MusicBrainz payloads).
- Ensure local commands and CI commands are aligned to avoid drift.