"""
Analytics URL Configuration
"""
from django.urls import path
from .views import (
    BlogViewsAnalyticsView,
    TopAnalyticsView,
    PerformanceAnalyticsView
)

app_name = 'analytics'

urlpatterns = [
    path('blog-views/', BlogViewsAnalyticsView.as_view(), name='blog-views'),
    path('top/', TopAnalyticsView.as_view(), name='top'),
    path('performance/', PerformanceAnalyticsView.as_view(), name='performance'),
]
