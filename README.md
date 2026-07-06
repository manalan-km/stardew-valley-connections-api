# Stardew Valley Connections API

FastAPI backend for [Stardew Valley Connections](https://github.com/manalan-km/stardew-valley-connections), a daily word-association puzzle game. Serves the daily puzzle, validates guesses, and generates a new challenge every day from a curated pool of Stardew Valley categories.

> **Status:** In development, working towards public release.

## How it works

- **Category pool:** `categories.json` holds the curated groups of Stardew Valley items (crops, fish, villagers, and more) that puzzles are built from.
- **Daily generation:** a scheduled Python script selects and shuffles four categories into the day's puzzle, so every player sees the same challenge on a given date. <!-- TODO: confirm mechanism — cron script vs on-request generation with a date seed -->
- **API:** the FastAPI app exposes the puzzle and game endpoints consumed by the React frontend.

## Tech

- Python 3 with FastAPI 0.116 + Uvicorn
- Pydantic v2 for request/response models
- Supabase Python client (database and auth)
- Sentry SDK for error monitoring
- python-dotenv for configuration

## Running locally

```bash
git clone https://github.com/manalan-km/stardew-valley-connections-api.git
cd stardew-valley-connections-api

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # then fill in values
```

The API starts on `http://localhost:8001` by default.

### Configuration

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
| --- | --- |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase API key |
| `CHALLENGE_FILE_CHECK` | Set to `0` to enable the challenge file check, `1` to skip it |


## Daily challenge generation

```bash
python src/generate_daily.py   # generate/rotate the daily puzzle
```

In deployment this runs on a daily cron schedule.

## Disclaimer

This is a non-commercial fan project. Stardew Valley and its assets belong to ConcernedApe; this project is not affiliated with or endorsed by ConcernedApe.
