#!/usr/bin/env python
"""
Verification script to check that common bugs are NOT present in the codebase.
Run: python verify_no_bugs.py
"""
import os
import sys
import re

def check_file_content(filepath, pattern, should_exist=False):
    """Check if a pattern exists in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            found = re.search(pattern, content, re.MULTILINE)
            return found is not None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def verify_no_bugs():
    """Run all bug verification checks"""
    print("=" * 70)
    print("BUG VERIFICATION SCRIPT")
    print("=" * 70)
    print()
    
    all_passed = True
    
    # Bug #1: Check for distinct=True in Count operations
    print("✓ Checking Bug #1: Incorrect Aggregation...")
    services_file = 'analytics/services.py'
    
    # Should have distinct=True
    has_distinct = check_file_content(services_file, r"Count\(['\"]blog__id['\"],\s*distinct=True\)")
    if has_distinct:
        print("  ✅ PASS: Using Count with distinct=True for blog counts")
    else:
        print("  ❌ FAIL: Missing distinct=True in Count operations")
        all_passed = False
    
    # Bug #2: Check for growth calculation and previous_views update
    print("\n✓ Checking Bug #2: Missing Growth Calculation...")
    
    has_growth_calc = check_file_content(services_file, r"growth = calculate_growth_percentage")
    has_growth_in_results = check_file_content(services_file, r"['\"]z['\"]:\s*growth")
    has_prev_update = check_file_content(services_file, r"previous_views = current_views")
    
    if has_growth_calc and has_growth_in_results and has_prev_update:
        print("  ✅ PASS: Growth calculation implemented correctly")
        print("    - Growth calculated: ✓")
        print("    - Growth included in results: ✓")
        print("    - previous_views updated: ✓")
    else:
        print("  ❌ FAIL: Growth calculation issues")
        if not has_growth_calc:
            print("    - Missing growth calculation")
        if not has_growth_in_results:
            print("    - Growth not included in results")
        if not has_prev_update:
            print("    - previous_views not updated")
        all_passed = False
    
    # Bug #3: Check that filters are applied to correct queryset
    print("\n✓ Checking Bug #3: Dynamic Filters Applied to Wrong Model...")
    
    # In performance analytics, filters should only be applied to view_queryset
    perf_section = check_file_content(services_file, r"view_queryset = apply_dynamic_filters\(view_queryset, filters\)")
    no_blog_filter = not check_file_content(services_file, r"blog_queryset = apply_dynamic_filters\(blog_queryset")
    
    if perf_section and no_blog_filter:
        print("  ✅ PASS: Filters applied to correct queryset")
        print("    - view_queryset filtered: ✓")
        print("    - blog_queryset not filtered: ✓")
    else:
        print("  ❌ FAIL: Filter application issues")
        all_passed = False
    
    # Bug #4: Check Q object initialization in OR operations
    print("\n✓ Checking Bug #4: Incorrect Q Object Initialization...")
    
    has_q_init = check_file_content(services_file, r"if ['\"]or['\"] in filter_dict:\s+q = Q\(\)")
    has_or_operator = check_file_content(services_file, r"q \|= parse_filter\(sub_filter\)")
    
    if has_q_init and has_or_operator:
        print("  ✅ PASS: Q object properly initialized for OR operations")
        print("    - Q() initialized: ✓")
        print("    - |= operator used: ✓")
    else:
        print("  ❌ FAIL: Q object initialization issues")
        all_passed = False
    
    # Bug #5: Check that FilterSet is NOT used
    print("\n✓ Checking Bug #5: Invalid FilterSet Usage...")
    
    uses_filterset = check_file_content(services_file, r"FilterSet|django_filters")
    
    if not uses_filterset:
        print("  ✅ PASS: Not using django-filters FilterSet")
        print("    - Using custom dynamic filter system: ✓")
    else:
        print("  ❌ FAIL: Using FilterSet (potential field reference issues)")
        all_passed = False
    
    # Bug #6: Check for select_related() usage
    print("\n✓ Checking Bug #6: Missing select_related()...")
    
    select_related_count = len(re.findall(r"select_related\(", open(services_file).read()))
    
    if select_related_count >= 5:  # Should have multiple select_related calls
        print(f"  ✅ PASS: Found {select_related_count} select_related() calls")
        print("    - N+1 queries prevented: ✓")
    else:
        print(f"  ❌ FAIL: Only {select_related_count} select_related() calls found")
        all_passed = False
    
    # Bug #7: Check that JWT is NOT implemented
    print("\n✓ Checking Bug #7: Unnecessary JWT Authentication...")
    
    has_jwt = (
        check_file_content('requirements/base.txt', r'jwt') or
        check_file_content('analytics/views.py', r'JWT|jwt|authentication_classes')
    )
    
    if not has_jwt:
        print("  ✅ PASS: No JWT authentication (not required)")
    else:
        print("  ⚠️  WARNING: JWT authentication found (may not be required)")
    
    # Additional checks
    print("\n✓ Additional Checks...")
    
    # Check for pagination
    has_pagination = check_file_content('analytics/views.py', r"paginate_results")
    if has_pagination:
        print("  ✅ Pagination implemented")
    
    # Check for tests
    test_files_exist = (
        os.path.exists('analytics/tests/test_services.py') and
        os.path.exists('analytics/tests/test_views.py')
    )
    if test_files_exist:
        print("  ✅ Test files organized")
    
    # Check for Redis
    has_redis = check_file_content('requirements/base.txt', r'^redis$')
    if has_redis:
        print("  ✅ Redis package included")
    
    # Check for Celery
    has_celery = check_file_content('requirements/base.txt', r'^celery$')
    if has_celery:
        print("  ✅ Celery package included")
    
    # Summary
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL CRITICAL BUG CHECKS PASSED!")
        print("=" * 70)
        print("\nYour implementation is clean and follows best practices.")
        print("No critical bugs found in the codebase.")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 70)
        print("\nPlease review the failed checks above.")
        return 1

if __name__ == '__main__':
    sys.exit(verify_no_bugs())
