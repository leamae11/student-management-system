from rest_framework import serializers
from .models import Note, NoteAttachment

class NoteAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteAttachment
        fields = ['id', 'file', 'file_type', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class NoteSerializer(serializers.ModelSerializer):
    attachments = NoteAttachmentSerializer(many=True, read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category', 'tags', 'tags_list', 'is_pinned', 
                  'color', 'attachments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
