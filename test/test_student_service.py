"""
Tests for the student service.
"""
import pytest
from source.college_erp.database import Database
from source.college_erp.services import student_service
from source.college_erp.models.enrollment import EnrollmentStatus

def test_student_view_courses(populated_db: Database):
    """Test that a student can view all available courses."""
    courses = student_service.view_courses(populated_db)
    assert len(courses) == 2
    assert "SUBJ-X" in [c.course_id for c in courses]
    assert "SUBJ-Y" in [c.course_id for c in courses]

def test_student_register_course(populated_db: Database):
    """Test a student registering for a course. Status should be PENDING."""
    enrollment = student_service.register_course(populated_db, "stud_a", "SUBJ-X")
    assert enrollment is not None
    assert enrollment.student_id == "stud_a"
    assert enrollment.course_id == "SUBJ-X"
    assert enrollment.status == EnrollmentStatus.PENDING
    assert enrollment.enrollment_id in populated_db.enrollments

def test_student_register_course_duplicate(populated_db: Database):
    """Test that a student cannot register for the same course twice."""
    # First registration
    enrollment1 = student_service.register_course(populated_db, "stud_a", "SUBJ-X")
    assert enrollment1 is not None
    
    # Second attempt
    enrollment2 = student_service.register_course(populated_db, "stud_a", "SUBJ-X")
    assert enrollment2 is None

def test_student_register_nonexistent_course(populated_db: Database):
    """Test failure when registering for a non-existent course."""
    enrollment = student_service.register_course(populated_db, "stud_a", "FAKE-101")
    assert enrollment is None

def test_student_view_grades_empty(populated_db: Database):
    """Test viewing grades when none have been uploaded."""
    grades = student_service.view_grades(populated_db, "stud_a")
    assert len(grades) == 0

def test_student_view_registered_courses(populated_db: Database):
    """Test viewing registered courses after registering."""
    student_service.register_course(populated_db, "stud_a", "SUBJ-X")
    student_service.register_course(populated_db, "stud_a", "SUBJ-Y")
    
    registrations = student_service.view_registered_courses(populated_db, "stud_a")
    assert len(registrations) == 2
    
    registrations_other_student = student_service.view_registered_courses(populated_db, "stud_b")
    assert len(registrations_other_student) == 0