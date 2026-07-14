from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import OJTRequirement, OJTLog
from .serializers import OJTRequirementSerializer, OJTLogSerializer

class OJTRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = OJTRequirementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'student', 'company_name']
    search_fields = ['company_name', 'position', 'student__username']
    ordering_fields = ['start_date', 'end_date', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'dept_head':
            return OJTRequirement.objects.all()
        elif user.role == 'instructor':
            return OJTRequirement.objects.filter(student__ojt_requirements__approved_by=user).distinct()
        return OJTRequirement.objects.filter(student=user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve OJT requirement"""
        ojt = self.get_object()
        if request.user.role not in ['instructor', 'admin', 'dept_head']:
            return Response({'error': 'Only instructors/admins can approve.'}, status=status.HTTP_403_FORBIDDEN)
        
        ojt.status = 'approved'
        ojt.approved_by = request.user
        ojt.approval_date = request.data.get('approval_date')
        ojt.remarks = request.data.get('remarks', '')
        ojt.save()
        return Response({'detail': 'OJT approved successfully.'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject OJT requirement"""
        ojt = self.get_object()
        if request.user.role not in ['instructor', 'admin', 'dept_head']:
            return Response({'error': 'Only instructors/admins can reject.'}, status=status.HTTP_403_FORBIDDEN)
        
        ojt.status = 'rejected'
        ojt.remarks = request.data.get('remarks', '')
        ojt.save()
        return Response({'detail': 'OJT rejected.'})
    
    @action(detail=False, methods=['get'])
    def pending_approval(self, request):
        """Get pending OJT requirements for approval"""
        ojts = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(ojts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get completed OJT requirements"""
        ojts = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(ojts, many=True)
        return Response(serializer.data)


class OJTLogViewSet(viewsets.ModelViewSet):
    serializer_class = OJTLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ojt_requirement', 'date', 'verified']
    ordering_fields = ['date', 'hours_worked']
    ordering = ['-date']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'dept_head':
            return OJTLog.objects.all()
        elif user.role == 'instructor':
            return OJTLog.objects.filter(ojt_requirement__approved_by=user)
        return OJTLog.objects.filter(ojt_requirement__student=user)
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify OJT log"""
        log = self.get_object()
        if request.user.role not in ['instructor', 'admin', 'dept_head']:
            return Response({'error': 'Only instructors/admins can verify.'}, status=status.HTTP_403_FORBIDDEN)
        
        log.verified = True
        log.verified_by = request.user
        log.save()
        
        # Update total hours in OJT requirement
        ojt = log.ojt_requirement
        ojt.hours_completed = ojt.logs.filter(verified=True).aggregate(
            models.Sum('hours_worked')
        )['hours_worked__sum'] or 0
        ojt.save()
        
        return Response({'detail': 'OJT log verified successfully.'})
