from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    RegisterView, LoginView, logout_view,
    StudentViewSet, CourseViewSet, EnrollmentViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('health/', health, name='Health'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', logout_view, name='user-logout'),
    path('', include(router.urls)),
]
