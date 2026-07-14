from rest_framework import serializers
from .models import OJTRequirement, OJTLog

class OJTLogSerializer(serializers.ModelSerializer):
    verified_by_name = serializers.CharField(source='verified_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = OJTLog
        fields = ['id', 'ojt_requirement', 'date', 'hours_worked', 'task_description', 'verified', 
                  'verified_by', 'verified_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class OJTRequirementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    progress_percentage = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    logs = OJTLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = OJTRequirement
        fields = ['id', 'student', 'student_name', 'company_name', 'position', 'start_date', 'end_date',
                  'hours_required', 'hours_completed', 'status', 'supervisor_name', 'supervisor_email',
                  'supervisor_phone', 'description', 'approved_by', 'approved_by_name', 'approval_date',
                  'remarks', 'progress_percentage', 'is_completed', 'days_remaining', 'logs',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'progress_percentage', 'is_completed', 'days_remaining', 'created_at', 'updated_at']
    
    def get_progress_percentage(self, obj):
        return obj.get_progress_percentage()
    
    def get_is_completed(self, obj):
        return obj.is_completed()
    
    def get_days_remaining(self, obj):
        return obj.days_remaining()
