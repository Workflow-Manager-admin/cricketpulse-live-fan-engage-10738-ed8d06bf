# Backend AI Poll Generator Service

This service simulates a live cricket commentary feed, uses simple AI-like rules to generate engaging MCQ fan polls, exposes REST API endpoints for poll participation/results, and is ready for frontend integration.

## Features

- Simulated ball-by-ball commentary API endpoint
- AI-driven (logic) poll generator based on live commentary context
- REST API: 
  - Fetch latest poll (`GET /api/polls`)
  - Submit poll vote (`POST /api/polls/<poll_id>/vote`)
  - Get poll results (`GET /api/polls/<poll_id>/results`)
  - Fetch latest commentary (`GET /api/commentary`)
- CORS enabled
- Fully documented entrypoints

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

The service runs on port 5001 by default.

## API Endpoints

- `GET /api/commentary` - Get simulated latest live commentary.
- `GET /api/polls` - Fetch the latest AI-generated poll.
- `POST /api/polls/<poll_id>/vote` - Submit a vote, request JSON: `{"option": <index>}`
- `GET /api/polls/<poll_id>/results` - Get live results (vote tallies) for a poll.

## Integration

- Enable CORS for frontend polling UI.
- Ready for extension with real live commentary or LLM-based poll generation.
