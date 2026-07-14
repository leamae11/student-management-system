from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .models import Grade
from .serializers import GradeSerializer

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'semester', 'subject']
    search_fields = ['subject', 'course_code']
    ordering_fields = ['grade', 'semester', 'date_issued']
    ordering = ['-date_issued']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'dept_head':
            return Grade.objects.all()
        elif user.role == 'instructor':
            return Grade.objects.filter(instructor=user)
        return Grade.objects.filter(student=user)
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user if self.request.user.role == 'instructor' else None)
    
    @action(detail=False, methods=['get'])
    def gpa(self, request):
        """Calculate GPA for current user"""
        grades = self.get_queryset()
        if request.user.role == 'student':
            grades = grades.filter(student=request.user)
        
        if not grades.exists():
            return Response({'gpa': 0.0, 'total_grades': 0})
        
        avg_grade = grades.aggregate(Avg('grade'))['grade__avg']
        return Response({
            'gpa': round(avg_grade, 2),
            'total_grades': grades.count(),
            'semester': request.query_params.get('semester', 'all')
        })
    
    @action(detail=False, methods=['get'])
    def by_semester(self, request):
        """Get grades by semester"""
        semester = request.query_params.get('semester')
        if not semester:
            return Response({'error': 'Semester parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        grades = self.get_queryset().filter(semester=semester)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)
