from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
        ('dept_head', 'Department Head'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def get_gpa(self):
        """Calculate GPA from grades"""
        from grades.models import Grade
        grades = Grade.objects.filter(student=self)
        if not grades.exists():
            return 0.0
        total = sum(grade.grade for grade in grades)
        return round(total / grades.count(), 2)


class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=100, blank=True)
    semester = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    gpa = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile of {self.user.username}"
