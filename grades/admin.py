from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'grade', 'semester', 'instructor']
    list_filter = ['semester', 'date_issued', 'grade']
    search_fields = ['student__username', 'subject', 'course_code']
    readonly_fields = ['date_issued', 'created_at', 'updated_at']
