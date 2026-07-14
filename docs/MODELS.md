# Database Models Documentation

## User Management (users app)

### CustomUser
Extended Django User model with additional fields:
- `role`: Student, Instructor, Admin, Department Head
- `student_id`: Unique student identifier
- `phone_number`: Contact number
- `profile_picture`: User avatar
- `bio`: User biography
- `date_of_birth`: Birth date
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

**Methods:**
- `get_gpa()`: Calculate GPA from student grades

### UserProfile
Extended profile information:
- `department`: Department name
- `semester`: Current semester (1-8)
- `gpa`: Current GPA
- `is_active`: Account status
- `last_login_ip`: Last login IP address

---

## Task Management (tasks app)

### Task
Task/Assignment management:
- `title`: Task title
- `description`: Task description
- `due_date`: Due date and time
- `priority`: Low, Medium, High
- `status`: Pending, In Progress, Completed, Cancelled
- `category`: Task category/course
- `is_completed`: Completion flag
- `user`: Foreign key to CustomUser

**Choices:**
```python
PRIORITY_CHOICES = ['low', 'medium', 'high']
STATUS_CHOICES = ['pending', 'in_progress', 'completed', 'cancelled']
```

### TaskReminder
Reminders for tasks:
- `task`: Foreign key to Task
- `reminder_time`: When to remind
- `is_sent`: Reminder status
- `created_at`: Creation timestamp

---

## Grade Management (grades app)

### Grade
Academic grades:
- `student`: Foreign key to Student (CustomUser)
- `subject`: Subject/Course name
- `course_code`: Course code
- `grade`: Numerical grade (0.0-4.0)
- `semester`: Semester identifier
- `instructor`: Foreign key to Instructor (CustomUser)
- `date_issued`: Grade issue date

**Constraints:**
- Unique per (student, subject, semester)
- Grade range: 0.0 to 4.0

---

## Notes (notes app)

### Note
Note-taking system:
- `title`: Note title
- `content`: Note content
- `category`: Subject/course
- `tags`: Comma-separated tags
- `is_pinned`: Pin status
- `color`: Visual color (yellow, blue, green, red, purple, pink)
- `user`: Foreign key to CustomUser

**Methods:**
- `get_tags_list()`: Parse tags into list

### NoteAttachment
File attachments for notes:
- `note`: Foreign key to Note
- `file`: Attached file
- `file_type`: File MIME type
- `uploaded_at`: Upload timestamp

---

## OJT Management (ojt app)

### OJTRequirement
On-the-Job Training tracking:
- `student`: Foreign key to Student
- `company_name`: Company name
- `position`: Job position
- `start_date`: OJT start date
- `end_date`: OJT end date
- `hours_required`: Total hours needed (default: 480)
- `hours_completed`: Completed hours
- `status`: Pending, In Progress, Completed, Approved, Rejected
- `supervisor_name`: Supervisor name
- `supervisor_email`: Supervisor email
- `supervisor_phone`: Supervisor phone
- `approved_by`: Instructor who approved
- `approval_date`: Approval date
- `remarks`: Approval remarks

**Methods:**
- `get_progress_percentage()`: Calculate completion %
- `is_completed()`: Check if hours met
- `days_remaining()`: Days until end date

### OJTLog
Daily OJT work logs:
- `ojt_requirement`: Foreign key to OJTRequirement
- `date`: Work date
- `hours_worked`: Hours worked
- `task_description`: Description of work
- `verified`: Verification status
- `verified_by`: Instructor who verified

**Constraints:**
- Minimum 0.5 hours per log
- Unique per (requirement, date)

---

## School Requirements (requirements_app)

### SchoolRequirement
School/Department requirements:
- `student`: Foreign key to Student
- `requirement_name`: Requirement name
- `requirement_type`: Document, Certificate, Course, Exam, Project, Other
- `description`: Requirement description
- `deadline`: Submission deadline
- `status`: Pending, In Progress, Completed, Exempted, Approved
- `is_mandatory`: Required status
- `semester`: Semester
- `submission_date`: When submitted
- `submission_notes`: Submission details
- `approved_by`: Approver (Instructor)
- `approval_date`: Approval date
- `approval_notes`: Approval remarks

**Methods:**
- `is_overdue()`: Check if past deadline

### RequirementFile
Files for requirements:
- `requirement`: Foreign key to SchoolRequirement
- `file`: Uploaded file
- `file_type`: File type
- `uploaded_by`: User who uploaded
- `uploaded_at`: Upload timestamp

---

## Database Schema Summary

```
CustomUser (extends Django User)
├── UserProfile (1-to-1)
├── tasks (1-to-many)
├── grades (1-to-many)
├── notes (1-to-many)
├── ojt_requirements (1-to-many)
├── school_requirements (1-to-many)
├── taught_grades (1-to-many) [Instructor role]
├── approved_ojt (1-to-many) [Instructor role]
└── approved_requirements (1-to-many) [Instructor role]

Task
└── reminders (1-to-many)

Note
└── attachments (1-to-many)

OJTRequirement
└── logs (1-to-many)

SchoolRequirement
└── files (1-to-many)
```

---

## Relationships Overview

### Many-to-One Relationships
- Task → CustomUser (user)
- Grade → CustomUser (student and instructor)
- Note → CustomUser (user)
- OJTRequirement → CustomUser (student and approved_by)
- SchoolRequirement → CustomUser (student and approved_by)
- OJTLog → CustomUser (verified_by)

### One-to-One Relationships
- UserProfile ↔ CustomUser

### One-to-Many Relationships
- Task → TaskReminder
- Note → NoteAttachment
- OJTRequirement → OJTLog
- SchoolRequirement → RequirementFile

---

## Data Validation

### Grade Validation
- Grade must be between 0.0 and 4.0
- Unique combination of (student, subject, semester)

### OJT Validation
- Hours required minimum: 1
- Hours completed minimum: 0
- Unique combination of (student, company_name, start_date)

### UserProfile Validation
- Semester must be between 1 and 8
- GPA must be between 0.0 and 4.0

### TaskReminder Validation
- Reminder time must be before or on task due date

---

## Indexing Strategy

Recommended database indexes for performance:

```python
class Meta:
    indexes = [
        models.Index(fields=['user', '-created_at']),
        models.Index(fields=['status', 'due_date']),
        models.Index(fields=['student', 'semester']),
        models.Index(fields=['status', '-updated_at']),
    ]
```

---

## Audit Logging

All models include:
- `created_at`: Automatic timestamp on creation
- `updated_at`: Automatic timestamp on updates

Implement audit logs for sensitive operations (grades, approvals).

---

## Future Enhancements

1. Add activity logging model
2. Implement soft deletes
3. Add versioning for historical tracking
4. Implement change history tracking
5. Add notifications model
6. Add file storage system
