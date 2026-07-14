from django.contrib import admin
from .models import Task, TaskReminder

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'priority', 'due_date']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TaskReminder)
class TaskReminderAdmin(admin.ModelAdmin):
    list_display = ['task', 'reminder_time', 'is_sent']
    list_filter = ['is_sent', 'created_at']
    readonly_fields = ['created_at']
