# Health Check API

A FastAPI-based health check service that monitors the status of your application and its dependencies, including PostgreSQL database and Redis cache connectivity.

## Features

- **Application Health Check**: Basic `/up` endpoint to verify the service is running
- **Database Health Check**: Comprehensive health checks for PostgreSQL connectivity
- **Cache Health Check**: Redis connectivity monitoring and health verification
- **Async Endpoints**: All health check endpoints are asynchronous for better performance
- **Docker Support**: Containerized deployment with Docker Compose
- **Structured Logging**: Comprehensive logging with configurable levels
- **CORS Support**: Configurable Cross-Origin Resource Sharing
- **OpenAPI Documentation**: Auto-generated API documentation

## API Endpoints

### Health Check Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/up` | Basic application health check | `{"status": "ok"}` |
| `GET` | `/api/v1/check/` | Comprehensive health check (PostgreSQL + Redis) | `{"success": bool, "up": {"postgres": bool, "redis": bool}}` |
| `GET` | `/api/v1/check/postgres/` | PostgreSQL-specific health check | `{"success": bool, "up": {"postgres": bool, "redis": true}}` |
| `GET` | `/api/v1/check/redis/` | Redis-specific health check | `{"success": bool, "up": {"postgres": true, "redis": bool}}` |

### Response Models

#### UpResponse
```json
{
  "status": "ok"
}
```

#### HealthCheckResponse
```json
{
  "success": true,
  "up": {
    "postgres": true,
    "redis": true
  }
}
```

## Health Check Behavior

The health check endpoints provide different levels of monitoring:

- **`/up`**: Basic application liveness check - always returns 200 OK if the service is running
- **`/api/v1/check/`**: Comprehensive health check that verifies both PostgreSQL and Redis connectivity
  - Returns 200 OK only if both services are healthy
  - Returns 503 Service Unavailable if any service is down
- **`/api/v1/check/postgres/`**: PostgreSQL-specific health check
- **`/api/v1/check/redis/`**: Redis-specific health check

All health check endpoints are asynchronous and include detailed logging for monitoring and debugging.

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd health-check-api
   ```

2. **Configure environment variables**
   ```bash
   # Set your PostgreSQL connection details
   export POSTGRES__HOST=your-postgres-host
   export POSTGRES__USERNAME=your-username
   export POSTGRES__PASSWORD=your-password
   export POSTGRES__DATABASE_NAME=your-database
   
   # Set your Redis connection details
   export REDIS__HOST=your-redis-host
   export REDIS__PORT=6379
   export REDIS__PASSWORD=your-redis-password
   export REDIS__DATABASE=0
   ```

3. **Build and run with Docker Compose**
   ```bash
   just run
   # or
   docker compose up --build
   ```

4. **Access the API**
   - API Base URL: `http://localhost:3001`
   - Health Check: `http://localhost:3001/up`
   - Full Health Check: `http://localhost:3001/api/v1/check/`
   - PostgreSQL Health: `http://localhost:3001/api/v1/check/postgres/`
   - Redis Health: `http://localhost:3001/api/v1/check/redis/`
   - OpenAPI Docs: `http://localhost:3001/docs`

### Development Setup

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Run the application**
   ```bash
   uv run fastapi run src/main.py --port 3000 --host 0.0.0.0
   ```

3. **Run linting**
   ```bash
   just lint
   ```

## Configuration

The application uses environment variables for configuration. Key settings include:

### Application Settings
- `APP__NAME`: Application name (default: "health-check")
- `APP__VERSION`: Application version (default: "0.0.1")
- `APP__ROOT_PATH`: Root path for the API (default: "/health")

### Database Settings
- `POSTGRES__HOST`: PostgreSQL host (default: "localhost")
- `POSTGRES__PORT`: PostgreSQL port (default: 5432)
- `POSTGRES__DATABASE_NAME`: Database name (default: "postgres")
- `POSTGRES__USERNAME`: Database username (default: "postgres")
- `POSTGRES__PASSWORD`: Database password (default: "postgres")

### Redis Settings
- `REDIS__HOST`: Redis host (default: "localhost")
- `REDIS__PORT`: Redis port (default: 6379)
- `REDIS__PASSWORD`: Redis password (default: "redis")
- `REDIS__DATABASE`: Redis database number (default: 0)

### Server Settings
- `SERVER__HTTP_PORT`: HTTP port (default: 3000)
- `PY_ENV`: Environment type (local, dev, prod)

## Docker Configuration

The application includes:
- **Dockerfile**: Multi-stage build with Python 3.12-slim base image
- **docker-compose.yaml**: Complete orchestration setup
- **Health checks**: Built-in container health monitoring
- **Port mapping**: Maps container port 3000 to host port 3001

## Development

### Available Commands

```bash
# Linting and formatting
just lint              # Run all linters
just lint-fix          # Auto-fix linting issues
just lint-ruff-fix     # Fix Ruff issues
just lint-black-fix    # Apply Black formatting
just lint-isort-fix    # Fix import sorting

# Docker operations
just build             # Build Docker image
just run               # Run with Docker Compose
just status            # Check container status
just logs              # View container logs
just stop              # Stop all containers
```

### Project Structure

```
src/
├── api.py                          # Main API router
├── main.py                         # FastAPI application entry point
├── checks/
│   ├── postgres.py                 # PostgreSQL health check logic
│   └── redis.py                    # Redis health check logic
├── infrastructure/
│   ├── settings.py                 # Environment configuration
│   └── logger.py                   # Logging configuration
├── controllers/
│   └── health_check_controller.py  # Health check endpoints
└── models/
    ├── health_check_response.py    # Health check response models
    └── up_response.py              # Up endpoint response model
```

## Monitoring and Logging

- **Structured Logging**: JSON-formatted logs with configurable levels
- **Health Check Monitoring**: Built-in health checks for container orchestration
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Request Logging**: Detailed request/response logging for debugging

## Production Deployment

The application is designed for production deployment with:
- **Multi-worker support**: Runs with 4 workers by default
- **Health check endpoints**: For load balancer and orchestration health checks
- **Configurable CORS**: Secure cross-origin resource sharing
- **Environment-based configuration**: Separate configs for different environments

## License

This project is part of the HomePi ecosystem and is designed for monitoring the health of your home automation services.
