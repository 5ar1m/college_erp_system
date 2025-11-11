import unittest
from erp_system import CollegeERPSystem
from models.users import Admin, Professor, Student
from models.academics import Course, Enrollment

class TestProfessorEntity(unittest.TestCase):

    def setUp(self):
        self.erp = CollegeERPSystem()
        self.admin = Admin("ADMIN_1", "Admin One", "admin_pass")
        self.erp.users[self.admin.id] = self.admin

        self.prof = Professor("PROF_1", "Professor One", "prof_pass", branch="Branch A")
        self.student = Student("STUDENT_1", "Student One", "stud_pass", branch="Branch A")
        self.course = Course("COURSE_1", "Course One", coordinator_id="PROF_1")

        self.erp.add_user(self.admin, self.prof)
        self.erp.add_user(self.admin, self.student)
        self.erp.add_course(self.admin, self.course)

        self.erp.enrollments = [Enrollment(self.student.id, self.course.id)]

    def test_professor_login_success(self):
        print("\n[TEST] Professor Login Success")
        user = self.erp.login("PROF_1", "prof_pass")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "Professor")
        self.assertEqual(user.id, "PROF_1")

    def test_professor_login_failure(self):
        print("\n[TEST] Professor Login Failure")
        user = self.erp.login("PROF_1", "wrong_pass")
        self.assertIsNone(user)

    def test_view_pending_registrations(self):
        print("\n[TEST] View Pending Registrations")
        self.erp.view_pending_registrations(self.prof)

    def test_approve_registration(self):
        print("\n[TEST] Approve Registration")
        self.assertEqual(self.erp.enrollments[0].status, "Pending")
        
        self.erp.approve_registration(self.prof, "STUDENT_1", "COURSE_1")
        
        self.assertEqual(self.erp.enrollments[0].status, "Enrolled")

    def test_approve_registration_unauthorized(self):
        print("\n[TEST] Unauthorized Approval Attempt")
        other_prof = Professor("PROF_2", "Professor Two", "prof_pass_2", branch="Branch B")
        self.erp.approve_registration(other_prof, "STUDENT_1", "COURSE_1")
        
        self.assertEqual(self.erp.enrollments[0].status, "Pending")

    def test_upload_grade(self):
        print("\n[TEST] Upload Grade")
        self.erp.enrollments[0].status = "Enrolled"
        
        self.erp.upload_grade(self.prof, "STUDENT_1", "COURSE_1", "A")
        
        self.assertEqual(len(self.erp.grades), 1)
        self.assertEqual(self.erp.grades[0].grade_value, "A")

    def test_upload_grade_not_enrolled(self):
        print("\n[TEST] Upload Grade (Fail - Not Enrolled)")
        self.assertEqual(self.erp.enrollments[0].status, "Pending")
        
        self.erp.upload_grade(self.prof, "STUDENT_1", "COURSE_1", "F")
        
        self.assertEqual(len(self.erp.grades), 0)

if __name__ == '__main__':
    unittest.main()