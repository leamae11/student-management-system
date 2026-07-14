from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile

class UserSerializer(serializers.ModelSerializer):
    gpa = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                  'student_id', 'phone_number', 'bio', 'date_of_birth', 'gpa', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_gpa(self, obj):
        return obj.get_gpa()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2', 'role']
    
    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'department', 'semester', 'gpa', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
