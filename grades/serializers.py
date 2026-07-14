from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'subject', 'course_code', 'grade', 
                  'semester', 'instructor', 'instructor_name', 'date_issued', 'created_at', 'updated_at']
        read_only_fields = ['id', 'date_issued', 'created_at', 'updated_at']
