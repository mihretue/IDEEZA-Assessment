"""
Analytics Service Layer
Contains business logic for all analytics endpoints
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from django.db.models import Q, Count, F, Case, When, Value, IntegerField
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncYear
from django.utils import timezone
from .models import BlogView, Blog, User, Country


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def apply_dynamic_filters(queryset, filters: Optional[Dict]) -> Any:
    """
    Apply dynamic filters to a queryset using and/or/not/eq operators.
    
    Filter format examples:
    - {"eq": {"field": "value"}}
    - {"and": [filter1, filter2]}
    - {"or": [filter1, filter2]}
    - {"not": filter}
    
    Args:
        queryset: Django queryset to filter
        filters: Dictionary with filter operators and conditions
    
    Returns:
        Filtered queryset
    """
    if not filters:
        return queryset
    
    def parse_filter(filter_dict: Dict) -> Q:
        """Recursively parse filter dictionary into Q objects"""
        if not isinstance(filter_dict, dict):
            raise ValueError("Filter must be a dictionary")
        
        # Handle 'eq' operator
        if 'eq' in filter_dict:
            return Q(**filter_dict['eq'])
        
        # Handle 'and' operator
        if 'and' in filter_dict:
            q = Q()
            for sub_filter in filter_dict['and']:
                q &= parse_filter(sub_filter)
            return q
        
        # Handle 'or' operator
        if 'or' in filter_dict:
            q = Q()
            for sub_filter in filter_dict['or']:
                q |= parse_filter(sub_filter)
            return q
        
        # Handle 'not' operator
        if 'not' in filter_dict:
            return ~parse_filter(filter_dict['not'])
        
        raise ValueError(f"Unknown filter operator in: {filter_dict}")
    
    try:
        q_filter = parse_filter(filters)
        return queryset.filter(q_filter)
    except Exception as e:
        raise ValueError(f"Invalid filter format: {str(e)}")


def get_time_range(range_type: str, start_date: Optional[datetime] = None, 
                   end_date: Optional[datetime] = None) -> tuple:
    """
    Calculate start and end dates for a given range type.
    
    Args:
        range_type: 'day', 'week', 'month', 'year', or 'all'
        start_date: Optional explicit start date
        end_date: Optional explicit end date
    
    Returns:
        Tuple of (start_date, end_date)
    """
    # If both dates provided, use them
    if start_date and end_date:
        return (start_date, end_date)
    
    now = timezone.now()
    
    if range_type == 'all':
        return (None, None)
    
    # Calculate date ranges from now
    if range_type == 'day':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif range_type == 'week':
        start = now - timedelta(days=now.weekday())  # Monday of current week
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    elif range_type == 'month':
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif range_type == 'year':
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError(f"Invalid range_type: {range_type}")
    
    return (start_date or start, end_date or now)


def get_period_label(date: datetime, compare_type: str) -> str:
    """
    Format a date into a period label based on comparison type.
    
    Args:
        date: The date to format
        compare_type: 'day', 'week', 'month', or 'year'
    
    Returns:
        Formatted period label (e.g., '2024-01', '2024-W05', '2024-01-15')
    """
    if compare_type == 'day':
        return date.strftime('%Y-%m-%d')
    elif compare_type == 'week':
        return date.strftime('%Y-W%U')
    elif compare_type == 'month':
        return date.strftime('%Y-%m')
    elif compare_type == 'year':
        return date.strftime('%Y')
    else:
        raise ValueError(f"Invalid compare_type: {compare_type}")


def calculate_growth_percentage(current: int, previous: int) -> float:
    """
    Calculate growth/decline percentage between two periods.
    
    Args:
        current: Current period value
        previous: Previous period value
    
    Returns:
        Percentage change (positive for growth, negative for decline)
    """
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    
    return round(((current - previous) / previous) * 100, 2)


def get_trunc_function(compare_type: str):
    """Get the appropriate Django Trunc function for a comparison type"""
    trunc_map = {
        'day': TruncDay,
        'week': TruncWeek,
        'month': TruncMonth,
        'year': TruncYear
    }
    return trunc_map.get(compare_type)


# ============================================================================
# API #1: BLOG VIEWS ANALYTICS
# ============================================================================

def get_blog_views_analytics(object_type: str, range_type: str = 'month',
                             filters: Optional[Dict] = None,
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> List[Dict]:
    """
    Get blog views analytics grouped by country or user.
    
    Args:
        object_type: 'country' or 'user'
        range_type: 'day', 'week', 'month', or 'year'
        filters: Optional dynamic filters
        start_date: Optional start date
        end_date: Optional end date
    
    Returns:
        List of dicts with x (grouping key), y (blog count), z (total views)
    """
    # Start with base queryset
    queryset = BlogView.objects.all()
    
    # Apply time range filtering
    start, end = get_time_range(range_type, start_date, end_date)
    if start:
        queryset = queryset.filter(viewed_at__gte=start)
    if end:
        queryset = queryset.filter(viewed_at__lte=end)
    
    # Apply dynamic filters
    queryset = apply_dynamic_filters(queryset, filters)
    
    # Group by object_type and aggregate
    if object_type == 'country':
        # Optimize with select_related for foreign keys
        queryset = queryset.select_related('country', 'blog')
        
        results = queryset.values(
            'country__name'
        ).annotate(
            blog_count=Count('blog__id', distinct=True),
            view_count=Count('id')
        ).order_by('-view_count')
        
        return [
            {
                'x': item['country__name'] or 'Unknown',
                'y': item['blog_count'],
                'z': item['view_count']
            }
            for item in results
        ]
    
    elif object_type == 'user':
        # Optimize with select_related for foreign keys
        queryset = queryset.select_related('user', 'blog')
        
        results = queryset.values(
            'user__username'
        ).annotate(
            blog_count=Count('blog__id', distinct=True),
            view_count=Count('id')
        ).order_by('-view_count')
        
        return [
            {
                'x': item['user__username'] or 'Anonymous',
                'y': item['blog_count'],
                'z': item['view_count']
            }
            for item in results
        ]
    
    else:
        raise ValueError(f"Invalid object_type: {object_type}. Must be 'country' or 'user'")


# ============================================================================
# API #2: TOP ANALYTICS
# ============================================================================

def get_top_analytics(top: str, range_type: str = 'all',
                     filters: Optional[Dict] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[Dict]:
    """
    Get top 10 rankings by user, country, or blog based on total views.
    
    Args:
        top: 'user', 'country', or 'blog'
        range_type: 'day', 'week', 'month', 'year', or 'all'
        filters: Optional dynamic filters
        start_date: Optional start date
        end_date: Optional end date
    
    Returns:
        List of dicts with x, y, z (structure varies by top type)
    """
    # Base queryset for BlogView
    view_queryset = BlogView.objects.all()
    
    # Apply time range filtering
    start, end = get_time_range(range_type, start_date, end_date)
    if start:
        view_queryset = view_queryset.filter(viewed_at__gte=start)
    if end:
        view_queryset = view_queryset.filter(viewed_at__lte=end)
    
    # Apply dynamic filters
    view_queryset = apply_dynamic_filters(view_queryset, filters)
    
    if top == 'user':
        # Top 10 users by blog authorship views
        # x = username, y = blog_count, z = total_views
        results = view_queryset.select_related(
            'blog__author'
        ).values(
            'blog__author__username'
        ).annotate(
            blog_count=Count('blog__id', distinct=True),
            total_views=Count('id')
        ).order_by('-total_views')[:10]
        
        return [
            {
                'x': item['blog__author__username'] or 'Unknown',
                'y': str(item['blog_count']),
                'z': item['total_views']
            }
            for item in results
        ]
    
    elif top == 'country':
        # Top 10 countries by views
        # x = country_name, y = blog_count, z = total_views
        results = view_queryset.select_related(
            'country'
        ).values(
            'country__name'
        ).annotate(
            blog_count=Count('blog__id', distinct=True),
            total_views=Count('id')
        ).order_by('-total_views')[:10]
        
        return [
            {
                'x': item['country__name'] or 'Unknown',
                'y': str(item['blog_count']),
                'z': item['total_views']
            }
            for item in results
        ]
    
    elif top == 'blog':
        # Top 10 blogs by views
        # x = blog_title, y = author_username, z = total_views
        results = view_queryset.select_related(
            'blog__author'
        ).values(
            'blog__title',
            'blog__author__username'
        ).annotate(
            total_views=Count('id')
        ).order_by('-total_views')[:10]
        
        return [
            {
                'x': item['blog__title'],
                'y': item['blog__author__username'] or 'Unknown',
                'z': item['total_views']
            }
            for item in results
        ]
    
    else:
        raise ValueError(f"Invalid top type: {top}. Must be 'user', 'country', or 'blog'")


# ============================================================================
# API #3: PERFORMANCE ANALYTICS
# ============================================================================

def get_performance_analytics(compare: str, user_id: Optional[int] = None,
                              filters: Optional[Dict] = None,
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None) -> List[Dict]:
    """
    Get time-series performance analytics for a user or all users.
    
    Args:
        compare: 'day', 'week', 'month', or 'year'
        user_id: Optional specific user ID (None for all users)
        filters: Optional dynamic filters
        start_date: Optional start date
        end_date: Optional end date
    
    Returns:
        List of dicts with x (period label + blog count), y (views), z (growth %)
    """
    # Get truncation function for period grouping
    trunc_func = get_trunc_function(compare)
    if not trunc_func:
        raise ValueError(f"Invalid compare type: {compare}")
    
    # Base queryset
    blog_queryset = Blog.objects.all()
    view_queryset = BlogView.objects.all()
    
    # Filter by user if specified
    if user_id:
        blog_queryset = blog_queryset.filter(author_id=user_id)
        view_queryset = view_queryset.filter(blog__author_id=user_id)
    
    # Apply time range
    if not start_date and not end_date:
        # Default to last 12 periods
        now = timezone.now()
        if compare == 'day':
            start_date = now - timedelta(days=30)
        elif compare == 'week':
            start_date = now - timedelta(weeks=12)
        elif compare == 'month':
            start_date = now - timedelta(days=365)
        elif compare == 'year':
            start_date = now - timedelta(days=365 * 3)
    
    if start_date:
        blog_queryset = blog_queryset.filter(created_at__gte=start_date)
        view_queryset = view_queryset.filter(viewed_at__gte=start_date)
    if end_date:
        blog_queryset = blog_queryset.filter(created_at__lte=end_date)
        view_queryset = view_queryset.filter(viewed_at__lte=end_date)
    
    # Apply dynamic filters to views (not blogs, to avoid model context mismatch)
    view_queryset = apply_dynamic_filters(view_queryset, filters)
    
    # Get blog counts per period
    blog_stats = blog_queryset.annotate(
        period=trunc_func('created_at')
    ).values('period').annotate(
        blog_count=Count('id')
    ).order_by('period')
    
    # Get view counts per period (with select_related optimization)
    view_queryset = view_queryset.select_related('blog')
    view_stats = view_queryset.annotate(
        period=trunc_func('viewed_at')
    ).values('period').annotate(
        view_count=Count('id')
    ).order_by('period')
    
    # Merge blog and view stats by period
    period_map = {}
    
    for item in blog_stats:
        period = item['period']
        if period:
            period_map[period] = {
                'blog_count': item['blog_count'],
                'view_count': 0
            }
    
    for item in view_stats:
        period = item['period']
        if period:
            if period not in period_map:
                period_map[period] = {'blog_count': 0, 'view_count': 0}
            period_map[period]['view_count'] = item['view_count']
    
    # Sort periods and calculate growth
    sorted_periods = sorted(period_map.keys())
    results = []
    previous_views = 0
    
    for period in sorted_periods:
        data = period_map[period]
        current_views = data['view_count']
        growth = calculate_growth_percentage(current_views, previous_views)
        
        period_label = get_period_label(period, compare)
        blog_count = data['blog_count']
        
        results.append({
            'x': f"{period_label} ({blog_count} blogs)",
            'y': current_views,
            'z': growth
        })
        
        previous_views = current_views
    
    return results
