from rest_framework import serializers
from .models import SchoolRequirement, RequirementFile

class RequirementFileSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = RequirementFile
        fields = ['id', 'file', 'file_type', 'uploaded_by', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class SchoolRequirementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    is_overdue = serializers.SerializerMethodField()
    files = RequirementFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = SchoolRequirement
        fields = ['id', 'student', 'student_name', 'requirement_name', 'requirement_type',
                  'description', 'deadline', 'status', 'is_mandatory', 'semester',
                  'submission_date', 'submission_notes', 'approved_by', 'approved_by_name',
                  'approval_date', 'approval_notes', 'is_overdue', 'files',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'is_overdue', 'created_at', 'updated_at']
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()
