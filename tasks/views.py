from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Task, TaskReminder
from .serializers import TaskSerializer, TaskReminderSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']
    ordering = ['-due_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()
        return Task.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        tasks = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        tasks = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        tasks = self.get_queryset().filter(due_date__lt=timezone.now(), status__in=['pending', 'in_progress'])
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.status = 'completed'
        task.save()
        return Response({'detail': 'Task marked as completed.'})
