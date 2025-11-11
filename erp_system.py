from models.users import Admin, Professor, Student
from models.academics import Enrollment, Grade

class CollegeERPSystem:
    def __init__(self):
        # Simulated Database
        self.users = {}
        self.courses = {}
        self.enrollments = []
        self.grades = []

    # --- Authentication ---
    def login(self, user_id, password):
        """Implements Login sequence."""
        user = self.users.get(user_id)
        if user and user.password == password:
            print(f"LOGIN SUCCESS: {user.role} {user.name} authenticated.")
            return user
        print("LOGIN FAILED: Invalid credentials.")
        return None

    # --- Admin Features ---
    def add_user(self, executor, user):
        """Implements Admin.addUser()."""
        if not isinstance(executor, Admin):
            return print("PERMISSION DENIED.")
        self.users[user.id] = user
        print(f"ADMIN: Added {user}")

    def add_course(self, executor, course):
        """Implements Admin.addCourse()."""
        if not isinstance(executor, Admin):
            return print("PERMISSION DENIED.")
        self.courses[course.id] = course
        print(f"ADMIN: Added {course}")

    # --- Student Features ---
    def view_available_courses(self, student):
        """Implements View Available Courses sequence."""
        if not isinstance(student, Student): return
        print(f"\n--- Courses Available for {student.name} ---")
        for c in self.courses.values():
            print(f"ID: {c.id} | Name: {c.name}")
        print("--------------------------------------------")

    def register_course(self, student, course_id):
        """Implements Request Registration sequence."""
        if not isinstance(student, Student): return
        if course_id not in self.courses:
            return print("ERROR: Course not found.")
        
        # Check strictly for existing enrollment to avoid duplicates
        if any(e.student_id == student.id and e.course_id == course_id for e in self.enrollments):
             return print("INFO: Already registered or pending.")

        # Create Enrollment with status="Pending"
        new_enrollment = Enrollment(student.id, course_id)
        self.enrollments.append(new_enrollment)
        print(f"REGISTRATION REQUEST: {student.id} for {course_id} -> Status: {new_enrollment.status}")

    def view_grades(self, student):
        """Implements Student.viewGrades()."""
        if not isinstance(student, Student): return
        print(f"\nGRADE REPORT: {student.name}")
        student_grades = [g for g in self.grades if g.student_id == student.id]
        for g in student_grades:
            print(f"Course: {g.course_id} | Grade: {g.grade_value}")
        if not student_grades: print("(No grades found)")
        print("-------------------------")

    # --- Professor Features ---
    def view_pending_registrations(self, professor):
        """Implements View Pending Registrations sequence."""
        if not isinstance(professor, Professor): return
        print(f"\n--- Pending Approvals for Prof. {professor.name} ---")
        # Filter for courses this professor coordinates
        for e in self.enrollments:
            course = self.courses[e.course_id]
            if course.coordinator_id == professor.id and e.status == "Pending":
                 print(f"Student: {e.student_id} | Course: {e.course_id}")
        print("----------------------------------------------------")

    def approve_registration(self, professor, student_id, course_id):
        """Implements Approve Registration sequence."""
        if not isinstance(professor, Professor): return
        
        course = self.courses.get(course_id)
        if course.coordinator_id != professor.id:
            return print("ERROR: You are not the coordinator for this course.")

        for e in self.enrollments:
            if e.student_id == student_id and e.course_id == course_id and e.status == "Pending":
                e.status = "Enrolled"
                print(f"APPROVAL: {student_id} is now ENROLLED in {course_id}")
                return
        print("ERROR: No pending registration found matching criteria.")

    def upload_grade(self, professor, student_id, course_id, grade_val):
        """Implements Professor.uploadGrades()."""
        if not isinstance(professor, Professor): return
        
        # Ensure student is officially enrolled before grading
        is_enrolled = any(e.student_id == student_id and e.course_id == course_id and e.status == "Enrolled" for e in self.enrollments)
        if not is_enrolled:
             return print("ERROR: Cannot grade: Student is not enrolled.")

        grade = Grade(student_id, course_id, grade_val)
        self.grades.append(grade)
        print(f"GRADE UPLOADED: {student_id} -> {grade_val} in {course_id}")