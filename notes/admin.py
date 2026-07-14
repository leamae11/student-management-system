from django.contrib import admin
from .models import Note, NoteAttachment

class NoteAttachmentInline(admin.TabularInline):
    model = NoteAttachment
    extra = 1

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'is_pinned', 'updated_at']
    list_filter = ['category', 'is_pinned', 'color', 'created_at']
    search_fields = ['title', 'content', 'user__username', 'tags']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [NoteAttachmentInline]

@admin.register(NoteAttachment)
class NoteAttachmentAdmin(admin.ModelAdmin):
    list_display = ['note', 'file_type', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['note__title']
    readonly_fields = ['uploaded_at']
