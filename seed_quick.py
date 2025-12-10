#!/usr/bin/env python
"""
Quick seed script for testing - creates data much faster
Run: python seed_quick.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ideeza_assessment.settings.local')
django.setup()

from analytics.models import User, Country, Blog, BlogView
from django.utils import timezone
from datetime import timedelta
import random

print("=" * 70)
print("QUICK SEED SCRIPT")
print("=" * 70)

# Clear existing data
print("\n1. Clearing existing data...")
BlogView.objects.all().delete()
Blog.objects.all().delete()
User.objects.all().delete()
Country.objects.all().delete()
print("   ✓ Data cleared")

# Create countries
print("\n2. Creating countries...")
countries_data = [
    ('United States', 'US'), ('Canada', 'CA'), ('United Kingdom', 'GB'),
    ('Germany', 'DE'), ('France', 'FR'), ('Japan', 'JP'),
    ('Australia', 'AU'), ('Brazil', 'BR'), ('India', 'IN'),
    ('China', 'CN'), ('South Korea', 'KR'), ('Italy', 'IT'),
    ('Spain', 'ES'), ('Mexico', 'MX'), ('Netherlands', 'NL'),
]

countries = []
for name, code in countries_data:
    country = Country.objects.create(name=name, code=code)
    countries.append(country)
print(f"   ✓ Created {len(countries)} countries")

# Create users
print("\n3. Creating users...")
users = []
for i in range(30):
    user = User.objects.create(
        username=f"user_{i+1}",
        email=f"user_{i+1}@example.com"
    )
    users.append(user)
print(f"   ✓ Created {len(users)} users")

# Create blogs
print("\n4. Creating blogs...")
blog_topics = [
    'Python', 'Django', 'JavaScript', 'React', 'Vue', 'Docker',
    'Kubernetes', 'AWS', 'Machine Learning', 'AI', 'DevOps',
    'Security', 'Web Development', 'Mobile Apps', 'Cloud Computing'
]

blogs = []
now = timezone.now()

for user in users:
    num_blogs = random.randint(3, 8)
    for j in range(num_blogs):
        days_ago = random.randint(0, 180)
        created_at = now - timedelta(days=days_ago)
        
        topic = random.choice(blog_topics)
        title = f"Guide to {topic} - Part {j+1}"
        content = f"This is a blog post about {topic}. " * 10
        
        blog = Blog.objects.create(
            title=title,
            content=content,
            author=user,
            country=random.choice(countries),
            created_at=created_at
        )
        blogs.append(blog)

print(f"   ✓ Created {len(blogs)} blogs")

# Create blog views (using bulk_create for speed)
print("\n5. Creating blog views...")
views_batch = []
batch_size = 1000
total_views = 0

for blog in blogs:
    num_views = random.randint(20, 200)
    blog_age_days = (now - blog.created_at).days
    
    for k in range(num_views):
        if blog_age_days > 0:
            days_after = random.randint(0, blog_age_days)
            viewed_at = blog.created_at + timedelta(
                days=days_after,
                hours=random.randint(0, 23)
            )
        else:
            viewed_at = blog.created_at + timedelta(hours=random.randint(0, 23))
        
        views_batch.append(BlogView(
            blog=blog,
            user=random.choice(users),
            country=random.choice(countries),
            viewed_at=viewed_at
        ))
        total_views += 1
        
        if len(views_batch) >= batch_size:
            BlogView.objects.bulk_create(views_batch)
            views_batch = []
            print(f"   Progress: {total_views} views created...")

if views_batch:
    BlogView.objects.bulk_create(views_batch)

print(f"   ✓ Created {total_views} blog views")

# Summary
print("\n" + "=" * 70)
print("SEEDING COMPLETED!")
print("=" * 70)
print(f"Countries:  {Country.objects.count()}")
print(f"Users:      {User.objects.count()}")
print(f"Blogs:      {Blog.objects.count()}")
print(f"Blog Views: {BlogView.objects.count()}")
print("=" * 70)

# Sample analytics
from django.db.models import Count

print("\nTop 5 Users by Blog Count:")
top_users = User.objects.annotate(
    blog_count=Count('blogs')
).order_by('-blog_count')[:5]

for i, user in enumerate(top_users, 1):
    print(f"  {i}. {user.username}: {user.blog_count} blogs")

print("\nTop 5 Blogs by Views:")
top_blogs = Blog.objects.annotate(
    view_count=Count('views')
).order_by('-view_count')[:5]

for i, blog in enumerate(top_blogs, 1):
    print(f"  {i}. {blog.title[:40]}: {blog.view_count} views")

print("\nTop 5 Countries by Views:")
top_countries = Country.objects.annotate(
    view_count=Count('blog_views')
).order_by('-view_count')[:5]

for i, country in enumerate(top_countries, 1):
    print(f"  {i}. {country.name}: {country.view_count} views")

print("\n" + "=" * 70)
print("✓ Database seeded successfully!")
print("\nTest the APIs:")
print("  - http://localhost:8000/analytics/blog-views/?object_type=country&range=month")
print("  - http://localhost:8000/analytics/top/?top=user&range=all")
print("  - http://localhost:8000/analytics/performance/?compare=week")
print("\nAPI Documentation:")
print("  - http://localhost:8000/api/docs/ (Swagger UI)")
print("  - http://localhost:8000/api/redoc/ (ReDoc)")
print("=" * 70)
