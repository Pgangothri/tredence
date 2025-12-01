# Real-Time Pair Programming Platform

FastAPI backend with WebSocket support and AI-powered autocomplete.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your DATABASE_URL
```

4. Run the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /rooms` - Create a new room
- `GET /ws/{room_id}` - WebSocket connection
- `POST /autocomplete` - Get AI code suggestions
  
# Architecture and design choices
# Backend:

## FastAPI app with a modular layout:

1. routers/ holds route definitions (e.g. rooms, autocomplete).

2. services/ contains business logic (e.g. room creation, code updates).

3. database.py manages SQLAlchemy engine, session factory, and get_db dependency.

4. models.py defines ORM models (e.g. Room) backed by PostgreSQL.​

## REST endpoints:

1. POST /rooms creates a new room and returns a room ID.

2. Additional endpoints (e.g. for autocomplete) are exposed via routers.

## Real-time editing:

1. A WebSocket endpoint /ws/{room_id} uses a ConnectionManager that:

2. racks active WebSocket connections per room.

3. Broadcasts code_update messages to all clients in a room so code stays in sync.​

4. The backend reads/writes room state via SQLAlchemy, so the latest code snapshot is persisted in the DB.

# What I would improve with more time
## Infrastructure and deployment:

1. Move WebSocket handling to infrastructure that fully supports long‑lived connections (Railway, Render, Fly.io, or a managed WebSocket/PubSub service) instead of basic serverless.​

2. Add Docker and docker-compose to spin up backend, frontend, and Postgres with one command.

## Features:

1. Per-user cursors and selection highlights, so collaborators can see each other’s caret positions.

2. Presence and chat (who’s online in a room, text chat alongside the editor).

3. Deeper AI integration: smarter autocomplete and refactor suggestions wired into Monaco’s completion API.​

## Quality and maintainability:

1. Use Alembic migrations instead of Base.metadata.create_all for schema evolution.​

2. Add unit/integration tests for room creation, WebSocket flows, and basic UI interactions.

3. Add observability: structured logging and simple metrics for active rooms and connection counts.
# Limitations
## WebSockets:

1. When deployed on a pure serverless platform (like Vercel functions), WebSocket connections are not fully reliable or long‑lived, so real‑time collaboration is best on a dedicated WebSocket host.​

## Security:

1. No authentication/authorization; any user with a room ID can join and edit.

2. No rate limiting or abuse protection on REST or WebSocket endpoints.

## Data model:

1. Simple rooms table; no version history or conflict-resolution algorithm beyond last-write-wins.

2. No multi-tenant separation or per-user permissions.

## Scalability:

1. Current ConnectionManager uses in-memory state, which works on a single instance but would need a shared store (e.g. Redis pub/sub) for horizontal scaling or multiple backend replicas.

# Frontend
Refer to [Frontend repository](https://github.com/Pgangothri/tredence-frontend)
# Deployment Link:[Deployed backend](https://tredence-dki6nsdcx-pgangothris-projects.vercel.app)

## Demo Video

[Watch the demo on Google Drive](https://drive.google.com/file/d/1Ik9OuFaB_SwJHoreiNoID0ccUrHuZF6T/view?usp=drive_link)


## Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.
