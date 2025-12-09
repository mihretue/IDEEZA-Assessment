"""
Analytics API Views
Expose analytics services through REST API endpoints
"""
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .services import (
    get_blog_views_analytics,
    get_top_analytics,
    get_performance_analytics
)
from .serializers import (
    BlogViewsAnalyticsSerializer,
    BlogViewsRequestSerializer,
    TopAnalyticsSerializer,
    TopAnalyticsRequestSerializer,
    PerformanceAnalyticsSerializer,
    PerformanceRequestSerializer,
    ErrorResponseSerializer,
    PaginatedResponseSerializer
)


def paginate_results(results, page, page_size):
    """
    Helper function to paginate results
    
    Args:
        results: List of results to paginate
        page: Current page number (1-indexed)
        page_size: Number of items per page
    
    Returns:
        Dictionary with pagination metadata and paginated results
    """
    total_count = len(results)
    total_pages = math.ceil(total_count / page_size) if page_size > 0 else 0
    
    # Calculate start and end indices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    # Get paginated results
    paginated_results = results[start_idx:end_idx]
    
    return {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'results': paginated_results
    }


class BlogViewsAnalyticsView(APIView):
    """
    API #1: Blog Views Analytics
    
    Group blogs and views by country or user with time range filtering.
    
    Query Parameters:
    - object_type (required): 'country' or 'user'
    - range: 'day', 'week', 'month', or 'year' (default: 'month')
    - start_date: ISO 8601 format (optional)
    - end_date: ISO 8601 format (optional)
    - filters: JSON object with dynamic filters (optional)
    
    Response: List of {x: grouping_key, y: blog_count, z: total_views}
    """
    
    @extend_schema(
        parameters=[BlogViewsRequestSerializer],
        responses={
            200: PaginatedResponseSerializer,
            400: ErrorResponseSerializer
        }
    )
    def get(self, request):
        # Validate request parameters
        serializer = BlogViewsRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid parameters', 'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        try:
            # Call service layer
            results = get_blog_views_analytics(
                object_type=validated_data['object_type'],
                range_type=validated_data.get('range', 'month'),
                filters=validated_data.get('filters'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date')
            )
            
            # Serialize results
            response_serializer = BlogViewsAnalyticsSerializer(results, many=True)
            
            # Paginate results
            page = validated_data.get('page', 1)
            page_size = validated_data.get('page_size', 10)
            paginated_data = paginate_results(response_serializer.data, page, page_size)
            
            return Response(paginated_data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {'error': 'Invalid filter or parameter', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TopAnalyticsView(APIView):
    """
    API #2: Top Analytics
    
    Get Top 10 users, countries, or blogs by total views.
    
    Query Parameters:
    - top (required): 'user', 'country', or 'blog'
    - range: 'day', 'week', 'month', 'year', or 'all' (default: 'all')
    - start_date: ISO 8601 format (optional)
    - end_date: ISO 8601 format (optional)
    - filters: JSON object with dynamic filters (optional)
    
    Response structure varies by 'top' type:
    - user: {x: username, y: blog_count, z: total_views}
    - country: {x: country_name, y: blog_count, z: total_views}
    - blog: {x: blog_title, y: author_username, z: total_views}
    """
    
    @extend_schema(
        parameters=[TopAnalyticsRequestSerializer],
        responses={
            200: PaginatedResponseSerializer,
            400: ErrorResponseSerializer
        }
    )
    def get(self, request):
        # Validate request parameters
        serializer = TopAnalyticsRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid parameters', 'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        try:
            # Call service layer
            results = get_top_analytics(
                top=validated_data['top'],
                range_type=validated_data.get('range', 'all'),
                filters=validated_data.get('filters'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date')
            )
            
            # Serialize results
            response_serializer = TopAnalyticsSerializer(results, many=True)
            
            # Paginate results
            page = validated_data.get('page', 1)
            page_size = validated_data.get('page_size', 10)
            paginated_data = paginate_results(response_serializer.data, page, page_size)
            
            return Response(paginated_data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {'error': 'Invalid filter or parameter', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PerformanceAnalyticsView(APIView):
    """
    API #3: Performance Analytics
    
    Get time-series performance for a user or all users with period-over-period comparison.
    
    Query Parameters:
    - compare (required): 'day', 'week', 'month', or 'year'
    - user_id: Specific user ID (optional, omit for all users)
    - start_date: ISO 8601 format (optional)
    - end_date: ISO 8601 format (optional)
    - filters: JSON object with dynamic filters (optional)
    
    Response: List of {x: period_label (blog_count), y: views, z: growth_%}
    """
    
    @extend_schema(
        parameters=[PerformanceRequestSerializer],
        responses={
            200: PaginatedResponseSerializer,
            400: ErrorResponseSerializer
        }
    )
    def get(self, request):
        # Validate request parameters
        serializer = PerformanceRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid parameters', 'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        try:
            # Call service layer
            results = get_performance_analytics(
                compare=validated_data['compare'],
                user_id=validated_data.get('user_id'),
                filters=validated_data.get('filters'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date')
            )
            
            # Serialize results
            response_serializer = PerformanceAnalyticsSerializer(results, many=True)
            
            # Paginate results
            page = validated_data.get('page', 1)
            page_size = validated_data.get('page_size', 10)
            paginated_data = paginate_results(response_serializer.data, page, page_size)
            
            return Response(paginated_data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {'error': 'Invalid filter or parameter', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
