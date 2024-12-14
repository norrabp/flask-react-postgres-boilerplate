# Flask React Application with PostgreSQL, Redis, and Celery

## Running with Docker Compose (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. Clone the repository
2. Run the application:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:5000
- Backend API: http://localhost:8000

### Services
- Flask Web Application (http://localhost:8000)
- Celery Worker for background tasks
- PostgreSQL Database (port 5432)
- Redis Server (port 6379)

## Local Development Setup (Alternative)

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Node.js 20+
- Poetry (Python package manager)

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies using Poetry
poetry install

# Install Node.js dependencies
cd frontend
npm install
```

### 2. Environment Setup

Create a `.env` file in the root directory with the following variables:
```
# PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/your_database_name

# Redis
REDIS_URL=redis://localhost:6379/0

# Flask
FLASK_SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### 3. Database Setup
```bash
# Create database and run migrations
poetry run flask db upgrade
```

### 4. Running the Application

Start each service in a separate terminal:

#### Backend Server
```bash
# Start Flask backend
poetry run python run.py
```

#### Frontend Development Server
```bash
# From the frontend directory
npm run dev
```

#### Celery Worker
```bash
# From the root directory
poetry run celery -A backend.celery_worker.celery worker --loglevel=info
```

#### Redis Server
Make sure Redis is running on the default port (6379)

### 5. Access the Application
- Frontend: http://localhost:5000
- Backend API: http://localhost:8000

## Test User Credentials
```
Email: test@example.com
Password: TestUser@2024Secure!
```

## Available Features
- User Authentication (Login/Register)
- Real-time Statistics Dashboard
- User Management
- Background Task Processing with Celery
- Redis Caching

## Development
- Frontend code is in the `frontend` directory
- Backend code is in the `backend` directory
- API routes are in `backend/api/routes.py`
- Authentication routes are in `backend/auth.py`

## Docker Development Commands

### Build and Start Services
```bash
docker-compose up --build
```

### View Logs
```bash
docker-compose logs -f [service_name]
```

### Stop Services
```bash
docker-compose down
```

### Access PostgreSQL
```bash
docker-compose exec db psql -U postgres -d flask_app
```

### Access Redis CLI
```bash
docker-compose exec redis redis-cli
```
