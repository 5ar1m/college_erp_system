"""
Tests for the admin service.
"""
import pytest
from source.college_erp.database import Database
from source.college_erp.services import admin_service
from source.college_erp.models.user import UserRole

def test_admin_add_student(populated_db: Database):
    """Test adding a new student."""
    student_data = {
        "user_id": "stud_c",
        "name": "Student C",
        "password": "pass",
        "branch": "Branch 1",
        "role": UserRole.STUDENT
    }
    new_user = admin_service.add_user(populated_db, student_data)
    assert new_user is not None
    assert new_user.user_id == "stud_c"
    assert new_user.role == UserRole.STUDENT
    assert "stud_c" in populated_db.users

def test_admin_add_professor(populated_db: Database):
    """Test adding a new professor."""
    prof_data = {
        "user_id": "prof_c",
        "name": "Professor C",
        "password": "pass",
        "branch": "Branch 3",
        "role": UserRole.PROFESSOR
    }
    new_user = admin_service.add_user(populated_db, prof_data)
    assert new_user is not None
    assert new_user.user_id == "prof_c"
    assert new_user.role == UserRole.PROFESSOR
    assert "prof_c" in populated_db.users

def test_admin_add_user_duplicate_id(populated_db: Database):
    """Test failure when adding a user with a duplicate ID."""
    student_data = {
        "user_id": "stud_a", # Already exists
        "name": "Student D",
        "password": "pass",
        "branch": "Branch 1",
        "role": UserRole.STUDENT
    }
    new_user = admin_service.add_user(populated_db, student_data)
    assert new_user is None

def test_admin_remove_user(populated_db: Database):
    """Test removing an existing user."""
    assert "stud_a" in populated_db.users
    result = admin_service.remove_user(populated_db, "stud_a")
    assert result is True
    assert "stud_a" not in populated_db.users

def test_admin_remove_nonexistent_user(populated_db: Database):
    """Test failure when removing a non-existent user."""
    result = admin_service.remove_user(populated_db, "stud_z")
    assert result is False

def test_admin_remove_admin_user(populated_db: Database):
    """Test failure when trying to remove an admin."""
    result = admin_service.remove_user(populated_db, "admin_user")
    assert result is False
    assert "admin_user" in populated_db.users

def test_admin_add_course(populated_db: Database):
    """Test adding a new course."""
    course_data = {
        "course_id": "SUBJ-Z",
        "name": "Subject Z",
        "coordinator_id": "prof_a"
    }
    new_course = admin_service.add_course(populated_db, course_data)
    assert new_course is not None
    assert new_course.course_id == "SUBJ-Z"
    assert "SUBJ-Z" in populated_db.courses

def test_admin_add_course_invalid_coordinator(populated_db: Database):
    """Test failure when adding a course with a non-existent coordinator."""
    course_data = {
        "course_id": "SUBJ-Z",
        "name": "Subject Z",
        "coordinator_id": "prof_z" # Does not exist
    }
    new_course = admin_service.add_course(populated_db, course_data)
    assert new_course is None

def test_admin_add_course_duplicate_id(populated_db: Database):
    """Test failure when adding a course with a duplicate ID."""
    course_data = {
        "course_id": "SUBJ-X", # Already exists
        "name": "Subject Z",
        "coordinator_id": "prof_a"
    }
    new_course = admin_service.add_course(populated_db, course_data)
    assert new_course is None

def test_admin_remove_course(populated_db: Database):
    """Test removing an existing course."""
    assert "SUBJ-X" in populated_db.courses
    result = admin_service.remove_course(populated_db, "SUBJ-X")
    assert result is True
    assert "SUBJ-X" not in populated_db.courses