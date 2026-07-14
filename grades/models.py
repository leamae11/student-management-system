from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Grade(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades', limit_choices_to={'role': 'student'})
    subject = models.CharField(max_length=255)
    course_code = models.CharField(max_length=50, blank=True)
    grade = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])
    semester = models.CharField(max_length=50)
    instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='taught_grades', limit_choices_to={'role': 'instructor'})
    date_issued = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grades'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        unique_together = ('student', 'subject', 'semester')
    
    def __str__(self):
        return f"{self.student.username} - {self.subject} ({self.grade})"
