from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import SchoolRequirement, RequirementFile
from .serializers import SchoolRequirementSerializer, RequirementFileSerializer

class SchoolRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolRequirementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'requirement_type', 'is_mandatory', 'semester']
    search_fields = ['requirement_name', 'description', 'student__username']
    ordering_fields = ['deadline', 'status', 'created_at']
    ordering = ['deadline']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'dept_head':
            return SchoolRequirement.objects.all()
        elif user.role == 'instructor':
            return SchoolRequirement.objects.filter(approved_by=user) | SchoolRequirement.objects.filter(status='pending')
        return SchoolRequirement.objects.filter(student=user)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit requirement"""
        requirement = self.get_object()
        from django.utils import timezone
        
        requirement.status = 'in_progress'
        requirement.submission_date = request.data.get('submission_date', timezone.now().date())
        requirement.submission_notes = request.data.get('submission_notes', '')
        requirement.save()
        
        return Response({'detail': 'Requirement submitted successfully.'})
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve requirement"""
        requirement = self.get_object()
        if request.user.role not in ['instructor', 'admin', 'dept_head']:
            return Response({'error': 'Only instructors/admins can approve.'}, status=status.HTTP_403_FORBIDDEN)
        
        from django.utils import timezone
        requirement.status = 'approved'
        requirement.approved_by = request.user
        requirement.approval_date = timezone.now().date()
        requirement.approval_notes = request.data.get('approval_notes', '')
        requirement.save()
        
        return Response({'detail': 'Requirement approved successfully.'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject requirement"""
        requirement = self.get_object()
        if request.user.role not in ['instructor', 'admin', 'dept_head']:
            return Response({'error': 'Only instructors/admins can reject.'}, status=status.HTTP_403_FORBIDDEN)
        
        requirement.status = 'pending'
        requirement.approval_notes = request.data.get('approval_notes', '')
        requirement.save()
        
        return Response({'detail': 'Requirement rejected. Please resubmit.'})
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending requirements"""
        requirements = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(requirements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue requirements"""
        from django.utils import timezone
        today = timezone.now().date()
        requirements = self.get_queryset().filter(deadline__lt=today, status__in=['pending', 'in_progress'])
        serializer = self.get_serializer(requirements, many=True)
        return Response(serializer.data)
