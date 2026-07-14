# Quick Reference Guide

## API Quick Start

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "role": "student"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

### 3. Use Access Token
```bash
# Copy the access token from login response
TOKEN="your_access_token_here"

# Make authenticated requests
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"
```

## Common API Calls

### Tasks
```bash
# Create task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Assignment",
    "description": "Project proposal",
    "due_date": "2024-08-30T23:59:59Z",
    "priority": "high",
    "status": "pending",
    "category": "CS301"
  }'

# Get all tasks
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"

# Get pending tasks
curl -X GET http://localhost:8000/api/tasks/pending/ \
  -H "Authorization: Bearer $TOKEN"

# Mark task complete
curl -X POST http://localhost:8000/api/tasks/{id}/mark_complete/ \
  -H "Authorization: Bearer $TOKEN"
```

### Grades
```bash
# Create grade (Instructor only)
curl -X POST http://localhost:8000/api/grades/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "subject": "Data Structures",
    "course_code": "CS201",
    "grade": 3.8,
    "semester": "Fall 2024"
  }'

# Get student GPA
curl -X GET http://localhost:8000/api/grades/gpa/ \
  -H "Authorization: Bearer $TOKEN"

# Get grades by semester
curl -X GET "http://localhost:8000/api/grades/by_semester/?semester=Fall%202024" \
  -H "Authorization: Bearer $TOKEN"
```

### Notes
```bash
# Create note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Database Concepts",
    "content": "Normalization, keys, relationships...",
    "category": "CS201",
    "tags": "database,sql,normalization",
    "color": "blue"
  }'

# Get all notes
curl -X GET http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer $TOKEN"

# Get pinned notes
curl -X GET http://localhost:8000/api/notes/pinned/ \
  -H "Authorization: Bearer $TOKEN"

# Toggle pin note
curl -X POST http://localhost:8000/api/notes/{id}/toggle_pin/ \
  -H "Authorization: Bearer $TOKEN"
```

### OJT
```bash
# Create OJT requirement
curl -X POST http://localhost:8000/api/ojt/requirements/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "company_name": "Tech Corp Inc",
    "position": "Junior Developer",
    "start_date": "2024-06-01",
    "end_date": "2024-08-31",
    "hours_required": 480,
    "supervisor_name": "Jane Smith",
    "supervisor_email": "jane@techcorp.com"
  }'

# Add OJT log
curl -X POST http://localhost:8000/api/ojt/logs/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ojt_requirement": 1,
    "date": "2024-07-15",
    "hours_worked": 8,
    "task_description": "Implemented user authentication"
  }'

# Get pending OJT approvals
curl -X GET http://localhost:8000/api/ojt/requirements/pending_approval/ \
  -H "Authorization: Bearer $TOKEN"

# Approve OJT
curl -X POST http://localhost:8000/api/ojt/requirements/{id}/approve/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"remarks": "Approved"}'
```

### Requirements
```bash
# Create requirement
curl -X POST http://localhost:8000/api/requirements/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "requirement_name": "Project Defense",
    "requirement_type": "project",
    "description": "Capstone project defense",
    "deadline": "2024-12-15",
    "is_mandatory": true,
    "semester": "Fall 2024"
  }'

# Get pending requirements
curl -X GET http://localhost:8000/api/requirements/pending/ \
  -H "Authorization: Bearer $TOKEN"

# Submit requirement
curl -X POST http://localhost:8000/api/requirements/{id}/submit/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "submission_date": "2024-07-15",
    "submission_notes": "Project submitted"
  }'

# Approve requirement
curl -X POST http://localhost:8000/api/requirements/{id}/approve/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"approval_notes": "Approved"}'
```

## User Roles

### Student Access
- View own tasks, grades, notes
- Create and manage own tasks
- View own OJT requirements
- Submit requirements
- Cannot modify others' data

### Instructor Access
- View assigned students
- Input and modify grades
- View student tasks
- Approve OJT submissions
- Approve requirements

### Admin Access
- Full system access
- User management
- View all data
- System configuration
- Data analytics

## Database Configuration

### PostgreSQL (Recommended)
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=student_management_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### SQLite (Development)
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

## Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test users
python manage.py test tasks
python manage.py test grades

# Run with verbosity
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Docker Commands

```bash
# Build and run
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access shell
docker-compose exec web python manage.py shell
```

## Useful Management Commands

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Flush database
python manage.py flush

# Access Django shell
python manage.py shell

# Run tests
python manage.py test

# Generate fixture
python manage.py dumpdata > fixture.json

# Load fixture
python manage.py loaddata fixture.json
```

## Admin Panel URLs

- Dashboard: http://localhost:8000/admin/
- Users: http://localhost:8000/admin/users/customuser/
- Tasks: http://localhost:8000/admin/tasks/task/
- Grades: http://localhost:8000/admin/grades/grade/
- Notes: http://localhost:8000/admin/notes/note/
- OJT: http://localhost:8000/admin/ojt/ojtrequirement/
- Requirements: http://localhost:8000/admin/requirements_app/schoolrequirement/

## Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database connection error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Module not found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Migration issues
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Important URLs

- API Base: http://localhost:8000/api/
- Swagger Docs: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/
- Admin: http://localhost:8000/admin/
- API Schema: http://localhost:8000/api/schema/

## API Response Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Successful with no content
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Server Error`: Internal error

## Useful Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/
- JWT: https://jwt.io/
