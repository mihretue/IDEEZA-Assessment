# IDEEZA Backend Developer Assessment

Advanced analytics APIs built with Django REST Framework, featuring dynamic filtering and optimized database queries.

## 🎯 Features

- **3 Analytics APIs** with complex aggregation and time-series analysis
- **Dynamic Filter System** supporting `and`, `or`, `not`, and `eq` operators
- **ORM Optimization** using `select_related`, `prefetch_related`, and efficient aggregation
- **Comprehensive Tests** covering services, views, and edge cases
- **N+1 Query Prevention** through strategic database query optimization

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

**Response Structure:**

```json
[
  {
    "x": "USA",           // Grouping key (country name or username)
    "y": 15,              // Number of blogs
    "z": 245              // Total views
  }
]
```

**Example Requests:**

```bash
# Group by country for the current month
GET /analytics/blog-views/?object_type=country&range=month

# Group by user for the current week
GET /analytics/blog-views/?object_type=user&range=week

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

**Response Structure varies by `top` parameter:**

**top=user:**

```json
[
  {
    "x": "john_doe",      // Username
    "y": "25",            // Blog count (string)
    "z": 1532             // Total views
  }
]
```

**top=country:**

```json
[
  {
    "x": "USA",           // Country name
    "y": "142",           // Blog count (string)
    "z": 5423             // Total views
  }
]
```

**top=blog:**

```json
[
  {
    "x": "My Awesome Blog", // Blog title
    "y": "jane_smith",      // Author username
    "z": 892                // Total views
  }
]
```

**Example Requests:**

```bash
# Top 10 users (all time)
GET /analytics/top/?top=user&range=all

# Top 10 countries (this month)
GET /analytics/top/?top=country&range=month

# Top 10 blogs (this week)
GET /analytics/top/?top=blog&range=week
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

**Response Structure:**

```json
[
  {
    "x": "2024-01 (15 blogs)",  // Period label with blog count
    "y": 423,                    // Views during period
    "z": 12.5                    // Growth percentage vs previous period
  }
]
```

**Example Requests:**

```bash
# Monthly performance for all users
GET /analytics/performance/?compare=month

# Weekly performance for specific user
GET /analytics/performance/?compare=week&user_id=5

# Daily performance with date range
GET /analytics/performance/?compare=day&start_date=2024-01-01&end_date=2024-01-31
```

---

## 🔍 Dynamic Filters

All endpoints support dynamic filtering with JSON-based filters.

**Operators:**

- `eq` - Equality check
- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT

**Filter Examples:**

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

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps

1. **Clone the repository:**

```bash
git clone <repository-url>
cd IDEEZA-Assessment
```

2. **Create and activate virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run migrations:**

```bash
python manage.py migrate
```

5. **Create sample data (optional):**

```bash
python manage.py shell
```

```python
from analytics.models import User, Country, Blog, BlogView
from django.utils import timezone
import random

# Create countries
countries = [
    Country.objects.create(name="USA", code="US"),
    Country.objects.create(name="Canada", code="CA"),
    Country.objects.create(name="UK", code="GB"),
    Country.objects.create(name="Germany", code="DE"),
]

# Create users
users = []
for i in range(10):
    user = User.objects.create(
        username=f"user{i}",
        email=f"user{i}@example.com"
    )
    users.append(user)

# Create blogs
blogs = []
for user in users:
    for j in range(random.randint(2, 8)):
        blog = Blog.objects.create(
            title=f"{user.username}'s Blog {j}",
            content=f"Content for blog {j}",
            author=user,
            country=random.choice(countries)
        )
        blogs.append(blog)

# Create views
for blog in blogs:
    view_count = random.randint(5, 50)
    for _ in range(view_count):
        BlogView.objects.create(
            blog=blog,
            user=random.choice(users),
            country=random.choice(countries)
        )

print(f"Created {len(users)} users, {len(blogs)} blogs, and {BlogView.objects.count()} views")
```

6. **Run development server:**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/analytics/`

---

## 🧪 Testing

### Run all tests:

```bash
python manage.py test analytics
```

### Run specific test classes:

```bash
# Service layer tests
python manage.py test analytics.tests.TestBlogViewsAnalyticsService
python manage.py test analytics.tests.TestTopAnalyticsService
python manage.py test analytics.tests.TestPerformanceAnalyticsService

# Dynamic filter tests
python manage.py test analytics.tests.TestDynamicFilters

# API endpoint tests
python manage.py test analytics.tests.TestBlogViewsAnalyticsView
python manage.py test analytics.tests.TestTopAnalyticsView
python manage.py test analytics.tests.TestPerformanceAnalyticsView
```

### Test with coverage:

```bash
pip install coverage
coverage run --source='analytics' manage.py test analytics
coverage report
```

---

## 🏗️ Architecture

### Service Layer Pattern

The project uses a **service layer architecture** to separate business logic from views:

- **`models.py`** - Data models (User, Country, Blog, BlogView)
- **`services.py`** - Business logic and analytics functions
- **`views.py`** - HTTP request/response handling
- **`serializers.py`** - Request validation and response serialization
- **`tests.py`** - Comprehensive test coverage

### Database Optimization

**Preventing N+1 Queries:**

- `select_related()` for forward foreign keys
- `prefetch_related()` for reverse foreign keys
- Strategic use of `values()` and `annotate()`
- Database indexes on frequently queried fields

**Example from `services.py`:**

```python
queryset = BlogView.objects.select_related(
    'country',        # Joins Country table
    'blog',           # Joins Blog table
    'blog__author'    # Joins User table through Blog
).values('country__name').annotate(
    blog_count=Count('blog__id', distinct=True),
    view_count=Count('id')
)
```

---

## 📁 Project Structure

```
IDEEZA-Assessment/
├── analytics/
│   ├── models.py           # Database models
│   ├── services.py         # Business logic layer
│   ├── views.py            # API views
│   ├── serializers.py      # Request/response serializers
│   ├── urls.py             # Analytics URL routing
│   ├── tests.py            # Comprehensive tests
│   └── admin.py            # Django admin configuration
├── ideeza_assessment/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── db.sqlite3              # SQLite database
└── README.md               # This file
```

---

## 🎓 Technical Highlights

1. **Dynamic Filtering System** - Recursive Q object builder supporting complex filter combinations
2. **Time-Series Analytics** - Period-based aggregation with growth calculations
3. **ORM Optimization** - Strategic use of select_related/prefetch_related
4. **Comprehensive Testing** - Unit tests, integration tests, edge cases
5. **Clean Architecture** - Service layer pattern for maintainability
6. **Type Safety** - Request validation with DRF serializers

---

## 📝 Requirements Met

✅ Three analytics APIs with x, y, z output structure  
✅ Dynamic filtering with and/or/not/eq operators  
✅ Multi-table filtering support  
✅ Time-series aggregation and comparison  
✅ Efficient Django ORM usage  
✅ N+1 query prevention  
✅ Comprehensive test coverage  
✅ Clean service layer architecture  
✅ Full documentation with examples

---

## 👤 Author

**Backend Developer Assessment**  
IDEEZA - Senior Backend Developer Position

---

## 📄 License

This project is created for assessment purposes.
