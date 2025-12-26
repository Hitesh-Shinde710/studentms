from django.urls import path
from . import views
from rest_framework import routers
from .api_views import StudentViewSet, CourseViewSet, EnrollmentViewSet
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),

    
    path('students/', views.student_list, name='student_list'),
    path('courses/', views.course_list, name='course_list'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    
    path('students/add/', views.add_student, name='add_student'),
    path('courses/add/', views.add_course, name='add_course'),
    path('enrollments/add/', views.add_enrollment, name='add_enrollment'),
    
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('courses/edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('enrollments/edit/<int:pk>/', views.edit_enrollment, name='edit_enrollment'),
    
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('enrollments/delete/<int:pk>/', views.delete_enrollment, name='delete_enrollment'),
    
    
    path('export/students/', views.export_students_csv, name='export_students_csv'),
    path('export/courses/', views.export_courses_csv, name='export_courses_csv'),
    path('export/enrollments/', views.export_enrollments_csv, name='export_enrollments_csv'),


]

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns += router.urls
