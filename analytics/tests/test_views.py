from rest_framework.test import APITestCase
from rest_framework import status
from analytics.models import User, Country, Blog, BlogView

class TestBlogViewsAnalyticsView(APITestCase):
    """Integration tests for API #1 endpoint"""
    
    def setUp(self):
        self.country = Country.objects.create(name="USA", code="US")
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.blog = Blog.objects.create(
            title="Test Blog", content="Content",
            author=self.user, country=self.country
        )
        BlogView.objects.create(blog=self.blog, country=self.country, user=self.user)
    
    def test_api_valid_request(self):
        """Test valid API request"""
        response = self.client.get('/analytics/blog-views/', {
            'object_type': 'country',
            'range': 'month'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('page', response.data)
        self.assertIn('page_size', response.data)
        self.assertIn('total_pages', response.data)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
    
    def test_api_missing_required_param(self):
        """Test missing required parameter"""
        response = self.client.get('/analytics/blog-views/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_api_invalid_object_type(self):
        """Test invalid object_type value"""
        response = self.client.get('/analytics/blog-views/', {
            'object_type': 'invalid',
            'range': 'month'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_api_pagination(self):
        """Test pagination parameters"""
        response = self.client.get('/analytics/blog-views/', {
            'object_type': 'country',
            'range': 'month',
            'page': 1,
            'page_size': 5
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 5)
        self.assertLessEqual(len(response.data['results']), 5)


class TestTopAnalyticsView(APITestCase):
    """Integration tests for API #2 endpoint"""
    
    def setUp(self):
        self.country = Country.objects.create(name="USA", code="US")
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.blog = Blog.objects.create(
            title="Test Blog", content="Content",
            author=self.user, country=self.country
        )
        BlogView.objects.create(blog=self.blog, country=self.country, user=self.user)
    
    def test_api_top_users(self):
        """Test top users API request"""
        response = self.client.get('/analytics/top/', {
            'top': 'user',
            'range': 'all'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
    
    def test_api_top_blogs(self):
        """Test top blogs API request"""
        response = self.client.get('/analytics/top/', {
            'top': 'blog'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
    
    def test_api_pagination(self):
        """Test pagination parameters"""
        response = self.client.get('/analytics/top/', {
            'top': 'user',
            'range': 'all',
            'page': 1,
            'page_size': 3
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 3)
        self.assertLessEqual(len(response.data['results']), 3)


class TestPerformanceAnalyticsView(APITestCase):
    """Integration tests for API #3 endpoint"""
    
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.country = Country.objects.create(name="USA", code="US")
        self.blog = Blog.objects.create(
            title="Test Blog", content="Content",
            author=self.user, country=self.country
        )
        BlogView.objects.create(blog=self.blog, country=self.country, user=self.user)
    
    def test_api_valid_request(self):
        """Test valid performance API request"""
        response = self.client.get('/analytics/performance/', {
            'compare': 'week'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
    
    def test_api_with_user_id(self):
        """Test performance API with specific user"""
        response = self.client.get('/analytics/performance/', {
            'compare': 'month',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
    
    def test_api_missing_compare(self):
        """Test missing required compare parameter"""
        response = self.client.get('/analytics/performance/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_api_pagination(self):
        """Test pagination parameters"""
        response = self.client.get('/analytics/performance/', {
            'compare': 'week',
            'page': 1,
            'page_size': 5
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 5)
        self.assertLessEqual(len(response.data['results']), 5)
