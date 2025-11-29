# AI Software Factory

Autonomous software development platform powered by AI agents.

## Architecture

```
                                +------------------+
                                |   Frontend       |
                                |   (Next.js 14)   |
                                +--------+---------+
                                         |
                                         | REST API
                                         v
+------------------+    +------------------+------------------+
|   PostgreSQL     |<-->|                                     |
|   (Persistence)  |    |         FastAPI Backend             |
+------------------+    |                                     |
                        |   +-------------+  +-------------+  |
+------------------+    |   | CrewAI      |  | LangChain   |  |
|   Redis          |<-->|   | Agents      |  | LLM Layer   |  |
|   (Cache/Queue)  |    |   +-------------+  +-------------+  |
+------------------+    |                                     |
                        +------------------+------------------+
+------------------+                       |
|   ChromaDB       |<----------------------+
|   (Vector Store) |
+------------------+
```

## Stack

### Backend
| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | 0.109.0 |
| Agent Orchestration | CrewAI | 0.41.1 |
| LLM Integration | LangChain | 0.1.20 |
| Database ORM | SQLAlchemy | 2.0.27 |
| Migrations | Alembic | 1.13.1 |
| Task Queue | Celery | 5.3.6 |

### Frontend
| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Next.js | 14.0.4 |
| UI Library | React | 18.2.0 |
| State Management | Zustand | 4.4.7 |
| Data Fetching | TanStack Query | 5.12.2 |
| Styling | Tailwind CSS | 3.3.6 |

### Infrastructure
| Component | Technology | Version |
|-----------|------------|---------|
| Database | PostgreSQL | 16 |
| Cache | Redis | 7 |
| Vector Store | ChromaDB | 0.4.24 |
| Containerization | Docker | 24+ |

## Quick Start

```bash
git clone https://github.com/Richardmsbr/ai-software-factory.git
cd ai-software-factory

cp config/example.env config/.env
# Edit config/.env with your API keys

docker-compose up -d
```

### Access

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| API Docs | http://localhost:8000/api/docs |
| Health | http://localhost:8000/api/health |

## Configuration

```bash
# config/.env

OPENROUTER_API_KEY=your_key
DEFAULT_LLM_PROVIDER=openrouter
DEFAULT_MODEL=anthropic/claude-3.5-sonnet

DATABASE_URL=postgresql+asyncpg://factory:factory@postgres:5432/ai_factory
SECRET_KEY=generate-secure-key
```

### Providers

| Provider | Models |
|----------|--------|
| OpenRouter | Multiple providers |
| OpenAI | GPT-4, GPT-3.5 |
| Anthropic | Claude 3.5, Claude 3 |
| Ollama | Local models |

## Project Structure

```
ai-software-factory/
├── backend/
│   ├── agents/           # AI agent definitions
│   ├── api/              # REST endpoints
│   ├── core/             # Configuration
│   ├── database/         # Models and migrations
│   └── services/         # Business logic
├── frontend/
│   └── src/
│       ├── components/   # React components
│       ├── pages/        # Next.js pages
│       └── lib/          # Utilities
├── config/               # Environment
└── docker-compose.yml
```

## API

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/projects | List projects |
| POST | /api/projects | Create project |
| GET | /api/projects/{id} | Get project |
| PUT | /api/projects/{id} | Update project |
| DELETE | /api/projects/{id} | Delete project |

### Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/agents | List agents |
| GET | /api/agents/{id} | Get agent |
| POST | /api/agents/{id}/assign | Assign task |

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Tests

```bash
# Backend
pytest -v --cov=.

# Frontend
npm test
```

## Operations

```bash
# Logs
docker-compose logs -f

# Stop
docker-compose down

# Reset
docker-compose down -v && docker-compose up -d
```

## License

MIT
