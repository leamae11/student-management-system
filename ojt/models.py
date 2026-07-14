from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator
from datetime import timedelta

class OJTRequirement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ojt_requirements', 
                               limit_choices_to={'role': 'student'})
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    hours_required = models.IntegerField(default=480, validators=[MinValueValidator(1)])
    hours_completed = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    supervisor_name = models.CharField(max_length=255, blank=True)
    supervisor_email = models.EmailField(blank=True)
    supervisor_phone = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='approved_ojt', limit_choices_to={'role': 'instructor'})
    approval_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ojt_requirements'
        verbose_name = 'OJT Requirement'
        verbose_name_plural = 'OJT Requirements'
        unique_together = ('student', 'company_name', 'start_date')
    
    def __str__(self):
        return f"OJT - {self.student.username} at {self.company_name}"
    
    def get_progress_percentage(self):
        if self.hours_required == 0:
            return 0
        return round((self.hours_completed / self.hours_required) * 100, 2)
    
    def is_completed(self):
        return self.hours_completed >= self.hours_required
    
    def days_remaining(self):
        from django.utils import timezone
        today = timezone.now().date()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days


class OJTLog(models.Model):
    ojt_requirement = models.ForeignKey(OJTRequirement, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    hours_worked = models.FloatField(validators=[MinValueValidator(0.5)])
    task_description = models.TextField()
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ojt_logs'
        verbose_name = 'OJT Log'
        verbose_name_plural = 'OJT Logs'
        ordering = ['-date']
    
    def __str__(self):
        return f"OJT Log - {self.ojt_requirement.student.username} on {self.date}"
