from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Note, NoteAttachment
from .serializers import NoteSerializer, NoteAttachmentSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_pinned', 'color']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'is_pinned']
    ordering = ['-is_pinned', '-updated_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Note.objects.all()
        return Note.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get notes by category"""
        category = request.query_params.get('category')
        if not category:
            return Response({'error': 'Category parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        notes = self.get_queryset().filter(category=category)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Get pinned notes"""
        notes = self.get_queryset().filter(is_pinned=True)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_pin(self, request, pk=None):
        """Toggle pin status of a note"""
        note = self.get_object()
        note.is_pinned = not note.is_pinned
        note.save()
        return Response({'detail': f"Note {'pinned' if note.is_pinned else 'unpinned'} successfully."})
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search notes by tag"""
        tag = request.query_params.get('tag')
        if not tag:
            return Response({'error': 'Tag parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        notes = self.get_queryset().filter(tags__icontains=tag)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)
