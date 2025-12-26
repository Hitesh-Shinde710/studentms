from django.core.management.base import BaseCommand
from students.models import Student, Course, Enrollment
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with sample students, courses, and enrollments'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Enrollment.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()

        # 1. Create Courses
        courses_data = [
            {"name": "Computer Science", "code": "CS101", "credits": 4},
            {"name": "Mathematics", "code": "MA102", "credits": 3},
            {"name": "Physics", "code": "PH103", "credits": 3},
            {"name": "Chemistry", "code": "CH104", "credits": 3},
            {"name": "English Literature", "code": "EN105", "credits": 2},
            {"name": "Economics", "code": "EC106", "credits": 3},
            {"name": "History", "code": "HI107", "credits": 2},
            {"name": "Biology", "code": "BI108", "credits": 3},
            {"name": "Political Science", "code": "PS109", "credits": 2},
            {"name": "Sociology", "code": "SO110", "credits": 2},
        ]
        courses = {}
        for data in courses_data:
            course = Course.objects.create(**data)
            courses[course.code] = course

        # 2. Create Students
        students_data = [
            {"first_name":"Aarav","last_name":"Sharma","email":"aarav.sharma@example.com","date_of_birth":date(2003,5,12)},
            {"first_name":"Ananya","last_name":"Gupta","email":"ananya.gupta@example.com","date_of_birth":date(2004,11,23)},
            {"first_name":"Rohan","last_name":"Iyer","email":"rohan.iyer@example.com","date_of_birth":date(2003,2,15)},
            {"first_name":"Priya","last_name":"Singh","email":"priya.singh@example.com","date_of_birth":date(2005,7,1)},
            {"first_name":"Aditya","last_name":"Kumar","email":"aditya.kumar@example.com","date_of_birth":date(2004,9,17)},
            {"first_name":"Sneha","last_name":"Reddy","email":"sneha.reddy@example.com","date_of_birth":date(2003,12,5)},
            {"first_name":"Kabir","last_name":"Mehta","email":"kabir.mehta@example.com","date_of_birth":date(2005,3,20)},
            {"first_name":"Ishita","last_name":"Nair","email":"ishita.nair@example.com","date_of_birth":date(2004,8,14)},
            {"first_name":"Arjun","last_name":"Patel","email":"arjun.patel@example.com","date_of_birth":date(2003,1,30)},
            {"first_name":"Kiara","last_name":"Joshi","email":"kiara.joshi@example.com","date_of_birth":date(2005,6,12)},
            {"first_name":"Vihaan","last_name":"Verma","email":"vihaan.verma@example.com","date_of_birth":date(2004,4,22)},
            {"first_name":"Riya","last_name":"Choudhary","email":"riya.choudhary@example.com","date_of_birth":date(2003,10,9)},
            {"first_name":"Yash","last_name":"Bansal","email":"yash.bansal@example.com","date_of_birth":date(2004,2,28)},
            {"first_name":"Meera","last_name":"Kapoor","email":"meera.kapoor@example.com","date_of_birth":date(2005,12,1)},
            {"first_name":"Arnav","last_name":"Desai","email":"arnav.desai@example.com","date_of_birth":date(2003,9,15)},
        ]
        students = {}
        for data in students_data:
            student = Student.objects.create(**data)
            students[student.email] = student

        # 3. Create Enrollments
        enrollments_data = [
            ("aarav.sharma@example.com","CS101","A"),
            ("ananya.gupta@example.com","MA102","B"),
            ("rohan.iyer@example.com","PH103","A-"),
            ("priya.singh@example.com","EN105","B+"),
            ("aditya.kumar@example.com","CS101","A"),
            ("sneha.reddy@example.com","BI108","B"),
            ("kabir.mehta@example.com","CH104","A-"),
            ("ishita.nair@example.com","MA102","B+"),
            ("arjun.patel@example.com","PH103","B"),
            ("kiara.joshi@example.com","EN105","A"),
            ("vihaan.verma@example.com","CS101","B+"),
            ("riya.choudhary@example.com","EC106","A"),
            ("yash.bansal@example.com","HI107","B"),
            ("meera.kapoor@example.com","SO110","A-"),
            ("arnav.desai@example.com","PS109","B+"),
        ]
        for email, code, grade in enrollments_data:
            Enrollment.objects.create(student=students[email], course=courses[code], grade=grade)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
