# API Documentation

## Overview

This document provides comprehensive API documentation for the CS Student Dashboard system. All endpoints are RESTful and require JWT authentication (except for registration and login).

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All endpoints except `/users/register/` and `/users/login/` require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

---

## Users API

### Register User

**POST** `/users/register/`

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "secure_password_123",
  "password2": "secure_password_123",
  "role": "student"
}
```

**Response (201 Created):**
```json
{
  "detail": "User registered successfully.",
  "user_id": 1
}
```

---

### Login User

**POST** `/users/login/`

```json
{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "student_id": null,
    "phone_number": "",
    "bio": "",
    "date_of_birth": null,
    "gpa": 0.0,
    "created_at": "2024-07-14T10:00:00Z"
  }
}
```

---

### Get User Profile

**GET** `/users/profile/`

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "student_id": "CS2024001",
  "phone_number": "555-0123",
  "bio": "Computer Science Student",
  "date_of_birth": "2000-01-15",
  "gpa": 3.75,
  "created_at": "2024-07-14T10:00:00Z"
}
```

---

### Update User Profile

**PUT** `/users/update_profile/`

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "555-9876",
  "bio": "Updated bio"
}
```

---

## Tasks API

### Create Task

**POST** `/tasks/`

```json
{
  "title": "Complete Project Proposal",
  "description": "Finish the project proposal for CS301",
  "due_date": "2024-08-15T23:59:59Z",
  "priority": "high",
  "status": "pending",
  "category": "academics"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete Project Proposal",
  "description": "Finish the project proposal for CS301",
  "due_date": "2024-08-15T23:59:59Z",
  "priority": "high",
  "status": "pending",
  "category": "academics",
  "is_completed": false,
  "reminders": [],
  "created_at": "2024-07-14T10:30:00Z",
  "updated_at": "2024-07-14T10:30:00Z"
}
```

---

### Get All Tasks

**GET** `/tasks/`

**Query Parameters:**
- `status`: pending, in_progress, completed, cancelled
- `priority`: low, medium, high
- `category`: filter by category
- `search`: search in title and description
- `ordering`: -due_date, -created_at, priority

**Example:**
```
GET /tasks/?status=pending&priority=high&ordering=-due_date
```

---

### Get Pending Tasks

**GET** `/tasks/pending/`

---

### Get Completed Tasks

**GET** `/tasks/completed/`

---

### Get Overdue Tasks

**GET** `/tasks/overdue/`

---

### Mark Task as Complete

**POST** `/tasks/{id}/mark_complete/`

**Response (200 OK):**
```json
{
  "detail": "Task marked as completed."
}
```

---

## Grades API

### Create Grade

**POST** `/grades/`

```json
{
  "student": 1,
  "subject": "Data Structures",
  "course_code": "CS201",
  "grade": 3.8,
  "semester": "Fall 2024"
}
```

---

### Get All Grades

**GET** `/grades/`

**Query Parameters:**
- `student`: filter by student ID
- `semester`: filter by semester
- `subject`: filter by subject

---

### Get GPA

**GET** `/grades/gpa/`

**Response (200 OK):**
```json
{
  "gpa": 3.75,
  "total_grades": 8,
  "semester": "all"
}
```

---

### Get Grades by Semester

**GET** `/grades/by_semester/?semester=Fall%202024`

---

## Notes API

### Create Note

**POST** `/notes/`

```json
{
  "title": "Database Design Concepts",
  "content": "Notes about normalization, primary keys...",
  "category": "CS201",
  "tags": "database,sql,normalization",
  "color": "blue"
}
```

---

### Get All Notes

**GET** `/notes/`

**Query Parameters:**
- `category`: filter by category
- `is_pinned`: true or false
- `color`: yellow, blue, green, red, purple, pink
- `search`: search in title, content, tags

---

### Get Pinned Notes

**GET** `/notes/pinned/`

---

### Get Notes by Category

**GET** `/notes/by_category/?category=CS201`

---

### Toggle Pin Note

**POST** `/notes/{id}/toggle_pin/`

---

### Search Notes by Tag

**GET** `/notes/search/?tag=database`

---

## OJT API

### Create OJT Requirement

**POST** `/ojt/requirements/`

```json
{
  "student": 1,
  "company_name": "Tech Solutions Inc.",
  "position": "Junior Developer",
  "start_date": "2024-06-01",
  "end_date": "2024-08-31",
  "hours_required": 480,
  "supervisor_name": "Jane Smith",
  "supervisor_email": "jane.smith@techsolutions.com",
  "supervisor_phone": "555-0456",
  "description": "Web development project"
}
```

---

### Get All OJT Requirements

**GET** `/ojt/requirements/`

---

### Get Pending OJT

**GET** `/ojt/requirements/pending_approval/`

---

### Approve OJT

**POST** `/ojt/requirements/{id}/approve/`

```json
{
  "remarks": "Approved. All requirements met."
}
```

---

### Add OJT Log

**POST** `/ojt/logs/`

```json
{
  "ojt_requirement": 1,
  "date": "2024-07-14",
  "hours_worked": 8,
  "task_description": "Implemented user authentication module"
}
```

---

### Verify OJT Log

**POST** `/ojt/logs/{id}/verify/`

---

## Requirements API

### Create School Requirement

**POST** `/requirements/`

```json
{
  "student": 1,
  "requirement_name": "Project Defense",
  "requirement_type": "project",
  "description": "Final year capstone project defense",
  "deadline": "2024-12-15",
  "is_mandatory": true,
  "semester": "Fall 2024"
}
```

---

### Get All Requirements

**GET** `/requirements/`

---

### Get Pending Requirements

**GET** `/requirements/pending/`

---

### Get Overdue Requirements

**GET** `/requirements/overdue/`

---

### Submit Requirement

**POST** `/requirements/{id}/submit/`

```json
{
  "submission_date": "2024-07-14",
  "submission_notes": "Project submitted with documentation"
}
```

---

### Approve Requirement

**POST** `/requirements/{id}/approve/`

```json
{
  "approval_notes": "All requirements met and approved."
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Example:**
```
GET /tasks/?page=2&page_size=20
```

**Response includes:**
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Rate Limiting

API rate limiting will be implemented to prevent abuse. Current limits (to be configured):
- 100 requests per hour per user

---

## Versioning

Current API Version: **1.0.0**

---

For more details, visit the interactive API documentation at:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
