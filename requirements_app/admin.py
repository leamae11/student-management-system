from django.contrib import admin
from .models import SchoolRequirement, RequirementFile

class RequirementFileInline(admin.TabularInline):
    model = RequirementFile
    extra = 1

@admin.register(SchoolRequirement)
class SchoolRequirementAdmin(admin.ModelAdmin):
    list_display = ['requirement_name', 'student', 'requirement_type', 'status', 'deadline']
    list_filter = ['status', 'requirement_type', 'is_mandatory', 'deadline']
    search_fields = ['requirement_name', 'student__username', 'description']
    readonly_fields = ['created_at', 'updated_at', 'is_overdue']
    inlines = [RequirementFileInline]
    fieldsets = (
        ('Requirement Info', {
            'fields': ('student', 'requirement_name', 'requirement_type', 'description', 'is_mandatory')
        }),
        ('Dates & Status', {
            'fields': ('deadline', 'semester', 'status', 'is_overdue')
        }),
        ('Submission', {
            'fields': ('submission_date', 'submission_notes')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approval_date', 'approval_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(RequirementFile)
class RequirementFileAdmin(admin.ModelAdmin):
    list_display = ['requirement', 'file_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['requirement__requirement_name', 'uploaded_by__username']
    readonly_fields = ['uploaded_at']
