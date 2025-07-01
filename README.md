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

### EC2 Deployment via GitHub Actions

The project includes a GitHub Actions workflow that:
1. Runs tests and linting
2. Deploys directly to EC2 via SSH
3. Uses systemd to manage the service
4. Sets up nginx as reverse proxy

### EC2 Setup Required

1. **Launch an EC2 instance:**
   - Use Ubuntu 22.04 LTS AMI
   - Instance type: t3.micro or larger
   - Security group: Allow SSH (22), HTTP (80), HTTPS (443)
   - Create or use existing key pair

2. **Run setup script on EC2:**
   ```bash
   # SSH into your EC2 instance
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Download and run setup script
   curl -sSL https://raw.githubusercontent.com/ekow1/fastapi-service/main/deploy/setup-ec2.sh | bash
   ```

3. **Configure GitHub Secrets:**
   Add these secrets to your GitHub repository:
   - `EC2_HOST`: Your EC2 public IP address
   - `EC2_USERNAME`: `ubuntu` (default for Ubuntu AMI)
   - `EC2_SSH_KEY`: Your private SSH key content

4. **Configure Nginx (optional):**
   ```bash
   # Copy nginx config and restart
   sudo cp /home/ubuntu/fastapi-service/deploy/nginx-fastapi.conf /etc/nginx/sites-available/fastapi
   sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   sudo systemctl restart nginx
   ```

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
