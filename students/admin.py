from django.contrib import admin
from .models import Student, Course, Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('enrollment_date',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits')
    search_fields = ('name', 'code')
    list_filter = ('credits',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'grade')
    search_fields = ('student__first_name', 'student__last_name', 'course__name', 'course__code')
    list_filter = ('enrollment_date', 'course')
