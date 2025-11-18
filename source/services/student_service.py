"""
Service layer for Student operations.
Corresponds to methods in the Student class and "Process Registration" in DFD.
"""
from typing import List, Optional
import uuid
from source.college_erp.database import Database
from source.college_erp.models.course import Course
from source.college_erp.models.grade import Grade
from source.college_erp.models.enrollment import Enrollment, EnrollmentStatus

def view_courses(db: Database) -> List[Course]:
    """
    Fetches a list of all available courses.
    Corresponds to "View Available Courses" in Sequence Diagram.
    """
    return list(db.courses.values())

def register_course(db: Database, student_id: str, course_id: str) -> Optional[Enrollment]:
    """
    Creates a new enrollment request for a student.
    Status is set to PENDING.
    Corresponds to "Request Registration" in Sequence Diagram.
    """
    # Check if student and course exist
    if student_id not in db.users or course_id not in db.courses:
        return None

    # Check for existing enrollment
    for enrollment in db.enrollments.values():
        if enrollment.student_id == student_id and enrollment.course_id == course_id:
            return None # Already registered or pending

    enrollment_id = str(uuid.uuid4())
    new_enrollment = Enrollment(
        enrollment_id=enrollment_id,
        student_id=student_id,
        course_id=course_id,
        status=EnrollmentStatus.PENDING
    )
    db.enrollments[enrollment_id] = new_enrollment
    return new_enrollment

def view_grades(db: Database, student_id: str) -> List[Grade]:
    """
    Fetches all grades for a specific student.
    Corresponds to "View Grades" use case.
    """
    return [grade for grade in db.grades.values() if grade.student_id == student_id]

def view_registered_courses(db: Database, student_id: str) -> List[Enrollment]:
    """
    Fetches all enrollments (pending, approved, rejected) for a student.
    Corresponds to "View Registered Courses" use case.
    """
    return [en for en in db.enrollments.values() if en.student_id == student_id]