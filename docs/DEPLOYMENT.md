# Deployment Guide

## Production Deployment

### Prerequisites
- Ubuntu 20.04 LTS or similar
- Python 3.10+
- PostgreSQL 12+
- Nginx
- Gunicorn

### Quick Setup

```bash
# Clone repository
git clone https://github.com/leamae11/student-management-system.git
cd student-management-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with production values

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Nginx Configuration

Proxy Django app through Nginx on production:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /app/staticfiles/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### SSL/TLS Setup

Use Let's Encrypt for free SSL certificates:

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Backup Strategy

```bash
# Backup database
pg_dump student_management_db | gzip > backup.sql.gz

# Backup media files
tar -czf media_backup.tar.gz media/
```