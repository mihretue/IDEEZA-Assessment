"""
Management command to seed the database with comprehensive test data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from analytics.models import User, Country, Blog, BlogView


class Command(BaseCommand):
    help = 'Seeds the database with comprehensive test data for analytics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)'
        )
        parser.add_argument(
            '--blogs-per-user',
            type=int,
            default=10,
            help='Average blogs per user (default: 10)'
        )
        parser.add_argument(
            '--views-per-blog',
            type=int,
            default=100,
            help='Average views per blog (default: 100)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        blogs_per_user = options['blogs_per_user']
        views_per_blog = options['views_per_blog']
        clear_data = options['clear']

        self.stdout.write(self.style.WARNING('Starting data seeding...'))
        
        # Clear existing data if requested
        if clear_data:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            BlogView.objects.all().delete()
            Blog.objects.all().delete()
            User.objects.all().delete()
            Country.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

        # Create countries
        self.stdout.write('Creating countries...')
        countries_data = [
            ('United States', 'US'),
            ('Canada', 'CA'),
            ('United Kingdom', 'GB'),
            ('Germany', 'DE'),
            ('France', 'FR'),
            ('Japan', 'JP'),
            ('Australia', 'AU'),
            ('Brazil', 'BR'),
            ('India', 'IN'),
            ('China', 'CN'),
            ('South Korea', 'KR'),
            ('Italy', 'IT'),
            ('Spain', 'ES'),
            ('Mexico', 'MX'),
            ('Netherlands', 'NL'),
            ('Sweden', 'SE'),
            ('Switzerland', 'CH'),
            ('Singapore', 'SG'),
            ('Norway', 'NO'),
            ('Denmark', 'DK'),
        ]
        
        countries = []
        for name, code in countries_data:
            country, created = Country.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            countries.append(country)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(countries)} countries'))

        # Create users
        self.stdout.write(f'Creating {num_users} users...')
        users = []
        user_prefixes = [
            'tech', 'dev', 'code', 'blog', 'write', 'data', 'cloud', 'web',
            'mobile', 'ai', 'ml', 'cyber', 'digital', 'smart', 'pro'
        ]
        
        for i in range(num_users):
            prefix = random.choice(user_prefixes)
            username = f"{prefix}_user_{i+1}"
            email = f"{username}@example.com"
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))

        # Create blogs with varied dates
        self.stdout.write(f'Creating blogs (avg {blogs_per_user} per user)...')
        blogs = []
        blog_topics = [
            'Python', 'Django', 'JavaScript', 'React', 'Vue', 'Angular',
            'Node.js', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
            'Machine Learning', 'AI', 'Data Science', 'DevOps', 'Security',
            'Blockchain', 'Web3', 'Mobile Development', 'iOS', 'Android',
            'Cloud Computing', 'Microservices', 'API Design', 'Database',
            'PostgreSQL', 'MongoDB', 'Redis', 'GraphQL', 'REST API'
        ]
        
        blog_templates = [
            'Getting Started with {}',
            'Advanced {} Techniques',
            'Best Practices for {}',
            'Complete Guide to {}',
            'Introduction to {}',
            '{} Tutorial for Beginners',
            'Mastering {}',
            '{} Tips and Tricks',
            'Building with {}',
            '{} in Production',
            'Scaling {} Applications',
            '{} Performance Optimization',
            'Understanding {}',
            '{} Architecture Patterns',
            'Modern {} Development'
        ]
        
        now = timezone.now()
        total_blogs = 0
        
        for user in users:
            # Vary the number of blogs per user
            num_blogs = random.randint(
                max(1, blogs_per_user - 5),
                blogs_per_user + 5
            )
            
            for j in range(num_blogs):
                # Create blogs over the past year
                days_ago = random.randint(0, 365)
                created_at = now - timedelta(days=days_ago)
                
                topic = random.choice(blog_topics)
                template = random.choice(blog_templates)
                title = template.format(topic)
                
                content = f"This is a comprehensive blog post about {topic}. " * random.randint(5, 20)
                
                blog = Blog.objects.create(
                    title=title,
                    content=content,
                    author=user,
                    country=random.choice(countries),
                    created_at=created_at
                )
                blogs.append(blog)
                total_blogs += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {total_blogs} blogs'))

        # Create blog views with realistic patterns (using bulk_create for speed)
        self.stdout.write(f'Creating blog views (avg {views_per_blog} per blog)...')
        total_views = 0
        batch_size = 1000
        views_batch = []
        
        for idx, blog in enumerate(blogs):
            # Vary views per blog (some blogs are more popular)
            popularity_factor = random.choice([0.5, 0.7, 1.0, 1.5, 2.0, 3.0])
            num_views = int(views_per_blog * popularity_factor)
            num_views = random.randint(
                max(10, num_views - 50),
                num_views + 50
            )
            
            # Create views over time since blog creation
            blog_age_days = (now - blog.created_at).days
            
            for k in range(num_views):
                # Views happen after blog creation
                if blog_age_days > 0:
                    days_after_creation = random.randint(0, blog_age_days)
                    viewed_at = blog.created_at + timedelta(
                        days=days_after_creation,
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                else:
                    viewed_at = blog.created_at + timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                
                views_batch.append(BlogView(
                    blog=blog,
                    user=random.choice(users),
                    country=random.choice(countries),
                    viewed_at=viewed_at
                ))
                total_views += 1
                
                # Bulk create in batches for performance
                if len(views_batch) >= batch_size:
                    BlogView.objects.bulk_create(views_batch)
                    views_batch = []
            
            # Progress indicator
            if (idx + 1) % 50 == 0:
                self.stdout.write(f'  Progress: {idx + 1}/{len(blogs)} blogs processed, {total_views} views created...')
        
        # Create remaining views
        if views_batch:
            BlogView.objects.bulk_create(views_batch)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {total_views} blog views'))

        # Summary statistics
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('DATA SEEDING COMPLETED!'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Countries:  {Country.objects.count()}')
        self.stdout.write(f'Users:      {User.objects.count()}')
        self.stdout.write(f'Blogs:      {Blog.objects.count()}')
        self.stdout.write(f'Blog Views: {BlogView.objects.count()}')
        self.stdout.write('=' * 70)
        
        # Sample queries
        self.stdout.write('\nSample Analytics:')
        self.stdout.write('-' * 70)
        
        # Top 5 users by blog count
        from django.db.models import Count
        top_users = User.objects.annotate(
            blog_count=Count('blogs')
        ).order_by('-blog_count')[:5]
        
        self.stdout.write('\nTop 5 Users by Blog Count:')
        for i, user in enumerate(top_users, 1):
            self.stdout.write(f'  {i}. {user.username}: {user.blog_count} blogs')
        
        # Top 5 blogs by views
        top_blogs = Blog.objects.annotate(
            view_count=Count('views')
        ).order_by('-view_count')[:5]
        
        self.stdout.write('\nTop 5 Blogs by Views:')
        for i, blog in enumerate(top_blogs, 1):
            self.stdout.write(f'  {i}. {blog.title[:50]}: {blog.view_count} views')
        
        # Top 5 countries by views
        top_countries = Country.objects.annotate(
            view_count=Count('blog_views')
        ).order_by('-view_count')[:5]
        
        self.stdout.write('\nTop 5 Countries by Views:')
        for i, country in enumerate(top_countries, 1):
            self.stdout.write(f'  {i}. {country.name}: {country.view_count} views')
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('✓ Database seeded successfully!'))
        self.stdout.write('\nYou can now test the analytics APIs:')
        self.stdout.write('  - http://localhost:8000/analytics/blog-views/?object_type=country&range=month')
        self.stdout.write('  - http://localhost:8000/analytics/top/?top=user&range=all')
        self.stdout.write('  - http://localhost:8000/analytics/performance/?compare=week')
        self.stdout.write('\nAPI Documentation:')
        self.stdout.write('  - http://localhost:8000/api/docs/ (Swagger UI)')
        self.stdout.write('  - http://localhost:8000/api/redoc/ (ReDoc)')
        self.stdout.write('=' * 70 + '\n')
