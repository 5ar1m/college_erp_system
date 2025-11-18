"""
Service layer for Professor operations.
Corresponds to methods in the Professor class and "Process Registration" in DFD.
"""
from typing import List, Optional
import uuid
from source.college_erp.database import Database
from source.college_erp.models.enrollment import Enrollment, EnrollmentStatus
from source.college_erp.models.grade import Grade
from source.college_erp.models.user import User

def view_pending_registrations(db: Database, professor_id: str) -> List[Enrollment]:
    """
    Fetches pending enrollments for courses coordinated by this professor.
    Corresponds to "View Pending Registrations" in Sequence Diagram.
    """
    pending_enrollments = []
    # Find courses coordinated by this professor
    prof_course_ids = [
        course.course_id for course in db.courses.values() 
        if course.coordinator_id == professor_id
    ]
    
    # Find pending enrollments for those courses
    for enrollment in db.enrollments.values():
        if (enrollment.course_id in prof_course_ids and 
            enrollment.status == EnrollmentStatus.PENDING):
            pending_enrollments.append(enrollment)
            
    return pending_enrollments

def approve_registration(db: Database, enrollment_id: str) -> Optional[Enrollment]:
    """
    Approves a pending enrollment.
    Corresponds to "Approve Registration" in Sequence Diagram.
    """
    enrollment = db.enrollments.get(enrollment_id)
    if enrollment and enrollment.status == EnrollmentStatus.PENDING:
        enrollment.status = EnrollmentStatus.ENROLLED
        db.enrollments[enrollment_id] = enrollment # Update in DB
        return enrollment
    return None

def upload_grade(db: Database, professor_id: str, student_id: str, course_id: str, grade_value: str) -> Optional[Grade]:
    """
    Uploads or updates a grade for a student in a course.
    Corresponds to "Upload Grades" use case.
    """
    # Check if professor coordinates this course
    course = db.courses.get(course_id)
    if not course or course.coordinator_id != professor_id:
        return None # Professor not authorized for this course

    # Check if student is enrolled in this course
    enrollment_found = False
    for en in db.enrollments.values():
        if (en.student_id == student_id and 
            en.course_id == course_id and 
            en.status == EnrollmentStatus.ENROLLED):
            enrollment_found = True
            break
    
    if not enrollment_found:
        return None # Student not enrolled

    # Find existing grade to update, or create a new one
    existing_grade: Optional[Grade] = None
    for grade in db.grades.values():
        if grade.student_id == student_id and grade.course_id == course_id:
            existing_grade = grade
            break
            
    if existing_grade:
        existing_grade.grade_value = grade_value
        db.grades[existing_grade.grade_id] = existing_grade
        return existing_grade
    else:
        new_grade_id = str(uuid.uuid4())
        new_grade = Grade(
            grade_id=new_grade_id,
            student_id=student_id,
            course_id=course_id,
            grade_value=grade_value
        )
        db.grades[new_grade_id] = new_grade
        return new_grade

def view_enrolled_students(db: Database, professor_id: str, course_id: str) -> List[User]:
    """
    Views all students enrolled in a specific course coordinated by the professor.
    Corresponds to "View Enrollment Info" use case.
    """
    course = db.courses.get(course_id)
    if not course or course.coordinator_id != professor_id:
        return [] # Not authorized or course doesn't exist

    enrolled_student_ids = [
        en.student_id for en in db.enrollments.values()
        if en.course_id == course_id and en.status == EnrollmentStatus.ENROLLED
    ]
    
    return [db.users[uid] for uid in enrolled_student_ids if uid in db.users]