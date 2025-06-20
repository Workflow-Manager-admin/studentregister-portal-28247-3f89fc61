from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout

from .models import Student, Course, Enrollment
from .serializers import (
    UserRegisterSerializer, LoginSerializer,
    StudentSerializer, CourseSerializer, EnrollmentSerializer
)


@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
class RegisterView(generics.CreateAPIView):
    """
    Register a new User account.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )


# PUBLIC_INTERFACE
class LoginView(generics.GenericAPIView):
    """
    Authenticate (login) a user and return an authentication token.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({"token": token.key, "username": user.username})


# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Log out the user and delete token."""
    user = request.user
    Token.objects.filter(user=user).delete()
    logout(request)
    return Response({"message": "Logged out."}, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
class StudentViewSet(viewsets.ModelViewSet):
    """
    CRUD for student profiles. Only the student or admin can update data.
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Student.objects.all()
        return Student.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# PUBLIC_INTERFACE
class CourseViewSet(viewsets.ModelViewSet):
    """
    List, create, and retrieve courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# PUBLIC_INTERFACE
class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    List/create/delete enrollments for authenticated students.
    """
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Enrollment.objects.all()
        student = getattr(self.request.user, 'student_profile', None)
        if student:
            return Enrollment.objects.filter(student=student)
        return Enrollment.objects.none()

    def perform_create(self, serializer):
        student = getattr(self.request.user, 'student_profile', None)
        if not student:
            from rest_framework import serializers
            raise serializers.ValidationError('Student profile required.')
        serializer.save(student=student)
