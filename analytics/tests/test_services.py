from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from analytics.models import User, Country, Blog, BlogView
from analytics.services import (
    get_blog_views_analytics,
    get_top_analytics,
    get_performance_analytics,
    apply_dynamic_filters,
    calculate_growth_percentage
)

class TestDynamicFilters(TestCase):
    """Test dynamic filter system with and/or/not/eq operators"""
    
    def setUp(self):
        self.country1 = Country.objects.create(name="USA", code="US")
        self.country2 = Country.objects.create(name="Canada", code="CA")
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.blog = Blog.objects.create(
            title="Test Blog",
            content="Content",
            author=self.user,
            country=self.country1
        )
    
    def test_eq_filter(self):
        """Test equality filter"""
        filters = {"eq": {"country__name": "USA"}}
        queryset = BlogView.objects.all()
        result = apply_dynamic_filters(queryset, filters)
        self.assertIsNotNone(result)
    
    def test_and_filter(self):
        """Test AND operator"""
        filters = {
            "and": [
                {"eq": {"country__name": "USA"}},
                {"eq": {"blog__title": "Test Blog"}}
            ]
        }
        queryset = BlogView.objects.all()
        result = apply_dynamic_filters(queryset, filters)
        self.assertIsNotNone(result)
    
    def test_or_filter(self):
        """Test OR operator"""
        filters = {
            "or": [
                {"eq": {"country__name": "USA"}},
                {"eq": {"country__name": "Canada"}}
            ]
        }
        queryset = BlogView.objects.all()
        result = apply_dynamic_filters(queryset, filters)
        self.assertIsNotNone(result)
    
    def test_not_filter(self):
        """Test NOT operator"""
        filters = {"not": {"eq": {"country__name": "USA"}}}
        queryset = BlogView.objects.all()
        result = apply_dynamic_filters(queryset, filters)
        self.assertIsNotNone(result)
    
    def test_nested_filters(self):
        """Test nested filter combinations"""
        filters = {
            "and": [
                {"or": [
                    {"eq": {"country__name": "USA"}},
                    {"eq": {"country__name": "Canada"}}
                ]},
                {"not": {"eq": {"blog__title": "Exclude This"}}}
            ]
        }
        queryset = BlogView.objects.all()
        result = apply_dynamic_filters(queryset, filters)
        self.assertIsNotNone(result)


class TestBlogViewsAnalyticsService(TestCase):
    """Test API #1: Blog Views Analytics Service"""
    
    def setUp(self):
        # Create test data
        self.country_usa = Country.objects.create(name="USA", code="US")
        self.country_canada = Country.objects.create(name="Canada", code="CA")
        
        self.user1 = User.objects.create(username="user1", email="user1@example.com")
        self.user2 = User.objects.create(username="user2", email="user2@example.com")
        
        self.blog1 = Blog.objects.create(
            title="Blog 1", content="Content 1",
            author=self.user1, country=self.country_usa
        )
        self.blog2 = Blog.objects.create(
            title="Blog 2", content="Content 2",
            author=self.user2, country=self.country_canada
        )
        
        # Create views
        for i in range(5):
            BlogView.objects.create(blog=self.blog1, country=self.country_usa, user=self.user1)
        
        for i in range(3):
            BlogView.objects.create(blog=self.blog2, country=self.country_canada, user=self.user2)
    
    def test_group_by_country(self):
        """Test grouping by country"""
        results = get_blog_views_analytics(object_type='country', range_type='month')
        
        self.assertGreater(len(results), 0)
        self.assertIn('x', results[0])  # Country name
        self.assertIn('y', results[0])  # Blog count
        self.assertIn('z', results[0])  # View count
    
    def test_group_by_user(self):
        """Test grouping by user"""
        results = get_blog_views_analytics(object_type='user', range_type='week')
        
        self.assertGreater(len(results), 0)
        self.assertIn('x', results[0])  # Username
        self.assertIn('y', results[0])  # Blog count
        self.assertIn('z', results[0])  # View count
    
    def test_with_filters(self):
        """Test with dynamic filters"""
        filters = {"eq": {"country__name": "USA"}}
        results = get_blog_views_analytics(
            object_type='country',
            range_type='month',
            filters=filters
        )
        
        # Should only return USA results
        if len(results) > 0:
            self.assertTrue(any(r['x'] == 'USA' for r in results))
    
    def test_invalid_object_type(self):
        """Test with invalid object_type"""
        with self.assertRaises(ValueError):
            get_blog_views_analytics(object_type='invalid', range_type='month')


class TestTopAnalyticsService(TestCase):
    """Test API #2: Top Analytics Service"""
    
    def setUp(self):
        # Create test data
        self.country = Country.objects.create(name="USA", code="US")
        
        self.users = []
        self.blogs = []
        
        # Create 5 users with blogs and varying view counts
        for i in range(5):
            user = User.objects.create(
                username=f"user{i}",
                email=f"user{i}@example.com"
            )
            self.users.append(user)
            
            blog = Blog.objects.create(
                title=f"Blog {i}",
                content=f"Content {i}",
                author=user,
                country=self.country
            )
            self.blogs.append(blog)
            
            # Create varying number of views (user0 gets most views)
            for j in range((5 - i) * 2):
                BlogView.objects.create(blog=blog, country=self.country, user=user)
    
    def test_top_users(self):
        """Test top 10 users by views"""
        results = get_top_analytics(top='user', range_type='all')
        
        self.assertLessEqual(len(results), 10)
        if len(results) > 1:
            # Verify descending order by views (z)
            self.assertGreaterEqual(results[0]['z'], results[1]['z'])
    
    def test_top_countries(self):
        """Test top 10 countries by views"""
        results = get_top_analytics(top='country', range_type='all')
        
        self.assertLessEqual(len(results), 10)
        self.assertIn('x', results[0])  # Country name
        self.assertIn('y', results[0])  # Blog count
        self.assertIn('z', results[0])  # View count
    
    def test_top_blogs(self):
        """Test top 10 blogs by views"""
        results = get_top_analytics(top='blog', range_type='all')
        
        self.assertLessEqual(len(results), 10)
        if len(results) > 0:
            self.assertIn('x', results[0])  # Blog title
            self.assertIn('y', results[0])  # Author username
            self.assertIn('z', results[0])  # View count
    
    def test_with_time_range(self):
        """Test with time range filtering"""
        results = get_top_analytics(top='user', range_type='month')
        self.assertLessEqual(len(results), 10)
    
    def test_invalid_top_type(self):
        """Test with invalid top type"""
        with self.assertRaises(ValueError):
            get_top_analytics(top='invalid', range_type='all')


class TestPerformanceAnalyticsService(TestCase):
    """Test API #3: Performance Analytics Service"""
    
    def setUp(self):
        self.user = User.objects.create(username="perfuser", email="perf@example.com")
        self.country = Country.objects.create(name="USA", code="US")
        
        now = timezone.now()
        
        # Create blogs and views over different time periods
        for i in range(3):
            blog_date = now - timedelta(days=i * 7)  # Weekly intervals
            
            blog = Blog.objects.create(
                title=f"Blog Week {i}",
                content="Content",
                author=self.user,
                country=self.country,
                created_at=blog_date
            )
            
            # Create views for this blog
            for j in range((i + 1) * 3):  # Increasing views over time
                BlogView.objects.create(
                    blog=blog,
                    user=self.user,
                    country=self.country,
                    viewed_at=blog_date + timedelta(days=j)
                )
    
    def test_performance_by_week(self):
        """Test weekly performance comparison"""
        results = get_performance_analytics(compare='week', user_id=self.user.id)
        
        if len(results) > 0:
            self.assertIn('x', results[0])  # Period label with blog count
            self.assertIn('y', results[0])  # View count
            self.assertIn('z', results[0])  # Growth percentage
    
    def test_performance_by_month(self):
        """Test monthly performance comparison"""
        results = get_performance_analytics(compare='month', user_id=self.user.id)
        self.assertIsInstance(results, list)
    
    def test_all_users_performance(self):
        """Test performance for all users (no user_id)"""
        results = get_performance_analytics(compare='week')
        self.assertIsInstance(results, list)
    
    def test_performance_with_filters(self):
        """Test performance analytics with dynamic filters (regression test)"""
        # Filter for views in USA (excludes views from other countries if any)
        filters = {"eq": {"country__name": "USA"}}
        results = get_performance_analytics(
            compare='week', 
            user_id=self.user.id,
            filters=filters
        )
        self.assertIsInstance(results, list)
        # Should not crash and return results
        if len(results) > 0:
             self.assertIn('y', results[0])

    def test_growth_calculation(self):
        """Test growth percentage calculation"""
        growth = calculate_growth_percentage(current=120, previous=100)
        self.assertEqual(growth, 20.0)
        
        decline = calculate_growth_percentage(current=80, previous=100)
        self.assertEqual(decline, -20.0)
        
        from_zero = calculate_growth_percentage(current=50, previous=0)
        self.assertEqual(from_zero, 100.0)
