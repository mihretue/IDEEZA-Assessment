from django.core.cache import cache
import sys

try:
    cache.set('test_redis_config', 'working', 5)
    val = cache.get('test_redis_config')
    if val == 'working':
        print("REDIS_TEST_SUCCESS")
    else:
        print(f"REDIS_TEST_FAILURE: Expected 'working', got '{val}'")
except Exception as e:
    print(f"REDIS_TEST_ERROR: {e}")
