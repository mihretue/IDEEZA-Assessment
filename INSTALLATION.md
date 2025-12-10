# Installation & Setup Guide

Complete installation and setup instructions for the IDEEZA Analytics API, including Redis configuration.

---

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- Redis (for Celery and caching)
- PostgreSQL (optional, SQLite works for development)

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd IDEEZA-Assessment
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# For local development
pip install -r requirements/local.txt

# For production
pip install -r requirements/production.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (optional, defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Redis (optional, for Celery)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Install and Configure Redis

Redis is required for Celery (async tasks) and Django caching.

#### Windows

**Option 1: Using Docker (Recommended)**
```bash
docker run -d -p 6379:6379 --name redis redis:7
```

**Option 2: Native Installation**
1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`
3. Default port: 6379

**Option 3: WSL2**
```bash
wsl
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server

# Enable on boot
sudo systemctl enable redis-server

# Check status
sudo systemctl status redis-server
```

#### macOS

```bash
# Using Homebrew
brew install redis

# Start Redis
brew services start redis

# Or run in foreground
redis-server
```

#### Docker (All Platforms)

```bash
# Run Redis container
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7

# Check if running
docker ps | grep redis

# View logs
docker logs redis

# Stop Redis
docker stop redis

# Start Redis
docker start redis
```

#### Verify Redis Installation

```bash
# Test connection
redis-cli ping
# Expected output: PONG

# Check Redis info
redis-cli info server

# Test with Python script
python test_redis_connection.py
```

#### Redis Configuration

The project uses Redis for:
1. **Celery Message Broker** - Task queue management
2. **Celery Result Backend** - Storing task results
3. **Django Caching** - Session storage and query caching

Configuration is in `.env`:
```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

For Docker Compose, Redis is automatically configured in `docker-compose.yml`.

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Seed the Database

```bash
# Quick seed (30 users, ~160 blogs, ~16,000 views)
python seed_quick.py

# Or use management command with custom data
python manage.py seed_data --users 50 --blogs-per-user 10 --views-per-blog 100

# Clear and reseed
python manage.py seed_data --clear
```

### 8. Run the Server

```bash
python manage.py runserver
```

The API will be available at: http://localhost:8000

**API Documentation:**
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

### 9. Run Tests (Optional)

```bash
# All tests
python manage.py test analytics.tests

# Specific test file
python manage.py test analytics.tests.test_services
python manage.py test analytics.tests.test_views

# With coverage
coverage run --source='analytics' manage.py test analytics.tests
coverage report
```

### 10. Run Celery (Optional)

```bash
# Windows
celery -A ideeza_assessment worker -l info --pool=solo

# Linux/Mac
celery -A ideeza_assessment worker -l info

# Celery Beat (for scheduled tasks)
celery -A ideeza_assessment beat -l info
```

---

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Start all services (PostgreSQL, Redis, Web)
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Seed database
docker-compose exec web python seed_quick.py

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

---

## Verification

Run the verification script to check everything:

```bash
python verify_setup.py
```

**Expected Output:**
- ✅ Django Setup
- ✅ Database
- ✅ URLs
- ✅ Swagger
- ✅ Tests
- ✅ Documentation

---

## Quick Start Testing

### 1. Start Server
```bash
python manage.py runserver
```

### 2. Open Swagger UI
Navigate to: http://localhost:8000/api/docs/

### 3. Test Endpoints

**Blog Views Analytics:**
```bash
curl "http://localhost:8000/analytics/blog-views/?object_type=country&range=month"
```

**Top Analytics:**
```bash
curl "http://localhost:8000/analytics/top/?top=user&range=all"
```

**Performance Analytics:**
```bash
curl "http://localhost:8000/analytics/performance/?compare=week"
```

---

## Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping

# Start Redis with Docker
docker run -d -p 6379:6379 redis:7
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements/local.txt
```

### Database Errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python seed_quick.py
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

---

## Project Structure

```
IDEEZA-Assessment/
├── analytics/              # Main application
│   ├── management/         # Management commands
│   │   └── commands/
│   │       └── seed_data.py
│   ├── tests/              # Test suite
│   │   ├── test_services.py
│   │   └── test_views.py
│   ├── models.py           # Database models
│   ├── services.py         # Business logic
│   ├── views.py            # API views
│   ├── serializers.py      # DRF serializers
│   └── urls.py             # URL routing
├── ideeza_assessment/      # Project settings
│   ├── settings/           # Split settings
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── celery.py           # Celery config
│   └── urls.py             # Main URL config
├── requirements/           # Dependencies
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── .env                    # Environment variables
├── docker-compose.yml      # Docker configuration
├── manage.py               # Django management
├── seed_quick.py           # Quick seed script
├── verify_setup.py         # Setup verification
└── README.md               # Project documentation
```

---

## Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Access admin panel
# http://localhost:8000/admin/

# Django shell
python manage.py shell

# Check for issues
python manage.py check

# Collect static files (production)
python manage.py collectstatic
```

---

## Next Steps

1. Start the server: `python manage.py runserver`
2. Open Swagger UI: http://localhost:8000/api/docs/
3. Test the APIs interactively
4. Review the code in `analytics/` directory
5. Run tests: `python manage.py test analytics.tests`

---

## Support

For issues or questions:
1. Check the README.md for API documentation
2. Run `python verify_setup.py` to check configuration
3. Review test files for usage examples
