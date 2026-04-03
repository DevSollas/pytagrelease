# Music album metadata tagger from MusicBrainz database

This python program tag your album with all MusicBrainz metadata information.

## What It Does

You input a musicbrainz link of specific release. The app search in your music folders, find this release, make a copy of it and store all the available matadata infromation from musicbrainz in this copy of your files of this album and clear all any other older metadata information from tis file, if you set this option in the config file. (aka. tag and clean your files metadata information)

This tool currently only work for flac files. Later for mp3 files.

The tool was developed with the API first approach, so all current and future features will be available with an API call also.  

## Development Setup

### Requirements

- Python 3.11+

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

### Configuration

The app reads runtime settings from environment variables (or `.env`):

- `APP_ENV`: `development`, `test`, or `production`
- `APP_HOST`: API bind host (default `0.0.0.0`)
- `APP_PORT`: API bind port (default `8000`)
- `LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- `MUSIC_SOURCE_ROOTS`: comma-separated source roots to scan
- `TAGGED_OUTPUT_ROOT`: destination root for tagged copies
- `CLEAR_METADATA`: `true` or `false`
- `MUSICBRAINZ_USER_AGENT`: MusicBrainz client user agent
- `MUSICBRAINZ_TIMEOUT_SECONDS`: request timeout
- `MUSICBRAINZ_RATE_LIMIT_PER_SECOND`: max request rate

`MUSIC_SOURCE_ROOT` is also accepted for backward compatibility.

### Run API

```bash
python app.py
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

### Quality checks

```bash
ruff check .
mypy .
pytest
```

## Fresh Environment Reproducibility

This repository includes two reproducibility mechanisms:

- GitHub Actions workflow: `.github/workflows/reproducibility.yml`
	- Fresh Python environment checks on `3.11` and `3.12`
	- Lint, type-check, and tests
- Docker reproducibility check:
	- Build with `Dockerfile`
	- Run the same quality checks inside the container

Run Docker reproducibility locally:

```bash
docker build -t pytagrelease-repro .
docker run --rm pytagrelease-repro
```
