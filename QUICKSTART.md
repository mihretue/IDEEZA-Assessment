# Quick Start Guide

Get the IDEEZA Analytics API running in 5 minutes!

## Option 1: Docker (Fastest)

```bash
# 1. Start all services
docker-compose up -d

# 2. Run migrations
docker-compose exec web python manage.py migrate

# 3. Test the API
curl "http://localhost:8000/analytics/blog-views/?object_type=country&range=month"

# Done! 🎉
```

## Option 2: Local Development

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements/local.txt
```

### Step 2: Start Redis

**Using Docker (Easiest):**
```bash
docker run -d -p 6379:6379 --name redis redis:7
```

**Or install locally:** See [REDIS_SETUP.md](REDIS_SETUP.md)

### Step 3: Configure Environment

Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Step 4: Setup Database

```bash
python manage.py migrate
```

### Step 5: Test Redis Connection

```bash
python test_redis_connection.py
```

### Step 6: Run Server

```bash
python manage.py runserver
```

### Step 7: Test API

Open browser or use curl:
```bash
curl "http://localhost:8000/analytics/blog-views/?object_type=country&range=month"
```

## Create Sample Data

```bash
python manage.py shell
```

```python
from analytics.models import User, Country, Blog, BlogView
import random

# Create countries
countries = [
    Country.objects.create(name="USA", code="US"),
    Country.objects.create(name="Canada", code="CA"),
    Country.objects.create(name="UK", code="GB"),
]

# Create users
users = [User.objects.create(username=f"user{i}", email=f"user{i}@test.com") for i in range(5)]

# Create blogs
for user in users:
    for i in range(3):
        blog = Blog.objects.create(
            title=f"{user.username}'s Blog {i}",
            content="Sample content",
            author=user,
            country=random.choice(countries)
        )
        # Create views
        for _ in range(random.randint(10, 50)):
            BlogView.objects.create(
                blog=blog,
                user=random.choice(users),
                country=random.choice(countries)
            )

print("✅ Sample data created!")
```

## Test the APIs

### 1. Blog Views Analytics
```bash
# By country
curl "http://localhost:8000/analytics/blog-views/?object_type=country&range=month"

# By user with pagination
curl "http://localhost:8000/analytics/blog-views/?object_type=user&range=week&page=1&page_size=5"
```

### 2. Top Analytics
```bash
# Top users
curl "http://localhost:8000/analytics/top/?top=user&range=all"

# Top countries
curl "http://localhost:8000/analytics/top/?top=country&range=month"

# Top blogs
curl "http://localhost:8000/analytics/top/?top=blog&range=week"
```

### 3. Performance Analytics
```bash
# Weekly performance
curl "http://localhost:8000/analytics/performance/?compare=week"

# Monthly performance for specific user
curl "http://localhost:8000/analytics/performance/?compare=month&user_id=1"
```

## Run Tests

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

## Optional: Start Celery

For async task processing:

```bash
# Windows
celery -A ideeza_assessment worker -l info --pool=solo

# Linux/Mac
celery -A ideeza_assessment worker -l info
```

## API Documentation

Visit: http://localhost:8000/api/schema/swagger-ui/

## Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping

# Start Redis with Docker
docker run -d -p 6379:6379 redis:7

# Test connection
python test_redis_connection.py
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
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

## Next Steps

1. Read [README.md](README.md) for detailed API documentation
2. Check [PAGINATION.md](PAGINATION.md) for pagination features
3. See [REDIS_SETUP.md](REDIS_SETUP.md) for Redis configuration
4. Explore the code in `analytics/` directory

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

# Run specific test
python manage.py test analytics.tests.test_views.TestBlogViewsAnalyticsView

# Collect static files (production)
python manage.py collectstatic
```

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

---

**Need Help?** Check the main [README.md](README.md) or additional documentation files.
