# Project Architecture

## System Architecture

```
┌─────────────────────────────────────────┐
│      Client Layer (Frontend)            │
└────────────────┬────────────────────────┘
                 │ HTTP/HTTPS
                 ↓
┌─────────────────────────────────────────┐
│    Django REST Framework API Layer      │
│  (ViewSets, Serializers, Permissions)   │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│      Django ORM (Models Layer)          │
│  Users, Tasks, Grades, Notes, OJT, etc. │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│    PostgreSQL Database Layer            │
└─────────────────────────────────────────┘
```

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Token-based)
- **API Documentation**: Swagger/OpenAPI
- **Deployment**: Docker + Gunicorn + Nginx

## App Structure

- **users**: User management and authentication
- **tasks**: Task/assignment management
- **grades**: Grade tracking and GPA calculation
- **notes**: Notes organizer with attachments
- **ojt**: On-the-Job Training tracking
- **requirements_app**: School requirements management

## Permission Model

- **Student**: View and manage own data only
- **Instructor**: View student data, approve submissions
- **Admin**: Full system access
- **Department Head**: View all students, generate reports