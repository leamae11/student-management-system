from django.db import models
from users.models import CustomUser

class SchoolRequirement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('exempted', 'Exempted'),
        ('approved', 'Approved'),
    ]
    
    REQUIREMENT_TYPE = [
        ('document', 'Document'),
        ('certificate', 'Certificate'),
        ('course', 'Course'),
        ('exam', 'Exam'),
        ('project', 'Project'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='school_requirements',
                               limit_choices_to={'role': 'student'})
    requirement_name = models.CharField(max_length=255)
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_mandatory = models.BooleanField(default=True)
    semester = models.CharField(max_length=50, blank=True)
    
    # Submission details
    submission_date = models.DateField(null=True, blank=True)
    submission_notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='approved_requirements', limit_choices_to={'role': 'instructor'})
    approval_date = models.DateField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'school_requirements'
        verbose_name = 'School Requirement'
        verbose_name_plural = 'School Requirements'
        unique_together = ('student', 'requirement_name', 'semester')
    
    def __str__(self):
        return f"{self.requirement_name} - {self.student.username}"
    
    def is_overdue(self):
        from django.utils import timezone
        return self.deadline < timezone.now().date() and self.status != 'completed'


class RequirementFile(models.Model):
    requirement = models.ForeignKey(SchoolRequirement, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='requirement_files/')
    file_type = models.CharField(max_length=50, blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'requirement_files'
        verbose_name = 'Requirement File'
        verbose_name_plural = 'Requirement Files'
    
    def __str__(self):
        return f"File for {self.requirement.requirement_name}"
