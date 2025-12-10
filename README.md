# IDEEZA Backend Developer Assessment

Advanced analytics APIs built with Django REST Framework, featuring dynamic filtering, pagination, and optimized database queries.

> **Installation:** See [INSTALLATION.md](INSTALLATION.md) for complete setup instructions.

---

## 🎯 Features

- **3 Analytics APIs** with complex aggregation and time-series analysis
- **Interactive API Documentation** (Swagger UI / ReDoc)
- **Pagination Support** with count, page, page_size, and total_pages metadata
- **Dynamic Filter System** supporting `and`, `or`, `not`, and `eq` operators
- **ORM Optimization** using `select_related`, `prefetch_related`, and efficient aggregation
- **Comprehensive Tests** covering services, views, and edge cases
- **N+1 Query Prevention** through strategic database query optimization
- **Senior-Level Architecture** with split settings, Celery integration, and Docker support

---

## 📋 API Endpoints

### 1. Blog Views Analytics - `/analytics/blog-views/`

Groups blogs and views by country or user with time range filtering.

**Query Parameters:**
- `object_type` (required): `country` or `user`
- `range` (optional): `day`, `week`, `month`, or `year` (default: `month`)
- `start_date` (optional): ISO 8601 format
- `end_date` (optional): ISO 8601 format
- `filters` (optional): JSON object with dynamic filters
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10, max: 100)

**Response Structure:**
```json
{
  "count": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3,
  "results": [
    {
      "x": "USA",
      "y": 15,
      "z": 245
    }
  ]
}
```

**Example Requests:**
```bash
# Group by country for the current month
GET /analytics/blog-views/?object_type=country&range=month

# Group by user with pagination
GET /analytics/blog-views/?object_type=user&range=week&page=1&page_size=20

# With dynamic filters
GET /analytics/blog-views/?object_type=country&filters={"eq":{"country__name":"USA"}}
```

---

### 2. Top Analytics - `/analytics/top/`

Returns Top 10 users, countries, or blogs based on total views.

**Query Parameters:**
- `top` (required): `user`, `country`, or `blog`
- `range` (optional): `day`, `week`, `month`, `year`, or `all` (default: `all`)
- `start_date` (optional): ISO 8601 format
- `end_date` (optional): ISO 8601 format
- `filters` (optional): JSON object with dynamic filters
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10, max: 100)

**Response Structure:**
```json
{
  "count": 50,
  "page": 1,
  "page_size": 10,
  "total_pages": 5,
  "results": [
    {
      "x": "john_doe",
      "y": "25",
      "z": 1532
    }
  ]
}
```

**Response data varies by `top` parameter:**
- **top=user:** `{x: username, y: blog_count, z: total_views}`
- **top=country:** `{x: country_name, y: blog_count, z: total_views}`
- **top=blog:** `{x: blog_title, y: author_username, z: total_views}`

**Example Requests:**
```bash
# Top 10 users (all time)
GET /analytics/top/?top=user&range=all

# Top 10 countries (this month)
GET /analytics/top/?top=country&range=month

# Top 10 blogs with pagination
GET /analytics/top/?top=blog&range=week&page=1&page_size=5
```

---

### 3. Performance Analytics - `/analytics/performance/`

Time-series performance with period-over-period growth analysis.

**Query Parameters:**
- `compare` (required): `day`, `week`, `month`, or `year`
- `user_id` (optional): Specific user ID (omit for all users)
- `start_date` (optional): ISO 8601 format
- `end_date` (optional): ISO 8601 format
- `filters` (optional): JSON object with dynamic filters
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10, max: 100)

**Response Structure:**
```json
{
  "count": 12,
  "page": 1,
  "page_size": 10,
  "total_pages": 2,
  "results": [
    {
      "x": "2024-01 (15 blogs)",
      "y": 423,
      "z": 12.5
    }
  ]
}
```

**Example Requests:**
```bash
# Monthly performance for all users
GET /analytics/performance/?compare=month

# Weekly performance for specific user
GET /analytics/performance/?compare=week&user_id=5

# Daily performance with pagination
GET /analytics/performance/?compare=day&page=1&page_size=15
```

---

## 📖 API Documentation

Interactive API documentation is available:

- **Swagger UI:** http://localhost:8000/api/docs/ (Interactive testing)
- **ReDoc:** http://localhost:8000/api/redoc/ (Clean documentation)
- **OpenAPI Schema:** http://localhost:8000/api/schema/ (JSON schema)

---

## 🔍 Dynamic Filters

All endpoints support dynamic filtering with JSON-based filters.

**Operators:**
- `eq` - Equality check
- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT

**Examples:**

**Simple equality:**
```json
{"eq": {"country__name": "USA"}}
```

**AND operator:**
```json
{
  "and": [
    {"eq": {"blog__author__username": "john"}},
    {"eq": {"country__code": "US"}}
  ]
}
```

**OR operator:**
```json
{
  "or": [
    {"eq": {"country__name": "USA"}},
    {"eq": {"country__name": "Canada"}}
  ]
}
```

**NOT operator:**
```json
{"not": {"eq": {"blog__title": "Exclude This"}}}
```

**Nested filters:**
```json
{
  "and": [
    {
      "or": [
        {"eq": {"country__name": "USA"}},
        {"eq": {"country__name": "Canada"}}
      ]
    },
    {"not": {"eq": {"blog__author__username": "spammer"}}}
  ]
}
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements/local.txt

# 2. Run migrations
python manage.py migrate

# 3. Seed database
python seed_quick.py

# 4. Start server
python manage.py runserver

# 5. Open Swagger UI
# http://localhost:8000/api/docs/
```

**For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)**

### Run Tests

```bash
# Run all tests
python manage.py test analytics.tests

# Run with coverage
coverage run --source='analytics' manage.py test analytics.tests
coverage report
```

---

## 🏗️ Architecture

### Service Layer Pattern

- **`models.py`** - Data models (User, Country, Blog, BlogView)
- **`services.py`** - Business logic and analytics functions
- **`views.py`** - HTTP request/response handling
- **`serializers.py`** - Request validation and response serialization
- **`tests/`** - Comprehensive test coverage

### Database Optimization

**Preventing N+1 Queries:**
- `select_related()` for forward foreign keys
- `prefetch_related()` for reverse foreign keys
- Strategic use of `values()` and `annotate()`
- Database indexes on frequently queried fields

**Example:**
```python
queryset = BlogView.objects.select_related(
    'country',
    'blog',
    'blog__author'
).values('country__name').annotate(
    blog_count=Count('blog__id', distinct=True),
    view_count=Count('id')
)
```

### Infrastructure

- **Redis:** Celery message broker, result backend, and Django caching
- **Celery:** Async task processing and scheduled jobs
- **PostgreSQL/SQLite:** Primary database
- **Docker:** Containerized deployment

---

## 📁 Project Structure

```
IDEEZA-Assessment/
├── analytics/
│   ├── management/commands/
│   │   └── seed_data.py
│   ├── tests/
│   │   ├── test_services.py
│   │   └── test_views.py
│   ├── models.py
│   ├── services.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── ideeza_assessment/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── celery.py
│   └── urls.py
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── .env
├── docker-compose.yml
├── manage.py
├── seed_quick.py
├── verify_setup.py
├── INSTALLATION.md
└── README.md
```

---

## 🎓 Technical Highlights

1. **Dynamic Filtering System** - Recursive Q object builder supporting complex filter combinations
2. **Pagination** - Built-in pagination with count and metadata for all endpoints
3. **Time-Series Analytics** - Period-based aggregation with growth calculations
4. **ORM Optimization** - Strategic use of select_related/prefetch_related
5. **Comprehensive Testing** - Unit tests, integration tests, edge cases, pagination tests
6. **Clean Architecture** - Service layer pattern for maintainability
7. **Type Safety** - Request validation with DRF serializers
8. **Senior-Level Structure** - Split settings, organized requirements, Celery integration
9. **Environment Management** - Separate configurations for local/production environments

---

## 📝 Requirements Met

✅ Three analytics APIs with x, y, z output structure  
✅ Pagination with count and metadata on all endpoints  
✅ Dynamic filtering with and/or/not/eq operators  
✅ Multi-table filtering support  
✅ Time-series aggregation and comparison  
✅ Efficient Django ORM usage  
✅ N+1 query prevention  
✅ Comprehensive test coverage  
✅ Clean service layer architecture  
✅ Full documentation with examples  
✅ Senior-level project structure  
✅ Split settings (base/local/production)  
✅ Organized requirements directory  
✅ Celery integration for async tasks  
✅ Organized test suite structure  
✅ Interactive API documentation (Swagger/ReDoc)

---

## 👤 Author

**Backend Developer Assessment**  
IDEEZA - Senior Backend Developer Position

---

## 📄 License

This project is created for assessment purposes.
