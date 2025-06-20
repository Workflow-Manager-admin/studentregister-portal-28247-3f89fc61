from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Student, Course, Enrollment


# PUBLIC_INTERFACE
class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user."""
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_student=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# PUBLIC_INTERFACE
class LoginSerializer(serializers.Serializer):
    """Serializer for user authentication (login)."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        return {'user': user}


# PUBLIC_INTERFACE
class StudentSerializer(serializers.ModelSerializer):
    """Serializer for student profile management."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'first_name', 'last_name', 'dob', 'student_id']


# PUBLIC_INTERFACE
class CourseSerializer(serializers.ModelSerializer):
    """Serializer for course representation."""

    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'credits']


# PUBLIC_INTERFACE
class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for course enrollment."""

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']
        read_only_fields = ['enrollment_date']

    def validate(self, attrs):
        # Prevent duplicate enrollment
        if Enrollment.objects.filter(student=attrs['student'], course=attrs['course']).exists():
            raise serializers.ValidationError("Student is already enrolled in this course.")
        return attrs
