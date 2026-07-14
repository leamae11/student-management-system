from rest_framework import serializers
from .models import Task, TaskReminder

class TaskReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReminder
        fields = ['id', 'reminder_time', 'is_sent', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    reminders = TaskReminderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'due_date', 'priority', 
                  'status', 'category', 'is_completed', 'reminders', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
