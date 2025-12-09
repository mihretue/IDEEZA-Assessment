from rest_framework import serializers


class PaginatedResponseSerializer(serializers.Serializer):
    """
    Wrapper for paginated responses with count and results
    """
    count = serializers.IntegerField(help_text="Total number of results")
    page = serializers.IntegerField(help_text="Current page number")
    page_size = serializers.IntegerField(help_text="Number of items per page")
    total_pages = serializers.IntegerField(help_text="Total number of pages")
    results = serializers.ListField(help_text="Paginated results")


class BlogViewsAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for API #1: /analytics/blog-views/
    Returns x, y, z structure for grouped blog views
    """
    x = serializers.CharField(help_text="Grouping key (user or country identifier)")
    y = serializers.IntegerField(help_text="Number of blogs")
    z = serializers.IntegerField(help_text="Total views")


class TopAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for API #2: /analytics/top/
    Returns x, y, z structure for top 10 rankings
    x, y, z meanings vary based on 'top' parameter
    """
    x = serializers.CharField(help_text="Primary identifier (username, country name, or blog title)")
    y = serializers.CharField(help_text="Secondary data (blog count or author name)")
    z = serializers.IntegerField(help_text="Total views")


class PerformanceAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for API #3: /analytics/performance/
    Returns x, y, z structure for time-series performance
    """
    x = serializers.CharField(help_text="Period label with blog count (e.g., '2024-01 (5 blogs)')")
    y = serializers.IntegerField(help_text="Views during the period")
    z = serializers.FloatField(help_text="Growth/decline percentage vs previous period")


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""
    error = serializers.CharField()
    detail = serializers.CharField(required=False)


class FilterRequestSerializer(serializers.Serializer):
    """
    Serializer to validate filter query parameters
    Supports: and, or, not, eq operators
    """
    filters = serializers.JSONField(
        required=False,
        help_text="Dynamic filters in JSON format. Supports 'and', 'or', 'not', 'eq' operators"
    )


class BlogViewsRequestSerializer(serializers.Serializer):
    """Request parameter validation for blog-views endpoint"""
    object_type = serializers.ChoiceField(
        choices=['country', 'user'],
        required=True,
        help_text="Group by country or user"
    )
    range = serializers.ChoiceField(
        choices=['month', 'week', 'year', 'day'],
        required=False,
        default='month',
        help_text="Time range for filtering"
    )
    filters = serializers.JSONField(
        required=False,
        help_text="Dynamic filters in JSON format"
    )
    start_date = serializers.DateTimeField(
        required=False,
        help_text="Start date for time range (ISO 8601 format)"
    )
    end_date = serializers.DateTimeField(
        required=False,
        help_text="End date for time range (ISO 8601 format)"
    )
    page = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        help_text="Page number (default: 1)"
    )
    page_size = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=100,
        help_text="Items per page (default: 10, max: 100)"
    )


class TopAnalyticsRequestSerializer(serializers.Serializer):
    """Request parameter validation for top analytics endpoint"""
    top = serializers.ChoiceField(
        choices=['user', 'country', 'blog'],
        required=True,
        help_text="Get top 10 by user, country, or blog"
    )
    range = serializers.ChoiceField(
        choices=['month', 'week', 'year', 'day', 'all'],
        required=False,
        default='all',
        help_text="Time range for filtering"
    )
    filters = serializers.JSONField(
        required=False,
        help_text="Dynamic filters in JSON format"
    )
    start_date = serializers.DateTimeField(
        required=False,
        help_text="Start date for time range (ISO 8601 format)"
    )
    end_date = serializers.DateTimeField(
        required=False,
        help_text="End date for time range (ISO 8601 format)"
    )
    page = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        help_text="Page number (default: 1)"
    )
    page_size = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=100,
        help_text="Items per page (default: 10, max: 100)"
    )


class PerformanceRequestSerializer(serializers.Serializer):
    """Request parameter validation for performance endpoint"""
    compare = serializers.ChoiceField(
        choices=['month', 'week', 'day', 'year'],
        required=True,
        help_text="Compare performance by time period"
    )
    user_id = serializers.IntegerField(
        required=False,
        help_text="Specific user ID (omit for all users)"
    )
    filters = serializers.JSONField(
        required=False,
        help_text="Dynamic filters in JSON format"
    )
    start_date = serializers.DateTimeField(
        required=False,
        help_text="Start date for analysis (ISO 8601 format)"
    )
    end_date = serializers.DateTimeField(
        required=False,
        help_text="End date for analysis (ISO 8601 format)"
    )
    page = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        help_text="Page number (default: 1)"
    )
    page_size = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=100,
        help_text="Items per page (default: 10, max: 100)"
    )
