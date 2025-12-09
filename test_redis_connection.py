#!/usr/bin/env python
"""
Quick script to test Redis connection
Run: python test_redis_connection.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_redis_connection():
    """Test Redis connection using redis-py"""
    try:
        import redis
        
        # Get Redis URL from environment
        redis_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        print(f"Testing Redis connection to: {redis_url}")
        
        # Parse Redis URL
        if redis_url.startswith('redis://'):
            # Simple connection
            r = redis.from_url(redis_url)
        else:
            print(f"Invalid Redis URL format: {redis_url}")
            return False
        
        # Test connection
        response = r.ping()
        if response:
            print("✅ Redis connection successful!")
            
            # Test set/get
            r.set('test_key', 'Hello from IDEEZA Assessment!')
            value = r.get('test_key')
            print(f"✅ Redis read/write test: {value.decode('utf-8')}")
            
            # Clean up
            r.delete('test_key')
            
            # Get Redis info
            info = r.info('server')
            print(f"✅ Redis version: {info.get('redis_version')}")
            
            return True
        else:
            print("❌ Redis ping failed")
            return False
            
    except ImportError:
        print("❌ Redis package not installed")
        print("Install with: pip install redis")
        return False
    except redis.ConnectionError as e:
        print(f"❌ Redis connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if Redis is running: redis-cli ping")
        print("2. Start Redis: redis-server (or docker run -d -p 6379:6379 redis:7)")
        print("3. Check CELERY_BROKER_URL in .env file")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_django_cache():
    """Test Django cache with Redis"""
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ideeza_assessment.settings.local')
        import django
        django.setup()
        
        from django.core.cache import cache
        
        print("\nTesting Django cache (django-redis)...")
        
        # Test cache operations
        cache.set('django_test_key', 'Django + Redis working!', 300)
        value = cache.get('django_test_key')
        
        if value:
            print(f"✅ Django cache test: {value}")
            cache.delete('django_test_key')
            return True
        else:
            print("❌ Django cache test failed")
            return False
            
    except Exception as e:
        print(f"⚠️  Django cache test skipped: {e}")
        return None


def test_celery_connection():
    """Test Celery connection to Redis"""
    try:
        from celery import Celery
        
        print("\nTesting Celery connection...")
        
        broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        app = Celery('test', broker=broker_url)
        
        # Test broker connection
        conn = app.connection()
        conn.connect()
        
        if conn.connected:
            print("✅ Celery broker connection successful!")
            conn.close()
            return True
        else:
            print("❌ Celery broker connection failed")
            return False
            
    except ImportError:
        print("⚠️  Celery not installed, skipping test")
        return None
    except Exception as e:
        print(f"❌ Celery connection error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("IDEEZA Assessment - Redis Connection Test")
    print("=" * 60)
    
    # Test 1: Direct Redis connection
    redis_ok = test_redis_connection()
    
    # Test 2: Django cache (optional)
    django_ok = test_django_cache()
    
    # Test 3: Celery connection (optional)
    celery_ok = test_celery_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    print(f"Redis Connection:    {'✅ PASS' if redis_ok else '❌ FAIL'}")
    if django_ok is not None:
        print(f"Django Cache:        {'✅ PASS' if django_ok else '❌ FAIL'}")
    if celery_ok is not None:
        print(f"Celery Connection:   {'✅ PASS' if celery_ok else '❌ FAIL'}")
    
    # Exit code
    if redis_ok:
        print("\n✅ All critical tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Redis connection failed. Please check Redis installation.")
        print("See REDIS_SETUP.md for installation instructions.")
        sys.exit(1)
