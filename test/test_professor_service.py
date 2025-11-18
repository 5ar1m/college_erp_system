"""
Tests for the professor service.
"""
import pytest
from source.college_erp.database import Database
from source.college_erp.services import professor_service, student_service
from source.college_erp.models.enrollment import EnrollmentStatus

@pytest.fixture
def db_with_pending_enrollment(populated_db: Database) -> Database:
    """Fixture to add a pending enrollment for testing."""
    student_service.register_course(populated_db, "stud_a", "SUBJ-X") # Coordinated by prof_a
    student_service.register_course(populated_db, "stud_b", "SUBJ-Y") # Coordinated by prof_b
    return populated_db

def test_professor_view_pending_registrations(db_with_pending_enrollment: Database):
    """Test that a professor can see pending registrations for their courses."""
    # prof_a is coordinator for SUBJ-X
    pending_cs = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_a")
    assert len(pending_cs) == 1
    assert pending_cs[0].student_id == "stud_a"
    assert pending_cs[0].course_id == "SUBJ-X"
    
    # prof_b is coordinator for SUBJ-Y
    pending_phy = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_b")
    assert len(pending_phy) == 1
    assert pending_phy[0].student_id == "stud_b"

def test_professor_approve_registration(db_with_pending_enrollment: Database):
    """Test approving a registration, as per the sequence diagram."""
    pending = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_a")
    enrollment_id = pending[0].enrollment_id
    
    approved_enrollment = professor_service.approve_registration(db_with_pending_enrollment, enrollment_id)
    assert approved_enrollment is not None
    assert approved_enrollment.status == EnrollmentStatus.ENROLLED
    
    # Check that it's no longer pending
    pending_after = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_a")
    assert len(pending_after) == 0

def test_professor_upload_grade_fail_not_enrolled(populated_db: Database):
    """Test failure when uploading a grade for a student not enrolled."""
    grade = professor_service.upload_grade(populated_db, "prof_a", "stud_a", "SUBJ-X", "A")
    assert grade is None

def test_professor_upload_grade_success(db_with_pending_enrollment: Database):
    """Test uploading a grade after a student is approved."""
    # 1. Approve student
    pending = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_a")
    enrollment_id = pending[0].enrollment_id
    professor_service.approve_registration(db_with_pending_enrollment, enrollment_id)
    
    # 2. Upload grade
    new_grade = professor_service.upload_grade(db_with_pending_enrollment, "prof_a", "stud_a", "SUBJ-X", "A+")
    assert new_grade is not None
    assert new_grade.grade_value == "A+"
    assert new_grade.grade_id in db_with_pending_enrollment.grades
    
    # 3. Verify student can see the grade
    student_grades = student_service.view_grades(db_with_pending_enrollment, "stud_a")
    assert len(student_grades) == 1
    assert student_grades[0].grade_value == "A+"

def test_professor_upload_grade_fail_not_coordinator(db_with_pending_enrollment: Database):
    """Test failure when a professor tries to upload a grade for a course they don't coordinate."""
    # Approve stud_b for SUBJ-Y
    pending = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_b")
    professor_service.approve_registration(db_with_pending_enrollment, pending[0].enrollment_id)
    
    # prof_a tries to upload grade for SUBJ-Y (coordinated by prof_b)
    grade = professor_service.upload_grade(db_with_pending_enrollment, "prof_a", "stud_b", "SUBJ-Y", "B")
    assert grade is None

def test_professor_view_enrolled_students(db_with_pending_enrollment: Database):
    """Test viewing enrolled students for a course."""
    # Approve stud_a for SUBJ-X
    pending_cs = professor_service.view_pending_registrations(db_with_pending_enrollment, "prof_a")
    professor_service.approve_registration(db_with_pending_enrollment, pending_cs[0].enrollment_id)

    # prof_a views enrolled students for SUBJ-X
    enrolled_students = professor_service.view_enrolled_students(db_with_pending_enrollment, "prof_a", "SUBJ-X")
    assert len(enrolled_students) == 1
    assert enrolled_students[0].user_id == "stud_a"

    # prof_a views enrolled students for SUBJ-Y (not coordinator)
    enrolled_students_phy = professor_service.view_enrolled_students(db_with_pending_enrollment, "prof_a", "SUBJ-Y")
    assert len(enrolled_students_phy) == 0