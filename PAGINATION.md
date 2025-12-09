# Pagination Feature

## Overview

All analytics API endpoints now support pagination with comprehensive metadata.

## Response Format

Every API endpoint returns a paginated response with the following structure:

```json
{
  "count": 25,           // Total number of results
  "page": 1,             // Current page number
  "page_size": 10,       // Items per page
  "total_pages": 3,      // Total number of pages
  "results": [...]       // Array of results for current page
}
```

## Query Parameters

All endpoints accept these pagination parameters:

- `page` (optional): Page number, starting from 1 (default: 1)
- `page_size` (optional): Number of items per page (default: 10, max: 100)

## Examples

### Blog Views Analytics

```bash
# Get first page with 10 items (default)
GET /analytics/blog-views/?object_type=country&range=month

# Get second page with 20 items per page
GET /analytics/blog-views/?object_type=country&range=month&page=2&page_size=20

# Get first page with maximum items
GET /analytics/blog-views/?object_type=user&range=week&page=1&page_size=100
```

### Top Analytics

```bash
# Get top users with default pagination
GET /analytics/top/?top=user&range=all

# Get top countries with custom page size
GET /analytics/top/?top=country&range=month&page=1&page_size=5

# Get second page of top blogs
GET /analytics/top/?top=blog&range=week&page=2&page_size=10
```

### Performance Analytics

```bash
# Get performance data with default pagination
GET /analytics/performance/?compare=month

# Get specific page with custom size
GET /analytics/performance/?compare=week&user_id=5&page=1&page_size=15

# Navigate through pages
GET /analytics/performance/?compare=day&page=3&page_size=20
```

## Implementation Details

### Backend

- **Helper Function**: `paginate_results()` in `analytics/views.py`
- **Serializer**: `PaginatedResponseSerializer` for response validation
- **Request Validation**: All request serializers include `page` and `page_size` fields

### Features

- Automatic calculation of `total_pages` based on count and page_size
- Validation: page must be >= 1, page_size must be 1-100
- Empty results handling: Returns empty array with count=0
- Out of range pages: Returns empty results array

### Tests

Comprehensive pagination tests added to `analytics/tests/test_views.py`:

- `test_api_pagination()` for each endpoint
- Validates pagination metadata in responses
- Ensures results array length respects page_size

## Benefits

1. **Performance**: Reduces payload size for large result sets
2. **User Experience**: Enables progressive loading in frontend applications
3. **Flexibility**: Configurable page size up to 100 items
4. **Metadata**: Complete information for building pagination UI
5. **Consistency**: Same pagination structure across all endpoints
