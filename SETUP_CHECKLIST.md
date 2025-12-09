# Setup Checklist

Use this checklist to ensure your development environment is properly configured.

## ✅ Prerequisites

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] virtualenv or venv available
- [ ] Redis installed or Docker available
- [ ] Git installed (for cloning)

## ✅ Installation Steps

### 1. Project Setup
- [ ] Clone repository
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements/local.txt`

### 2. Redis Setup
- [ ] Redis installed (see REDIS_SETUP.md)
- [ ] Redis running on port 6379
- [ ] Test connection: `redis-cli ping` returns `PONG`
- [ ] Or: `python test_redis_connection.py` passes

### 3. Environment Configuration
- [ ] `.env` file created in project root
- [ ] `SECRET_KEY` set in .env
- [ ] `DEBUG=True` set in .env
- [ ] `DATABASE_URL` configured (or using default SQLite)
- [ ] `CELERY_BROKER_URL` set to Redis URL
- [ ] `CELERY_RESULT_BACKEND` set to Redis URL

### 4. Database Setup
- [ ] Run migrations: `python manage.py migrate`
- [ ] No migration errors
- [ ] `db.sqlite3` file created (if using SQLite)

### 5. Verification
- [ ] Server starts: `python manage.py runserver`
- [ ] No import errors
- [ ] Server accessible at http://localhost:8000
- [ ] API endpoint responds: `/analytics/blog-views/?object_type=country&range=month`

### 6. Optional: Sample Data
- [ ] Created sample countries
- [ ] Created sample users
- [ ] Created sample blogs
- [ ] Created sample blog views
- [ ] API returns data

### 7. Optional: Celery
- [ ] Celery worker starts without errors
  - Windows: `celery -A ideeza_assessment worker -l info --pool=solo`
  - Linux/Mac: `celery -A ideeza_assessment worker -l info`
- [ ] Celery connects to Redis broker
- [ ] Test task executes successfully

### 8. Testing
- [ ] All tests pass: `python manage.py test analytics.tests`
- [ ] No test failures
- [ ] Service tests pass: `python manage.py test analytics.tests.test_services`
- [ ] View tests pass: `python manage.py test analytics.tests.test_views`

## ✅ API Endpoints Working

Test each endpoint:

### Blog Views Analytics
- [ ] GET `/analytics/blog-views/?object_type=country&range=month`
- [ ] Returns paginated response with count, page, page_size, total_pages, results
- [ ] Results contain x, y, z structure
- [ ] Pagination works: `&page=1&page_size=5`

### Top Analytics
- [ ] GET `/analytics/top/?top=user&range=all`
- [ ] GET `/analytics/top/?top=country&range=month`
- [ ] GET `/analytics/top/?top=blog&range=week`
- [ ] All return paginated responses

### Performance Analytics
- [ ] GET `/analytics/performance/?compare=week`
- [ ] GET `/analytics/performance/?compare=month&user_id=1`
- [ ] Returns paginated response with growth percentages

## ✅ Documentation

- [ ] README.md reviewed
- [ ] QUICKSTART.md reviewed
- [ ] PAGINATION.md reviewed
- [ ] REDIS_SETUP.md reviewed
- [ ] API documentation accessible at `/api/schema/swagger-ui/`

## ✅ Code Quality

- [ ] No Python syntax errors
- [ ] No import errors
- [ ] All migrations applied
- [ ] Tests pass
- [ ] Redis connection working
- [ ] Celery configuration correct

## 🐳 Docker Setup (Alternative)

If using Docker:

- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] `docker-compose up -d` runs successfully
- [ ] All services running: web, db, redis
- [ ] Migrations run: `docker-compose exec web python manage.py migrate`
- [ ] API accessible at http://localhost:8000

## 🚨 Common Issues

### Redis Connection Failed
- [ ] Redis is running: `redis-cli ping`
- [ ] CELERY_BROKER_URL is correct in .env
- [ ] Firewall not blocking port 6379
- [ ] Run: `python test_redis_connection.py`

### Import Errors
- [ ] Virtual environment activated
- [ ] All packages installed: `pip install -r requirements/local.txt`
- [ ] Check for typos in import statements

### Migration Errors
- [ ] Delete db.sqlite3 and retry
- [ ] Check for model conflicts
- [ ] Run: `python manage.py makemigrations` then `migrate`

### Test Failures
- [ ] Redis is running
- [ ] Database is migrated
- [ ] No conflicting data in database
- [ ] Run tests individually to isolate issues

### Celery Won't Start
- [ ] Redis is running
- [ ] Use `--pool=solo` on Windows
- [ ] Check CELERY_BROKER_URL in .env
- [ ] Verify celery package is installed

## 📊 Success Criteria

Your setup is complete when:

1. ✅ Server runs without errors
2. ✅ All three API endpoints return data
3. ✅ Pagination works on all endpoints
4. ✅ All tests pass
5. ✅ Redis connection successful
6. ✅ No import or configuration errors

## 🎉 Next Steps

Once everything is checked:

1. Explore the API endpoints
2. Review the code structure
3. Run tests with coverage
4. Try dynamic filters
5. Test pagination with different page sizes
6. Experiment with Celery tasks
7. Review the senior-level project structure

## 📞 Need Help?

- Check [QUICKSTART.md](QUICKSTART.md) for quick setup
- See [REDIS_SETUP.md](REDIS_SETUP.md) for Redis issues
- Review [README.md](README.md) for detailed documentation
- Run `python test_redis_connection.py` to diagnose Redis issues

---

**Pro Tip:** Use this checklist every time you set up the project on a new machine or after pulling updates!
