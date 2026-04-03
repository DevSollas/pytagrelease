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
