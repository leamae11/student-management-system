# Installation & Setup Guide

## Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip and virtualenv
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/leamae11/student-management-system.git
cd student-management-system
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Setup Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Important Environment Variables:

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL recommended)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=student_management_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Step 5: Database Setup

### Option A: PostgreSQL (Recommended)

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE student_management_db;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE student_management_db TO your_username;
\q
```

### Option B: SQLite (Development Only)

No setup required, Django will create `db.sqlite3` automatically.

## Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 9: Run Development Server

```bash
python manage.py runserver
```

The server will be available at `http://localhost:8000`

---

## Accessing the Application

### Admin Panel
- URL: `http://localhost:8000/admin/`
- Username: (your superuser username)
- Password: (your superuser password)

### API Documentation
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

### API Base URLs
- Users: `http://localhost:8000/api/users/`
- Tasks: `http://localhost:8000/api/tasks/`
- Grades: `http://localhost:8000/api/grades/`
- Notes: `http://localhost:8000/api/notes/`
- OJT: `http://localhost:8000/api/ojt/`
- Requirements: `http://localhost:8000/api/requirements/`

---

## API Authentication

The API uses JWT (JSON Web Token) authentication. Here's how to authenticate:

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "secure_password_123",
    "password2": "secure_password_123",
    "role": "student"
  }'
```

### 2. Login to Get Tokens

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password_123"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "student"
  }
}
```

### 3. Use Access Token in API Requests

```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## Common Tasks

### Create a Task

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Project Proposal",
    "description": "Finish the project proposal for CS301",
    "due_date": "2024-08-15T23:59:59Z",
    "priority": "high",
    "status": "pending",
    "category": "academics"
  }'
```

### Get All Tasks

```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Pending Tasks

```bash
curl -X GET http://localhost:8000/api/tasks/pending/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Testing

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test users
python manage.py test tasks
python manage.py test grades
```

---

## Troubleshooting

### Issue: Database connection error
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

### Issue: Module not found error
**Solution**: Ensure virtual environment is activated and all dependencies are installed.

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution**: Run on a different port

```bash
python manage.py runserver 8001
```

### Issue: Static files not loading
**Solution**: Collect static files

```bash
python manage.py collectstatic --noinput
```

---

## Production Deployment

For production deployment, follow these steps:

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL)
4. Set up HTTPS/SSL
5. Use Gunicorn or uWSGI as application server
6. Use Nginx as reverse proxy
7. Set up environment variables securely

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Support

For issues or questions, please create an issue on GitHub.
