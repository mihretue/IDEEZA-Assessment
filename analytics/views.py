"""
Analytics API Views
Expose analytics services through REST API endpoints
"""
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
    ErrorResponseSerializer
)


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
            200: BlogViewsAnalyticsSerializer(many=True),
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
            
            # Serialize and return response
            response_serializer = BlogViewsAnalyticsSerializer(results, many=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
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
            200: TopAnalyticsSerializer(many=True),
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
            
            # Serialize and return response
            response_serializer = TopAnalyticsSerializer(results, many=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
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
            200: PerformanceAnalyticsSerializer(many=True),
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
            
            # Serialize and return response
            response_serializer = PerformanceAnalyticsSerializer(results, many=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
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
