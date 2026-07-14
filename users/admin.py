from django.contrib import admin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number')}),
        ('Profile', {'fields': ('role', 'student_id', 'bio', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'semester', 'gpa', 'is_active']
    list_filter = ['department', 'semester', 'is_active']
    search_fields = ['user__username', 'department']
    readonly_fields = ['created_at', 'updated_at']
