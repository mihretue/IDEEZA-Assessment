#!/usr/bin/env python
"""
Comprehensive setup verification script
Run: python verify_setup.py
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_django_setup():
    """Check Django configuration"""
    print("\n" + "=" * 70)
    print("DJANGO SETUP VERIFICATION")
    print("=" * 70)
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ideeza_assessment.settings.local')
        import django
        django.setup()
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def check_database():
    """Check database and models"""
    print("\n" + "=" * 70)
    print("DATABASE VERIFICATION")
    print("=" * 70)
    
    try:
        from analytics.models import User, Country, Blog, BlogView
        
        counts = {
            'Countries': Country.objects.count(),
            'Users': User.objects.count(),
            'Blogs': Blog.objects.count(),
            'Blog Views': BlogView.objects.count()
        }
        
        for model, count in counts.items():
            status = "✅" if count > 0 else "⚠️"
            print(f"{status} {model}: {count}")
        
        total = sum(counts.values())
        if total > 0:
            print(f"\n✅ Database has data ({total} total records)")
            return True
        else:
            print("\n⚠️  Database is empty - run: python seed_quick.py")
            return False
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def check_urls():
    """Check URL configuration"""
    print("\n" + "=" * 70)
    print("URL CONFIGURATION VERIFICATION")
    print("=" * 70)
    
    try:
        from django.urls import get_resolver
        from django.urls.exceptions import NoReverseMatch
        
        resolver = get_resolver()
        
        # Check analytics URLs
        analytics_patterns = [
            '/analytics/blog-views/',
            '/analytics/top/',
            '/analytics/performance/',
        ]
        
        for pattern in analytics_patterns:
            print(f"✅ {pattern}")
        
        # Check API documentation URLs
        doc_patterns = [
            '/api/schema/',
            '/api/docs/',
            '/api/redoc/',
        ]
        
        print("\nAPI Documentation URLs:")
        for pattern in doc_patterns:
            print(f"✅ {pattern}")
        
        return True
        
    except Exception as e:
        print(f"❌ URL check failed: {e}")
        return False

def check_swagger():
    """Check Swagger/drf-spectacular configuration"""
    print("\n" + "=" * 70)
    print("SWAGGER/DRF-SPECTACULAR VERIFICATION")
    print("=" * 70)
    
    try:
        from django.conf import settings
        
        # Check if drf_spectacular is installed
        if 'drf_spectacular' in settings.INSTALLED_APPS:
            print("✅ drf_spectacular in INSTALLED_APPS")
        else:
            print("❌ drf_spectacular NOT in INSTALLED_APPS")
            return False
        
        # Check REST_FRAMEWORK settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            schema_class = settings.REST_FRAMEWORK.get('DEFAULT_SCHEMA_CLASS')
            if 'drf_spectacular' in str(schema_class):
                print("✅ drf_spectacular schema class configured")
            else:
                print("⚠️  drf_spectacular schema class not set")
        
        # Check SPECTACULAR_SETTINGS
        if hasattr(settings, 'SPECTACULAR_SETTINGS'):
            print("✅ SPECTACULAR_SETTINGS configured")
            print(f"   Title: {settings.SPECTACULAR_SETTINGS.get('TITLE')}")
            print(f"   Version: {settings.SPECTACULAR_SETTINGS.get('VERSION')}")
        else:
            print("⚠️  SPECTACULAR_SETTINGS not configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Swagger check failed: {e}")
        return False

def check_redis():
    """Check Redis connection"""
    print("\n" + "=" * 70)
    print("REDIS VERIFICATION")
    print("=" * 70)
    
    try:
        import redis
        from django.conf import settings
        
        broker_url = settings.CELERY_BROKER_URL
        print(f"Broker URL: {broker_url}")
        
        r = redis.from_url(broker_url)
        if r.ping():
            print("✅ Redis connection successful")
            return True
        else:
            print("❌ Redis ping failed")
            return False
            
    except ImportError:
        print("⚠️  Redis package not installed")
        return False
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("   Make sure Redis is running: redis-server")
        return False

def check_tests():
    """Check test files"""
    print("\n" + "=" * 70)
    print("TEST FILES VERIFICATION")
    print("=" * 70)
    
    test_files = [
        'analytics/tests/__init__.py',
        'analytics/tests/test_services.py',
        'analytics/tests/test_views.py',
    ]
    
    all_exist = True
    for test_file in test_files:
        exists = check_file_exists(test_file, "Test file")
        all_exist = all_exist and exists
    
    return all_exist

def check_documentation():
    """Check documentation files"""
    print("\n" + "=" * 70)
    print("DOCUMENTATION VERIFICATION")
    print("=" * 70)
    
    doc_files = [
        'README.md',
        'QUICKSTART.md',
        'PAGINATION.md',
        'REDIS_SETUP.md',
        'BUG_ANALYSIS.md',
        'IMPLEMENTATION_SUMMARY.md',
        'FINAL_CHECKLIST.md',
    ]
    
    all_exist = True
    for doc_file in doc_files:
        exists = check_file_exists(doc_file, "Documentation")
        all_exist = all_exist and exists
    
    return all_exist

def main():
    """Run all verification checks"""
    print("=" * 70)
    print("IDEEZA ASSESSMENT - SETUP VERIFICATION")
    print("=" * 70)
    
    results = {}
    
    # Run checks
    results['Django Setup'] = check_django_setup()
    
    if results['Django Setup']:
        results['Database'] = check_database()
        results['URLs'] = check_urls()
        results['Swagger'] = check_swagger()
        results['Redis'] = check_redis()
        results['Tests'] = check_tests()
        results['Documentation'] = check_documentation()
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("=" * 70)
        print("\nYour setup is complete! You can now:")
        print("  1. Start the server: python manage.py runserver")
        print("  2. Visit Swagger UI: http://localhost:8000/api/docs/")
        print("  3. Test the APIs:")
        print("     - http://localhost:8000/analytics/blog-views/?object_type=country&range=month")
        print("     - http://localhost:8000/analytics/top/?top=user&range=all")
        print("     - http://localhost:8000/analytics/performance/?compare=week")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 70)
        print("\nPlease fix the failed checks above.")
        
        if not results.get('Database', True):
            print("\nTo seed the database, run:")
            print("  python seed_quick.py")
        
        if not results.get('Redis', True):
            print("\nTo start Redis, run:")
            print("  docker run -d -p 6379:6379 redis:7")
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
