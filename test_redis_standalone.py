import os
import django
import sys

# Add project root to path if needed (implicit in current dir usually)
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ideeza_assessment.settings')
django.setup()

from django.core.cache import cache

try:
    cache.set('test_redis_standalone', 'working_sa', 5)
    val = cache.get('test_redis_standalone')
    if val == 'working_sa':
        print("REDIS_standalone_SUCCESS")
    else:
        print(f"REDIS_standalone_FAILURE: val={val}")
except Exception as e:
    print(f"REDIS_standalone_ERROR: {e}")
