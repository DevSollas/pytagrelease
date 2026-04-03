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