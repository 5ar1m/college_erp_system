"""
Service layer for Admin operations.
Corresponds to methods in the Admin class and "Perform Admin Management" in DFD.
"""
from typing import Optional, Union
from source.college_erp.database import Database
from source.college_erp.models.user import User, UserRole
from source.college_erp.models.student import Student
from source.college_erp.models.professor import Professor
from source.college_erp.models.course import Course

def add_user(db: Database, user_data: dict) -> Optional[User]:
    """
    Adds a new user (Student or Professor) to the database.
    """
    user_id = user_data.get("user_id")
    if not user_id or user_id in db.users:
        return None  # User ID is invalid or already exists

    role = user_data.get("role")
    new_user: Optional[User] = None

    if role == UserRole.STUDENT:
        new_user = Student(
            user_id=user_id,
            name=user_data.get("name", ""),
            password=user_data.get("password", ""),
            branch=user_data.get("branch", "")
        )
    elif role == UserRole.PROFESSOR:
        new_user = Professor(
            user_id=user_id,
            name=user_data.get("name", ""),
            password=user_data.get("password", ""),
            branch=user_data.get("branch", "")
        )
    
    if new_user:
        db.users[user_id] = new_user
        return new_user
    
    return None

def remove_user(db: Database, user_id: str) -> bool:
    """
    Removes a user from the database.
    """
    if user_id in db.users:
        # Cannot remove an admin this way
        if db.users[user_id].role == UserRole.ADMIN:
            return False
        del db.users[user_id]
        return True
    return False

def add_course(db: Database, course_data: dict) -> Optional[Course]:
    """
    Adds a new course to the database.
    """
    course_id = course_data.get("course_id")
    if not course_id or course_id in db.courses:
        return None # Course ID is invalid or already exists
        
    # Check if coordinator exists and is a professor
    coord_id = course_data.get("coordinator_id")
    coordinator = db.users.get(coord_id)
    
    if not coordinator or coordinator.role != UserRole.PROFESSOR:
        return None # Invalid coordinator

    new_course = Course(
        course_id=course_id,
        name=course_data.get("name", ""),
        coordinator_id=coord_id
    )
    db.courses[course_id] = new_course
    return new_course

def remove_course(db: Database, course_id: str) -> bool:
    """
    Removes a course from the database.
    """
    if course_id in db.courses:
        del db.courses[course_id]
        # In a real system, you'd also handle related enrollments/grades
        return True
    return False