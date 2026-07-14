from django.contrib import admin
from .models import OJTRequirement, OJTLog

class OJTLogInline(admin.TabularInline):
    model = OJTLog
    extra = 1

@admin.register(OJTRequirement)
class OJTRequirementAdmin(admin.ModelAdmin):
    list_display = ['student', 'company_name', 'position', 'hours_completed', 'hours_required', 'status']
    list_filter = ['status', 'start_date', 'end_date', 'company_name']
    search_fields = ['student__username', 'company_name', 'supervisor_name']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']
    inlines = [OJTLogInline]
    fieldsets = (
        ('Student & Company Info', {
            'fields': ('student', 'company_name', 'position', 'supervisor_name', 'supervisor_email', 'supervisor_phone')
        }),
        ('Dates & Hours', {
            'fields': ('start_date', 'end_date', 'hours_required', 'hours_completed', 'progress_percentage')
        }),
        ('Status & Approval', {
            'fields': ('status', 'approved_by', 'approval_date', 'remarks')
        }),
        ('Additional Info', {
            'fields': ('description', 'created_at', 'updated_at')
        }),
    )

@admin.register(OJTLog)
class OJTLogAdmin(admin.ModelAdmin):
    list_display = ['ojt_requirement', 'date', 'hours_worked', 'verified']
    list_filter = ['verified', 'date', 'ojt_requirement__student']
    search_fields = ['ojt_requirement__student__username', 'task_description']
    readonly_fields = ['created_at', 'updated_at']
