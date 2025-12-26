import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import Student, Course, Enrollment
from django.shortcuts import redirect
from .forms import StudentForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .forms import StudentForm, CourseForm, EnrollmentForm




def home(request):
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
    }
    return render(request, 'students/home.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
   
@login_required
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Date of Birth', 'Enrollment Date'])

    for student in Student.objects.all():
        writer.writerow([
            student.id,
            student.first_name,
            student.last_name,
            student.email,
            student.date_of_birth,
            student.enrollment_date
        ])

    return response


@login_required
def export_courses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=courses.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Code', 'Name', 'Description', 'Credits'])

    for course in Course.objects.all():
        writer.writerow([
            course.id,
            course.code,
            course.name,
            course.description,
            course.credits
        ])

    return response


@login_required
def export_enrollments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=enrollments.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Student', 'Course', 'Enrollment Date', 'Grade'])

    for enrollment in Enrollment.objects.all():
        writer.writerow([
            enrollment.id,
            f"{enrollment.student.first_name} {enrollment.student.last_name}",
            enrollment.course.name,
            enrollment.enrollment_date,
            enrollment.grade if enrollment.grade else ''
        ])

    return response

# Students
@login_required
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Student.objects.filter(
        Q(name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone__icontains=search_query)
    ) if search_query else Student.objects.all()
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'students/student_list.html', {'page_obj': page_obj, 'search_query': search_query})

# Courses
@login_required
def course_list(request):
    search_query = request.GET.get('search', '')
    courses = Course.objects.filter(
        Q(name__icontains=search_query) |
        Q(code__icontains=search_query)
    ) if search_query else Course.objects.all()
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'students/course_list.html', {'page_obj': page_obj, 'search_query': search_query})

# Enrollments
@login_required
def enrollment_list(request):
    search_query = request.GET.get('search', '')
    enrollments = Enrollment.objects.filter(
        Q(student__name__icontains=search_query) |
        Q(course__name__icontains=search_query)
    ) if search_query else Enrollment.objects.all()
    paginator = Paginator(enrollments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'students/enrollment_list.html', {'page_obj': page_obj, 'search_query': search_query})

@staff_member_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

@staff_member_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})

@staff_member_required
def add_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment added successfully!")
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'students/add_enrollment.html', {'form': form})

@staff_member_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student edited successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

@staff_member_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course edited successfully!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'students/edit_course.html', {'form': form, 'course': course})

@staff_member_required
def edit_enrollment(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment edited successfully!")
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'students/edit_enrollment.html', {'form': form, 'enrollment': enrollment})

# Delete student
@staff_member_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')
    return render(request, 'students/delete_student.html', {'student': student})



# Delete course
@staff_member_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'students/delete_course.html', {'course': course})



# Delete enrollment
@staff_member_required
def delete_enrollment(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, "Enrollment deleted successfully!")
        return redirect('enrollment_list')
    return render(request, 'students/delete_enrollment.html', {'enrollment': enrollment})
