# Redis Setup Guide

## Why Redis is Required

This project uses Redis for:

1. **Celery Message Broker**: Manages task queue for async processing
2. **Celery Result Backend**: Stores task results and status
3. **Django Caching**: Session storage and query result caching (configured in local.py)

## Installation

### Windows

**Option 1: Using Docker (Recommended)**
```bash
docker run -d -p 6379:6379 --name redis redis:7
```

**Option 2: Native Installation**
1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`
3. Default port: 6379

**Option 3: WSL2**
```bash
wsl
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server

# Enable on boot
sudo systemctl enable redis-server

# Check status
sudo systemctl status redis-server
```

### macOS

```bash
# Using Homebrew
brew install redis

# Start Redis
brew services start redis

# Or run in foreground
redis-server
```

### Docker (All Platforms)

```bash
# Run Redis container
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7

# Check if running
docker ps | grep redis

# View logs
docker logs redis

# Stop Redis
docker stop redis

# Start Redis
docker start redis
```

## Verification

Test if Redis is running:

```bash
# Test connection
redis-cli ping
# Expected output: PONG

# Check Redis info
redis-cli info server

# Monitor Redis commands (useful for debugging)
redis-cli monitor
```

## Configuration

### Environment Variables (.env)

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### For Docker Compose

If using docker-compose.yml, Redis is automatically configured:

```yaml
redis:
  image: redis:7
  ports:
    - "6379:6379"
```

Update .env for Docker network:
```env
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## Testing Redis Integration

### Test Django Cache

```python
# In Django shell
python manage.py shell

from django.core.cache import cache

# Set a value
cache.set('test_key', 'Hello Redis!', 300)

# Get the value
print(cache.get('test_key'))  # Should print: Hello Redis!

# Delete the value
cache.delete('test_key')
```

### Test Celery Connection

```bash
# Start Celery worker
celery -A ideeza_assessment worker -l info

# In another terminal, test a task
python manage.py shell
```

```python
from ideeza_assessment.celery import debug_task

# Run async task
result = debug_task.delay()
print(result.id)  # Task ID
print(result.status)  # Task status
```

## Common Issues

### Issue: Connection Refused

**Error**: `redis.exceptions.ConnectionError: Error 10061 connecting to localhost:6379`

**Solution**:
1. Check if Redis is running: `redis-cli ping`
2. Start Redis if not running
3. Check firewall settings
4. Verify CELERY_BROKER_URL in .env

### Issue: Redis Not Found (Windows)

**Solution**: Use Docker or WSL2 for easier Redis management on Windows

### Issue: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 6379
# Windows
netstat -ano | findstr :6379

# Linux/Mac
lsof -i :6379

# Kill the process or use different port
redis-server --port 6380
```

Update .env:
```env
CELERY_BROKER_URL=redis://localhost:6380/0
```

### Issue: Celery Worker Not Starting

**Windows Specific**:
```bash
# Use solo pool on Windows
celery -A ideeza_assessment worker -l info --pool=solo
```

**Linux/Mac**:
```bash
celery -A ideeza_assessment worker -l info
```

## Redis CLI Commands

Useful commands for debugging:

```bash
# Connect to Redis
redis-cli

# List all keys
KEYS *

# Get value of a key
GET key_name

# Delete a key
DEL key_name

# Clear all data (use with caution!)
FLUSHALL

# Get database size
DBSIZE

# Monitor all commands in real-time
MONITOR

# Check memory usage
INFO memory
```

## Production Considerations

### Security

1. **Bind to localhost only** (if not using Docker network):
   ```bash
   redis-server --bind 127.0.0.1
   ```

2. **Set password**:
   ```bash
   redis-server --requirepass your_strong_password
   ```
   
   Update .env:
   ```env
   CELERY_BROKER_URL=redis://:your_strong_password@localhost:6379/0
   ```

3. **Disable dangerous commands**:
   ```bash
   redis-server --rename-command FLUSHALL "" --rename-command FLUSHDB ""
   ```

### Performance

1. **Persistence**: Configure RDB or AOF for data persistence
2. **Memory Limit**: Set maxmemory and eviction policy
3. **Connection Pooling**: Already configured in django-redis

### Monitoring

Use Redis monitoring tools:
- RedisInsight (GUI)
- redis-cli INFO
- Prometheus + Redis Exporter

## Alternative: Redis Cloud

For production without managing Redis:

1. **Redis Cloud**: https://redis.com/try-free/
2. **AWS ElastiCache**: Redis managed service
3. **Azure Cache for Redis**: Microsoft's managed Redis

Update .env with cloud connection string:
```env
CELERY_BROKER_URL=rediss://username:password@host:port/0
CELERY_RESULT_BACKEND=rediss://username:password@host:port/0
```

## Resources

- Official Redis Documentation: https://redis.io/docs/
- Django Redis: https://github.com/jazzband/django-redis
- Celery with Redis: https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html
