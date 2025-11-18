"""
Pytest configuration file for fixtures.
"""
import pytest
from datetime import date
from source.college_erp.database import Database, mock_db
from source.college_erp.models.admin import Admin
from source.college_erp.models.professor import Professor
from source.college_erp.models.student import Student
from source.college_erp.models.course import Course

@pytest.fixture(scope="function")
def populated_db() -> Database:
    """
    Fixture to get a clean, populated database for each test function.
    Uses generic names as requested.
    """
    # Clear any existing data
    mock_db.clear_all()
    
    # Add Users
    admin = Admin(user_id="admin_user", name="Admin", password="admin_pass")
    prof1 = Professor(user_id="prof_a", name="Professor A", password="prof_pass_a", branch="Branch 1")
    prof2 = Professor(user_id="prof_b", name="Professor B", password="prof_pass_b", branch="Branch 2")
    stud1 = Student(user_id="stud_a", name="Student A", password="stud_pass_a", branch="Branch 1")
    stud2 = Student(user_id="stud_b", name="Student B", password="stud_pass_b", branch="Branch 2")
    
    mock_db.users = {
        "admin_user": admin,
        "prof_a": prof1,
        "prof_b": prof2,
        "stud_a": stud1,
        "stud_b": stud2
    }
    
    # Add Courses
    course1 = Course(course_id="SUBJ-X", name="Subject X", coordinator_id="prof_a")
    course2 = Course(course_id="SUBJ-Y", name="Subject Y", coordinator_id="prof_b")
    
    mock_db.courses = {
        "SUBJ-X": course1,
        "SUBJ-Y": course2
    }
    
    # Clear enrollments and grades
    mock_db.enrollments.clear()
    mock_db.grades.clear()
    
    return mock_db