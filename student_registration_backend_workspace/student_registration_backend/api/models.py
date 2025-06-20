from django.db import models
from django.contrib.auth.models import AbstractUser


# PUBLIC_INTERFACE
class User(AbstractUser):
    """
    Custom User model extending Django AbstractUser.
    Used for authentication and related to Student profile.
    """
    # Username and password are inherited
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# PUBLIC_INTERFACE
class Student(models.Model):
    """
    Represents a student profile linked 1-1 with a User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(verbose_name="Date of Birth")
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


# PUBLIC_INTERFACE
class Course(models.Model):
    """
    Represents a course that students can enroll in.
    """
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    credits = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"


# PUBLIC_INTERFACE
class Enrollment(models.Model):
    """
    Represents an enrollment record linking a Student to a Course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} -> {self.course}"
