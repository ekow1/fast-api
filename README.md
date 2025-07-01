# FastAPI Service

A simple FastAPI service with uv, Docker, and AWS deployment capabilities.

## Features

- FastAPI web framework
- UV for fast Python package management
- Docker containerization
- GitHub Actions CI/CD pipeline
- AWS ECS deployment ready
- Health check endpoints
- CORS middleware
- Pydantic models for data validation

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `POST /items/` - Create a new item
- `GET /items/` - List all items (with pagination)
- `GET /items/{item_id}` - Get specific item
- `DELETE /items/{item_id}` - Delete an item

## Local Development

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) installed
- Docker (optional)

### Setup

1. Install dependencies:
```bash
uv sync
```

2. Run the application:
```bash
uv run python main.py
```

3. Visit `http://localhost:8000` to see the API
4. Visit `http://localhost:8000/docs` for interactive API documentation

### Using Docker

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Or build and run manually:
```bash
docker build -t fastapi-service .
docker run -p 8000:8000 fastapi-service
```

## Testing

Run tests (when test files are added):
```bash
uv run pytest tests/ -v
```

## Deployment

### GitHub Actions

The project includes a GitHub Actions workflow that:
1. Runs tests and linting
2. Builds Docker image
3. Pushes to AWS ECR
4. Deploys to AWS ECS

### AWS Setup Required

1. Create an ECR repository named `fastapi-service`
2. Create an ECS cluster named `fastapi-cluster`
3. Create an ECS service named `fastapi-service`
4. Add GitHub secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

## Environment Variables

- `PORT`: Port to run the application (default: 8000)

## Development

### Code Formatting
```bash
uv run black main.py
```

### Linting
```bash
uv run flake8 main.py --max-line-length=88
```

### Type Checking
```bash
uv run mypy main.py
```
